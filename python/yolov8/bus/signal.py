from PyQt5.QtCore import QObject, pyqtSignal


# 更新悬浮窗的信号
class __FloatWindowSignal(QObject):
    updated = pyqtSignal()


# 更新主窗口的信息
class __MainInfoSignal(QObject):

    # 识别信息
    info_changed = pyqtSignal(str)

    # 当前帧率
    current_fps_changed = pyqtSignal(int)



