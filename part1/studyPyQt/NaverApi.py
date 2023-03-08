# NaverApi 클래스 - OpneAPI 인터넷 통해서 데이터를 전달받음
from urllib.request import Request, urlopen
from urllib.parse import quote
import datetime # 현재시간 사용
import json # 결과는 json으로 리턴받음

class NaverApi:
    # 생성자
    def __init__(self) -> None:
        print(f'[{datetime.datetime.now()}] Naver API 생성')

    # Naver API 요청 함수
    def get_request_url(self, url):
        req = Request(url)
        # Naver API 개인별 인증
        req.add_header('X-NAVER-Client-Id','X4wzWwxTGyAaWNaVlzr6')
        req.add_header('X-NAVER-Client-Secret','HjVfjQzjRC')
        
        try:
            res = urlopen(req)  # 요청 결과 바로 돌아옴
            if res.getcode() == 200: # response OK
                print(f'[{datetime.datetime.now()}] NaverAPI 요청 성공')
                return res.read().decode('utf-8')
            else:
                print(f'[{datetime.datetime.now}] NaverAPI 요청 실패')
                return None
        except Exception as e:
            print(f'[{datetime.datetime.now}] 예외발생 : {e}')
            return None

    # 실제 호출 함수
    def get_naver_search(self, node, search, start, display):
        base_url = 'https://openapi.naver.com/v1/search'
        node_url = f'/{node}.json'
        params = f'?query={quote(search)}&start={start}&display={display}'
        
        url = base_url + node_url + params
        retData = self.get_request_url(url)

        if retData == None:
            return None
        else:
            return json.loads(retData)

    # # json 데이터를 list로 변환시키는 함수 => 사용안함
    # def get_post_data(self, post, outputs) -> None:
    #     title = post['title']
    #     description = post['description']
    #     originallink = post['originallink']
    #     link = post['link']
    #     # 문자열로 들어있는 시간 정보 'Tue, 07 Mar 2023 09:45:00 +0900'를 날짜형으로 변환 
    #     pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S + 0900')
    #     pubDate = pDate.strftime('%Y-%m-%d %H:%M:%S') # 2023-03-07 09:45:00 으로 변경하는 것

    #     # outputs에 옮기기
    #     outputs.append({'title':title, 'description':description, 
    #                     'originallink':originallink, 'link':link,
    #                     'pubDate':pubDate})

