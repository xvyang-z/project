import json
import os.path
from PyQt5.QtCore import QObject, pyqtSignal

from setting import ROOT_DIR


# 更新悬浮窗的信号
class __FloatWindowSignal(QObject):
    pos_updated = pyqtSignal()


# 更新主窗口的信息
class __MainInfoSignal(QObject):

    # 识别信息
    info_changed = pyqtSignal(str)

    # 当前帧率
    current_fps_changed = pyqtSignal(int)


# 控制鼠标的标志位
class __MouseEvent(QObject):
    move = False
    press = False


# 识别到的所有目标窗口坐标 和 攻击目标坐标
class __TargetWindow:
    # 全部目标 [[中心x, 中心y, w, h]]
    target_all: list[list[float, float, float, float]] = [[0, 0, 0, 0]]

    # 当前攻击目标 [中心x, 中心y, w, h]
    target: list[float, float, float, float] = [0, 0, 0, 0]


# 游戏窗口坐标
class __GameWindow:
    left: float = 0
    top: float = 0
    right: float = 0
    bottom: float = 0


# 选项
class __Option:
    __option_file_path = ROOT_DIR / 'option.json'

    show_border: bool = None
    target_border_num_index: int = None

    auto_aim: bool = None
    aim_scale: int = None

    auto_fire: bool = None

    select_fps: int = None

    def __init__(self):
        self.__init_attr()

    def __init_attr(self):
        if os.path.exists(self.__option_file_path):
            with open(self.__option_file_path, 'r') as f:
                json_data = json.load(f)

            self.show_border = json_data['show_border']
            self.target_border_num_index = json_data['target_border_num_index']
            self.auto_aim = json_data['auto_aim']
            self.aim_scale = json_data['aim_scale']
            self.auto_fire = json_data['auto_fire']
            self.select_fps = json_data['select_fps']

        else:
            # option 的默认值
            self.show_border = False
            self.target_border_num_index = 0
            self.auto_aim = False
            self.aim_scale = 100
            self.auto_fire = False
            self.select_fps = 0

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        json_data = {
            'show_border': self.show_border,
            'target_border_num_index': self.target_border_num_index,
            'auto_aim': self.auto_aim,
            'aim_scale': self.aim_scale,
            'auto_fire': self.auto_fire,
            'select_fps': self.select_fps,
        }
        with open(self.__option_file_path, 'w') as f:
            f.write(json.dumps(json_data))

    def get_select_fps(self) -> int:
        return {
            0: 1e10,  # 不限 等价于一个大数, 主要是根据该值计算每次识别后的sleep时间, 直接给一个大数, 后面可以不再做特殊判断
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50,
            6: 60,
        }[self.select_fps]

