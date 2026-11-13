import win32gui
import win32con
import win32api
import win32process
import time
import random
import math

from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

VK_1 = 0x31  # 数字键 1：抛竿
VK_2 = 0x37  # 数字键 7：收竿（互动键）
VK_3 = 0x33
VK_4 = 0x34

# ===== 声音检测参数（按实际情况调整）=====
TRIGGER_DB = -20.0        # 绝对阈值：峰值至少要超过该分贝
MARGIN_DB = 15.0          # 相对阈值：且要比背景噪声高出这么多分贝
CAST_GRACE = 2.0          # 抛竿后忽略的秒数（避免把抛竿声误判为咬钩）
BASELINE_TIME = 1.0       # 抛竿后用于测量背景噪声的秒数
POLL_INTERVAL = 0.02      # 采样间隔（秒）
CONFIRM_SAMPLES = 3      # 连续多少个采样超过阈值才判定，防止偶发尖峰
CAST_TIMEOUT = (25, 28)   # 每次抛竿最长等待时间（随机范围）
REEL_DELAY = (0.5, 1.0)   # 检测到咬钩后，随机延迟多少秒再收竿（模拟人反应时间）


def send_key(hwnd, key):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0)


def to_db(peak):
    """把 0~1 的峰值转换为 dBFS（0 dB 为最大）"""
    return 20 * math.log10(peak) if peak > 1e-6 else -120.0


def get_game_meter(hwnd):
    """根据窗口句柄找到对应进程的音频会话，返回其音量表接口"""
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    for session in AudioUtilities.GetAllSessions():
        if session.Process and session.ProcessId == pid:
            return session._ctl.QueryInterface(IAudioMeterInformation)
    return None


def read_db(meter):
    return to_db(meter.GetPeakValue())


def wait_for_bite(meter, timeout):
    """抛竿后监听游戏声音，检测到咬钩返回 True，超时返回 False"""
    start = time.time()

    # 1. 忽略抛竿音效
    time.sleep(CAST_GRACE)

    # 2. 测量背景噪声（取这段时间的最大峰值）
    baseline = -120.0
    t0 = time.time()
    while time.time() - t0 < BASELINE_TIME:
        baseline = max(baseline, read_db(meter))
        time.sleep(POLL_INTERVAL)
    # 取较大者：必须同时满足绝对阈值和相对背景噪声阈值
    threshold = max(TRIGGER_DB, baseline + MARGIN_DB)
    print(f"背景噪声 {baseline:.1f} dB，触发阈值 {threshold:.1f} dB")

    # 3. 监听咬钩溅水声
    hits = 0
    while time.time() - start < timeout:
        db = read_db(meter)
        if db > threshold:
            hits += 1
            if hits >= CONFIRM_SAMPLES:
                print(f"检测到咬钩！当前 {db:.1f} dB")
                return True
        else:
            hits = 0
        time.sleep(POLL_INTERVAL)
    return False


def main():
    print("请确保魔兽世界正在运行，并开启『后台播放声音』。")
    hwnd = win32gui.FindWindow(None, "魔兽世界")
    if not hwnd:
        print("未找到指定窗口")
        return
    print(f"找到窗口，句柄为: {hwnd}")

    meter = get_game_meter(hwnd)
    if meter is None:
        print("未找到游戏的音频会话，请先让游戏发出一次声音（如抛一次竿）后再运行")
        return
    print("已连接到游戏音频会话")

    try:
        while True:
            send_key(hwnd, VK_1)
            timeout = random.uniform(*CAST_TIMEOUT)
            print(f"已抛竿，最长等待 {timeout:.2f} 秒")

            if wait_for_bite(meter, timeout):
                delay = random.uniform(*REEL_DELAY)
                print(f"随机等待 {delay:.2f} 秒后收竿")
                time.sleep(delay)
                send_key(hwnd, VK_2)
                print("已收竿")
            else:
                print("超时未咬钩，重新抛竿")

            time.sleep(random.uniform(2.0, 3.0))
    except KeyboardInterrupt:
        print("\n程序已停止")


if __name__ == "__main__":
    main()
