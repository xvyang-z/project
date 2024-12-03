from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QItemSelection, QItemSelectionModel, QRect

class SelectableTableWidget(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setSelectionMode(QTableWidget.NoSelection)  # 禁用默认选择方式，改为自定义选择
        self.start_index = None  # 用于存储起始位置

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_index = self.indexAt(event.pos())  # 记录开始选择的单元格索引
            if self.start_index.isValid():
                self.clearSelection()  # 开始新选择时，清除之前的选择
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.start_index:
            current_index = self.indexAt(event.pos())  # 获取鼠标移动时的当前单元格索引
            if current_index.isValid():
                self.select_range(self.start_index, current_index)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_index:
            print(self.top_left)
            print(self.bottom_right)
            self.start_index = None  # 重置开始索引
            self.top_left = None
            self.top_right = None
        super().mouseReleaseEvent(event)

    def select_range(self, start_index, end_index):
        # 确定选择区域的矩形范围
        top_left = start_index if start_index.row() <= end_index.row() else end_index
        bottom_right = end_index if start_index.row() <= end_index.row() else start_index

        # 创建选择区域
        selection = QItemSelection(top_left, bottom_right)
        self.selectionModel().select(selection, QItemSelectionModel.Select)

        self.top_left = top_left
        self.bottom_right = end_index

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建表格
        self.table = SelectableTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(["Name", "Age", "Status"])

        # 添加示例数据
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f"Item {row + 1}, {col + 1}")
                self.table.setItem(row, col, item)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
