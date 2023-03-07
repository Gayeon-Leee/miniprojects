# PyQt 복습
import sys
from PyQt5.QtWidgets import *

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lblMessage = QLabel('메시지: ', self)
        self.lblMessage.setGeometry(10, 5, 300, 50)

        btnOK = QPushButton('OK', self) # def 안에서만 쓰는 지역변수라 self 안붙임
        btnOK.setGeometry(280, 250, 100, 40)
        # PyQt 클릭하고 키보드 누르는 등의 시그널 => 이벤트 // 시그널 처리 => 이벤트핸들러(슬롯)
        btnOK.clicked.connect(self.btnOK_clicked)

        self.setGeometry(300, 200, 400, 300)
        self.setWindowTitle('복습PyQt')
        self.show()

    def btnOK_clicked(self):
        self.lblMessage.clear()
        self.lblMessage.setText('메시지: OK!!!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    sys.exit(app.exec_())