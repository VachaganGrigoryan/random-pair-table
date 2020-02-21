from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont

from models import Player, Team, RandomPairTable

class PlayerPairs(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.MainLayout = QtWidgets.QGridLayout()
        
        self.Players = QtWidgets.QGridLayout()
        self.Players.addWidget(QtWidgets.QLabel("People\'s names", objectName='players'), 0, 0)
        
        self.isPair = QtWidgets.QCheckBox('Pair', objectName='checkBox')
        self.isPair.setChecked(True)
        self.Players.addWidget(self.isPair, 0, 1)
        self.isPair.stateChanged.connect(self.checkPairState)

        self.Players.addWidget(QtWidgets.QLineEdit(), 1, 0)
        
        self.pb_addPlayer = QtWidgets.QPushButton("Add", objectName='addBtn')
        self.Players.addWidget(self.pb_addPlayer, 1, 1)
        self.pb_addPlayer.clicked.connect(self.addRow('Players'))
        self.MainLayout.addLayout(self.Players, 0, 0)

        self.Teams = QtWidgets.QGridLayout()
        self.Teams.addWidget(QtWidgets.QLabel(f"Team names", objectName='teams'), 0, 0)

        self.isTeam = QtWidgets.QCheckBox('On', objectName='checkBox')
        self.isTeam.setChecked(True)
        self.Teams.addWidget(self.isTeam, 0, 1)
        self.isTeam.stateChanged.connect(self.checkTeamState)

        self.Teams.addWidget(QtWidgets.QLineEdit(), 1, 0)
        
        self.pb_addTeam = QtWidgets.QPushButton("Add", objectName='addBtn')
        self.Teams.addWidget(self.pb_addTeam, 1, 1)
        self.pb_addTeam.clicked.connect(self.addRow('Teams'))
        self.MainLayout.addLayout(self.Teams, 0, 1)
             
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MainLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.MainLayout)

        self.MainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.Players.setAlignment(QtCore.Qt.AlignTop)
        self.Teams.setAlignment(QtCore.Qt.AlignTop)
        
        self.equal = QtWidgets.QPushButton("Create", objectName='createBtn')
        self.verticalLayout.addWidget(self.equal)
        self.equal.clicked.connect(self.EqualCtrl)

    def checkTeamState(self):
        if self.isTeam.isChecked() == True:
            self.isTeam.setText("On")
            self.setTeamState(True)
        else:
            self.isTeam.setText("Off")
            self.setTeamState(False)

    def setTeamState(self, state):
        rows = self.Teams.rowCount()
        for row in range(1, rows):
            for column in range(self.Teams.columnCount()):
                layout = self.Teams.itemAtPosition(row, column)
                if layout is not None:
                    widget = layout.widget()
                    if isinstance(widget, QtWidgets.QPushButton) or row == rows-1:
                        widget.setEnabled(state)

    def checkPairState(self):
        if self.isPair.isChecked() == True:
            self.isPair.setText("Pair")
            self.isTeam.setEnabled(True)        
        else:
            self.isPair.setText("Unpair")
            self.setTeamState(True)
            self.isTeam.setEnabled(False)
            self.isTeam.setChecked(True)  

    def addRow(self, key):
        def _addRow():
            _func = eval(f'self.{key}')
            rows = _func.rowCount()
            for column in range(_func.columnCount()):
                layout = _func.itemAtPosition(rows - 1, column)
                if layout is not None:
                    widget = layout.widget()
                    if not widget.text():
                        return
                    if isinstance(widget, QtWidgets.QPushButton):
                        widget.setText('Remove')
                        widget.setStyleSheet("background-color: #f20c3a")
                        widget.clicked.disconnect(_addRow)
                        widget.clicked.connect(self.removeRow(key))
                    else:
                        widget.setEnabled(False)

            _func.addWidget(QtWidgets.QLineEdit(), rows, 0)

            widget = QtWidgets.QPushButton('Add', objectName='addBtn')
            widget.clicked.connect(self.addRow(key))
            _func.addWidget(widget, rows, 1)
        return _addRow
    
    def removeRow(self, key):
        def _removeRow():
            _func = eval(f'self.{key}')
            index = _func.indexOf(self.sender())
            row = _func.getItemPosition(index)[0]
            for column in range(_func.columnCount()):
                layout = _func.itemAtPosition(row, column)
                if layout is not None:
                    layout.widget().deleteLater()
                    _func.removeItem(layout)
        return _removeRow
       

    def EqualCtrl(self):

        p_len, t_len = self.Players.rowCount(), self.Teams.rowCount()

        players = [Player(self.Players.itemAtPosition(row, 0).widget().text()) for row in range(1, p_len-1) if self.Players.itemAtPosition(row, 0)]
        
        if self.isTeam.isChecked():
            teams = [Team(self.Teams.itemAtPosition(row, 0).widget().text()) for row in range(1, t_len-1) if self.Teams.itemAtPosition(row, 0)]
        else:
            teams = []
        
        layout = self.MainLayout.itemAtPosition(2, 0)
        if layout is not None:
            if layout.widget():
                layout.widget().deleteLater()
            else:
                PlayerPairs.deleteItemsOfLayout(layout)
            self.MainLayout.removeItem(layout)
        
        len_p = len(players)
        len_t = len(teams)

        if len_p  and len_p <= len_t and not self.isPair.isChecked():
            table = RandomPairTable(players, teams, False)
        elif len_p > 1 and (2*len_t >= len_p or not self.isTeam.isChecked()) and self.isPair.isChecked():
            table = RandomPairTable(players, teams, True)
        else:
            self.MainLayout.addWidget(QtWidgets.QLabel('Please enter all fields', objectName='error'), 2, 0, 2, 3)
            return
        
        self.Table = QtWidgets.QGridLayout(objectName='table')        
        # self.Table.addWidget(QtWidgets.QLabel('Id\'s', objectName='tableId'), 0, 0)
        self.Table.addWidget(QtWidgets.QLabel('Pairs of participants', objectName='tableId'), 0, 1, 0, 2)
        self.Table.addWidget(QtWidgets.QLabel('Game teams', objectName='tableId'), 0, 3)
        for item in table.pairs:
            # self.Table.addWidget(QtWidgets.QLabel(f'{item.id}', objectName='cell'), item.id, 0)
            self.Table.addWidget(QtWidgets.QLabel(f'{item.player_1}', objectName='cell'), item.id, 1)
            if item.player_2:
                self.Table.addWidget(QtWidgets.QLabel(f'{item.player_2}', objectName='cell'), item.id, 2)
            self.Table.addWidget(QtWidgets.QLabel(f'{item.team}', objectName='cell'), item.id, 3)
        
        self.MainLayout.addLayout(self.Table, 2, 0, 2, 3)

    @staticmethod
    def deleteItemsOfLayout(layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    deleteItemsOfLayout(item.layout())