import win32gui
import win32con
import win32api
import time
import random
import numpy as np
from PIL import ImageGrab
import threading

VK_1 = 0x31  # 数字键 1 的虚拟键码
VK_2 = 0x32  # 数字键 2 的虚拟键码
VK_3 = 0x33
VK_4 = 0x34
VK_RB = 0x5D

# 初始化捕获参数
CAPTURE_POINT = None
COLOR_CHANGE_THRESHOLD = 30  # 颜色变化阈值，可以根据需要调整

# 全局变量用于线程间通信
color_changed = False
color_change_lock = threading.Lock()
pause_detection = threading.Event()

# 新增：初始颜色
initial_color = None
timer_hwnd = None
timer_stop_event = threading.Event()

def set_capture_point():
    global CAPTURE_POINT
    # 监视的点的Y坐标
    x = 406
    y = 840  
    CAPTURE_POINT = (x, y)
    print(f"捕获点已设置为：{CAPTURE_POINT}")

def send_key(hwnd, key):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0)

def color_distance(color1, color2):
    return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

def detect_color_change():
    global initial_color
    screenshot = ImageGrab.grab(bbox=(CAPTURE_POINT[0], CAPTURE_POINT[1], CAPTURE_POINT[0] + 1, CAPTURE_POINT[1] + 1))
    current_color = screenshot.getpixel((0, 0))

    if initial_color is None:
        initial_color = current_color
        return False

    distance = color_distance(initial_color, current_color)
    return distance > COLOR_CHANGE_THRESHOLD

def pixel_detection_thread():
    global color_changed
    print("开始监测像素颜色变化...")

    while True:
        if pause_detection.is_set():
            time.sleep(0.1)
            continue

        changed = detect_color_change()
        if changed:
            with color_change_lock:
                color_changed = True
            print("检测到颜色变化！")
            pause_detection.set()  # 暂停检测
        time.sleep(0.05)  # 每0.05秒检测一次

# def timer_thread():
#     """定时器线程：测试版本 - 每10-15秒发送一次数字键4"""
#     timer_hwnd = win32gui.FindWindow(None, "魔兽世界")
    
#     while not timer_stop_event.is_set():
#         # 测试用短等待时间：10-15秒
#         wait_time = random.uniform(300,303)


#         print(f"定时器：下次发送数字键4还需等待 {wait_time:.1f} 秒")
        
#         # 分段等待，以便能够响应停止事件
#         elapsed = 0
#         while elapsed < wait_time and not timer_stop_event.is_set():
#             time.sleep(1)  # 每秒检查一次是否需要停止
#             elapsed += 1
        
#         # 检查是否被停止
#         if timer_stop_event.is_set():
#             print("定时器线程正在退出...")
#             return
        
#         # 发送数字键4
#         if timer_hwnd:
#             try:
#                 print(f"定时器：准备发送数字键4到窗口句柄 {timer_hwnd}")
#                 send_key(timer_hwnd, VK_3)
#                 print("定时器：已成功发送数字键4")
#             except Exception as e:
#                 print(f"定时器发送按键失败: {e}")
#         else:
#             print("定时器：窗口句柄无效，无法发送按键")

def main():
    global color_changed, initial_color
    print("请确保魔兽世界窗口可见。")
    hwnd = win32gui.FindWindow(None, "魔兽世界")
    if not hwnd:
        print("未找到指定窗口")
        return
    print(f"找到窗口，句柄为: {hwnd}")

    # timer = threading.Thread(target=timer_thread)
    # timer.daemon = True
    # timer.start()
    # print("定时器线程已启动")
    
    try:
        while True:
                    t = random.randint(20,30)
                    print(t)
                    send_key(hwnd, VK_2)
                    delay = random.uniform(0.3, 0.5)
                    #print(f"等待 {delay:.2f} 秒后继续等待循环")
                    time.sleep(delay)
                    for i in range(t):
                        send_key(hwnd, VK_1)
                        delay = random.uniform(0.3, 0.6)
                        time.sleep(delay)
                    #print(f"等待 {delay:.2f} 秒后继续等待循环")
                    time.sleep(delay)  # 短暂睡眠以避免过度消耗 CPU

    except KeyboardInterrupt:
        print("\n程序已停止")
        timer_stop_event.set()  # 停止定时器线程

if __name__ == "__main__":
    main()