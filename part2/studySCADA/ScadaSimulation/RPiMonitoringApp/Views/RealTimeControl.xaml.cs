using MahApps.Metro.Controls;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// RealTimeControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class RealTimeControl : UserControl
    {
        public RealTimeControl()
        {
            InitializeComponent();

            // 모든 차트의 최초값을 0으로 초기화
            LvcLivingTemp.Value = LvcDiningTemp.Value = LvcBedTemp.Value = LvcBathTemp.Value = 0;
            LvcLivingHumid.Value = LvcDiningHumid.Value = LvcBedHumid.Value = LvcBathHumid.Value = 0;
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected) // DB 모니터링을 실행한 뒤 실시간 모니터링으로 넘어왔다면
            {
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
            }
            else // DB 모니터링은 실행하지 않고 바로 실시간 모니터링 메뉴를 클릭했으면
            {
                Commons.MQTT_CLIENT = new MqttClient(Commons.BROKERHOST);
                Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                Commons.MQTT_CLIENT.Connect("MONITOR");
                Commons.MQTT_CLIENT.Subscribe(new string[] {Commons.MQTTTOPIC}, new byte[] {MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE});
            }
        }


        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            var msg = Encoding.UTF8.GetString(e.Message);
            Debug.WriteLine(msg);

            var currSensor = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg); // 역직렬화

            if (currSensor["DEV_ID"] == "IOT77") 
            {
                this.Invoke(() => {
                    var dfValue = DateTime.Parse(currSensor["CURR_DT"]).ToString("yyyy-MM-dd HH:mm:ss"); // 원하는 값만 나오게 파싱
                    LblSensingDt.Content = $"Sensing DateTime : {dfValue}";
                });
                /*
                MQTTclient는 단독 스레드 사용, UI 스레드에 직접 접근이 안됨 
                - 오류메세지 : 다른 스레드가 이 개체를 소유하고 있어 호출한 스레드가 해당 개체에 액세스할 수 없습니다.
                this.Invoke();로 UI 스레드 안에 있는 리소스에 접근하는 것
                */


                switch ("Living".ToUpper()) // 오류 방지 위해 대문자로 변경. 원래는 처음부터 대문자로 이름 정하는게 좋음!
                {
                    
                    case "LIVING":
                        this.Invoke(() => { // UI 스레드랑 충돌 안나게 하는거. 이렇게 안하면 스레드간 충돌일어나서 오류남
                            var tmp = currSensor["STAT"].Split('|');
                            var temp = tmp[0].Trim(); // "29. 0 " 형태로 값 넘어오기때문에 Trim()으로 공백 제거
                            var humid = tmp[1].Trim();
                            LvcLivingTemp.Value = Math.Round(Convert.ToDouble(temp), 1);
                            LvcLivingHumid.Value = Convert.ToDouble(humid); // Value에 들어가는 값이 double 이라 형변환 해줘야함
                        });
                       
                        break;

                    case "DINING":
                        this.Invoke(() =>{
                            LvcDiningTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1);
                            LvcDiningHumid.Value = Convert.ToDouble(currSensor["Humid"]);
                        });
                        
                        break;

                    case "BED":
                        this.Invoke(() => { 
                            LvcBedTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1); 
                            LvcBedHumid.Value = Convert.ToDouble(currSensor["Humid"]); 
                        });
                        break;

                    case "BATH":
                        this.Invoke(() => { 
                            LvcBathTemp.Value = Math.Round(Convert.ToDouble(currSensor["Temp"]), 1); 
                            LvcBathHumid.Value = Convert.ToDouble(currSensor["Humid"]); 
                        });
                        break;

                    default: break; // default값 없긴함
                }
            }
        }

        private void BtnOpen_Click(object sender, RoutedEventArgs e)
        {
            // Json으로 서보모터 90도 오픈한다는 데이터 생성
            var topic = "pknu/monitor/control/";

            JObject origin_data = new JObject();
            origin_data.Add("DEV_ID", "MONITOR");
            origin_data.Add("CURR_DT", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            origin_data.Add("STAT", "OPEN");

            string pub_data = JsonConvert.SerializeObject(origin_data, Formatting.Indented);

            Commons.MQTT_CLIENT.Publish(topic, Encoding.UTF8.GetBytes(pub_data));
            LblDoorStat.Content = "OPEN!";
        }

        private void BtnClose_Click(object sender, RoutedEventArgs e)
        {
            // Json으로 서보모터 90도 오픈한다는 데이터 생성
            var topic = "pknu/monitor/control/";

            JObject origin_data = new JObject();
            origin_data.Add("DEV_ID", "MONITOR");
            origin_data.Add("CURR_DT", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            origin_data.Add("STAT", "CLOSE");

            string pub_data = JsonConvert.SerializeObject(origin_data, Formatting.Indented);

            Commons.MQTT_CLIENT.Publish(topic, Encoding.UTF8.GetBytes(pub_data));
            LblDoorStat.Content = "CLOSE!";
        }
    }
}
