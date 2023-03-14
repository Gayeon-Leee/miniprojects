import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon 여기서 가져옴
from PyQt5.QtCore import * 

from gtts import gTTS
from playsound import playsound
import time


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/ttsApp.ui', self)
        # self.setWindowIcon(QIcon('./studyPython/settings.png'))
        self.setWindowTitle('Text To Speech v0.1')

        self.btnQrGen.clicked.connect(self.btnQrGenClicked)
        self.txtQrData.returnPressed.connect(self.btnQrGenClicked)

    def btnQrGenClicked(self):
        text = self.txtQrData.text()

        if text == '':
            QMessageBox.warning(self, '경고', '텍스트를 입력하세요')
            return
        
        tts = gTTS(text=text, lang='ko', slow=False)
        tts.save('./studyPython/output/hi.mp3')
        time.sleep(1.0)
        playsound('./studyPython/output/hi.mp3')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())