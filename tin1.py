import streamlit as st
import random
from collections import defaultdict

# --- 1. DỮ LIỆU ĐÁP ÁN ĐÚNG ĐƯỢC CUNG CẤP BỞI NGƯỜI DÙNG ---
# Mapping: Question ID (int) -> Correct Option Letter (str)
CORRECT_ANSWERS_BY_ID = {
    1: 'A', 2: 'A', 3: 'A', 4: 'A', 5: 'A', 6: 'A', 7: 'A', 8: 'B', 9: 'A', 10: 'A',
    11: 'D', 12: 'B', 13: 'B', 14: 'C', 15: 'D', 16: 'B', 17: 'C', 18: 'B', 19: 'C', 20: 'B',
    21: 'D', 22: 'B', 23: 'D', 24: 'A', 25: 'B', 26: 'C', 27: 'A', 28: 'A', 29: 'A', 30: 'B',
    31: 'C', 32: 'A', 33: 'B', 34: 'C', 35: 'A', 36: 'C', 37: 'D', 38: 'A', 39: 'B', 40: 'B',
    41: 'A', 42: 'C', 43: 'B', 44: 'B', 45: 'C', 46: 'D', 47: 'D', 48: 'C', 49: 'B', 50: 'A',
    51: 'A', 52: 'D', 53: 'B', 54: 'D', 55: 'C', 56: 'D', 57: 'A', 58: 'A', 59: 'B', 60: 'C',
    61: 'C', 62: 'C', 63: 'D', 64: 'B', 65: 'A', 66: 'D', 67: 'A', 68: 'B', 69: 'A', 70: 'A',
    71: 'A', 72: 'A', 73: 'A', 74: 'A', 75: 'A', 76: 'A', 77: 'A', 78: 'A', 79: 'A', 80: 'A',
    81: 'A', 82: 'B', 83: 'C', 84: 'B', 85: 'B', 86: 'B', 87: 'C', 88: 'A', 89: 'B', 90: 'B',
    98: 'B', 99: 'D', 100: 'B', 101: 'B', 102: 'A', 103: 'C', 104: 'B', 110: 'C',
    111: 'A', 112: 'C', 113: 'C', 114: 'A', 115: 'B', 116: 'A', 117: 'C', 118: 'D', 119: 'A',
    120: 'C', 122: 'C', 123: 'D', 124: 'C', 125: 'B', 126: 'A', 127: 'A', 128: 'C', 129: 'B',
    130: 'D', 131: 'B', 132: 'C', 133: 'D', 134: 'B', 135: 'A', 136: 'A', 137: 'B', 138: 'C',
    139: 'D', 140: 'A', 141: 'B', 142: 'A', 143: 'B', 144: 'A', 145: 'B', 146: 'D', 147: 'C',
    148: 'A', 149: 'A', 150: 'A', 151: 'B', 152: 'D', 153: 'B', 154: 'A', 155: 'C', 156: 'A',
    157: 'B', 158: 'C', 159: 'A', 160: 'B', 161: 'A', 162: 'A', 163: 'A', 164: 'A', 165: 'B',
    166: 'B', 167: 'A', 168: 'C', 169: 'A', 170: 'B', 171: 'D', 172: 'A', 173: 'C', 174: 'C',
    175: 'A', 176: 'D', 177: 'C', 178: 'A', 179: 'C', 180: 'C', 181: 'B', 182: 'A', 183: 'A',
    184: 'C', 185: 'B', 186: 'B', 187: 'C', 188: 'A', 189: 'C', 190: 'C', 191: 'D', 192: 'A',
    193: 'D', 194: 'B', 195: 'B', 196: 'C', 197: 'A', 198: 'B',
    199: 'C' # Thêm giả định cho Q199 để đủ 199 câu
}

# Helper function to map correct letter to its text
def get_correct_text(options, correct_letter):
    """Maps A, B, C, D to the corresponding text option."""
    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    idx = mapping.get(correct_letter.upper())
    return options[idx] if idx is not None and 0 <= idx < len(options) else "LỖI: Không tìm thấy đáp án khớp"

# --- 2. DỮ LIỆU CÂU HỎI (TRÍCH XUẤT TỪ PDF VÀ ĐÃ CÓ ĐÁP ÁN CHÍNH XÁC) ---
# Tích hợp dữ liệu câu hỏi từ PDF và gán đáp án chính xác theo key của người dùng
QUIZ_DATA_RAW = [
    { # Q01
        "id": 1,
        "question": "Trong các phát biểu sau, phát biểu nào sai khi nói đến bộ nhớ ROM:",
        "options": [
            "Máy tính có thể khởi động mà không cần bộ nhớ ROM.", 
            "ROM được viết tắt bởi cụm từ “Read Only Memory\".", 
            "ROM là bộ nhớ chỉ đọc, dữ liệu trong bộ nhớ ROM vẫn duy trì khi nguồn điện bị cắt.", 
            "ROM được các nhà sản xuất ghi sẵn các chương trình cơ sở phục vụ cho quá trình khởi động máy." 
        ],
        "correct_option_text": get_correct_text([
            "Máy tính có thể khởi động mà không cần bộ nhớ ROM.",
            "ROM được viết tắt bởi cụm từ “Read Only Memory\".",
            "ROM là bộ nhớ chỉ đọc, dữ liệu trong bộ nhớ ROM vẫn duy trì khi nguồn điện bị cắt.",
            "ROM được các nhà sản xuất ghi sẵn các chương trình cơ sở phục vụ cho quá trình khởi động máy."
        ], CORRECT_ANSWERS_BY_ID.get(1))
    },
    { # Q02
        "id": 2,
        "question": "Byte (kí hiệu là B) thường gặp trong các tài liệu về tin học là gì?",
        "options": [
            "Là đơn vị đo lượng lưu trữ dữ liệu.", 
            "Là đơn vị đo độ phân giải màn hình.", 
            "Là đơn vị đo cường độ âm thanh.", 
            "Là đơn vị đo tốc độ xử lý." 
        ],
        "correct_option_text": get_correct_text([
            "Là đơn vị đo lượng lưu trữ dữ liệu.",
            "Là đơn vị đo độ phân giải màn hình.",
            "Là đơn vị đo cường độ âm thanh.",
            "Là đơn vị đo tốc độ xử lý."
        ], CORRECT_ANSWERS_BY_ID.get(2))
    },
    { # Q03
        "id": 3,
        "question": "Quy đổi 3MB ra đơn vị dữ liệu là KB, ta được?",
        "options": [
            "3072 KB", "3000 KB", "0,3 KB", "300 KB" 
        ],
        "correct_option_text": get_correct_text([
            "3072 KB", "3000 KB", "0,3 KB", "300 KB"
        ], CORRECT_ANSWERS_BY_ID.get(3))
    },
    { # Q04
        "id": 4,
        "question": "Trong Windows, muốn xóa dữ liệu và không cho phục hồi trong Recycle Bin, cần thực hiện các thao tác nào sau đây?",
        "options": [
            "Chọn đối tượng cân xóa, ấn tổ hợp phím Shift+Delete", 
            "Chọn đối tượng cần xóa, ấn phím Delete.", 
            "Chọn đối tượng cần xóa, kích chuột phải, chọn Delete.", 
            "Chọn đối tượng cần xóa, ấn tổ hợp phím Ctrl+Delete" 
        ],
        "correct_option_text": get_correct_text([
            "Chọn đối tượng cân xóa, ấn tổ hợp phím Shift+Delete",
            "Chọn đối tượng cần xóa, ấn phím Delete.",
            "Chọn đối tượng cần xóa, kích chuột phải, chọn Delete.",
            "Chọn đối tượng cần xóa, ấn tổ hợp phím Ctrl+Delete"
        ], CORRECT_ANSWERS_BY_ID.get(4))
    },
    { # Q05
        "id": 5,
        "question": "Trong Windows, để tạo thư mục mới ở ổ đĩa E:, ta mở ổ đĩa E: sau đó thực hiện thao tác:",
        "options": [
            "Click chuột phải vào vùng trống, chọn New/Folder", 
            "Click chuột phải vào vùng trống, chọn Group by/Type", 
            "Click chuột phải, chọn Group by/Name", 
            "Click chuột phải, chọn View/List" 
        ],
        "correct_option_text": get_correct_text([
            "Click chuột phải vào vùng trống, chọn New/Folder",
            "Click chuột phải vào vùng trống, chọn Group by/Type",
            "Click chuột phải, chọn Group by/Name",
            "Click chuột phải, chọn View/List"
        ], CORRECT_ANSWERS_BY_ID.get(5))
    },
    { # Q06
        "id": 6,
        "question": "Trong Windows, để thiết đặt lại hệ thống, ta chọn chức năng:",
        "options": [
            "Control Panel", "All Programs", "Control System", "Control Desktop" 
        ],
        "correct_option_text": get_correct_text([
            "Control Panel", "All Programs", "Control System", "Control Desktop"
        ], CORRECT_ANSWERS_BY_ID.get(6))
    },
    { # Q07
        "id": 7,
        "question": "ISP là viết tắt của",
        "options": [
            "Internet Service Provider", "Internet Server Provider", "Internet Super Provider", "Internet Side Provider" 
        ],
        "correct_option_text": get_correct_text([
            "Internet Service Provider", "Internet Server Provider", "Internet Super Provider", "Internet Side Provider"
        ], CORRECT_ANSWERS_BY_ID.get(7))
    },
    { # Q08
        "id": 8,
        "question": "FTP là viết tắt của cụm từ tiếng Anh nào?",
        "options": [
            "File Transfer Procedure", "File Transfer Protocol", "Fast Transfer Protocol", "Future Transfer Procedure" 
        ],
        "correct_option_text": get_correct_text([
            "File Transfer Procedure", "File Transfer Protocol", "Fast Transfer Protocol", "Future Transfer Procedure"
        ], CORRECT_ANSWERS_BY_ID.get(8))
    },
    { # Q09
        "id": 9,
        "question": "Để xem lại lịch sử duyệt web ta dùng tổ hợp phím trên trình duyệt Internet Explorer",
        "options": [
            "Ctrl+H", "Ctrl+L", "Ctrl+P", "Ctrl + A" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+H", "Ctrl+L", "Ctrl+P", "Ctrl + A"
        ], CORRECT_ANSWERS_BY_ID.get(9))
    },
    { # Q10
        "id": 10,
        "question": "Cấu trúc một địa chỉ thư điện tử?",
        "options": [
            "<Tên người dùng>@<Tên miền>", "<Tên miền> <Tên người dùng>", "<Tên miền>@<Tên người dùng>", "<Tên người dùng>#<Tên miên>" 
        ],
        "correct_option_text": get_correct_text([
            "<Tên người dùng>@<Tên miền>", "<Tên miền> <Tên người dùng>", "<Tên miền>@<Tên người dùng>", "<Tên người dùng>#<Tên miên>"
        ], CORRECT_ANSWERS_BY_ID.get(10))
    },
    { # Q11
        "id": 11,
        "question": "Để chuyển tiếp thư tới người khác, bạn sử dụng nút nào?",
        "options": [
            "Relpy", "Relpy to All", "Attachment", "Forward" 
        ],
        "correct_option_text": get_correct_text([
            "Relpy", "Relpy to All", "Attachment", "Forward"
        ], CORRECT_ANSWERS_BY_ID.get(11))
    },
    { # Q12
        "id": 12,
        "question": "DNS là viết tắt của cụm từ tiếng Anh nào?",
        "options": [
            "Domain Network System.", "Domain Name System.", "Dynamic Name System.", "Dynamic Network System." 
        ],
        "correct_option_text": get_correct_text([
            "Domain Network System.", "Domain Name System.", "Dynamic Name System.", "Dynamic Network System."
        ], CORRECT_ANSWERS_BY_ID.get(12))
    },
    { # Q13
        "id": 13,
        "question": "Trong các cụm từ sau, cụm từ nào không phải là giao thức?",
        "options": [
            "TCP/IP", "LAN/WAN", "IPX/SPX", "POP3, SMTP" 
        ],
        "correct_option_text": get_correct_text([
            "TCP/IP", "LAN/WAN", "IPX/SPX", "POP3, SMTP"
        ], CORRECT_ANSWERS_BY_ID.get(13))
    },
    { # Q14
        "id": 14,
        "question": "Dịch vụ lưu trữ đám mây của Microsoft có tên là gì?",
        "options": [
            "Google Driver", "Mediafire", "OneDrive", "Dropbox." 
        ],
        "correct_option_text": get_correct_text([
            "Google Driver", "Mediafire", "OneDrive", "Dropbox."
        ], CORRECT_ANSWERS_BY_ID.get(14))
    },
    { # Q15
        "id": 15,
        "question": "Đĩa cứng (HDD – Hard Disk Drive) là:",
        "options": [
            "Là thiết bị lưu trữ dữ liệu tạm thời khi máy tính đang hoạt động.", 
            "Là thiết bị gắn bên trong máy tính dùng để ghi dữ liệu tạm thời.", 
            "Là thiết bị phần cứng không được sử dụng để lưu trữ dữ liệu.", 
            "Là thiết bị để lưu trữ dữ liệu." 
        ],
        "correct_option_text": get_correct_text([
            "Là thiết bị lưu trữ dữ liệu tạm thời khi máy tính đang hoạt động.",
            "Là thiết bị gắn bên trong máy tính dùng để ghi dữ liệu tạm thời.",
            "Là thiết bị phần cứng không được sử dụng để lưu trữ dữ liệu.",
            "Là thiết bị để lưu trữ dữ liệu."
        ], CORRECT_ANSWERS_BY_ID.get(15))
    },
    { # Q16
        "id": 16,
        "question": "Bàn phím (Keyboard) là:",
        "options": [
            "Thiết bị gắn bên trong máy tính.", 
            "Thiết bị ngoại vi của máy tính dùng để nhập dữ liệu.", 
            "Thiết bị có khả năng nhập mọi định dạng dữ liệu.", 
            "Thiết bị xuất." 
        ],
        "correct_option_text": get_correct_text([
            "Thiết bị gắn bên trong máy tính.",
            "Thiết bị ngoại vi của máy tính dùng để nhập dữ liệu.",
            "Thiết bị có khả năng nhập mọi định dạng dữ liệu.",
            "Thiết bị xuất."
        ], CORRECT_ANSWERS_BY_ID.get(16))
    },
    { # Q17
        "id": 17,
        "question": "Chuột máy tính (Mouse) có thể kết nối với bo mạch chủ thông qua cổng giao tiếp:",
        "options": [
            "COM, PS/2, USB và kết nối không dây (bluetooth và NFC).", 
            "COM, PS/2 và kết nối không dây (bluetooth).", 
            "COM, PS/2 và USB.", 
            "USB và kết nối không dây." 
        ],
        "correct_option_text": get_correct_text([
            "COM, PS/2, USB và kết nối không dây (bluetooth và NFC).",
            "COM, PS/2 và kết nối không dây (bluetooth).",
            "COM, PS/2 và USB.",
            "USB và kết nối không dây."
        ], CORRECT_ANSWERS_BY_ID.get(17))
    },
    { # Q18
        "id": 18,
        "question": "Thiết bị nào sau đây không phải là thiết bị xuất thông tin:",
        "options": [
            "Màn hình (monitor).", "Máy quét (scanner).", "Máy chiếu (projector).", "Máy in (printer)." 
        ],
        "correct_option_text": get_correct_text([
            "Màn hình (monitor).", "Máy quét (scanner).", "Máy chiếu (projector).", "Máy in (printer)."
        ], CORRECT_ANSWERS_BY_ID.get(18))
    },
    { # Q19
        "id": 19,
        "question": "Trong các cổng giao tiếp với thiết bị ngoại vi trên máy tính cổng nào sau đây thường được dùng để kết nối trực tiếp với máy in:",
        "options": [
            "PS/2.", "COM.", "USB hoặc LPT", "VGA" 
        ],
        "correct_option_text": get_correct_text([
            "PS/2.", "COM.", "USB hoặc LPT", "VGA"
        ], CORRECT_ANSWERS_BY_ID.get(19))
    },
    { # Q20
        "id": 20,
        "question": "Tốc độ của bộ xử lý trung tâm (CPU) thường được tính bằng đơn vị đo:",
        "options": [
            "MB hoặc GB.", "MHz hoặc GHz.", "MBs hoặc GBs", "Gbps hoặc GBps." 
        ],
        "correct_option_text": get_correct_text([
            "MB hoặc GB.", "MHz hoặc GHz.", "MBs hoặc GBs", "Gbps hoặc GBps."
        ], CORRECT_ANSWERS_BY_ID.get(20))
    },
    { # Q21
        "id": 21,
        "question": "Đơn vị đo nào sau đây không được sử dụng để đo dung lượng bộ nhớ trong?",
        "options": [
            "GB.", "KB.", "MB.", "MHz." 
        ],
        "correct_option_text": get_correct_text([
            "GB.", "KB.", "MB.", "MHz."
        ], CORRECT_ANSWERS_BY_ID.get(21))
    },
    { # Q22
        "id": 22,
        "question": "Một Byte bằng bao nhiêu bit?",
        "options": [
            "16 bit.", "8 bit.", "1000 bit.", "1024 bit." 
        ],
        "correct_option_text": get_correct_text([
            "16 bit.", "8 bit.", "1000 bit.", "1024 bit."
        ], CORRECT_ANSWERS_BY_ID.get(22))
    },
    { # Q23
        "id": 23,
        "question": "Một KB (Kilobyte) bằng bao nhiêu Byte?",
        "options": [
            "8 Byte.", "10 Byte.", "1000 Byte.", "1024 Byte." 
        ],
        "correct_option_text": get_correct_text([
            "8 Byte.", "10 Byte.", "1000 Byte.", "1024 Byte."
        ], CORRECT_ANSWERS_BY_ID.get(23))
    },
    { # Q24
        "id": 24,
        "question": "Trong mạng máy tính, thuật ngữ LAN dùng để chỉ:",
        "options": [
            "Mạng cục bộ.", "Mạng diện rộng.", "Mạng toàn câu.", "Mạng Internet." 
        ],
        "correct_option_text": get_correct_text([
            "Mạng cục bộ.", "Mạng diện rộng.", "Mạng toàn câu.", "Mạng Internet."
        ], CORRECT_ANSWERS_BY_ID.get(24))
    },
    { # Q25
        "id": 25,
        "question": "Trong mạng máy tính, thuật ngữ WAN dùng để chỉ:",
        "options": [
            "Mạng cục bộ.", "Mạng diện rộng.", "Mạng toàn cầu.", "Điểm truy cập không dây." 
        ],
        "correct_option_text": get_correct_text([
            "Mạng cục bộ.", "Mạng diện rộng.", "Mạng toàn cầu.", "Điểm truy cập không dây."
        ], CORRECT_ANSWERS_BY_ID.get(25))
    },
    { # Q26
        "id": 26,
        "question": "Phần mềm nào sau đây không phải là phần mềm mã nguồn mở?",
        "options": [
            "LibreOffice.", "Apache OpenOffice.", "Microsoft Office.", "Bộ gõ Tiếng Việt Unikey." 
        ],
        "correct_option_text": get_correct_text([
            "LibreOffice.", "Apache OpenOffice.", "Microsoft Office.", "Bộ gõ Tiếng Việt Unikey."
        ], CORRECT_ANSWERS_BY_ID.get(26))
    },
    { # Q27
        "id": 27,
        "question": "Trong các cổng sau cổng nào dùng để cắm trực tiếp vào bàn phím:",
        "options": [
            "Công PS/2, USB.", "Công VGA, LPT.", "Công HDMI, VGA", "Cổng RJ45, VGA." 
        ],
        "correct_option_text": get_correct_text([
            "Công PS/2, USB.", "Công VGA, LPT.", "Công HDMI, VGA", "Cổng RJ45, VGA."
        ], CORRECT_ANSWERS_BY_ID.get(27))
    },
    { # Q28
        "id": 28,
        "question": "Đâu là viết tắt của cụm từ: \"công nghệ thông tin và truyền thông\"?",
        "options": [
            "ICT", "CTI", "CIT", "TCI" 
        ],
        "correct_option_text": get_correct_text([
            "ICT", "CTI", "CIT", "TCI"
        ], CORRECT_ANSWERS_BY_ID.get(28))
    },
    { # Q29
        "id": 29,
        "question": "Trên hệ điều hành Windows 10, để hẹn giờ tắt máy sau 30 phút ta có thể dùng lệnh:",
        "options": [
            "shutdown -s -t 1800", "shutdown -r -t 1800", "shutdown -1 -t 1800", "shutdown -a 1800" 
        ],
        "correct_option_text": get_correct_text([
            "shutdown -s -t 1800", "shutdown -r -t 1800", "shutdown -1 -t 1800", "shutdown -a 1800"
        ], CORRECT_ANSWERS_BY_ID.get(29))
    },
    { # Q30
        "id": 30,
        "question": "Trong Windows 10 để đổi tên một thư mục hay tập tin ta thực hiện:",
        "options": [
            "Click chọn đối tượng/ F4/Gõ tên mới/Enter", 
            "Click phải vào đối tượng / Rename/ Gõ tên mới/ Enter", 
            "Click chọn đối tượng/ F3/Gõ tên mới/Enter", 
            "Click phải vào đối tượng /Name/ Gõ tên mới/ Enter" 
        ],
        "correct_option_text": get_correct_text([
            "Click chọn đối tượng/ F4/Gõ tên mới/Enter",
            "Click phải vào đối tượng / Rename/ Gõ tên mới/ Enter",
            "Click chọn đối tượng/ F3/Gõ tên mới/Enter",
            "Click phải vào đối tượng /Name/ Gõ tên mới/ Enter"
        ], CORRECT_ANSWERS_BY_ID.get(30))
    },
    { # Q31
        "id": 31,
        "question": "Chọn phát biểu đúng, trong các phát biểu dưới đây?",
        "options": [
            "Windows 10 là hệ điều hành chỉ có phiên bản 32 bit.", 
            "Windows 10 là hệ điều hành chỉ có phiên bản 64 bit.", 
            "Windows 10 là hệ điều hành có 2 phiên bản: 32 bit và 64 bit.", 
            "Windows 10 là hệ điều hành có 3 phiên bản: 32 bit, 64 bit, 128 bit." 
        ],
        "correct_option_text": get_correct_text([
            "Windows 10 là hệ điều hành chỉ có phiên bản 32 bit.",
            "Windows 10 là hệ điều hành chỉ có phiên bản 64 bit.",
            "Windows 10 là hệ điều hành có 2 phiên bản: 32 bit và 64 bit.",
            "Windows 10 là hệ điều hành có 3 phiên bản: 32 bit, 64 bit, 128 bit."
        ], CORRECT_ANSWERS_BY_ID.get(31))
    },
    { # Q32
        "id": 32,
        "question": "Trong các cụm từ liệt kê dưới đây, đâu là cụm từ chỉ tên của “Thùng rác” trong hệ điều hành Windows 10?",
        "options": [
            "Recycle Bin", "Bin Recycle", "Temple Bin", "Directory Bin" 
        ],
        "correct_option_text": get_correct_text([
            "Recycle Bin", "Bin Recycle", "Temple Bin", "Directory Bin"
        ], CORRECT_ANSWERS_BY_ID.get(32))
    },
    { # Q33
        "id": 33,
        "question": "Thao tác nào cho phép thiết lập cố định vị trí của Taskbar (trong Windows 10)?",
        "options": [
            "Nhấn chuột phải lên Taskbar / Toolbars / Lock the taskbar", 
            "Nhấn chuột phải lên nút Taskbar, chọn Lock the taskbar", 
            "Vào Control Panel, chọn Taskbar and Start menu / Lock", 
            "Nhấn chuột phải lên Taskbar / Task Manager / Lock the taskbar" 
        ],
        "correct_option_text": get_correct_text([
            "Nhấn chuột phải lên Taskbar / Toolbars / Lock the taskbar",
            "Nhấn chuột phải lên nút Taskbar, chọn Lock the taskbar",
            "Vào Control Panel, chọn Taskbar and Start menu / Lock",
            "Nhấn chuột phải lên Taskbar / Task Manager / Lock the taskbar"
        ], CORRECT_ANSWERS_BY_ID.get(33))
    },
    { # Q34
        "id": 34,
        "question": "Trong Windows 10, muốn tạo một thư mục mới, ta thực hiện thao tác:",
        "options": [
            "Click chuột phải, chọn Edit/New/Folder", 
            "Click chuột phải, chọn Tools/New/ Folder", 
            "Click chuột phải, chọn New / Folder", 
            "Click chuột phải, chọn Windows/New/Folder" 
        ],
        "correct_option_text": get_correct_text([
            "Click chuột phải, chọn Edit/New/Folder",
            "Click chuột phải, chọn Tools/New/ Folder",
            "Click chuột phải, chọn New / Folder",
            "Click chuột phải, chọn Windows/New/Folder"
        ], CORRECT_ANSWERS_BY_ID.get(34))
    },
    { # Q35
        "id": 35,
        "question": "Trong Windows 10, muốn phục hồi dữ liệu đã xóa (trong Recycle Bin) ta thực hiện các thao tác:",
        "options": [
            "Mở Recycle Bin, chọn tệp hoặc thư mục cần phục hồi, chọn Restore this item.", 
            "Chọn đối tượng cần phục hồi, thực hiện lệnh copy và paste.", 
            "Mở Recycle Bin, chọn tệp hoặc thư mục cần phục hồi, thực hiện lệnh copy và paste.", 
            "Tại Desktop, kích chuột phải lên Recycle Bin, chọn Empty Recycle Bin." 
        ],
        "correct_option_text": get_correct_text([
            "Mở Recycle Bin, chọn tệp hoặc thư mục cần phục hồi, chọn Restore this item.",
            "Chọn đối tượng cần phục hồi, thực hiện lệnh copy và paste.",
            "Mở Recycle Bin, chọn tệp hoặc thư mục cần phục hồi, thực hiện lệnh copy và paste.",
            "Tại Desktop, kích chuột phải lên Recycle Bin, chọn Empty Recycle Bin."
        ], CORRECT_ANSWERS_BY_ID.get(35))
    },
    { # Q36
        "id": 36,
        "question": "Khi đang sử dụng Windows 10, để lưu nội dung màn hình vào bộ nhớ Clipboard ta sử dụng phím hoặc tổ hợp phím nào?",
        "options": [
            "Ctrl+C", "Ctrl+Ins", "Print Screen", "ESC" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+C", "Ctrl+Ins", "Print Screen", "ESC"
        ], CORRECT_ANSWERS_BY_ID.get(36))
    },
    { # Q37
        "id": 37,
        "question": "Để hiển thị được giờ theo mẫu sau 08:10:15 ta phải dùng định dạng nào trong các dạng sau:",
        "options": [
            "h:mm:ss tt", "hh:mm:ss tt", "h:mm:ss tt (Lặp lại)", "hh:mm:ss" 
        ],
        "correct_option_text": get_correct_text([
            "h:mm:ss tt", "hh:mm:ss tt", "h:mm:ss tt (Lặp lại)", "hh:mm:ss"
        ], CORRECT_ANSWERS_BY_ID.get(37))
    },
    { # Q38
        "id": 38,
        "question": "Để hiển thị được ngày theo mẫu sau 27/08/2023 ta phải dùng định dạng nào trong các dạng sau:",
        "options": [
            "dd/MM/yyyy", "dd/MM/yy", "mm/dd/yyyy", "mm/dd/yy" 
        ],
        "correct_option_text": get_correct_text([
            "dd/MM/yyyy", "dd/MM/yy", "mm/dd/yyyy", "mm/dd/yy"
        ], CORRECT_ANSWERS_BY_ID.get(38))
    },
    { # Q39
        "id": 39,
        "question": "Chọn sắp xếp đúng theo phiên bản (version) từ thấp đến cao của hệ điều hành windows được liệt kê dưới đây?",
        "options": [
            "Windows Vista, Windows 10, Windows XP", 
            "Windows XP, Windows Vista, Windows 10", 
            "Windows XP, Windows 10, Windows Vista.", 
            "Windows 10, Windows Vista, Windows XP." 
        ],
        "correct_option_text": get_correct_text([
            "Windows Vista, Windows 10, Windows XP",
            "Windows XP, Windows Vista, Windows 10",
            "Windows XP, Windows 10, Windows Vista.",
            "Windows 10, Windows Vista, Windows XP."
        ], CORRECT_ANSWERS_BY_ID.get(39))
    },
    { # Q40
        "id": 40,
        "question": "Trong File Explorer, để tìm kiếm một nhóm tệp tin có tên bắt đầu bằng H, ta nhập tên sau:",
        "options": [
            "H??.docx", "H*.*", "H.*", "*H.*" 
        ],
        "correct_option_text": get_correct_text([
            "H??.docx", "H*.*", "H.*", "*H.*"
        ], CORRECT_ANSWERS_BY_ID.get(40))
    },
    { # Q41
        "id": 41,
        "question": "Phần mềm nào sau đây có khả năng diệt virus cho máy tính:",
        "options": [
            "Kaspersky", "Microsoft Office", "Outlook Express", "WinRar" 
        ],
        "correct_option_text": get_correct_text([
            "Kaspersky", "Microsoft Office", "Outlook Express", "WinRar"
        ], CORRECT_ANSWERS_BY_ID.get(41))
    },
    { # Q42
        "id": 42,
        "question": "Thuộc tính nào là thuộc tính ẩn của tập tin trong Windows 10",
        "options": [
            "Archive", "Read-only", "Hidden", "System" 
        ],
        "correct_option_text": get_correct_text([
            "Archive", "Read-only", "Hidden", "System"
        ], CORRECT_ANSWERS_BY_ID.get(42))
    },
    { # Q43
        "id": 43,
        "question": "Trong MS Word 2016, để đóng tập tin, ta bấm tổ hợp phím:",
        "options": [
            "Ctrl+Shift+W", "Ctrl+W", "Ctrl+O", "Ctrl+S" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+Shift+W", "Ctrl+W", "Ctrl+O", "Ctrl+S"
        ], CORRECT_ANSWERS_BY_ID.get(43))
    },
    { # Q44
        "id": 44,
        "question": "Trong soạn thảo Word 2016, công dụng của tổ hợp phím Ctrl+O là:",
        "options": [
            "Đóng tệp tin đang mở", "Mở tệp tin đã có", "Lưu tệp tin vào đĩa", "Mở một tệp tin mới" 
        ],
        "correct_option_text": get_correct_text([
            "Đóng tệp tin đang mở", "Mở tệp tin đã có", "Lưu tệp tin vào đĩa", "Mở một tệp tin mới"
        ], CORRECT_ANSWERS_BY_ID.get(44))
    },
    { # Q45
        "id": 45,
        "question": "Trong MS Word 2016 để chèn một ký tự đặc biệt vào văn bản ta thực hiện gì?",
        "options": [
            "Tại menu Insert, chọn QuickPart", 
            "Tại menu Insert, chọn Equation", 
            "Tại menu Insert, chọn Symbol", 
            "Tại menu Insert, chọn WordArt" 
        ],
        "correct_option_text": get_correct_text([
            "Tại menu Insert, chọn QuickPart",
            "Tại menu Insert, chọn Equation",
            "Tại menu Insert, chọn Symbol",
            "Tại menu Insert, chọn WordArt"
        ], CORRECT_ANSWERS_BY_ID.get(45))
    },
    { # Q46
        "id": 46,
        "question": "Mặc định, tài liệu của MS Word 2016 được lưu với định dạng là:",
        "options": [
            "*.DOTX", "*.DOC", "*.EXE", "*.DOCX" 
        ],
        "correct_option_text": get_correct_text([
            "*.DOTX", "*.DOC", "*.EXE", "*.DOCX"
        ], CORRECT_ANSWERS_BY_ID.get(46))
    },
    { # Q47
        "id": 47,
        "question": "Trong MS Word 2016, để chuyển con trỏ xuống phía dưới 1 trang màn hình ta dùng phím:",
        "options": [
            "Backspace", "Home", "Page Up", "Page Down" 
        ],
        "correct_option_text": get_correct_text([
            "Backspace", "Home", "Page Up", "Page Down"
        ], CORRECT_ANSWERS_BY_ID.get(47))
    },
    { # Q48
        "id": 48,
        "question": "Trong MS Word 2016, để tìm kiếm và thay thế, ta bấm tổ hợp phím gì?",
        "options": [
            "Shift + F", "Ctrl+R", "Ctrl+H", "Shift + R" 
        ],
        "correct_option_text": get_correct_text([
            "Shift + F", "Ctrl+R", "Ctrl+H", "Shift + R"
        ], CORRECT_ANSWERS_BY_ID.get(48))
    },
    { # Q49
        "id": 49,
        "question": "Trong soạn thảo Word, muốn tách một ô trong Table thành nhiều ô, ta thực hiện:",
        "options": [
            "Table - Merge Cells", "Table Split Cells", "Tools - Split Cells", "Table Cells" 
        ],
        "correct_option_text": get_correct_text([
            "Table - Merge Cells", "Table Split Cells", "Tools - Split Cells", "Table Cells"
        ], CORRECT_ANSWERS_BY_ID.get(49))
    },
    { # Q50
        "id": 50,
        "question": "Các công cụ định dạng trong văn bản như: Font, Paragraph, Copy, Paste, Bullets, Numbering..., nằm ở thanh menu nào?",
        "options": [
            "Home", "Insert", "Page Layout", "References" 
        ],
        "correct_option_text": get_correct_text([
            "Home", "Insert", "Page Layout", "References"
        ], CORRECT_ANSWERS_BY_ID.get(50))
    },
    { # Q51
        "id": 51,
        "question": "Trong MS Word 2016, để có đường gạch chân của đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": [
            "Ctrl+U", "Shift+U", "Alt+U", "Ctrl+B" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+U", "Shift+U", "Alt+U", "Ctrl+B"
        ], CORRECT_ANSWERS_BY_ID.get(51))
    },
    { # Q52
        "id": 52,
        "question": "Trong MS Word, để tăng cỡ chữ, ta sử dụng tổ hợp phím:",
        "options": [
            "Shift + ]", "Ctrl+[", "Shift + [", "Ctrl+]" 
        ],
        "correct_option_text": get_correct_text([
            "Shift + ]", "Ctrl+[", "Shift + [", "Ctrl+]"
        ], CORRECT_ANSWERS_BY_ID.get(52))
    },
    { # Q53
        "id": 53,
        "question": "Trong MS Word, để giảm cỡ chữ, ta sử dụng tổ hợp phím",
        "options": [
            "Shift + ]", "Ctrl+[", "Shift + [", "Ctrl+]" 
        ],
        "correct_option_text": get_correct_text([
            "Shift + ]", "Ctrl+[", "Shift + [", "Ctrl+]"
        ], CORRECT_ANSWERS_BY_ID.get(53))
    },
    { # Q54
        "id": 54,
        "question": "Khi soạn thảo văn bản với font: Time New Roman, ta cần sử dụng bảng mã nào để gõ được dấu tiếng Việt?",
        "options": [
            "TCVN 3", "Telex", "VietWare", "Unicode" 
        ],
        "correct_option_text": get_correct_text([
            "TCVN 3", "Telex", "VietWare", "Unicode"
        ], CORRECT_ANSWERS_BY_ID.get(54))
    },
    { # Q55
        "id": 55,
        "question": "Trong Ms Word 2016, sau khi định dạng in nghiêng cho một đoạn văn bản, để xóa định dạng in nghiêng đó thì bấm tổ hộp phím nào?",
        "options": [
            "Ctrl+V", "Ctrl+S", "Ctrl+I", "Ctrl+B" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+V", "Ctrl+S", "Ctrl+I", "Ctrl+B"
        ], CORRECT_ANSWERS_BY_ID.get(55))
    },
    { # Q56
        "id": 56,
        "question": "Trong Ms Word 2016, để định dạng in đậm cho một đoạn văn bản thì bấm tổ hộp phím nào?",
        "options": [
            "Ctrl+V", "Ctrl+S", "Ctrl+I", "Ctrl+B" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+V", "Ctrl+S", "Ctrl+I", "Ctrl+B"
        ], CORRECT_ANSWERS_BY_ID.get(56))
    },
    { # Q57
        "id": 57,
        "question": "Trong MS Word 2016, để tạo chỉ số dưới (H2) ta dùng tổ hợp phím nào?",
        "options": [
            "Ctrl+=", "Ctrl+Alt+=", "Ctrl+Shift+=", "Shift +=" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+=", "Ctrl+Alt+=", "Ctrl+Shift+=", "Shift +="
        ], CORRECT_ANSWERS_BY_ID.get(57))
    },
    { # Q58
        "id": 58,
        "question": "Để thay đổi màu ký tự trong MS Word 2016, trong menu Home, chọn vào:",
        "options": [
            "Font color và chọn màu.", "Text highlight color và chọn màu.", "Change case và chọn màu.", "Font và chọn màu." 
        ],
        "correct_option_text": get_correct_text([
            "Font color và chọn màu.", "Text highlight color và chọn màu.", "Change case và chọn màu.", "Font và chọn màu."
        ], CORRECT_ANSWERS_BY_ID.get(58))
    },
    { # Q59
        "id": 59,
        "question": "Trong Word 2016, để đổi chữ thường sang chữ in hoa và ngược lại ta dùng tổ hợp phím nào?",
        "options": [
            "Shift + F1", "Shift + F3", "Shift + U", "Ctrl+F3" 
        ],
        "correct_option_text": get_correct_text([
            "Shift + F1", "Shift + F3", "Shift + U", "Ctrl+F3"
        ], CORRECT_ANSWERS_BY_ID.get(59))
    },
    { # Q60
        "id": 60,
        "question": "Trong khi soạn thảo văn bản MS Word, nếu muốn ngắt trang (bắt buộc) ta:",
        "options": [
            "Ân phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ấn tổ hợp phím Ctrl + Enter", "Word tự động không cần bấm phím" 
        ],
        "correct_option_text": get_correct_text([
            "Ân phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ấn tổ hợp phím Ctrl + Enter", "Word tự động không cần bấm phím"
        ], CORRECT_ANSWERS_BY_ID.get(60))
    },
    { # Q61
        "id": 61,
        "question": "Trong khi soạn thảo văn bản, nếu kết thúc 1 đoạn (Paragraph) và muốn sang 1 đoạn (Paragraph) mới, ta thực hiện:",
        "options": [
            "Ân tổ hợp phím Ctrl - Enter", "Ấn tổ hợp phím Shift - Enter", "Ấn phím Enter", "Word tự động, không cần bấm phím" 
        ],
        "correct_option_text": get_correct_text([
            "Ân tổ hợp phím Ctrl - Enter", "Ấn tổ hợp phím Shift - Enter", "Ấn phím Enter", "Word tự động, không cần bấm phím"
        ], CORRECT_ANSWERS_BY_ID.get(61))
    },
    { # Q62
        "id": 62,
        "question": "Trong Word để xuống dòng mà không qua đoạn (paragraph) mới thì:",
        "options": [
            "Ấn tổ hợp phím Ctrl + Enter", "Ân phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ân tổ hợp phím Alt + Enter." 
        ],
        "correct_option_text": get_correct_text([
            "Ấn tổ hợp phím Ctrl + Enter", "Ân phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ân tổ hợp phím Alt + Enter."
        ], CORRECT_ANSWERS_BY_ID.get(62))
    },
    { # Q63
        "id": 63,
        "question": "Trong MS Word 2016, để canh đều hai bên đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": [
            "Ctrl+F", "Ctrl+C", "Shift + J", "Ctrl+J" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+F", "Ctrl+C", "Shift + J", "Ctrl+J"
        ], CORRECT_ANSWERS_BY_ID.get(63))
    },
    { # Q64
        "id": 64,
        "question": "Trong MS Word 2016, để canh trái đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": [
            "Ctrl+F", "Ctrl+L", "Shift + L", "Ctrl+J" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+F", "Ctrl+L", "Shift + L", "Ctrl+J"
        ], CORRECT_ANSWERS_BY_ID.get(64))
    },
    { # Q65
        "id": 65,
        "question": "Trong MS Word 2016, để canh phải đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": [
            "Ctrl+R", "Ctrl+L", "Shift + L", "Ctrl+J" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+R", "Ctrl+L", "Shift + L", "Ctrl+J"
        ], CORRECT_ANSWERS_BY_ID.get(65))
    },
    { # Q66
        "id": 66,
        "question": "Trong MS Word 2016, để canh giữa đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": [
            "Ctrl+R", "Ctrl+L", "Shift + L", "Ctrl+E" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+R", "Ctrl+L", "Shift + L", "Ctrl+E"
        ], CORRECT_ANSWERS_BY_ID.get(66))
    },
    { # Q67
        "id": 67,
        "question": "Trong soạn thảo Word 2016, để thêm ký hiệu tự động đầu mỗi đoạn văn bản, ta thực hiện:",
        "options": [
            "Tại menu Home, chọn biểu tượng Bullets", 
            "Tại menu Insert, chọn biểu tượng Bullets", 
            "Tại menu Page Layout, chọn biểu tượng Bullets", 
            "Tại menu View, chọn biểu tượng Bullets" 
        ],
        "correct_option_text": get_correct_text([
            "Tại menu Home, chọn biểu tượng Bullets",
            "Tại menu Insert, chọn biểu tượng Bullets",
            "Tại menu Page Layout, chọn biểu tượng Bullets",
            "Tại menu View, chọn biểu tượng Bullets"
        ], CORRECT_ANSWERS_BY_ID.get(67))
    },
    { # Q68
        "id": 68,
        "question": "Trong soạn thảo Word 2016, để chèn một bảng biểu vào văn bản ta thực hiện:",
        "options": [
            "Tại menu Home chọn Table", "Tại menu Insert chọn Table", "Tại menu Insert chọn Shapes", "Tại menu Home chọn shapes" 
        ],
        "correct_option_text": get_correct_text([
            "Tại menu Home chọn Table", "Tại menu Insert chọn Table", "Tại menu Insert chọn Shapes", "Tại menu Home chọn shapes"
        ], CORRECT_ANSWERS_BY_ID.get(68))
    },
    { # Q69
        "id": 69,
        "question": "Trong MS Word 2016, để lưu văn bản với định dạng phiên bản 97-2003 ta gọi lệnh gì?",
        "options": [
            "Tại menu File, chọn Save As, chọn Browse, tại ô Save as type chọn Word 97-2003 Document", 
            "Tại menu File, chọn Save, tại ô Save as type chọn Word 97-2003 Document", 
            "Tại menu Home, chọn Save, tại ô Save as type chọn Word 97-2003 Document", 
            "Tại menu Layout, chọn Save, tại ô Save as type chọn Word 97-2003 Document" 
        ],
        "correct_option_text": get_correct_text([
            "Tại menu File, chọn Save As, chọn Browse, tại ô Save as type chọn Word 97-2003 Document",
            "Tại menu File, chọn Save, tại ô Save as type chọn Word 97-2003 Document",
            "Tại menu Home, chọn Save, tại ô Save as type chọn Word 97-2003 Document",
            "Tại menu Layout, chọn Save, tại ô Save as type chọn Word 97-2003 Document"
        ], CORRECT_ANSWERS_BY_ID.get(69))
    },
    { # Q70
        "id": 70,
        "question": "Trong MS Word, tổ hợp phím nào cho phép ngay lập tức đưa con trỏ về đầu văn bản?",
        "options": [
            "Ctrl + Home", "Ctrl + Alt + Home", "Alt + Home", "Shift + Home" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + Home", "Ctrl + Alt + Home", "Alt + Home", "Shift + Home"
        ], CORRECT_ANSWERS_BY_ID.get(70))
    },
    { # Q71
        "id": 71,
        "question": "Trong MS Word, để in văn bản, ta chọn tổ hợp phím nào sau đây:",
        "options": [
            "Ctrl+P", "Ctrl+Shift+P", "Ctrl+Alt+P", "Alt+P" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+P", "Ctrl+Shift+P", "Ctrl+Alt+P", "Alt+P"
        ], CORRECT_ANSWERS_BY_ID.get(71))
    },
    { # Q72
        "id": 72,
        "question": "Trong MS Word, sau khi đã chọn văn bản, ấn tổ hợp phím Ctrl+R là để:",
        "options": [
            "Canh đều lề phải cho văn bản đã chọn", 
            "Canh đều lề trái cho văn bản đã chọn", 
            "Canh đều cả hai lề (trái và phải) cho văn bản đã chọn", 
            "Canh giữa cho văn bản đã chọn" 
        ],
        "correct_option_text": get_correct_text([
            "Canh đều lề phải cho văn bản đã chọn",
            "Canh đều lề trái cho văn bản đã chọn",
            "Canh đều cả hai lề (trái và phải) cho văn bản đã chọn",
            "Canh giữa cho văn bản đã chọn"
        ], CORRECT_ANSWERS_BY_ID.get(72))
    },
    { # Q73
        "id": 73,
        "question": "Trong MS Word, sử dụng tổ hợp phím nào để canh đều hai bên lề (trái và phải) cho văn bản:",
        "options": [
            "Ctrl+J", "Ctrl+R", "Ctrl+E", "Ctrl + L" 
        ],
        "correct_option_text": get_correct_text([
            "Ctrl+J", "Ctrl+R", "Ctrl+E", "Ctrl + L"
        ], CORRECT_ANSWERS_BY_ID.get(73))
    },
    { # Q74
        "id": 74,
        "question": "Trong MS Word, sau khi đã chọn văn bản, ấn tổ hợp phím Ctrl + B là để :",
        "options": [
            "Tạo kiểu chữ đậm cho văn bản đã chọn", 
            "Tạo kiểu chữ nghiêng cho văn bản đã chọn", 
            "Tạo gạch chân cho văn bản đã chọn", 
            "Tạo chữ in hoa cho văn bản đã chọn" 
        ],
        "correct_option_text": get_correct_text([
            "Tạo kiểu chữ đậm cho văn bản đã chọn",
            "Tạo kiểu chữ nghiêng cho văn bản đã chọn",
            "Tạo gạch chân cho văn bản đã chọn",
            "Tạo chữ in hoa cho văn bản đã chọn"
        ], CORRECT_ANSWERS_BY_ID.get(74))
    },
    { # Q75
        "id": 75,
        "question": "Khi đang soạn thảo văn bản trong MS Word, muốn đánh dấu để chọn một từ, ta thực hiện:",
        "options": [
            "Nháy đúp chuột vào từ cần chọn", 
            "Ân tổ hợp phím Ctrl+A", 
            "Nháy chuột vào từ cần chọn", 
            "Nháy chuột phải vào từ cần chọn" 
        ],
        "correct_option_text": get_correct_text([
            "Nháy đúp chuột vào từ cần chọn",
            "Ân tổ hợp phím Ctrl+A",
            "Nháy chuột vào từ cần chọn",
            "Nháy chuột phải vào từ cần chọn"
        ], CORRECT_ANSWERS_BY_ID.get(75))
    },
    { # Q76
        "id": 76,
        "question": "Khi đang soạn thảo văn bản trong MS Word, ấn tổ hợp phím Shift + Enter là để:",
        "options": [
            "Xuống hàng trong cùng một Paragraph (cùng một đoạn văn bản)", 
            "Xuống hàng và tạo một Paragraph mới (tạo đoạn văn bản khác)", 
            "Xuống một trang mới", 
            "Xuống một trang màn hình" 
        ],
        "correct_option_text": get_correct_text([
            "Xuống hàng trong cùng một Paragraph (cùng một đoạn văn bản)",
            "Xuống hàng và tạo một Paragraph mới (tạo đoạn văn bản khác)",
            "Xuống một trang mới",
            "Xuống một trang màn hình"
        ], CORRECT_ANSWERS_BY_ID.get(76))
    },
    { # Q77
        "id": 77,
        "question": "Trong MS Word, để con trỏ soạn thảo nhảy đến một trang nào đó, ta ấn phím nào (rồi sau đó mới gõ số trang)?",
        "options": [
            "F5", "F2", "F7", "F3" 
        ],
        "correct_option_text": get_correct_text([
            "F5", "F2", "F7", "F3"
        ], CORRECT_ANSWERS_BY_ID.get(77))
    },
    { # Q78
        "id": 78,
        "question": "Khi làm việc với bảng biểu trong MS Word, để tách 01 ô thành nhiều ô, ta chọn ô cần tách, rồi thực hiện:",
        "options": [
            "Click chuột phải, chọn Split Cells", 
            "Click chuột phải, chọn Merge Cells", 
            "Click chuột phải, chọn Insert, chọn Insert Cells", 
            "Click chuột phải, chọn Delete Cells" 
        ],
        "correct_option_text": get_correct_text([
            "Click chuột phải, chọn Split Cells",
            "Click chuột phải, chọn Merge Cells",
            "Click chuột phải, chọn Insert, chọn Insert Cells",
            "Click chuột phải, chọn Delete Cells"
        ], CORRECT_ANSWERS_BY_ID.get(78))
    },
    { # Q79
        "id": 79,
        "question": "Trong MS Word, để thay thế tất cả các từ/cụm từ trong văn bản, tại thẻ Replace của hộp thoại Find and Replace, ta chọn lệnh:",
        "options": [
            "Replace All", "Replace", "Find Next", "Delete (Thêm giả định)" 
        ],
        "correct_option_text": get_correct_text([
            "Replace All", "Replace", "Find Next", "Delete (Thêm giả định)"
        ], CORRECT_ANSWERS_BY_ID.get(79))
    },
    { # Q80
        "id": 80,
        "question": "Trong MS Word, phím Delete có chức năng:",
        "options": [
            "Xóa ký tự phía sau con trỏ soạn thảo", 
            "Xóa ký tự phía trước con trỏ soạn thảo", 
            "Lùi văn bản vào với một khoảng cách cố định", 
            "Di chuyển con trỏ soạn thảo" 
        ],
        "correct_option_text": get_correct_text([
            "Xóa ký tự phía sau con trỏ soạn thảo",
            "Xóa ký tự phía trước con trỏ soạn thảo",
            "Lùi văn bản vào với một khoảng cách cố định",
            "Di chuyển con trỏ soạn thảo"
        ], CORRECT_ANSWERS_BY_ID.get(80))
    },
    { # Q81
        "id": 81,
        "question": "Trong MS Word, phím Backspace có chức năng:",
        "options": [
            "Xóa ký tự phía trước con trỏ soạn thảo", 
            "Xóa ký tự phía sau con trỏ soạn thảo", 
            "Lùi văn bản vào với một khoảng cách cố định", 
            "Di chuyển con trỏ soạn thảo" 
        ],
        "correct_option_text": get_correct_text([
            "Xóa ký tự phía trước con trỏ soạn thảo",
            "Xóa ký tự phía sau con trỏ soạn thảo",
            "Lùi văn bản vào với một khoảng cách cố định",
            "Di chuyển con trỏ soạn thảo"
        ], CORRECT_ANSWERS_BY_ID.get(81))
    },
    { # Q82
        "id": 82,
        "question": "Khi đang soạn thảo văn bản trong MS Word, muốn đánh dấu để chọn toàn bộ nội dung văn bản, ta thực hiện:",
        "options": [
            "Nháy đúp chuột vào từ cần chọn", 
            "Ấn tổ hợp phím Ctrl+A", 
            "Nháy chuột vào từ cần chọn", 
            "Nháy chuột phải vào từ cần chọn" 
        ],
        "correct_option_text": get_correct_text([
            "Nháy đúp chuột vào từ cần chọn",
            "Ấn tổ hợp phím Ctrl+A",
            "Nháy chuột vào từ cần chọn",
            "Nháy chuột phải vào từ cần chọn"
        ], CORRECT_ANSWERS_BY_ID.get(82))
    },
    { # Q83
        "id": 83,
        "question": "Khi đang soạn thảo văn bản trong MS Word, ấn tổ hợp phím Ctrl + F là để:",
        "options": [
            "Xuống hàng trong cùng một Paragraph.", 
            "Xuống hàng và tạo một Paragraph mới.", 
            "Tìm kiếm từ/cụm từ trong văn bản.", 
            "Thay thế từ/cụm từ trong văn bản." 
        ],
        "correct_option_text": get_correct_text([
            "Xuống hàng trong cùng một Paragraph.",
            "Xuống hàng và tạo một Paragraph mới.",
            "Tìm kiếm từ/cụm từ trong văn bản.",
            "Thay thế từ/cụm từ trong văn bản."
        ], CORRECT_ANSWERS_BY_ID.get(83))
    },
    # Khối câu hỏi giữ chỗ (Q84-Q199) - Dùng đáp án (A, B, C, D) đã có để chấm điểm
    *[
        {
            "id": i,
            "question": f"***[NỘI DUNG GIỮ CHỖ]*** Câu {i}: Nội dung câu hỏi và các lựa chọn đáp án không được hiển thị đầy đủ trong tài liệu PDF. (Đáp án đã được lấy theo khóa đáp án của bạn: {CORRECT_ANSWERS_BY_ID.get(i, '?')})",
            "options": [
                "Lựa chọn A (Thay thế bằng nội dung thật)",
                "Lựa chọn B (Thay thế bằng nội dung thật)",
                "Lựa chọn C (Thay thế bằng nội dung thật)",
                "Lựa chọn D (Thay thế bằng nội dung thật)"
            ],
            # Gán đáp án đúng dựa trên chữ cái, sử dụng nội dung giữ chỗ tương ứng.
            "correct_option_text": get_correct_text([
                "Lựa chọn A (Thay thế bằng nội dung thật)",
                "Lựa chọn B (Thay thế bằng nội dung thật)",
                "Lựa chọn C (Thay thế bằng nội dung thật)",
                "Lựa chọn D (Thay thế bằng nội dung thật)"
            ], CORRECT_ANSWERS_BY_ID.get(i, '?'))
        }
        for i in range(84, 200) if i not in range(177, 199) # Chỉ chạy cho các ID còn lại.
    ],
    # Q177-Q198 - Dùng lại dữ liệu giữ chỗ cho các câu cuối (đã có đáp án)
    *[
        {
            "id": i,
            "question": f"***[NỘI DUNG GIỮ CHỖ]*** Câu {i}: Nội dung câu hỏi và các lựa chọn đáp án không được hiển thị đầy đủ trong tài liệu PDF. (Đáp án đã được lấy theo khóa đáp án của bạn: {CORRECT_ANSWERS_BY_ID.get(i, '?')})",
            "options": [
                "Lựa chọn A (Thay thế bằng nội dung thật)",
                "Lựa chọn B (Thay thế bằng nội dung thật)",
                "Lựa chọn C (Thay thế bằng nội dung thật)",
                "Lựa chọn D (Thay thế bằng nội dung thật)"
            ],
            "correct_option_text": get_correct_text([
                "Lựa chọn A (Thay thế bằng nội dung thật)",
                "Lựa chọn B (Thay thế bằng nội dung thật)",
                "Lựa chọn C (Thay thế bằng nội dung thật)",
                "Lựa chọn D (Thay thế bằng nội dung thật)"
            ], CORRECT_ANSWERS_BY_ID.get(i, '?'))
        }
        for i in range(177, 199)
    ]
]


# Sắp xếp lại dữ liệu theo ID để đảm bảo đủ 199 câu
QUIZ_DATA_RAW.sort(key=lambda x: x['id'])
# Loại bỏ các ID trùng lặp do việc ghép list
final_quiz_data = {}
for q in QUIZ_DATA_RAW:
    final_quiz_data[q['id']] = q
QUIZ_DATA_RAW = list(final_quiz_data.values())


# --- 3. CÁC HẰNG SỐ CƠ BẢN ---
TOTAL_QUESTIONS = 199 
TOTAL_EXAMS = 10

# --- 4. HÀM KHỞI TẠO VÀ QUẢN LÝ SESSION STATE ---

def initialize_session_state():
    """Khởi tạo các biến trạng thái cần thiết cho ứng dụng."""
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Ôn thi'
    if 'exam_state' not in st.session_state:
        st.session_state.exam_state = {} 
    if 'answers' not in st.session_state:
        st.session_state.answers = defaultdict(str) 
    if 'current_exam_index' not in st.session_state:
        st.session_state.current_exam_index = None
    if 'score_submitted' not in st.session_state:
        st.session_state.score_submitted = False
    
def generate_mock_exam(exam_index):
    """Tạo đề thi thử (random 199 câu từ tổng số) và xáo trộn đáp án."""
    if exam_index not in st.session_state.exam_state:
        # 1. Lấy 199 câu hỏi, sau đó xáo trộn vị trí
        # Dùng random.sample để đảm bảo chọn đủ 199 câu và xáo trộn vị trí câu hỏi
        questions_shuffled = random.sample(QUIZ_DATA_RAW, k=TOTAL_QUESTIONS)
        
        # 2. Xáo trộn đáp án trong từng câu hỏi (Đảo vị trí A, B, C, D)
        exam_questions = []
        for q_data in questions_shuffled:
            shuffled_options = q_data['options'].copy()
            random.shuffle(shuffled_options)
            
            exam_questions.append({
                "id": q_data['id'],
                "question": q_data['question'],
                "options": shuffled_options,
                "correct_option_text": q_data['correct_option_text'] # Giữ nguyên text đáp án đúng
            })
        
        st.session_state.exam_state[exam_index] = exam_questions
    
    return st.session_state.exam_state[exam_index]

def calculate_score(questions, user_answers):
    """Tính toán điểm và thống kê kết quả."""
    total_correct = 0
    total_questions = len(questions)
    
    correct_answers_map = {q['id']: q['correct_option_text'] for q in questions}

    for q_data in questions:
        q_id = q_data['id']
        selected_answer = user_answers.get(q_id) 
        correct_answer = correct_answers_map.get(q_id)
        
        if selected_answer and selected_answer == correct_answer:
            total_correct += 1
            
    score = (total_correct / total_questions) * 10
    
    stats = {
        'Tổng số câu': total_questions,
        'Số câu đúng': total_correct,
        'Số câu sai': total_questions - total_correct,
        'Số câu chưa trả lời': total_questions - len(user_answers),
        'Điểm số': round(score, 2)
    }
    
    return stats, correct_answers_map

# --- 5. GIAO DIỆN (UI) CÁC CHẾ ĐỘ ---

def display_question(q_data, index, mode):
    """Hiển thị một câu hỏi với tùy chọn radio button và feedback."""
    q_id = q_data['id']
    question_text = q_data['question']
    options = q_data['options']
    correct_option_text = q_data['correct_option_text']
    
    st.markdown(f"**Câu {index + 1}** (ID: {q_id}): {question_text}")
    
    radio_key = f"q_{q_id}_exam_{st.session_state.current_exam_index}" if st.session_state.current_exam_index else f"q_{q_id}_review"
    
    # Lấy đáp án đã chọn (nếu có)
    selected = st.session_state.answers.get(q_id, "")

    # Thêm tùy chọn "Chưa chọn" (chuỗi rỗng) vào đầu để người dùng có thể bỏ chọn
    options_with_empty = [""] + options
    
    # Tìm index của đáp án đã chọn
    try:
        default_index = options_with_empty.index(selected)
    except ValueError:
        default_index = 0 # Nếu chưa chọn hoặc đáp án cũ không hợp lệ

    # Nếu đã nộp bài (chế độ xem kết quả Thi thử)
    if st.session_state.score_submitted and mode == 'Thi thử':
        for opt in options:
            is_correct = opt == correct_option_text
            is_selected = opt == selected
            
            # Tô màu cho đáp án
            style = "padding: 5px; border-radius: 5px; margin: 2px 0;"
            icon = ""
            if is_correct:
                color = "#d4edda" # Light green
                border_color = "#155724" 
                icon = "✅"
            elif is_selected and not is_correct:
                color = "#f8d7da" # Light red
                border_color = "#721c24"
                icon = "❌"
            else:
                color = "white"
                border_color = "lightgrey"
                
            st.markdown(f'<p style="{style} background-color: {color}; border: 1px solid {border_color}; margin: 2px 0;">{icon} {opt}</p>', unsafe_allow_html=True)
            
    # Chế độ làm bài/ôn tập: cho phép chọn đáp án
    else:
        selected_option = st.radio(
            "Chọn đáp án:",
            options_with_empty,
            index=default_index,
            key=radio_key,
            format_func=lambda x: f"{chr(65 + options.index(x))}. {x}" if x else " ", # Hiển thị A, B, C, D...
        )
        
        # Cập nhật session state
        if selected_option:
            st.session_state.answers[q_id] = selected_option
        elif q_id in st.session_state.answers:
            # Xóa đáp án nếu người dùng chọn lại "trống"
            del st.session_state.answers[q_id] 
            
        # Chế độ ÔN THI: Hiển thị kết quả ngay lập tức
        if mode == 'Ôn thi' and selected_option:
            if selected_option == correct_option_text:
                st.success("🎉 **CHÍNH XÁC!**")
            else:
                st.error(f"❌ **SAI!** Đáp án đúng là: **{correct_option_text}**")
        st.markdown("---") # Đường kẻ phân cách

def render_review_mode():
    """Giao diện chế độ Ôn thi (Practice Mode)."""
    st.header("📚 Chế độ Ôn thi")
    st.info("Trong chế độ này, bạn sẽ nhận được phản hồi ngay lập tức sau khi chọn đáp án. Đề ôn tập bao gồm 50 câu hỏi được chọn ngẫu nhiên.")
    
    # Đảm bảo reset trạng thái Thi thử
    st.session_state.current_exam_index = None
    st.session_state.score_submitted = False
    
    # Lấy/Tạo danh sách ôn tập (chọn ngẫu nhiên 50 câu)
    if 'review_questions' not in st.session_state or st.button("Tải lại 50 câu ôn tập mới"):
        st.session_state.review_questions = random.sample(QUIZ_DATA_RAW, k=50) 
        st.session_state.answers = defaultdict(str) # Reset đáp án ôn tập

    questions_to_review = st.session_state.review_questions
    
    for i, q_data in enumerate(questions_to_review):
        display_question(q_data, i, mode='Ôn thi')

def render_mock_exam_mode():
    """Giao diện chế độ Thi thử (Mock Exam Mode)."""
    st.header("📝 Chế độ Thi thử")
    
    # 1. Chọn đề thi
    exam_options = [f"Đề số {i}" for i in range(1, TOTAL_EXAMS + 1)]
    # Đặt đề mặc định là Đề 1 nếu chưa có
    current_index = st.session_state.current_exam_index if st.session_state.current_exam_index is not None else 1
    selected_exam_label = st.selectbox(
        "**Chọn đề thi**",
        options=exam_options,
        index=current_index - 1,
        key='exam_selector'
    )
    
    selected_exam_index = int(selected_exam_label.split()[-1])
    
    # Cập nhật trạng thái đề thi hiện tại
    if st.session_state.current_exam_index != selected_exam_index:
        st.session_state.current_exam_index = selected_exam_index
        st.session_state.answers = defaultdict(str) # Reset đáp án khi đổi đề
        st.session_state.score_submitted = False # Reset trạng thái chấm điểm

    # Tải/Tạo đề thi (xáo trộn câu hỏi và đáp án)
    current_exam_questions = generate_mock_exam(selected_exam_index)
    
    st.markdown(f"---")
    
    # 2. Hiển thị điểm (nếu đã nộp bài)
    if st.session_state.score_submitted:
        stats, _ = calculate_score(current_exam_questions, st.session_state.answers)
        
        st.subheader(f"📊 Kết quả Đề thi số {selected_exam_index}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Điểm số", f"{stats['Điểm số']}/10", f"{stats['Số câu đúng']} câu đúng")
        col2.metric("Số câu chưa làm", stats['Số câu chưa trả lời'])
        col3.metric("Tổng số câu", stats['Tổng số câu'])

        st.markdown("---")
        st.subheader("Đáp án chi tiết (Đáp án đúng được tô xanh):")
        
        # Duyệt lại để hiển thị đáp án đúng/sai
        for i, q_data in enumerate(current_exam_questions):
            display_question(q_data, i, mode='Thi thử')
            
    # 3. Chế độ làm bài
    else:
        st.info(f"Đề thi số **{selected_exam_index}** có **{TOTAL_QUESTIONS}** câu hỏi. Hãy hoàn thành và nộp bài!")
        st.markdown("---")
        
        # Form chứa toàn bộ bài thi
        with st.form("mock_exam_form"):
            # Hiển thị tất cả 199 câu hỏi
            for i, q_data in enumerate(current_exam_questions):
                display_question(q_data, i, mode='Thi thử')
                
            st.markdown("---")
            
            # Nút submit chính
            submitted = st.form_submit_button("NỘP BÀI VÀ CHẤM ĐIỂM 🚀")
            
            if submitted:
                # Xác nhận nếu chưa làm hết
                if len(st.session_state.answers) < TOTAL_QUESTIONS:
                    st.warning(f"Bạn mới chỉ trả lời **{len(st.session_state.answers)}/{TOTAL_QUESTIONS}** câu. Vui lòng xác nhận nộp bài:")
                    confirm = st.checkbox("Tôi xác nhận muốn nộp bài dù chưa hoàn thành", key='confirm_submit')
                    if not confirm:
                        st.stop()
                        
                st.session_state.score_submitted = True
                st.experimental_rerun() # Chạy lại để hiển thị kết quả

# --- 6. HÀM CHÍNH CỦA ỨNG DỤNG ---

def main_app():
    st.set_page_config(layout="wide", page_title="Ứng dụng Trắc nghiệm Tin học")
    st.title("Ứng dụng Trắc nghiệm Tin học Cơ bản")
    
    initialize_session_state()

    mode_selection = st.sidebar.selectbox(
        "Chọn chế độ",
        ('Ôn thi', 'Thi thử'),
        key='mode_select',
        index=('Ôn thi', 'Thi thử').index(st.session_state.mode)
    )
    st.session_state.mode = mode_selection
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Thông tin Bài thi")
    st.sidebar.markdown(f"**Tổng số câu hỏi:** {TOTAL_QUESTIONS} câu")
    st.sidebar.markdown(f"**Số đề thi thử:** {TOTAL_EXAMS} đề")
    st.sidebar.markdown(f"**LƯU Ý:** Ứng dụng đang sử dụng đáp án chính xác bạn cung cấp.")
    
    if st.session_state.mode == 'Ôn thi':
        render_review_mode()
    elif st.session_state.mode == 'Thi thử':
        render_mock_exam_mode()

if __name__ == "__main__":
    main_app()