import threading

import pyautogui
import pydirectinput

def move():
    pydirectinput.moveRel(
        int(20),
        int(20),
        tween=pyautogui.easeOutQuad,
        duration=5,
        relative=True
    )

for i in range(10):
    move()
    # threading.Thread(target=move).start()