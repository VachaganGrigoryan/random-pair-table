from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont

import view as ui


class MainWindowUi(QtWidgets.QMainWindow):
    """MainWindowUi's View (GUI)."""

    def __init__(self, parent=None, flags=QtCore.Qt.WindowFlags(), *args, **kwargs):
        super(MainWindowUi, self).__init__(parent=parent, flags=flags, *args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.centralwidget = ui.PlayerPairs()
        self.setCentralWidget(self.centralwidget)

