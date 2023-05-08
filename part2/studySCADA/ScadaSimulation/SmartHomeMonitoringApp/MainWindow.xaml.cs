using MahApps.Metro.Controls;
using SmartHomeMonitoringApp.Views;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
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

namespace SmartHomeMonitoringApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void MetroWindow_Loaded(object sender, RoutedEventArgs e)
        {
            // <Frame> ==> Page.xaml
            // <Contentcontrol> ==> UserControl.xaml
            // ActiveItem.Content = new Views.DataBaseControl();
        }

        // 끝내기 버튼 이벤트 핸들러
        private void MnuExitSubxcribe_Click(object sender, RoutedEventArgs e)
        {
            Process.GetCurrentProcess().Kill(); // 작업관리자에서 프로세스 종료하는거랑 같음
            
            // Environment.Exit(0); 이걸로 종료해도 되는데 위에거보다 느림
        }

        // MQTT 시작메뉴 클릭 이벤트 핸들러
        private void MnuStartSubxcribe_Click(object sender, RoutedEventArgs e)
        {
            var mqttPopWin = new MqttPopupWindow();
            mqttPopWin.Owner = this;
            mqttPopWin.WindowStartupLocation = WindowStartupLocation.CenterOwner;
            var result = mqttPopWin.ShowDialog();

            if (result == true)
            {
                ActiveItem.Content = new Views.DataBaseControl();
            }
        }
    }
}
