class Window:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


INIT_WINDOW = Window(0, 0, 0, 0, )


# 识别到的所有目标窗口坐标 和 攻击目标坐标
class __TARGET_WINDOW:
    # 全部目标 [[中心x, 中心y, w, h]]
    target_all: list[Window] = [INIT_WINDOW]

    # 当前攻击目标 [中心x, 中心y, w, h]
    target: Window = INIT_WINDOW


# 游戏窗口四点坐标
class __GAME_WINDOW:
    left: float = 0
    top: float = 0
    right: float = 0
    bottom: float = 0
