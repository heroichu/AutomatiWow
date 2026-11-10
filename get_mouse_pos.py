import win32api
import time

print("将鼠标移动到目标位置，坐标会实时打印在下方。")
print("按 Ctrl+C 停止。\n")

try:
    last_pos = None
    while True:
        pos = win32api.GetCursorPos()
        if pos != last_pos:
            print(f"x = {pos[0]}, y = {pos[1]}")
            last_pos = pos
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n已停止")
