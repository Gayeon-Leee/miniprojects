using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        public bool IsConnected { get; set; } // 접속 여부 확인하기 위함

        Thread MqttThred { get; set; } // 없으면 UI 컨트롤 어려워짐

        int MaxCount { get; set; } = 50; // 23.05.11 09:29 MQTT Subscribtion text 과도 문제 속도 저하를 잡기 위해 변수 추가

        public DataBaseControl()
        {
            InitializeComponent();
        }


        // 유저 컨트롤 로드 이벤트 핸들러
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxtConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false; // 아직 접속 안됨
            BtnConnDB.IsChecked = false;

            // 실시간 모니터링에서 넘어왔을때
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
            {
                IsConnected = true;
                BtnConnDB.IsChecked = true;
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;

            }
        }

        // 토글버튼 클릭 이벤트 핸들러 (토글버튼은 한 번 누르면 on / 한 번 더 누르면 off 개념) 
        private void BtnConnDB_Click(object sender, RoutedEventArgs e)
        {
           ConnectDB();
        }

        private void ConnectDB()
        {
            if (IsConnected == false)
            {

                // Mqtt 브로커 생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);

                try
                {
                    // Mqtt subscribe 로직 처리
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        // Mqtt 접속
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR"); // clientId = 모니터
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                                                      new byte[] { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE }); // QOS는 네트워크 통신의 옵션. QOS_LEVEL_AT_LEAST_ONCE는 수신여부와 상관없이 한 번 보내는 것
                        UpdateLog(">>> MQTT Broker Connected");

                        BtnConnDB.IsChecked = true;
                        BtnConnDB.Content = "MQTT 연결중";
                        IsConnected = true; // 예외 발생하면 IsConnected true X => try문 안에 넣는 것

                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT Error 발생 : {ex.Message}");
                }

            }
            else // 접속 끊을 때
            {
                try
                {
                    if (Commons.MQTT_CLIENT.IsConnected)
                    {
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived -= MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Disconnect();
                        UpdateLog(">>> MQTT Broker Disconnected...");

                        BtnConnDB.IsChecked = false;
                        BtnConnDB.Content = "MQTT 연결 종료";
                        IsConnected = false;
                    }
                }
                catch (Exception ex)
                {
                    UpdateLog($"!!! MQTT Error 발생 : {ex.Message}");
                }
            }
        }

        private void UpdateLog(string msg)
        {
            this.Invoke(() => {
                if(MaxCount <= 0)
                {
                    TxtLog.Text = string.Empty;
                    TxtLog.Text += ">>> 문서 건수가 많아져서 초기화!\n";
                    TxtLog.ScrollToEnd();
                    MaxCount = 50; // 실제 운영시는 50으로 하더라도 테스트 할때는 10정도로 작은 숫자 넣어서 볼 것
                }

                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
                MaxCount--;
            });
        }

        // Subscribe 발생할 때 이벤트 핸들러
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            UpdateLog(msg);
            SetToDataBase(msg, e.Topic); // 실제 DB에 저장처리
        }

        // DB 저장 처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null)
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["Room_Name"]);
                //Debug.WriteLine(currValue["Sensing_DateTime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);
                try
                {
                    using(MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                    {
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        {
                            string insQuery = @"INSERT INTO smarthomesensor
                                                            (Home_Id,
                                                            Room_Name,
                                                            Sensing_DateTime,
                                                            Temp,
                                                            Humid)
                                                           VALUES
                                                            (@Home_Id,
                                                            @Room_Name,
                                                            @Sensing_DateTime,
                                                            @Temp,
                                                            @Humid)";

                            MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                            cmd.Parameters.AddWithValue("@Home_Id", currValue["Home_Id"]);
                            cmd.Parameters.AddWithValue("@Room_Name", currValue["Room_Name"]);
                            cmd.Parameters.AddWithValue("@Sensing_DateTime", currValue["Sensing_DateTime"]);
                            cmd.Parameters.AddWithValue("@Temp", currValue["Temp"]);
                            cmd.Parameters.AddWithValue("@Humid", currValue["Humid"]);

                            if (cmd.ExecuteNonQuery() == 1)
                            {
                                UpdateLog(">>> DB Insert succeed");
                            }
                            else
                            {
                                UpdateLog(">>> DB Insert failed"); // 일어날일 거의 없긴함
                            }
                        }
                    }
                }
                catch (Exception ex)
                {

                    UpdateLog($"!!! DB Error 발생 : {ex.Message}");
                }
            }
        }
    }
}
