using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BogusTestApp.Models
{
    public class Order // 주문테이블
    {
        public Guid Id { get; set; } // 키값
        public DateTime Date { get; set; } // 주문일자
        public decimal OrderValue { get; set; } // 주문개수
        public bool Shipped { get; set; }   // 선적여부


    }
}
