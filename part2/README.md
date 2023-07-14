# 미니프로젝트 part2
기간 - 2023.05.02 ~ 2023.05.16

## WPF 학습
- SCADA 시뮬레이션 (SmartHome 시스템) 시작
	- C# WPF
	- MahApps.Metro (MetroUI 라이브러리)
	- Bogus (더미데이터 생성 라이브러리)
	- Newtonsoft.json
	- M2Mqtt(통신 라이브러리)
	- DB 데이터바인딩 (MySql)
	- LiveCharts
	- OxyPlot
	
- SmartHome 시스템 문제점
	- 실행 후 시간이 소요되면 UI 제어가 느려짐 - TextBox에 텍스트가 과도해서 발생 - 해결!
	- LiveCharts는 대용량 데이터 차트는 무리(LiveChart v.2도 동일)
	- 대용량 데이터 차트는 OxyPlot 사용
	

온습도 더미데이터 시뮬레이터
<img src="https://raw.githubusercontent.com/Gayeon-Leee/miniprojects/main/Images/smartghome_publisher.gif" width="514" />

스마트홈 모니터링 앱
<img src="https://raw.githubusercontent.com/Gayeon-Leee/miniprojects/main/Images/samrthome_monitoring.gif" width="514" />
<img src="https://raw.githubusercontent.com/Gayeon-Leee/miniprojects/main/Images/smarthome_monitoring2.png" width="514" />
