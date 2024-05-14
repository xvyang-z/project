import time

import pydirectinput
from PyQt5.QtCore import QThread

import control_mouse


class AutoAttack(QThread):

    def __init__(self):
        super().__init__()
        self.stop = False

    def run(self):
        is_mouse_up = False

        while not self.stop:
            if control_mouse.attacked:
                is_mouse_up = False
                pydirectinput.mouseDown(button='left')
                print('开始攻击`')
            else:
                if not is_mouse_up:
                    pydirectinput.mouseUp(button='left')
                    is_mouse_up = True
                    print('停止攻击')

            time.sleep(0.01)





