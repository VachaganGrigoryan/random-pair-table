from PyQt5 import QtWidgets
from controller import MainWindowUi
import sys

class AppContext(QtWidgets.QApplication):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open('style.qss', 'r') as style:
            qss = style.read()
        self.setStyleSheet(qss)

    def run(self):
        window = MainWindowUi(objectName='mainWidget')
        window.setWindowTitle("Player Random Pairs")
        window.resize(550, 300)
        window.show()
        return self.exec_() 


if __name__ == "__main__":
   
    appctxt = AppContext(sys.argv)                  
    exit_code = appctxt.run()
    sys.exit(exit_code)