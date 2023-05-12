using ControlzEx.Theming;
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
        
        string DefaultTheme { get; set; } = "Light";    // 기본 테마 담을 변수
        string DefaultAccent { get; set; } = "Cobalt";  // 기본 액센트 담을 변수

        public MainWindow()
        {
            InitializeComponent();

            ThemeManager.Current.ThemeSyncMode = ThemeSyncMode.SyncWithAppMode;
            ThemeManager.Current.SyncTheme();
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

        private void MnuDataBaseMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.DataBaseControl();
            StsSelScreen.Content = "DataBase Monitoring";
        }

        private void MnuRealTimeMon_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.RealTimeControl();
            StsSelScreen.Content = "RealTime Monitoring";
        }

        private void MnuVisualization_Click(object sender, RoutedEventArgs e)
        {
            ActiveItem.Content = new Views.VisualizationControl();
            StsSelScreen.Content = "Visualization View";
        }

        private void MnuAbout_Click(object sender, RoutedEventArgs e)
        {
            var about = new About();
            about.Owner = this;
            about.ShowDialog();
        }

        // 모든 테마와 액센트를 전부 처리할 체크 이벤트 핸들러 => 클릭 이벤트 핸들러로 변경함
        private void MnuThemeAccent_Checked(object sender, RoutedEventArgs e)
        {
            Debug.WriteLine((sender as MenuItem).Header);
            
            // 클릭되는 테마가 라이트인지 다크인지 판단 - 다크를 클릭하면 라이트 체크 해제 
            // 액센트도 체크 하는 값만 받아오고 나머지 액센트는 전부 체크 해제
            switch ((sender as MenuItem).Header)
            {
                case "Light":
                    MnuLightTheme.IsChecked = true;
                    MnuDarkTheme.IsChecked = false;
                    DefaultTheme = "Light";
                    break;
                case "Dark":
                    MnuLightTheme.IsChecked = false;
                    MnuDarkTheme.IsChecked = true;
                    DefaultTheme = "Dark";
                    break;
                case "Amber":
                    MnuAccentAmber.IsChecked = true;
                    MnuAccentBlue.IsChecked = false;
                    MnuAccentBrown.IsChecked = false;
                    MnuAccentCobalt.IsChecked = false;
                    DefaultAccent = "Amber";
                    break;
                case "Blue":
                    MnuAccentAmber.IsChecked = false;
                    MnuAccentBlue.IsChecked = true;
                    MnuAccentBrown.IsChecked = false;
                    MnuAccentCobalt.IsChecked = false;
                    DefaultAccent = "Blue";
                    break;
                case "Brown":
                    MnuAccentAmber.IsChecked = false;
                    MnuAccentBlue.IsChecked = false;
                    MnuAccentBrown.IsChecked = true;
                    MnuAccentCobalt.IsChecked = false;
                    DefaultAccent = "Brown";
                    break;
                case "Cobalt":
                    MnuAccentAmber.IsChecked = false;
                    MnuAccentBlue.IsChecked = false;
                    MnuAccentBrown.IsChecked = false;
                    MnuAccentCobalt.IsChecked = true;
                    DefaultAccent = "Cobalt";
                    break;
            }

            ThemeManager.Current.ChangeTheme(this, $"{DefaultTheme}.{DefaultAccent}");
        }
    }
}
