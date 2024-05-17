import threading
import time

import pyautogui
import pydirectinput
from PyQt5.QtCore import QObject, pyqtSignal

import bus


class AutoAim(QObject):
    aimed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.stop = False
        self.aimed.connect(self.aim_task)

    def aim_task(self):
        threading.Thread(target=self.aim, daemon=True).start()

    def aim(self):
        """
        鼠标移动到目标
        """
        target_center = (bus.target_window.target.x, bus.target_window.target.y)

        game_window_center = (
            (bus.game_window.right - bus.game_window.left) // 2,
            (bus.game_window.bottom - bus.game_window.top) // 2
        )

        x_offset = target_center[0] - game_window_center[0]
        y_offset = target_center[1] - game_window_center[1]

        # 先设置鼠标位置到游戏窗口的中心处(相对于电脑屏幕左上角)，不引起移动
        game_window_center_real = (
            (bus.game_window.left + bus.game_window.right) // 2,
            (bus.game_window.top + bus.game_window.bottom) // 2
        )
        pyautogui.moveTo(game_window_center_real[0], game_window_center_real[1])

        # 实际移动的像素, 乘上鼠标灵敏度
        x = int(x_offset / 100 * bus.option.aim_scale)
        y = int(y_offset / 100 * bus.option.aim_scale)

        pydirectinput.moveRel(
            int(x),
            int(y),
            relative=True
        )

        # pydirectinput.moveRel 测试下来 duration 参数不起作用, 这里分成10次逐渐逼近
        # 等比数列 a = 1/5   r = 0.8316573192  n = 10   s = a(1-r**n) / (1-r) = 0.9999999998717592
        # rate_list = [
        #     0.2,
        #     0.16633146384,
        #     0.13833077931578613,
        #     0.11504380508861349,
        #     0.09567702253056362,
        #     0.07957049606680652,
        #     0.06617538544633447,
        #     0.05503524365732522,
        #     0.04577046320156989,
        #     0.03806534072475986,
        # ]
        # for i in rate_list:
        #     pydirectinput.moveRel(
        #         int(x * i),
        #         int(y * i),
        #         relative=True
        #     )

        print('瞄准')
