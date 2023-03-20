import pandas as pd
import folium

filePath = './studyPython/university_locations.xlsx'
df_excel = pd.read_excel(filePath, engine='openpyxl', header=None)
df_excel.columns = ['학교명', '주소', 'lng', 'lat'] # 0,1,2,3 인덱스에 학교명, 주소, 경도, 위도 넣어주는 것

# print(df_excel)

name_list = df_excel['학교명'].to_list()
addr_list = df_excel['주소'].to_list()
lng_list = df_excel['lng'].to_list()
lat_list = df_excel['lat'].to_list()

fMap = folium.Map(location=[37.553175, 126.989326], zoom_start=10)

for i in range(len(name_list)): # 총 개수인 446번 반복
    if lng_list[i] != 0:    # 위/경도 값이 0이 아니면 출력
        marker = folium.Marker([lat_list[i], lng_list[i]], popup=name_list[i], icon=folium.Icon(color='blue'))
        marker.add_to(fMap)

fMap.save('./studyPython/Korea_universities.html')