using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using uPLibrary.Networking.M2Mqtt;

namespace SmartHomeMonitoringApp.Logics
{
    internal class Commons
    {
        // 화면마다 공유할 MQTT 브로커 ip 변수
        public static string BROKERHOST { get; set; } = "127.0.0.1";

        public static string MQTTTOPIC { get; set; } = "SmartHome/IoTData/";

        public static string MYSQL_CONNSTRING { get; set; } = "Server=localhost;" + 
                                                "Port=3306;" + 
                                                "Database=miniproject;" + 
                                                "Uid=root;" + 
                                                "Pwd=12345;";

        // MQTT 클라이언트 공용 객체
        public static MqttClient MQTT_CLIENT { get; set; }

        // UserControlr같이 자식 클래스이면서 MetroWindow를 직접 사용하지 않아서 MahApps.Metro에 있는 Metro메세지 창을 못쓸 때 사용하기 위한 메서드
        public static async Task<MessageDialogResult> ShowCustomMessAsync(string title, string message, MessageDialogStyle style = MessageDialogStyle.Affirmative)
        {
            return await ((MetroWindow)Application.Current.MainWindow).ShowMessageAsync(title, message, style, null);
        }

    }
}
