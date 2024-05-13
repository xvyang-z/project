import time

import pyautogui
import pydirectinput
from PyQt5.QtCore import QThread

import bus


class MouseMoveTask(QThread):
    def __init__(self):
        super().__init__()

        self.stop = False

    def run(self):
        while not self.stop:
            if bus.mouse_event.move:
                self.move()
            else:
                time.sleep(0.001)  # 这里要停一下, 否则当if不执行时会一直 while True, 占满cpu, 卡死其他线程

    def move(self):
        """
        鼠标移动到目标
        """
        target_center = (bus.target_window.target[0], bus.target_window.target[1])
        game_window_center = (
            (bus.game_window.right - bus.game_window.left) // 2,
            (bus.game_window.bottom - bus.game_window.top) // 2
        )

        x_offset = target_center[0] - game_window_center[0]
        y_offset = target_center[1] - game_window_center[1]

        # 先设置鼠标位置到游戏窗口相对于整个屏幕的中心处，不引起移动
        game_window_center_real = (
                (bus.game_window.left + bus.game_window.right) // 2,
                (bus.game_window.top + bus.game_window.bottom) // 2
        )
        pyautogui.moveTo(game_window_center_real[0], game_window_center_real[1])

        # 每次移动10ms, todo 按选择的fps加上随机
        pydirectinput.moveRel(
            int(x_offset / 100 * bus.option.aim_scale),
            int(y_offset / 100 * bus.option.aim_scale),
            duration=0.01,
            relative=True
        )
