import time

import pydirectinput
from PyQt5.QtCore import QThread

attacked = False


class AutoAttack(QThread):

    def __init__(self):
        super().__init__()
        self.stop = False

    def run(self):
        is_mouse_up = False

        while not self.stop:
            if attacked:
                pydirectinput.mouseDown(button='left')
                is_mouse_up = False
                print('开始攻击`')
            else:
                if not is_mouse_up:
                    pydirectinput.mouseUp(button='left')
                    is_mouse_up = True
                    print('停止攻击')

            time.sleep(0.01)

        pydirectinput.mouseUp(button='left')
        print('停止攻击')





