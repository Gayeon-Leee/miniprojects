import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon 여기서 가져옴
from PyQt5.QtCore import * 

import time

class BackgrondWorker(QThread): # PyQt5의 QThread 상속
    procChanged = pyqtSignal(int)

    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = True # 스레드 동작여부 확인
        self.count = count

    def run(self):
        # GUI 에 표시하기 위한거였는데,, 이거때문에 오류남
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txbLog.append(f'스레드 출력 > {i}')
        while self.working:
            self.procChanged.emit(self.count)   #emit()이 시그널을 내보내는 역할
            self.count += 1 # 단순히 값 증가만 확인하는 것
            time.sleep(0.0001)

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('Thread App v0.1')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked)
        
        self.worker = BackgrondWorker(parent=self, count=0) # 스레드 초기화
        self.worker.procChanged.connect(self.procUpdated)    # BackgroundWorker에 있는 시그널에 접근하는 슬롯함수

        self.pgbTask.setRange(0, 1000000)

    @pyqtSlot(int)
    def procUpdated(self, count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')
        
    @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start()
        self.worker.working = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())