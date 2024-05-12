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
                print('移动')
            time.sleep(0.01)  # 这里要停一下, 否则当if不执行时会一直 while True, 占满cpu, 卡死其他线程

    def move(self):
        """
        鼠标移动到最近目标
        """
        target_center = (bus.target_window.target[0], bus.target_window.target[1])
        game_window_center = (
            (bus.game_window.right - bus.game_window.left) // 2,
            (bus.game_window.bottom - bus.game_window.top) // 2
        )

        x_offset = target_center[0] - game_window_center[0]
        y_offset = target_center[1] - game_window_center[1]

        # 每次移动10ms, todo 按选择的fps加上随机
        pydirectinput.moveRel(
            int(x_offset / 100 * bus.option.aim_scale),
            int(y_offset / 100 * bus.option.aim_scale),
            duration=0.01,
            tween=pyautogui.easeOutQuad,
            relative=True
        )
