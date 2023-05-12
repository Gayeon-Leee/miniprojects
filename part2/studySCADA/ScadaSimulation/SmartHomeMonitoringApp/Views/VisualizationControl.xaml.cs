using OxyPlot;
using OxyPlot.Series;
using MySql.Data.MySqlClient;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using OxyPlot.Legends;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// VisualizationControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class VisualizationControl : UserControl
    {
        List<string> Divisons = null;

        string FirstSensingDate = string.Empty;

        int TotalDateCount = 0; // 검색된 데이터 개수 받을 변수



        public VisualizationControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            // 방 선택 콤보박스 초기화
            Divisons = new List<string> { "SELECT", "LIVING", "DINING", "BED", "BATH" };
            CboRoomName.ItemsSource = Divisons;
            CboRoomName.SelectedIndex = 0; // SELECT가 기본 선택

            // 검색시작일 날짜 - DB에서 제일 오래된 날짜 가져와서 할당
            using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                conn.Open();
                var dtQuery = @"SELECT F.Sensing_Date
                                 FROM(
	                                SELECT DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') AS Sensing_Date
	                                  FROM smarthomesensor
                                ) AS F
                                GROUP BY F.Sensing_Date
                                ORDER BY F.Sensing_Date ASC Limit 1;"; // Limit는 MySQL 에만 있음
                MySqlCommand cmd = new MySqlCommand(dtQuery, conn);
                var result = cmd.ExecuteScalar();
                Debug.WriteLine(result.ToString());
                FirstSensingDate = DtpStart.Text = result.ToString();

                // 검색 종료일은 현재일자 할당
                DtpEnd.Text = DateTime.Now.ToString("yyyy-MM-dd"); // 날짜 포맷 스트링 각 언어마다 다름.. 유의할것!
            }
            
        }

        // 검색버튼 클릭 이벤트 핸들러
        private async void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            // 입력검증 위한 변수
            bool isValid = true;
            string errorMsg = string.Empty;
            
            // DB상에 있던 데이터 담는 변수
            DataSet ds = new DataSet(); 

            #region < 입력검증 >
            // 검색, 저장, 수정, 삭제 전 반드시 검증
            if (CboRoomName.SelectedValue.ToString() == "SELECT")
            {
                isValid = false;
                errorMsg += "방구분을 선택하세요.\n";
                //await Commons.ShowCustomMessAsync("검색", "방 구분을 선택하세요.");
                //return;
            }

            if (DateTime.Parse(DtpStart.Text) < DateTime.Parse(FirstSensingDate)) // 시스템 시작된 날짜보다 이전 날짜로 검색할 경우
            {
                isValid = false;
                errorMsg += $"검색 시작일은 {FirstSensingDate} 이후로 선택하세요.\n";
                //await Commons.ShowCustomMessAsync("검색", $"검색 시작일은 {FirstSensingDate} 이후로 선택하세요.");
                //return;
            }

            if (DateTime.Parse(DtpEnd.Text) > DateTime.Now) // 오늘 날짜 이후 날짜로 검색할 경우
            {
                isValid = false;
                errorMsg += "검색 종료일은 오늘까지 가능합니다.\n";
                //await Commons.ShowCustomMessAsync("검색", "검색 종료일은 오늘까지 가능합니다.");
                //return;
            }

            if (DateTime.Parse(DtpStart.Text) > DateTime.Parse(DtpEnd.Text)) // 검색 시작일이 검색 종료일보다 이후면
            {
                isValid = false;
                errorMsg += "검색 시작일이 검색 종료일보다 최신일 수 없습니다.\n";
                //await Commons.ShowCustomMessAsync("검색", "검색 시작일이 검색 종료일보다 최신일 수 없습니다.");
                //return;
            }

            if (isValid == false) // 검증 사항이 여러개 일 경우 일일이 검색메세지 띄우는 것 보다 이런식으로 한꺼번에 띄워주는게 좋음
            {
                await Commons.ShowCustomMessAsync("검색", errorMsg);
                return;
            }
            #endregion

            #region < 실제 검색 >
            TotalDateCount = 0;
            try
            {
                using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                {
                    conn.Open();
                    var searchQuery = @"SELECT id,
	                                           Home_Id,
	                                           Room_Name,
                                               Sensing_DateTime,
                                               Temp,
                                               Humid
                                          FROM smarthomesensor
                                         WHERE UPPER(Room_Name) = @Room_Name    
                                           AND DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d')
                                       BETWEEN @StartDate AND @EndDate";
                    // 41행에서 Divisons = new List<string> { "SELECT", "LIVING", "DINING", "BED", "BATH" }; 이렇게 받았기 때문에
                    // WHERE 절에 UPPER 써써 대문자로 검색해주는게 좋음
                    MySqlCommand cmd = new MySqlCommand(searchQuery, conn);
                    cmd.Parameters.AddWithValue("@Room_Name", CboRoomName.SelectedValue.ToString());
                    cmd.Parameters.AddWithValue("@StartDate", DtpStart.Text); 
                    cmd.Parameters.AddWithValue("@EndDate", DtpEnd.Text);
                    // DtpStart/End.ToString() 하면 데이터 안넘어옴!!!!! 파라미터에 값이 제대로 안들어가서 검색이 안되기 때문
                    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);
                    
                    adapter.Fill(ds, "smarthomesensor");

                    //MessageBox.Show(ds.Tables["smarthomesensor"].Rows.Count.ToString(), "TotalData"); // -> 데이터 넘어왔는지 개수 확인
                }
            }
            catch(Exception ex)
            {
                await Commons.ShowCustomMessAsync("DB검색", $"DB검색 오류 {ex.Message}");
            }
            #endregion

            #region < DB에서 가져온 데이터 차트에 뿌리기 >
            // Create the plot model
            var tmp = new PlotModel { Title = $"{CboRoomName.SelectedValue} ROOM" }; // 선택한 방 이름이 타이틀로 나오게

            var legend = new Legend
            {
                LegendBorder = OxyColors.DarkGray,
                LegendBackground = OxyColor.FromArgb(150, 255, 255, 255),
                LegendPosition = LegendPosition.TopRight,
                LegendPlacement = LegendPlacement.Outside
            };
            tmp.Legends.Add(legend); // 범례 추가


            // Create two line series (markers are hidden by default)
            // 데이터가 있든 없든 차트에 반영되게 해야 데이터 없을 때 차트 안그림 -> 기본 설정을 아래 if문 안에 넣으면 데이터 없어도 이전 차트값 남아있음
            var tempSeries = new LineSeries
            {
                Title = "Temperature(℃)",
                MarkerType = MarkerType.Circle,
                Color = OxyColors.DarkOrange // 라인 색상 변경
            };
            var humidSeries = new LineSeries
            {
                Title = "Humidity(%)",
                MarkerType = MarkerType.Square,
                Color = OxyColors.CornflowerBlue // 라인 색상 변경
            };

            // 개수가 있을때 차트에 그리기
            if (ds.Tables[0].Rows.Count > 0)
            {
                TotalDateCount = ds.Tables[0].Rows.Count;

                var count = 0;
                foreach (DataRow row in ds.Tables[0].Rows)
                {
                    tempSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Temp"])));
                    humidSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Humid"])));
                }
            }

            tmp.Series.Add(tempSeries);
            tmp.Series.Add(humidSeries);

            OpvSmartHome.Model = tmp;

            LblTotalCount.Content = $"검색데이터 {TotalDateCount}개";
            #endregion
        }
    }
}
