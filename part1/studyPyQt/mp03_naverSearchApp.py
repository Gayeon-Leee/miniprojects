import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from NaverApi import *
import webbrowser   # 웹브라우저 모듈

class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiSearch.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/newspaper.png'))

        # 검색 버튼 클릭시그널 / 슬롯함수
        self.btnSearch.clicked.connect(self.btnSearchClieked)
        # 검색어 입력 후 엔터 치면 처리
        self.txtSearch.returnPressed.connect(self.txtSearchReturned)
        self.tblResult.doubleClicked.connect(self.tblResultDoubleClicked)

    def tblResultDoubleClicked(self):
        # row = self.tblResult.currentIndex().row()
        # column = self.tblResult.currentIndex().column()
        # print(row, column)
        selected = self.tblResult.currentRow()
        url = self.tblResult.item(selected, 1).text()
        webbrowser.open(url)    # 웹사이트 오픈

    def txtSearchReturned(self):
        self.btnSearchClieked() 

    def btnSearchClieked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '검색어를 입력하세요')
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'news' # movie 로 변경하면 영화검색
            outputs = [] # 결과 담을 리스트 변수
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # 테이블위젯에 출력
            items = result['items'] # json 결과 중에서 items 아래 배열만 추출
            self.makeTable(items)   # 테이블위젯에 데이터들 할당

    # 테이블 위젯에 데이터 표시하기 위한 함수
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(items))  # 현재 지정한 100개만큼 행 생성
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 310)
        self.tblResult.setColumnWidth(1, 260)
        # 컬럼 데이터 수정 금지
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, post in enumerate(items): # 0, 뉴스 .. 
            title = self.replaceHtmlTag(post['title'])
            originallink = post['originallink']
            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(originallink))

    def replaceHtmlTag(self, sentence) -> str :
        result = sentence.replace('&lt', '<').replace('&gt;', '>').replace('<b>', '').replace('</b>', '').replace('&apos;', "'").replace('&quot;', '"') 
        # 변환 안된 특수문자가 나타나면 여기 추가

        return result



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())