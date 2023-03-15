import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon 여기서 가져옴
from PyQt5.QtCore import * 

import time

MAX = 10000

class BackgrondWorker(QThread): # PyQt5의 QThread 상속
    procChanged = pyqtSignal(int)   # 커스텀 시그널(마우스 클릭 같은 시그널을 따로 만드는 것) - 해야 정상적으로 스레드 처리 할 수 있음

    def __init__(self, count=0, parent=None) -> None:
        super().__init__()
        self.main = parent
        self.working = False # 스레드 동작여부 확인
        self.count = count

    def run(self):  # thread.star() 하면 대신 실행되는 함수
        # GUI 에 표시하기 위한거였는데,, 이 부분때문에 오류남
        # self.parent.pgbTask.setRange(0, 100)
        # for i in range(0, 101):
        #     print(f'스레드 출력 > {i}')
        #     self.parent.pgbTask.setValue(i)
        #     self.parent.txbLog.append(f'스레드 출력 > {i}')
        while self.working:
            if self.count <= MAX:
                self.procChanged.emit(self.count)   #emit()이 시그널을 내보내는 역할
                self.count += 1 # 단순히 값 증가만 확인 // 업무프로세스 동작하는 위치
                time.sleep(0.0001)  # 타임슬립안주면 스레드가 동시적으로 다 실행되어서 GUI 에 보일때 응답없음으로 처리 이상 생김.. 시간 쪼개줘야 GUI 에도 잘 보임
            else:
                self.working = False    # self.working이 True인 동안 동작하기 때문에, False 값을 줘서 동작을 멈추게 하는 것임    

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyThread/threadApp.ui', self)
        self.setWindowTitle('Thread App v0.1')
        self.pgbTask.setValue(0)

        self.btnStart.clicked.connect(self.btnStartClicked) # 내장된 시그널
        
        self.worker = BackgrondWorker(parent=self, count=0) # 스레드 생성
        self.worker.procChanged.connect(self.procUpdated)    # BackgroundWorker에 있는 시그널에 접근하는 슬롯함수

        self.pgbTask.setRange(0, MAX)

    # @pyqtSlot(int)    -- decoration.. 여기서는 없어도 동작함
    def procUpdated(self, count):
        self.txbLog.append(f'스레드 출력 > {count}')
        self.pgbTask.setValue(count)
        print(f'스레드 출력 > {count}')
        
    # @pyqtSlot()
    def btnStartClicked(self):
        self.worker.start() # 스레드 클래스 안의 run() 실행
        self.worker.working = True
        self.worker.count = 0 # 실행 끝난 후 버튼 누르면 재실행


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())