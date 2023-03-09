import sys 
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *   # QIcon 여기서 가져옴
from NaverApi import *
import webbrowser   # 웹브라우저 모듈
from urllib.request import urlopen


class qtApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./studyPyQt/naverApiMovie.ui', self)
        self.setWindowIcon(QIcon('./studyPyQt/movie.png'))

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
        url = self.tblResult.item(selected, 5).text()   #url link 5번 컬럼에 온다
        webbrowser.open(url)    # 웹사이트 오픈

    def txtSearchReturned(self):
        self.btnSearchClieked() 

    def btnSearchClieked(self):
        search = self.txtSearch.text()

        if search == '':
            QMessageBox.warning(self, '경고', '영화명 입력하세요')
            return
        else:
            api = NaverApi() # NaverApi 클래스 객체 생성
            node = 'movie' 
            display = 100

            result = api.get_naver_search(node, search, 1, display)
            # print(result)
            # 테이블위젯에 출력
            items = result['items'] # json 결과 중에서 items 아래 배열만 추출
            self.makeTable(items)   # 테이블위젯에 데이터들 할당

    # 테이블 위젯에 데이터 표시하기 위한 함수 - 네이버 영화 결과에 맞춰서 변경
    def makeTable(self, items) -> None:
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) # 단일선택
        self.tblResult.setColumnCount(7)    #컬럼 개수 변경
        self.tblResult.setRowCount(len(items))  # 현재 지정한 100개만큼 행 생성
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '개봉년도', '감독', '출연진', '평점', '링크', '포스터'])
        self.tblResult.setColumnWidth(0, 150)
        self.tblResult.setColumnWidth(1, 70) # 개봉년도
        self.tblResult.setColumnWidth(4, 50) # 평점        
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # 컬럼 데이터 수정 금지

        for i, post in enumerate(items): # 0, 뉴스 .. 
            title = self.replaceHtmlTag(post['title'])  #HTML 특수문자 변환 // 영어제목 가져오기 추가해야함
            subtitle = post['subtitle']
            title = f'{title} ({subtitle})'
            pubDate = post['pubDate']
            director = post['director'].replace('|', ',')[:-1]  # [:-1] 형태로 자르는건 파이썬에서만 가능
            actor = post['actor'].replace('|', ',')[:-1]
            userRating = post['userRating']
            link = post['link']
            img_url = post['image']
            # 포스터 이미지 추가
            if img_url != '': # 빈값이면 포스터 없는 영화임
                data = urlopen(img_url).read()  # 2진데이터 - 네이버영화에 있는 이미지 다운 -> 이때 이미지는 텍스트형태의 데이터임
                image = QImage()
                image.loadFromData(data)
                # QTableWidget에는 이미지를 그냥 넣을 수 없음.. QLabel() 집어 넣은 뒤 QLabeldmf QTableWidget에 할당
                imgLabel = QLabel()
                imgLabel.setPixmap(QPixmap(image))

                # data를 이미지로 저장
                # f = open(f'./studyPyQt/temp/image_{i+1}.png', mode='wb')    #파일쓰기
                # f.write(data)
                # f.close()
            

            # setItem(행, 열, 넣을 데이터)
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(director))
            self.tblResult.setItem(i, 3, QTableWidgetItem(actor))
            self.tblResult.setItem(i, 4, QTableWidgetItem(userRating))
            self.tblResult.setItem(i, 5, QTableWidgetItem(link))
            if img_url != '':
                self.tblResult.setCellWidget(i,6, imgLabel)    
                self.tblResult.setRowHeight(i, 150)      # 포스터가 있으면 쉘 높이를 늘림 
            else:
                self.tblResult.setItem(i, 6, QTableWidgetItem('No Poster!'))
                
            

    def replaceHtmlTag(self, sentence) -> str :
        result = sentence.replace('&lt', '<').replace('&gt;', '>').replace('<b>', '').replace('</b>', '').replace('&apos;', "'").replace('&quot;', '"') 
        # 변환 안된 특수문자가 나타나면 여기 추가

        return result



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = qtApp()
    ex.show()
    sys.exit(app.exec_())