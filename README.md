# 魔兽世界自动按键脚本

这是一个用于魔兽世界的自动按键脚本，可以定时发送指定按键。

## 功能特性

- 自动发送数字键 1 和 2
- 定时发送数字键 4（288-299秒间隔）
- 像素颜色变化检测（可选）
- 多线程安全的按键发送

## 系统要求

- Windows 操作系统
- Python 3.7+
- 魔兽世界客户端

## 安装步骤

### 方法1：直接运行（推荐）

1. 克隆仓库
```bash
git clone https://github.com/heroichu/AutomatiWow.git
cd AutomatiWow
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行脚本
```bash
python main.py
```

## 依赖库说明

- `pywin32`: Windows API 调用，用于发送按键和窗口操作
- `Pillow`: 图像处理，用于屏幕截图和像素检测
- `pynput`: 跨平台输入控制，用于鼠标监听
- `pycaw`: 读取游戏进程的音量峰值，用于钓鱼咬钩检测

## 自动钓鱼（fishing.py）

`fishing.py` 直接读取魔兽世界进程的音量峰值（分贝），听到鱼咬钩的溅水声后自动收竿：

1. 按数字键 1 抛竿
2. 忽略抛竿后 2 秒的声音，再用 1 秒测量背景噪声
3. 音量同时超过 `TRIGGER_DB`，并且比背景噪声高出 `MARGIN_DB`，判定为咬钩
4. 随机等待 `REEL_DELAY` 秒后按数字键 7 收竿；25~28 秒内没有咬钩就重新抛竿

使用前请在游戏里开启「后台播放声音」，并关闭或调低音乐和环境音，只保留音效。

检测灵敏度等参数都在 `fishing.py` 开头修改：误收竿就调大 `MARGIN_DB` 或 `CONFIRM_SAMPLES`，漏掉咬钩就调小 `MARGIN_DB`。

## 打包成 exe

在项目目录下运行：

```bash
python -m PyInstaller --onefile --console --name fishing --distpath . --workpath _build --specpath _build --hidden-import comtypes.stream fishing.py
```

打包完会在项目根目录生成 `fishing.exe`，`_build` 文件夹是临时文件，可以删掉。

| 参数 | 作用 |
|---|---|
| `--onefile` | 打包成单个 exe |
| `--console` | 保留命令行窗口，能看到检测日志 |
| `--name fishing` | 生成的文件名为 `fishing.exe` |
| `--distpath .` | exe 输出到当前目录 |
| `--workpath _build --specpath _build` | 中间文件放在 `_build`，必须和项目在同一个盘，否则 PyInstaller 会报错 |
| `--hidden-import comtypes.stream` | 手动带上 pycaw 用到的 comtypes 模块，防止漏打包 |

注意：
- 需要先安装 PyInstaller：`pip install pyinstaller`
- 请用 `python -m PyInstaller` 运行；直接输入 `pyinstaller` 可能会提示找不到命令
- exe 里的参数是打包时固定的，修改 `fishing.py` 的参数后需要重新打包

## 使用说明

1. 确保魔兽世界窗口标题为"魔兽世界"
2. 运行脚本前请确保游戏窗口可见
3. 按 Ctrl+C 停止脚本

## 注意事项

⚠️ **使用风险提醒**：
- 此脚本仅供学习交流使用
- 使用自动化脚本可能违反游戏服务条款
- 使用者需自行承担相关风险
