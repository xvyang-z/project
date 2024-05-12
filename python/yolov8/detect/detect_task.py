import math
import time

from PyQt5.QtCore import QThread
from ultralytics import YOLO

import bus
from setting import MODEL_PATH
from utils.get_screen_shot import win32_screenshot

model = YOLO(MODEL_PATH)


class DetectTask(QThread):
    def __init__(self):
        super().__init__()
        self.stop = False

        self.start_time: float = 0  # 记录每次循环开始的时间

    def run(self):
        bus.info_signal.info_changed.emit('加载模型中...')

        while not self.stop:
            self.correction_fps()
            self.start_time = time.time()

            result = win32_screenshot()
            if result is None:
                bus.info_signal.info_changed.emit('未获取到游戏窗口')
                continue

            screen_shot, (l, t, r, b) = result
            bus.game_window.left = l
            bus.game_window.top = t
            bus.game_window.right = r
            bus.game_window.bottom = b

            model_output = model.predict(screen_shot, verbose=False)  # 关闭识别日志输出

            if len(model_output[0].boxes.data) == 0:
                bus.info_signal.info_changed.emit('未识别到目标')
                bus.float_window_signal.pos_updated.emit()
                bus.mouse_event.move = False
                bus.mouse_event.press = False
                continue

            bus.info_signal.info_changed.emit('识别到目标')

            # 更新所有目标框信息
            bus.target_window.target_all = model_output[0].boxes.xywh.tolist()

            # 提交更新信号, 让 bus.update_target 决定用什么规则更新攻击目标
            bus.update_target.updated.emit()

            if bus.option.show_border:
                bus.float_window_signal.pos_updated.emit()

            if bus.option.auto_aim:
                bus.mouse_event.move = True

            if bus.option.auto_fire:
                bus.mouse_event.press = True

        # 停止识别后将提示信息置空
        bus.info_signal.info_changed.emit('None')
        bus.info_signal.current_fps_changed.emit(0)

    def correction_fps(self):
        """
        修正 fps 为设置的值
        :return:
        """
        # 识别 + 操作 结束后计算用时, 再根据当前选择的fps判断是否需要sleep
        end_time = time.time()
        time_of_every_detect = 1 / bus.option.get_select_fps()
        if end_time - self.start_time < time_of_every_detect:
            time.sleep(time_of_every_detect - (end_time - self.start_time))

        # sleep 后, 整个流程结束, 再次获取时间, 计算实际的fps, 显示在界面上
        real_end_time = time.time()
        bus.info_signal.current_fps_changed.emit(1 // (real_end_time - self.start_time))
