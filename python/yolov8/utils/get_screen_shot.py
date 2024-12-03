from typing import Union

import cv2
import numpy
import win32con
import win32gui
import win32ui

from setting import GAME_HANDLE_NAME


def win32_screenshot() -> Union[None, tuple[numpy.ndarray, tuple[int, int, int, int]]]:
    # 获取窗口的句柄，注意窗口不能最小化
    hWnd = win32gui.FindWindow(None, GAME_HANDLE_NAME)

    if hWnd == 0:
        return None

    # 获取句柄窗口的大小信息
    left, top, right, bot = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

    signedIntsArray = saveBitMap.GetBitmapBits(True)

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd, hWndDC)

    im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')

    im_opencv.shape = (height, width, 4)

    return cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB), (left, top, right, bot)

    # cv2.imwrite("im_opencv.jpg", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
    # cv2.namedWindow('im_opencv')  # 命名窗口
    # cv2.imshow("im_opencv", im_opencv)  # 显示
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
