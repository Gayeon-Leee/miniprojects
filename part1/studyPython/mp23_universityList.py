# 전국 대학교 지도 표시
# pip install pandas
import pandas as pd

filePath = './studyPython/university_list_2020.xlsx'
df_execl = pd.read_excel(filePath, engine='openpyxl')
df_execl.columns = df_execl.loc[4].tolist()
df_execl = df_execl.drop(index=list(range(0, 5)))   # 필요하지 않은 데이터 행 drop 시킴

print(df_execl.head())  # 상위 5개만 출력

print(df_execl['학교명'].values)
print(df_execl['주소'].values)