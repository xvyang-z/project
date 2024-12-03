from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import Qt

import bus


# 悬浮窗
class FloatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())  # 设置窗口为全屏的大小

        # 这里直接初始化 5 个目标框, 避免运行时频繁创建销毁影响性能
        self.label1 = QLabel('+', self)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setGeometry(0, 0, 0, 0)
        self.label1.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: red; border: 2px solid red;')

        self.label2 = QLabel('+', self)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setGeometry(0, 0, 0, 0)
        self.label2.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: red; border: 2px solid red;')

        self.label3 = QLabel('+', self)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setGeometry(0, 0, 0, 0)
        self.label3.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: red; border: 2px solid red;')

        self.label4 = QLabel('+', self)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setGeometry(0, 0, 0, 0)
        self.label4.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: red; border: 2px solid red;')

        self.label5 = QLabel('+', self)
        self.label5.setAlignment(Qt.AlignCenter)
        self.label5.setGeometry(0, 0, 0, 0)
        self.label5.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: red; border: 2px solid red;')

        self.all_label = [self.label1, self.label2, self.label3, self.label4, self.label5]

        bus.float_window_signal.updated.connect(self.update_fw_position)

    def update_fw_position(self):
        """
        更新悬浮窗位置
        """
        if bus.option.target_border_num_index == 0:  # 仅显示当前攻击目标框
            x = bus.target_window.target.x
            y = bus.target_window.target.y
            w = bus.target_window.target.width
            h = bus.target_window.target.height

            self.all_label[0].resize(w, h)

            # 设置悬浮窗位置, 这里需要加上 游戏窗口 的 左 上 偏移量
            self.all_label[0].move(bus.game_window.left + x - w/2, bus.game_window.top + y - h/2)

            # 将其他 label 设为不显示
            for i in self.all_label[1:]:
                i.resize(0, 0)

        elif bus.option.target_border_num_index == 1:  # 显示全部目标框
            target_num = len(bus.target_window.target_all)

            for index, elem in enumerate(bus.target_window.target_all[:5]):  # 最多取前5个
                self.all_label[index].resize(elem.width, elem.height)
                self.all_label[index].move(
                    bus.game_window.left + elem.x - elem.width / 2,
                    bus.game_window.top + elem.y - elem.height / 2
                )

            for i in self.all_label[target_num:]:
                i.resize(0, 0)

