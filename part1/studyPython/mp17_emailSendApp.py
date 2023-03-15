# 이메일 보내기 앱
import smtplib  # smtp : 메일 전송 프로토콜
from email.mime.text import MIMEText

send_email = 'gy9411@naver.com'
send_pass = '메일비밀번호'

recv_email = 'gy9411@gmail.com'

smtp_name = 'smtp.naver.com'
smtp_port = 587 # 포트 번호

text = '''메일 내용입니다. 긴급입니다. 
조심하세요~ 빨리 연락주세요!
'''

msg = MIMEText(text)
msg['Subject']  = '메일 제목입니다'
msg['From'] = send_email   
msg['To'] = recv_email
print(msg.as_string())

mail = smtplib.SMTP(smtp_name, smtp_port)   # SMTP 객체 생성
mail.starttls() #전송계층 보안시작
mail.login(send_email, send_pass)
mail.sendmail(send_email, recv_email, msg=msg.as_string())
mail.quit()
print('전송완료!')