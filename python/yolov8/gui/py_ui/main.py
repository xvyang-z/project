from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
import bus
from control_mouse.auto_attack import AutoAttack

from detect.detect_task import DetectTask
from gui.py_ui.float_window import FloatWindow
from setting import UI_DIR

from system_hotkey import SystemHotkey


class Main(QWidget):

    def __init__(self):
        super().__init__()

        self.detect_task = None  # 识别任务(开始识别)
        self.float_window = None  # 悬浮窗任务(显示目标框)
        self.auto_aim_task = None  # 鼠标移动的任务(自动瞄准)
        self.auto_attack_task = None  # 鼠标按下的任务(自动攻击)

        uic.loadUi(UI_DIR / 'main.ui', self)

        # 为 按钮组 self.target_border_num 设置一组 单选button和对应序号
        self.target_border_num.addButton(self.show_one_target, 0)
        self.target_border_num.addButton(self.show_all_target, 1)

        # 监听动作进行更改
        self.show_border.toggled[bool].connect(self.show_border_toggled)
        self.target_border_num.buttonClicked[int].connect(self.target_border_num_buttonClicked)

        self.auto_aim.toggled[bool].connect(self.auto_aim_toggled)
        self.aim_scale.valueChanged[int].connect(self.aim_scale_valueChanged)

        self.auto_attack.toggled[bool].connect(self.auto_attack_toggled)

        self.select_fps.currentIndexChanged[int].connect(self.select_fps_changed)

        self.start_or_stop.clicked.connect(self.start_or_stop_clicked)

        # 鼠标无法控制, 这里用快捷键操作, Qt的快捷键在焦点丢失时会失效
        shk = SystemHotkey()
        shk.register(('control', 'f1'), callback=lambda x: self.show_border.toggle())
        shk.register(('control', 'f2'), callback=lambda x: self.auto_aim.toggle())
        shk.register(('control', 'f3'), callback=lambda x: self.auto_attack.toggle())
        shk.register(('control', 'p'), callback=lambda x: self.aim_scale.setValue(self.aim_scale.value() + 1))
        shk.register(('control', 'm'), callback=lambda x: self.aim_scale.setValue(self.aim_scale.value() - 1))
        shk.register(('control', 'return'), callback=lambda x: self.start_or_stop.click())

        # 为选项设置保存的值, 这一步放在 connect 后, 以执行特殊操作
        self.show_border.setChecked(bus.option.show_border)
        self.target_border_num.button(bus.option.target_border_num_index).setChecked(True)
        self.auto_aim.setChecked(bus.option.auto_aim)
        self.aim_scale.setValue(bus.option.aim_scale)
        self.auto_attack.setChecked(bus.option.auto_attack)
        self.select_fps.setCurrentIndex(bus.option.select_fps)

        # 将全局信号绑定到对应函数以更改组件内容
        bus.main_info_signal.info_changed.connect(self.change_info)
        bus.main_info_signal.current_fps_changed.connect(self.change_current_fps)

    def show_border_toggled(self, checked: bool):
        """
        显示目标框 改变时触发
        :param checked: 当前选中状态
        """
        bus.option.show_border = checked

        if checked:
            self.float_window = FloatWindow()
            self.float_window.show()
        else:
            self.float_window = None

    def closeEvent(self, a0):
        self.float_window = None  # fix 悬浮窗不自动退出

    def target_border_num_buttonClicked(self, index: int):
        """
        目标框数量 改变时触发
        :param index: 当前选中的单选按钮序号, 序号在 self.__init__ 中定义
        """
        bus.option.target_border_num_index = index

    def auto_aim_toggled(self, checked: bool):
        """
        自动瞄准 改变时触发
        :param checked: 当前选中状态
        """
        bus.option.auto_aim = checked

    def aim_scale_valueChanged(self, index: int):
        """
        瞄准灵敏度滑块的值 改变时触发
        :param index: 滑块改变后的值
        """
        self.aim_scale_label.setText(f'瞄准灵敏度 {index}')
        bus.option.aim_scale = index

    def auto_attack_toggled(self, checked: bool):
        """
        自动攻击 改变时触发
        :param checked: 当前选中状态
        """
        bus.option.auto_attack = checked

        if checked:
            if self.auto_attack_task is None:
                self.auto_attack_task = AutoAttack()
                self.auto_attack_task.start()

        else:
            if self.auto_attack_task:
                self.auto_attack_task.stop = True
                self.auto_attack_task = None

    def select_fps_changed(self, current_index: int):
        """
        fps限制 改变时触发
        :param current_index: 当前选中项的索引
        """
        bus.option.select_fps = current_index

    def start_or_stop_clicked(self):
        """
        开始识别/停止识别 点击时执行
        """
        start_text = '开始识别 (Ctrl+Return)'
        stop_text = '停止识别 (Ctrl+Return)'
        if self.start_or_stop.text() == start_text:
            self.start_or_stop.setText(stop_text)

            self.detect_task = DetectTask()
            self.detect_task.start()

        elif self.start_or_stop.text() == stop_text:
            self.start_or_stop.setText(start_text)

            self.detect_task.stop = True
            self.detect_task = None

    def change_info(self, info: str):
        """
        全局信号 bus.info_signal.info 触发时执行
        :param info:
        :return:
        """
        self.info.setText(info)

    def change_current_fps(self, fps: int):
        """
        全局信号 bus.info_signal.current_fps 触发时执行
        :param fps:
        :return:
        """
        self.current_fps.setText(str(fps))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
