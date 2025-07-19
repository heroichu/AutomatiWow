import sys
from pynput import mouse

def on_move(x, y):
    print(f"鼠标移动到坐标: ({x} {y})")

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print(f"x = {x}\ny = {y}")

# 创建鼠标监听器
listener = mouse.Listener(
    # on_move=on_move,
    on_click=on_click)

# 开始监听
listener.start()


# 保持程序运行
try:
    listener.join()
except KeyboardInterrupt:
    listener.stop()