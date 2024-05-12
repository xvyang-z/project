import time

import pydirectinput
from PyQt5.QtCore import QThread

import bus


class MousePressTask(QThread):
    def __init__(self):
        super().__init__()
        self.stop = False

    def run(self):
        while not self.stop:
            if bus.mouse_event.press:
                pydirectinput.mouseDown(button='left')
                print('攻击')

            else:
                pydirectinput.mouseUp(button='left')
                print('停止攻击')

            time.sleep(0.01)  # 10ms检测一次  todo 按选中的fps

        pydirectinput.mouseUp(button='left')
        print('停止攻击')
        return

