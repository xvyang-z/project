from PyQt5.QtCore import QThread, QObject, pyqtSignal

import bus


class __UpdateTarget(QObject):
    updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.last_target_center: tuple[float, float] = (0, 0)  # 记录上次识别的目标中心点 x, y 坐标
        self.updated.connect(self.update)

    def update(self):
        self.update_target_recent_center()

    # def max_score_target(self, all_target: list) -> list[float, float, float, float]:
    #     """
    #     :param all_target: 所有目标 左 上 右 下 坐标
    #     :return: 得分最高的目标
    #     """
    #     return all_target[0]

    def update_target_recent_last(self):
        """
        更新 攻击目标为 上次攻击目标 的 最近目标
        """
        min_distances = 1e10
        min_index = 0
        for index, elem in enumerate(bus.target_window.target_all):
            center = (elem[0], elem[1])

            # 不用开方一样
            distance = (center[0] - bus.target_window.target[0]) ** 2 + (center[1] - bus.target_window.target[1]) ** 2
            if distance < min_distances:
                min_index = index

        bus.target_window.target = bus.target_window.target_all[min_index]

    def update_target_recent_center(self):
        """
        更新 攻击目标为 离游戏中心(准星位置)最近的的目标
        :return:
        """
        min_distances = 1e10
        min_index = 0

        game_window_center = (
            (bus.game_window.right - bus.game_window.left) // 2,
            (bus.game_window.bottom - bus.game_window.top) // 2
        )

        for index, elem in enumerate(bus.target_window.target_all):
            center = (elem[0], elem[1])

            # 不用开方一样
            distance = (center[0] - game_window_center[0]) ** 2 + (center[1] - game_window_center[1]) ** 2
            if distance < min_distances:
                min_index = index

        bus.target_window.target = bus.target_window.target_all[min_index]
