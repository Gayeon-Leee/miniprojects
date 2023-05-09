using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using SmartHomeMonitoringApp.Logics;
using SmartHomeMonitoringApp.Views;
using System;
using System.Collections.Generic;
using System.ComponentModel;
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
                var userControl = new Views.DataBaseControl();
                ActiveItem.Content = userControl;
                StsSelScreen.Content = "DataBase Monitoring";
            }
        }

        private async void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            // e.Cancle을 true로 하고 시작해야함
            e.Cancel = true;

            var mySettings = new MetroDialogSettings
                                {
                                    AffirmativeButtonText = "끝내기",
                                    NegativeButtonText = "취소",
                                    AnimateShow = true,
                                    AnimateHide = true
                                };

            var result = await this.ShowMessageAsync("프로그램을 끝내기", "프로그램을 끝내시겠습니까?", MessageDialogStyle.AffirmativeAndNegative, mySettings);

            if (result == MessageDialogResult.Negative)
            {
                e.Cancel = true;
            }
            else if (result == MessageDialogResult.Affirmative) // 프로그램 종료
            {
                if (Commons.MQTT_CLIENT != null && Commons.MQTT_CLIENT.IsConnected)
                {
                    Commons.MQTT_CLIENT.Disconnect();
                }
                Process.GetCurrentProcess().Kill(); // 제일 확실한 끝내기 
            }
        }

        private void BtnExitProgram_Click(object sender, RoutedEventArgs e)
        {
            // 윈도우 클로징 이벤트 핸들러 호출
            this.MetroWindow_Closing(sender, new CancelEventArgs());
        }
    }
}
