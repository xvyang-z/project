import sys

from PyQt5.QtWidgets import QApplication

from gui.py_ui.main import Main


def run_gui():
    app = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
