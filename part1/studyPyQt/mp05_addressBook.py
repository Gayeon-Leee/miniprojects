# 주소록 GUI 프로그램 - MySQL 연동
import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon 여기서 가져옴
import pymysql

class qtApp(QMainWindow):
    conn = None
    curIdx = 0  # 현재 데이터의 PK

    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/addressBook.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/address-book.png'))
        self.setWindowTitle('주소록 v0.5')

        self.initDB()   # DB초기화

        # 버튼 시그널에 대한 슬롯함수 지정
        self.btnNew.clicked.connect(self.btnNewClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)
        self.tblAddress.doubleClicked.connect(self.tblAddressDoubleClicked)
        self.btnDel.clicked.connect(self.btnDelClicked)

    def btnDelClicked(self):
        if self.curIdx == 0:
            QMessageBox.warning(self, '경고', '삭제할 데이터를 선택하세요!')
            return  # 함수를 빠져나감
        else:
            reply = QMessageBox.question(self, '확인', '정말 삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.Yes)
            if reply == QMessageBox.No:
                return  # 삭제 진행 안함(함수 빠져나감)

            self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                        db='miniproject', charset='utf8')  
            query = 'DELETE FROM addressbook WHERE Idx = %s'
            cur = self.conn.cursor()
            cur.execute(query, (self.curIdx))

            self.conn.commit()
            self.conn.close()

            QMessageBox.about(self, '성공', '데이터를 삭제했습니다.')

            self.initDB()
            self.btnNewClicked()

    def btnNewClicked(self):    # 신규 버튼 누르면
        # 라인에디트 내용 모두 삭제 후 이름에 포커스 맞추게 하는 작업
        self.txtName.setText('')
        self.txtPhone.setText('')
        self.txtEmail.setText('')
        self.txtAddress.setText('')
        self.txtName.setFocus()
        self.curIdx = 0 # 0은 신규 => 0이면 신규저장, 0이 아닌 번호가 있으면 수정저장되도록 할 것임
        print(self.curIdx)

    def tblAddressDoubleClicked(self):
        rowIndex = self.tblAddress.currentRow() # 행번호
        self.txtName.setText(self.tblAddress.item(rowIndex, 1).text())
        self.txtPhone.setText(self.tblAddress.item(rowIndex, 2).text())
        self.txtEmail.setText(self.tblAddress.item(rowIndex, 3).text())
        self.txtAddress.setText(self.tblAddress.item(rowIndex, 4).text())
        self.curIdx = int(self.tblAddress.item(rowIndex, 0).text())
        print(self.curIdx)    

    def btnSaveClicked(self): # 저장
        Fullname = self.txtName.text()
        Phonenum = self.txtPhone.text()
        Email = self.txtEmail.text()
        Address = self.txtAddress.text()

        # print(Fullname, Phonenum, Email, Address)
        # 이름과 전화번호를 입력하지 않으면 알람
        if Fullname == '' or Phonenum == '':
            QMessageBox.warning(self, '주의', '이름과 핸드폰 번호를 입력하세요!')
            return # 이름, 전화번호 미입력시 진행불가
        else:
            self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db='miniproject', charset='utf8')
            if self.curIdx == 0:    # 신규 네개 변수값 받아서 INSERT 쿼리문 만들기
                query = '''INSERT INTO addressbook (Fullname, Phonenum, Email, Address)
				            VALUES (%s, %s, %s, %s)'''    
            else:
                query = '''UPDATE addressbook
                              SET Fullname = %s
                                ,  Phonenum = %s
                                ,  Email = %s
                                ,  Address = %s
                            WHERE Idx = %s'''     
            
            cur = self.conn.cursor()
            if self.curIdx == 0:
                cur.execute(query, (Fullname, Phonenum, Email, Address))
            else:
                cur.execute(query, (Fullname, Phonenum, Email, Address, self.curIdx))

            self.conn.commit()
            self.conn.close()

            # 저장성공 메세지 출력
            if self.curIdx == 0:
                QMessageBox.about(self, '성공', '저장 완료했습니다!')
            else:
                QMessageBox.about(self, '성공', '변경 완료했습니다!')
                
            
            self.initDB() # QTableWidget에 새 데이터 반영
            self.btnNewClicked() # 저장 후 입력 창 내용 없어지게



    def initDB(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='12345',
                                    db='miniproject', charset='utf8')
        cur = self.conn.cursor()
        query = '''SELECT Idx
                        , Fullname
                        , Phonenum
                        , Email
                        , Address
                     FROM addressbook''' # 멀티라인 문자열
        cur.execute(query)
        rows = cur.fetchall()

        # print(rows)
        self.makeTable(rows)
        self.conn.close()   # 프로그램 종료할 때 

    def makeTable(self, rows):
        self.tblAddress.setColumnCount(5)   # 열개수
        self.tblAddress.setRowCount(len(rows))  # 행개수
        self.tblAddress.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        self.tblAddress.setHorizontalHeaderLabels(['번호', '이름', '핸드폰', '이메일', '주소']) # 열제목
        self.tblAddress.setColumnWidth(0,0) # 번호는 숨김
        self.tblAddress.setColumnWidth(1,70) # 이름 열 사이즈 70
        self.tblAddress.setColumnWidth(2,105) # 핸드폰 열 사이즈 105
        self.tblAddress.setColumnWidth(3,175)  # 이메일 열 사이즈 175
        self.tblAddress.setColumnWidth(4,200)   # 주소 열 사이즈 200
        self.tblAddress.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 컬럼 수정금지

        for i, row in enumerate(rows):
            Idx = row[0]
            Fullname = row[1]
            Phonenum = row[2]
            Email = row[3]
            Address = row[4]

            self.tblAddress.setItem(i, 0, QTableWidgetItem(str(Idx)))
            self.tblAddress.setItem(i, 1, QTableWidgetItem(Fullname))
            self.tblAddress.setItem(i, 2, QTableWidgetItem(Phonenum))
            self.tblAddress.setItem(i, 3, QTableWidgetItem(Email))
            self.tblAddress.setItem(i, 4, QTableWidgetItem(Address))

        self.stbCurrent.showMessage(f'전체 주소록 : {len(rows)}개')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())