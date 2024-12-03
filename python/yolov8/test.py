# import threading
#
# import pyautogui
# import pydirectinput
#
# def move():
#     pydirectinput.moveRel(
#         int(20),
#         int(20),
#         tween=pyautogui.easeOutQuad,
#         duration=5,
#         relative=True
#     )
#
# for i in range(10):
#     move()
#     # threading.Thread(target=move).start()
#
# def x(r):
#     return r ** 10 - 5 * r + 4
#
#
# for i in range(1000):
#     r = 0.8316573192 + 0.0000000001 * i
#     print(x(r), r)

# for i in range(10):
#     print(0.8316573192 ** i / 5)

var = [0.2,
       0.16633146384,
       0.13833077931578613,
       0.11504380508861349,
       0.09567702253056362,
       0.07957049606680652,
       0.06617538544633447,
       0.05503524365732522,
       0.04577046320156989,
       0.03806534072475986,
       ]
print(sum(var))
