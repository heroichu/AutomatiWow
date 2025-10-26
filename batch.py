import win32gui
import win32con
import win32api
import time
import random
import threading

VK_1 = 0x31  # 数字键 1 的虚拟键码
VK_2 = 0x32  # 数字键 2 的虚拟键码
VK_3 = 0x33
VK_4 = 0x34
VK_RB = 0x5D

# 全局变量用于线程间通信
timer_stop_event = threading.Event()

def find_all_wow_windows():
    """查找所有魔兽世界窗口"""
    wow_windows = []
    
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if "魔兽世界" in window_title:
                results.append((hwnd, window_title))
    
    win32gui.EnumWindows(enum_callback, wow_windows)
    return wow_windows


def send_key(hwnd, key):
    """向指定窗口发送按键"""
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key, 0)

def control_single_window(hwnd, window_title, window_index):
    """控制单个窗口的主循环"""
    print(f"[窗口{window_index}] 开始控制: {window_title} (句柄: {hwnd})")
    
    try:
        last_key3_press = time.time()  # 记录上次按下数字3的时间（相对时间）
        last_key4_press = time.time()  # 记录上次按下数字4的时间（相对时间）

        while not timer_stop_event.is_set():
            t = random.randint(20, 30)
            print(f"[窗口{window_index}] 循环次数: {t}")
            
            send_key(hwnd, VK_2)
            delay = random.uniform(0.3, 0.5)
            time.sleep(delay)
            
            for i in range(t):
                if timer_stop_event.is_set():  # 允许中途退出
                    break
                send_key(hwnd, VK_1)
                delay = random.uniform(0.3, 0.6)
                time.sleep(delay)
            delay = random.uniform(0.5, 0.7)
            time.sleep(delay)
            current_time = time.time()
                    
                # 检查是否超过90秒，按下数字3
            if current_time - last_key3_press >= 90:
                delay = random.uniform(1.0, 1.5)
                time.sleep(delay)
                print(f"[窗口{window_index}] 间隔{current_time - last_key3_press:.1f}秒，按下数字键3")
                send_key(hwnd, VK_3)
                last_key3_press = current_time  
                    
                # 检查是否超过120秒，按下数字4
            if current_time - last_key4_press >= 120:
                delay = random.uniform(1.0, 1.5)
                time.sleep(delay)
                print(f"[窗口{window_index}] 已运行{current_time - last_key4_press:.1f}秒，按下数字键4")
                send_key(hwnd, VK_4)
                last_key4_press = current_time
                
    except Exception as e:
        print(f"[窗口{window_index}] 发生错误: {e}")


def main():
    print("正在查找所有魔兽世界窗口...")
    wow_windows = find_all_wow_windows()
    
    if not wow_windows:
        print("未找到任何魔兽世界窗口")
        return
    
    print(f"\n找到 {len(wow_windows)} 个魔兽世界窗口：")
    for i, (hwnd, title) in enumerate(wow_windows, 1):
        print(f"  [{i}] 句柄: {hwnd}, 标题: {title}")
    
    # 为每个窗口创建控制线程和定时按键线程
    threads = []
    for i, (hwnd, title) in enumerate(wow_windows, 1):
        # 主控制线程
        control_thread = threading.Thread(
            target=control_single_window, 
            args=(hwnd, title, i),
            daemon=True
        )
        control_thread.start()
        threads.append(control_thread)
        
        
        print(f"已为窗口 {i} 启动控制线程和定时按键线程")
    
    print("\n所有窗口控制线程已启动，按 Ctrl+C 停止程序")
    print("提示：数字3每90秒按一次，数字4每120秒按一次\n")
    
    try:
        # 主线程等待，让子线程运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n正在停止所有窗口控制...")
        timer_stop_event.set()  # 通知所有线程停止
        
        # 等待所有线程结束
        for thread in threads:
            thread.join(timeout=2)
        
        print("程序已停止")


if __name__ == "__main__":
    main()