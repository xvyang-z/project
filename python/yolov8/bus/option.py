import json
import os

from setting import ROOT_DIR


class __Option:
    __option_file_path = ROOT_DIR / 'option.json'

    show_border: bool = None
    target_border_num_index: int = None

    auto_aim: bool = None
    aim_scale: int = None

    auto_attack: bool = None

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
            self.auto_attack = json_data['auto_attack']
            self.select_fps = json_data['select_fps']

        else:
            # option 的默认值
            self.show_border = False
            self.target_border_num_index = 0
            self.auto_aim = False
            self.aim_scale = 50
            self.auto_attack = False
            self.select_fps = 0

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        json_data = {
            'show_border': self.show_border,
            'target_border_num_index': self.target_border_num_index,
            'auto_aim': self.auto_aim,
            'aim_scale': self.aim_scale,
            'auto_attack': self.auto_attack,
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



