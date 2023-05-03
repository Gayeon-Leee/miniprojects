using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FakeIotDeviceApp.Models
{
    public class SensorInfo
    {
        public string Home_Id { get; set; } // D101H101 식으로 동호수
        public string Room_Name { get; set;} // Living, Dining, Bed, Bath
        public DateTime Sensing_DateTime { get; set; } // 
        public float Temp { get; set; }
        public float Humid { get; set; }

    }
}
