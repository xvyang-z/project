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
        y_offset = target_center[1] - game_window_center[1] - 20

        # 先设置鼠标位置到游戏窗口的中心处(相对于电脑屏幕左上角)，不引起移动
        game_window_center_real = (
            (bus.game_window.left + bus.game_window.right) // 2,
            (bus.game_window.top + bus.game_window.bottom) // 2
        )
        pyautogui.moveTo(game_window_center_real[0], game_window_center_real[1])

        pydirectinput.moveRel(
            int(x_offset / 100 * bus.option.aim_scale),
            int(y_offset / 100 * bus.option.aim_scale),
            relative=True
        )
        print('瞄准')



