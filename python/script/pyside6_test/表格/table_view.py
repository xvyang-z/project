import random
import sys

from PySide6.QtCore import Qt, QAbstractTableModel, QEvent
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QApplication, QTableView, QStyledItemDelegate, QStyleOptionButton, QStyle, QWidget, QVBoxLayout,
    QPushButton, QMenu
)


class XTableViewDelegate(QStyledItemDelegate):
    def __init__(self, parent: 'XTableView'):
        super().__init__(parent)
        self.parent = parent

    def paint(self, painter, option, index):
        """ 指定列实现样式重绘 """
        match index.column():
            case 3 | 4:
                btn_opt = QStyleOptionButton()
                btn_opt.rect = option.rect
                btn_opt.text = self.parent.model.headers[index.column()]
                QApplication.style().drawControl(QStyle.ControlElement.CE_PushButton, btn_opt, painter)
            case _:
                super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        """ 事件触发时做些操作 """
        match index.column(), event.type():
            case 3, QEvent.Type.MouseButtonRelease:
                print(self.parent.model.headers[index.column()], index.row())
                return True
            case 4, QEvent.Type.MouseButtonRelease:
                print(self.parent.model.headers[index.column()], index.row())
                return True
            case _:
                return super().editorEvent(event, model, option, index)


class XTableViewModel(QAbstractTableModel):
    def __init__(self, headers: list[str], parent: 'XTableView' = None):
        super().__init__(parent)
        self.page_size: int = 10
        self.headers: list[str] = headers

        self.data_all: list = []
        self.data_show: list = []

        self.__parent = parent

    def rowCount(self, index=...):
        return len(self.data_show)

    def columnCount(self, index=...):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        match role:
            case Qt.ItemDataRole.DisplayRole:
                return str(self.data_show[index.row()][index.column()])

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        match orientation, role:
            case Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole:
                return self.headers[section]
            case Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole:
                return str(section)
            case _:
                return super().headerData(section, orientation, role)

    def get_data_all(self):
        self.data_all = [[f'{random.random():.2f}'] * 3] * 100

    def update(self):
        self.data_show = self.data_all[:self.page_size]
        self.layoutChanged.emit()


class XTableView(QTableView):
    def __init__(self, headers: list[str], parent: QWidget = None):
        super().__init__(parent)

        self.setStyleSheet("""
            QTableView::item:selected {
                background-color: #26d;  /* 选中项的背景颜色 */
                color: white;  /* 选中项的文字颜色 */
            }
        """)

        self.verticalHeader().hide()

        self.model = XTableViewModel(headers, self)
        self.delegate = XTableViewDelegate(self)

        self.setModel(self.model)
        self.setItemDelegate(self.delegate)

    def contextMenuEvent(self, event):
        selected_all_row = set([index.row() for index in self.selectedIndexes()])
        if selected_all_row:
            menu = QMenu(self)
            action = QAction(f'启动当前选中项 {len(selected_all_row)}')
            action.triggered.connect(self.启动当前选中项)
            menu.addAction(action)
            menu.exec(event.globalPos())
        super().contextMenuEvent(event)

    def 启动当前选中项(self):
        all_row = set([index.row() for index in self.selectedIndexes()])
        print(all_row)


class Main(QWidget):
    def __init__(self):
        super().__init__()

        h = ['h0', 'h1', 'h2', 'h3', 'h4']

        self.table = XTableView(h, self)
        self.table.setGeometry(1000, 200, 600, 400)

        self.btn = QPushButton('???', self)
        self.btn.clicked.connect(lambda: (self.table.model.get_data_all(), self.table.model.update()))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    main = Main()
    main.show()

    app.exec()
