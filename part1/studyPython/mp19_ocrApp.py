# 글자 추출
from PIL import Image  # 이미지처리 모듈 pip install pillow
import pytesseract as tess # OCR 모듈 pip install pytesseract
# Tesseract-OCR 컴퓨터 설치 필요 - 파이썬의 모듈은 이걸 가져다쓰는 중간단계임!

img_path = './studyPython/이미지.png'
tess.pytesseract.tesseract_cmd = 'C:/DEV/Tools/Tesseract-OCR/tesseract.exe'

result = tess.image_to_string(Image.open(img_path), lang='kor')
print(result)