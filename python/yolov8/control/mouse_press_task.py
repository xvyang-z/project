import time

import pydirectinput
from PyQt5.QtCore import QThread

import bus


class MousePressTask(QThread):
    def __init__(self):
        super().__init__()
        self.stop = False

    def run(self):
        is_mouseup = False  # 鼠标是否已经放开
        while not self.stop:
            if bus.mouse_event.press:  # 如果识别到
                is_mouseup = False
                pydirectinput.mouseDown(button='left')
            else:
                if not is_mouseup:
                    is_mouseup = True
                    pydirectinput.mouseUp(button='left')

            time.sleep(0.001)  # 10ms检测一次  todo 按选中的fps

        pydirectinput.mouseUp(button='left')
        return

