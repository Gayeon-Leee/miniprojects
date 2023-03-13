import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon 여기서 가져옴
from PyQt5.QtCore import * 

import psutil
import socket
import requests


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPython/comInfo.ui', self)
        self.setWindowIcon(QIcon('./studyPython/settings.png'))
        self.setWindowTitle('내 컴퓨터 정보 v0.1')

        self.btnRefresh.clicked.connect(self.btnRefreshClicked)
        self.initInfo()

    def btnRefreshClicked(self):
        self.initInfo()


    def initInfo(self):
        cpu = psutil.cpu_freq()
        cpu_ghz = round(cpu.current / 1000, 2)  # 1000으로 나누고 소수점 2번째자리에서 반올림
        self.lblCPU.setText(f'{cpu_ghz:.2f} GHz') #2.90 으로 나오게 포맷팅 한 것(.2f 없으면 2.9로 나옴)
        
        core = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)
        self.lblCore.setText(f'{core} 개 / 논리프로세서 {logical} 개')
        
        memory = psutil.virtual_memory()
        mem_total = round(memory.total / 1024**3)
        self.lblMemory.setText(f'{mem_total} GB')

        disks = psutil.disk_partitions()
        for disk in disks:
            if disk.fstype == 'NTFS':
                du = psutil.disk_usage(disk.mountpoint)
                du_total = round(du.total / 1024**3)
                msg = f'{disk.mountpoint} {disk.fstype} - {du_total} GB'
                self.lblDisk.setText(msg)
                break
        
       # print(psutil.net_if_addrs()) 결과값 // 내부.외부 IP 확인
        in_addr = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #내부아이피
        in_addr.connect(('www.google.com', 443))
        self.lblInnerNet.setText(in_addr.getsockname()[0])

        req = requests.get('http://ipconfig.kr')    #외부아이피
        out_addr = req.text[req.text.find('<font color=red>')+17:req.text.find('</font><br>')]
        self.lblExtraNet.setText(out_addr)

        #전송상태
        net_stat = psutil.net_io_counters()
        sent = round(net_stat.bytes_sent / 1024**2, 1)
        recv = round(net_stat.bytes_recv / 1024**2, 1)
        self.lblNetStat.setText(f'송신 - {sent} MB / 수신 = {recv} MB')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())