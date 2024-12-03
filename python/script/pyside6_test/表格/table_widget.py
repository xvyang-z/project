import random
from enum import Enum

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QTableWidget, QPushButton, QVBoxLayout, QApplication, QTableWidgetItem, QMenu


class StrEnum(str, Enum):
    """
    https://github.com/irgeek/StrEnum/blob/master/strenum/__init__.py
    StrEnum is a Python ``enum.Enum`` that inherits from ``str``. The default
    ``auto()`` behavior uses the member name as its value.

    Example usage::

        class Example(StrEnum):
            UPPER_CASE = auto()
            lower_case = auto()
            MixedCase = auto()

        assert Example.UPPER_CASE == "UPPER_CASE"
        assert Example.lower_case == "lower_case"
        assert Example.MixedCase == "MixedCase"
    """

    def __new__(cls, value, *args, **kwargs):
        if not isinstance(value, str):
            raise TypeError(
                f"Values of StrEnums must be strings: {value!r} is a {type(value)}"
            )
        return super().__new__(cls, value, *args, **kwargs)  # noqa

    def __str__(self):
        return str(self.value)

    def _generate_next_value_(self, *_):
        return self


class XTableWidget(QTableWidget):

    class RowData:
        def __init__(self, id_: int, name: str, age: int, is_active: bool):
            self.id = id_
            self.name = name
            self.age = age
            self.is_active = is_active

    class Header(StrEnum):
        名字 = 'name'
        年龄 = 'age'
        可用 = 'is_active'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QTableWidget::item:selected {
                background: #3399FF;
            }
        ''')

        self.setLineWidth(1)
        self.page_size = 20
        self.__data_all: list[XTableWidget.RowData] = []
        self.setColumnCount(len(self.Header))
        self.setHorizontalHeaderLabels(self.Header)

    @property
    def data_show(self):
        return self.__data_all[:self.page_size]

    def update_data_all(self):
        """ 更新所有数据 """
        self.__data_all = [self.RowData(id_=i+1, name=str(random.randint(1, 999)), age=random.randint(1, 999), is_active=True) for i in range(100)]

    def refresh_view(self):
        """ 刷新表格的显示, 只取 self.data_show 的进行显示 """
        self.setHorizontalHeaderLabels(self.Header)
        self.setRowCount(len(self.data_show))
        self.setColumnCount(len(self.Header))

        # 填充数据
        for row, row_data in enumerate(self.data_show):
            for col, header in enumerate(self.Header):
                item = QTableWidgetItem(str(getattr(row_data, header)))
                custom_data = {'原始前景色': item.foreground().color()}  # 设置一个自定义数据, 用于还原文本颜色
                item.setData(Qt.ItemDataRole.UserRole, custom_data)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.setItem(row, col, item)

    def contextMenuEvent(self, event):
        """ 自定义上下文菜单, 对选中的数据操作 """
        all_row = list(set([index.row() for index in self.selectedIndexes()]))

        if self.selectedItems():
            menu = QMenu(self)
            start_action = QAction(f'启动当前选中项 {len(all_row)}')
            delete_action = QAction(f'删除当前选中项 {len(all_row)}')

            start_action.triggered.connect(lambda: self.启动当前选中项(all_row))
            delete_action.triggered.connect(lambda: self.删除当前选中项(all_row))

            menu.addAction(start_action)
            menu.addSeparator()
            menu.addAction(delete_action)

            menu.exec(event.globalPos())
        super().contextMenuEvent(event)

    def 启动当前选中项(self, all_row: list[int]):
        self.启动(all_row)
        self.__禁用(all_row)
        self.clearSelection()

    def 删除当前选中项(self, all_row: list[int]):
        self.删除(all_row)
        self.__禁用(all_row)
        self.clearSelection()

    def 启动(self, all_row: list[int]):
        # 模拟api请求
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.__恢复(all_row))
        timer.start(3000)

    def 删除(self, all_row: list[int]):
        # 模拟api请求
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.__恢复(all_row))
        timer.start(3000)

    def __禁用(self, all_row: list[int]):
        for row in all_row:
            for col in range(self.columnCount()):
                item = self.item(row, col)
                item.setForeground(Qt.GlobalColor.lightGray)
                item and item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)

    def __恢复(self, all_row: list[int]):
        for row in all_row:
            for col in range(self.columnCount()):
                item = self.item(row, col)
                custom_data = item.data(Qt.ItemDataRole.UserRole)
                item.setForeground(custom_data['原始前景色'])
                item and item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEnabled)


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(1000, 200, 600, 400)

        self.table = XTableWidget(self)

        self.btn = QPushButton('获取数据并更新', self)
        self.btn.clicked.connect(lambda: (self.table.update_data_all(), self.table.refresh_view()))
        self.btn.click()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')  # QTableWidgetItem.setForeground() 设置前景色在 style == windows11 时失效

    main = Main()
    main.show()

    app.exec()
