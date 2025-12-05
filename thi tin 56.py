import streamlit as st
import random
from collections import defaultdict
import uuid

# --- CẤU HÌNH ỨNG DỤNG ---
TOTAL_QUESTIONS = 199
QUESTIONS_PER_EXAM = 30
TOTAL_EXAMS = 14

# --- 1. DỮ LIỆU ĐÁP ÁN ĐÚNG CẬP NHẬT TỪ TÀI LIỆU (199 câu) ---
# Đây là các đáp án đúng ban đầu (A, B, C, D) theo ID câu hỏi
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
    91: 'A', 92: 'A', 93: 'A', 94: 'A', 95: 'B', 96: 'A', 97: 'A', 98: 'B', 99: 'D', 100: 'B',
    101: 'B', 102: 'A', 103: 'C', 104: 'B', 105: 'C', 106: 'D', 107: 'B', 108: 'A', 109: 'A',
    110: 'C', 111: 'A', 112: 'C', 113: 'C', 114: 'A', 115: 'C', 116: 'C', 117: 'A', 118: 'D',
    119: 'A', 120: 'A', 121: 'B', 122: 'C', 123: 'D', 124: 'C', 125: 'B', 126: 'C', 127: 'A',
    128: 'D', 129: 'B', 130: 'A', 131: 'A', 132: 'A', 133: 'A', 134: 'A', 135: 'A', 136: 'C',
    137: 'B', 138: 'A', 139: 'C', 140: 'A', 141: 'B', 142: 'B', 143: 'B', 144: 'D', 145: 'B',
    146: 'C', 147: 'C', 148: 'B', 149: 'C', 150: 'B', 151: 'A', 152: 'B', 153: 'B', 154: 'B',
    155: 'B', 156: 'B', 157: 'B', 158: 'B', 159: 'C', 160: 'B', 161: 'C', 162: 'A', 163: 'A',
    164: 'B', 165: 'B', 166: 'B', 167: 'A', 168: 'B', 169: 'A', 170: 'B', 171: 'D', 172: 'A',
    173: 'C', 174: 'C', 175: 'A', 176: 'D', 177: 'C', 178: 'C', 179: 'C', 180: 'D', 181: 'C',
    182: 'A', 183: 'A', 184: 'C', 185: 'B', 186: 'B', 187: 'C', 188: 'D', 189: 'A', 190: 'A',
    191: 'C', 192: 'A', 193: 'D', 194: 'B', 195: 'B', 196: 'C', 197: 'A', 198: 'B', 199: 'A'
}

# Helper function
def get_correct_text(options, correct_letter):
    """Tìm nội dung đáp án đúng dựa trên chữ cái đáp án (A, B, C, D)"""
    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    idx = mapping.get(correct_letter.upper())
    return options[idx] if idx is not None and 0 <= idx < len(options) else "LỖI: Không tìm thấy đáp án"

# --- 2. DỮ LIỆU CÂU HỎI ĐẦY ĐỦ (199 CÂU) ---
QUIZ_DATA_RAW = [
    { # Q01
        "id": 1,
        "question": "Trong các phát biểu sau, phát biểu nào sai khi nói đến bộ nhớ ROM:",
        "options": [
            "Máy tính có thể khởi động mà không cần bộ nhớ ROM.",
            "ROM được viết tắt bởi cụm từ \"Read Only Memory\".",
            "ROM là bộ nhớ chỉ đọc, dữ liệu trong bộ nhớ ROM vẫn duy trì khi nguồn điện bị cắt.",
            "ROM được các nhà sản xuất ghi sẵn các chương trình cơ sở phục vụ cho quá trình khởi động máy."
        ],
        "correct_option_text": get_correct_text([
            "Máy tính có thể khởi động mà không cần bộ nhớ ROM.",
            "ROM được viết tắt bởi cụm từ \"Read Only Memory\".",
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
        "options": ["3072 KB", "3000 KB", "0,3 KB", "300 KB"],
        "correct_option_text": get_correct_text(["3072 KB", "3000 KB", "0,3 KB", "300 KB"], CORRECT_ANSWERS_BY_ID.get(3))
    },
    { # Q04
        "id": 4,
        "question": "Trong Windows, muốn xóa dữ liệu và không cho phục hồi trong Recycle Bin, cần thực hiện các thao tác nào sau đây?",
        "options": [
            "Chọn đối tượng cần xóa, ấn tổ hợp phím Shift+Delete",
            "Chọn đối tượng cần xóa, ấn phím Delete.",
            "Chọn đối tượng cần xóa, kích chuột phải, chọn Delete.",
            "Chọn đối tượng cần xóa, ấn tổ hợp phím Ctrl+Delete"
        ],
        "correct_option_text": get_correct_text([
            "Chọn đối tượng cần xóa, ấn tổ hợp phím Shift+Delete",
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
        "options": ["Control Panel", "All Programs", "Control System", "Control Desktop"],
        "correct_option_text": get_correct_text(["Control Panel", "All Programs", "Control System", "Control Desktop"], CORRECT_ANSWERS_BY_ID.get(6))
    },
    { # Q07
        "id": 7,
        "question": "ISP là viết tắt của",
        "options": ["Internet Service Provider", "Internet Server Provider", "Internet Super Provider", "Internet Side Provider"],
        "correct_option_text": get_correct_text(["Internet Service Provider", "Internet Server Provider", "Internet Super Provider", "Internet Side Provider"], CORRECT_ANSWERS_BY_ID.get(7))
    },
    { # Q08
        "id": 8,
        "question": "FTP là viết tắt của cụm từ tiếng Anh nào?",
        "options": ["File Transfer Procedure", "File Transfer Protocol", "Fast Transfer Protocol", "Future Transfer Procedure"],
        "correct_option_text": get_correct_text(["File Transfer Procedure", "File Transfer Protocol", "Fast Transfer Protocol", "Future Transfer Procedure"], CORRECT_ANSWERS_BY_ID.get(8))
    },
    { # Q09
        "id": 9,
        "question": "Để xem lại lịch sử duyệt web ta dùng tổ hợp phím trên trình duyệt Internet Explorer",
        "options": ["Ctrl + H", "Ctrl + L", "Ctrl + P", "Ctrl + A"],
        "correct_option_text": get_correct_text(["Ctrl + H", "Ctrl + L", "Ctrl + P", "Ctrl + A"], CORRECT_ANSWERS_BY_ID.get(9))
    },
    { # Q10
        "id": 10,
        "question": "Cấu trúc một địa chỉ thư điện tử?",
        "options": ["<Tên người dùng>@<Tên miền>", "<Tên miền> <Tên người dùng>", "<Tên miền>@<Tên người dùng>", "<Tên người dùng>#<Tên miền>"],
        "correct_option_text": get_correct_text(["<Tên người dùng>@<Tên miền>", "<Tên miền> <Tên người dùng>", "<Tên miền>@<Tên người dùng>", "<Tên người dùng>#<Tên miền>"], CORRECT_ANSWERS_BY_ID.get(10))
    },
    { # Q11
        "id": 11,
        "question": "Để chuyển tiếp thư tới người khác, bạn sử dụng nút nào?",
        "options": ["Relpy", "Relpy to All", "Attachment", "Forward"],
        "correct_option_text": get_correct_text(["Relpy", "Relpy to All", "Attachment", "Forward"], CORRECT_ANSWERS_BY_ID.get(11))
    },
    { # Q12
        "id": 12,
        "question": "DNS là viết tắt của cụm từ tiếng Anh nào?",
        "options": ["Domain Network System", "Domain Name System", "Dynamic Name System", "Dynamic Network System"],
        "correct_option_text": get_correct_text(["Domain Network System", "Domain Name System", "Dynamic Name System", "Dynamic Network System"], CORRECT_ANSWERS_BY_ID.get(12))
    },
    { # Q13
        "id": 13,
        "question": "Trong các cụm từ sau, cụm từ nào không phải là giao thức?",
        "options": ["TCP/IP", "LAN/WAN", "IPX/SPX", "POP3, SMTP"],
        "correct_option_text": get_correct_text(["TCP/IP", "LAN/WAN", "IPX/SPX", "POP3, SMTP"], CORRECT_ANSWERS_BY_ID.get(13))
    },
    { # Q14
        "id": 14,
        "question": "Dịch vụ lưu trữ đám mây của Microsoft có tên là gì?",
        "options": ["Google Driver", "Mediafire", "OneDrive", "Dropbox"],
        "correct_option_text": get_correct_text(["Google Driver", "Mediafire", "OneDrive", "Dropbox"], CORRECT_ANSWERS_BY_ID.get(14))
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
        "options": ["Màn hình (monitor)", "Máy quét (scanner)", "Máy chiếu (projector)", "Máy in (printer)"],
        "correct_option_text": get_correct_text(["Màn hình (monitor)", "Máy quét (scanner)", "Máy chiếu (projector)", "Máy in (printer)"], CORRECT_ANSWERS_BY_ID.get(18))
    },
    { # Q19
        "id": 19,
        "question": "Trong các cổng giao tiếp với thiết bị ngoại vi trên máy tính cổng nào sau đây thường được dùng để kết nối trực tiếp với máy in:",
        "options": ["PS/2", "COM", "USB hoặc LPT", "VGA"],
        "correct_option_text": get_correct_text(["PS/2", "COM", "USB hoặc LPT", "VGA"], CORRECT_ANSWERS_BY_ID.get(19))
    },
    { # Q20
        "id": 20,
        "question": "Tốc độ của bộ xử lý trung tâm (CPU) thường được tính bằng đơn vị đo:",
        "options": ["MB hoặc GB", "MHz hoặc GHz", "MBs hoặc GBs", "Gbps hoặc GBps"],
        "correct_option_text": get_correct_text(["MB hoặc GB", "MHz hoặc GHz", "MBs hoặc GBs", "Gbps hoặc GBps"], CORRECT_ANSWERS_BY_ID.get(20))
    },
    { # Q21
        "id": 21,
        "question": "Đơn vị đo nào sau đây không được sử dụng để đo dung lượng bộ nhớ trong?",
        "options": ["GB", "KB", "MB", "MHz"],
        "correct_option_text": get_correct_text(["GB", "KB", "MB", "MHz"], CORRECT_ANSWERS_BY_ID.get(21))
    },
    { # Q22
        "id": 22,
        "question": "Một Byte bằng bao nhiêu bit?",
        "options": ["16 bit", "8 bit", "1000 bit", "1024 bit"],
        "correct_option_text": get_correct_text(["16 bit", "8 bit", "1000 bit", "1024 bit"], CORRECT_ANSWERS_BY_ID.get(22))
    },
    { # Q23
        "id": 23,
        "question": "Một KB (Kilobyte) bằng bao nhiêu Byte?",
        "options": ["8 Byte", "10 Byte", "1000 Byte", "1024 Byte"],
        "correct_option_text": get_correct_text(["8 Byte", "10 Byte", "1000 Byte", "1024 Byte"], CORRECT_ANSWERS_BY_ID.get(23))
    },
    { # Q24
        "id": 24,
        "question": "Trong mạng máy tính, thuật ngữ LAN dùng để chỉ:",
        "options": ["Mạng cục bộ", "Mạng diện rộng", "Mạng toàn cầu", "Mạng Internet"],
        "correct_option_text": get_correct_text(["Mạng cục bộ", "Mạng diện rộng", "Mạng toàn cầu", "Mạng Internet"], CORRECT_ANSWERS_BY_ID.get(24))
    },
    { # Q25
        "id": 25,
        "question": "Trong mạng máy tính, thuật ngữ WAN dùng để chỉ:",
        "options": ["Mạng cục bộ", "Mạng diện rộng", "Mạng toàn cầu", "Điểm truy cập không dây"],
        "correct_option_text": get_correct_text(["Mạng cục bộ", "Mạng diện rộng", "Mạng toàn cầu", "Điểm truy cập không dây"], CORRECT_ANSWERS_BY_ID.get(25))
    },
    { # Q26
        "id": 26,
        "question": "Phần mềm nào sau đây không phải là phần mềm mã nguồn mở?",
        "options": ["LibreOffice", "Apache OpenOffice", "Microsoft Office", "Bộ gõ Tiếng Việt Unikey"],
        "correct_option_text": get_correct_text(["LibreOffice", "Apache OpenOffice", "Microsoft Office", "Bộ gõ Tiếng Việt Unikey"], CORRECT_ANSWERS_BY_ID.get(26))
    },
    { # Q27
        "id": 27,
        "question": "Trong các cổng sau cổng nào dùng để cắm trực tiếp vào bàn phím:",
        "options": ["Cổng PS/2, USB", "Cổng VGA, LPT", "Cổng HDMI, VGA", "Cổng RJ45, VGA"],
        "correct_option_text": get_correct_text(["Cổng PS/2, USB", "Cổng VGA, LPT", "Cổng HDMI, VGA", "Cổng RJ45, VGA"], CORRECT_ANSWERS_BY_ID.get(27))
    },
    { # Q28
        "id": 28,
        "question": "Đâu là viết tắt của cụm từ: \"công nghệ thông tin và truyền thông\"?",
        "options": ["ICT", "CTI", "CIT", "TCI"],
        "correct_option_text": get_correct_text(["ICT", "CTI", "CIT", "TCI"], CORRECT_ANSWERS_BY_ID.get(28))
    },
    { # Q29
        "id": 29,
        "question": "Trên hệ điều hành Windows 10, để hẹn giờ tắt máy sau 30 phút ta có thể dùng lệnh:",
        "options": ["shutdown -s -t 1800", "shutdown -r -t 1800", "shutdown -l -t 1800", "shutdown -a 1800"],
        "correct_option_text": get_correct_text(["shutdown -s -t 1800", "shutdown -r -t 1800", "shutdown -l -t 1800", "shutdown -a 1800"], CORRECT_ANSWERS_BY_ID.get(29))
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
        "question": "Trong các cụm từ liệt kê dưới đây, đâu là cụm từ chỉ tên của \"Thùng rác\" trong hệ điều hành Windows 10?",
        "options": ["Recycle Bin", "Bin Recycle", "Temple Bin", "Directory Bin"],
        "correct_option_text": get_correct_text(["Recycle Bin", "Bin Recycle", "Temple Bin", "Directory Bin"], CORRECT_ANSWERS_BY_ID.get(32))
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
            "Click chuột phải, chọn Edit / New /Folder",
            "Click chuột phải, chọn Tools / New / Folder",
            "Click chuột phải, chọn New / Folder",
            "Click chuột phải, chọn Windows / New / Folder"
        ],
        "correct_option_text": get_correct_text([
            "Click chuột phải, chọn Edit / New /Folder",
            "Click chuột phải, chọn Tools / New / Folder",
            "Click chuột phải, chọn New / Folder",
            "Click chuột phải, chọn Windows / New / Folder"
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
        "options": ["Ctrl+C", "Ctrl+Ins", "Print Screen", "ESC"],
        "correct_option_text": get_correct_text(["Ctrl+C", "Ctrl+Ins", "Print Screen", "ESC"], CORRECT_ANSWERS_BY_ID.get(36))
    },
    { # Q37
        "id": 37,
        "question": "Để hiển thị được giờ theo mẫu sau 08:10:15 ta phải dùng định dạng nào trong các dạng sau:",
        "options": ["h:mm:ss tt", "hh:mm:ss tt", "h:mm:ss tt", "hh:mm:ss"],
        "correct_option_text": get_correct_text(["h:mm:ss tt", "hh:mm:ss tt", "h:mm:ss tt", "hh:mm:ss"], CORRECT_ANSWERS_BY_ID.get(37))
    },
    { # Q38
        "id": 38,
        "question": "Để hiển thị được ngày theo mẫu sau 27/08/2023 ta phải dùng định dạng nào trong các dạng sau:",
        "options": ["dd/MM/yyyy", "dd/MM/yy", "mm/dd/yyyy", "mm/dd/yy"],
        "correct_option_text": get_correct_text(["dd/MM/yyyy", "dd/MM/yy", "mm/dd/yyyy", "mm/dd/yy"], CORRECT_ANSWERS_BY_ID.get(38))
    },
    { # Q39
        "id": 39,
        "question": "Chọn sắp xếp đúng theo phiên bản (version) từ thấp đến cao của hệ điều hành windows được liệt kê dưới đây?",
        "options": [
            "Windows Vista, Windows 10, Windows XP",
            "Windows XP, Windows Vista, Windows 10",
            "Windows XP, Windows 10, Windows Vista",
            "Windows 10, Windows Vista, Windows XP"
        ],
        "correct_option_text": get_correct_text([
            "Windows Vista, Windows 10, Windows XP",
            "Windows XP, Windows Vista, Windows 10",
            "Windows XP, Windows 10, Windows Vista",
            "Windows 10, Windows Vista, Windows XP"
        ], CORRECT_ANSWERS_BY_ID.get(39))
    },
    { # Q40
        "id": 40,
        "question": "Trong File Explorer, để tìm kiếm một nhóm tệp tin có tên bắt đầu bằng H, ta nhập tên sau:",
        "options": ["H??.docx", "H*.*", "H.*", "*H.*"],
        "correct_option_text": get_correct_text(["H??.docx", "H*.*", "H.*", "*H.*"], CORRECT_ANSWERS_BY_ID.get(40))
    },
    { # Q41
        "id": 41,
        "question": "Phần mềm nào sau đây có khả năng diệt virus cho máy tính:",
        "options": ["Kaspersky", "Microsoft Office", "Outlook Express", "WinRar"],
        "correct_option_text": get_correct_text(["Kaspersky", "Microsoft Office", "Outlook Express", "WinRar"], CORRECT_ANSWERS_BY_ID.get(41))
    },
    { # Q42
        "id": 42,
        "question": "Thuộc tính nào là thuộc tính ẩn của tập tin trong Windows 10",
        "options": ["Archive", "Read-only", "Hidden", "System"],
        "correct_option_text": get_correct_text(["Archive", "Read-only", "Hidden", "System"], CORRECT_ANSWERS_BY_ID.get(42))
    },
    { # Q43
        "id": 43,
        "question": "Trong MS Word 2016, để đóng tập tin, ta bấm tổ hợp phím:",
        "options": ["Ctrl + Shift + W", "Ctrl + W", "Ctrl + O", "Ctrl + S"],
        "correct_option_text": get_correct_text(["Ctrl + Shift + W", "Ctrl + W", "Ctrl + O", "Ctrl + S"], CORRECT_ANSWERS_BY_ID.get(43))
    },
    { # Q44
        "id": 44,
        "question": "Trong soạn thảo Word 2016, công dụng của tổ hợp phím Ctrl+O là:",
        "options": ["Đóng tệp tin đang mở", "Mở tệp tin đã có", "Lưu tệp tin vào đĩa", "Mở một tệp tin mới"],
        "correct_option_text": get_correct_text(["Đóng tệp tin đang mở", "Mở tệp tin đã có", "Lưu tệp tin vào đĩa", "Mở một tệp tin mới"], CORRECT_ANSWERS_BY_ID.get(44))
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
        "options": ["*.DOTX", "*.DOC", "*.EXE", "*.DOCX"],
        "correct_option_text": get_correct_text(["*.DOTX", "*.DOC", "*.EXE", "*.DOCX"], CORRECT_ANSWERS_BY_ID.get(46))
    },
    { # Q47
        "id": 47,
        "question": "Trong MS Word 2016, để chuyển con trỏ xuống phía dưới 1 trang màn hình ta dùng phím:",
        "options": ["Backspace", "Home", "Page Up", "Page Down"],
        "correct_option_text": get_correct_text(["Backspace", "Home", "Page Up", "Page Down"], CORRECT_ANSWERS_BY_ID.get(47))
    },
    { # Q48
        "id": 48,
        "question": "Trong MS Word 2016, để tìm kiếm và thay thế, ta bấm tổ hợp phím gì?",
        "options": ["Shift + F", "Ctrl + R", "Ctrl + H", "Shift + R"],
        "correct_option_text": get_correct_text(["Shift + F", "Ctrl + R", "Ctrl + H", "Shift + R"], CORRECT_ANSWERS_BY_ID.get(48))
    },
    { # Q49
        "id": 49,
        "question": "Trong soạn thảo Word, muốn tách một ô trong Table thành nhiều ô, ta thực hiện:",
        "options": ["Table -- Merge Cells", "Table -- Split Cells", "Tools -- Split Cells", "Table -- Cells"],
        "correct_option_text": get_correct_text(["Table -- Merge Cells", "Table -- Split Cells", "Tools -- Split Cells", "Table -- Cells"], CORRECT_ANSWERS_BY_ID.get(49))
    },
    { # Q50
        "id": 50,
        "question": "Các công cụ định dạng trong văn bản như: Font, Paragraph, Copy, Paste, Bullets, Numbering..., nằm ở thanh menu nào?",
        "options": ["Home", "Insert", "Page Layout", "References"],
        "correct_option_text": get_correct_text(["Home", "Insert", "Page Layout", "References"], CORRECT_ANSWERS_BY_ID.get(50))
    },
    { # Q51
        "id": 51,
        "question": "Trong MS Word 2016, để có đường gạch chân của đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": ["Ctrl + U", "Shift + U", "Alt + U", "Ctrl + B"],
        "correct_option_text": get_correct_text(["Ctrl + U", "Shift + U", "Alt + U", "Ctrl + B"], CORRECT_ANSWERS_BY_ID.get(51))
    },
    { # Q52
        "id": 52,
        "question": "Trong MS Word, để tăng cỡ chữ, ta sử dụng tổ hợp phím:",
        "options": ["Shift + ]", "Ctrl + [", "Shift + [", "Ctrl + ]"],
        "correct_option_text": get_correct_text(["Shift + ]", "Ctrl + [", "Shift + [", "Ctrl + ]"], CORRECT_ANSWERS_BY_ID.get(52))
    },
    { # Q53
        "id": 53,
        "question": "Trong MS Word, để giảm cỡ chữ, ta sử dụng tổ hợp phím",
        "options": ["Shift + ]", "Ctrl + [", "Shift + [", "Ctrl + ]"],
        "correct_option_text": get_correct_text(["Shift + ]", "Ctrl + [", "Shift + [", "Ctrl + ]"], CORRECT_ANSWERS_BY_ID.get(53))
    },
    { # Q54
        "id": 54,
        "question": "Khi soạn thảo văn bản với font: Time New Roman, ta cần sử dụng bảng mã nào để gõ được dấu tiếng Việt?",
        "options": ["TCVN 3", "Telex", "VietWare", "Unicode"],
        "correct_option_text": get_correct_text(["TCVN 3", "Telex", "VietWare", "Unicode"], CORRECT_ANSWERS_BY_ID.get(54))
    },
    { # Q55
        "id": 55,
        "question": "Trong Ms Word 2016, sau khi định dạng in nghiêng cho một đoạn văn bản, để xóa định dạng in nghiêng đó thì bấm tổ hộp phím nào?",
        "options": ["Ctrl + V", "Ctrl + S", "Ctrl + I", "Ctrl + B"],
        "correct_option_text": get_correct_text(["Ctrl + V", "Ctrl + S", "Ctrl + I", "Ctrl + B"], CORRECT_ANSWERS_BY_ID.get(55))
    },
    { # Q56
        "id": 56,
        "question": "Trong Ms Word 2016, để định dạng in đậm cho một đoạn văn bản thì bấm tổ hộp phím nào?",
        "options": ["Ctrl + V", "Ctrl + S", "Ctrl + I", "Ctrl + B"],
        "correct_option_text": get_correct_text(["Ctrl + V", "Ctrl + S", "Ctrl + I", "Ctrl + B"], CORRECT_ANSWERS_BY_ID.get(56))
    },
    { # Q57
        "id": 57,
        "question": "Trong MS Word 2016, để tạo chỉ số dưới (H2) ta dùng tổ hợp phím nào?",
        "options": ["Ctrl + =", "Ctrl + Alt + =", "Ctrl + Shift + =", "Shift + ="],
        "correct_option_text": get_correct_text(["Ctrl + =", "Ctrl + Alt + =", "Ctrl + Shift + =", "Shift + ="], CORRECT_ANSWERS_BY_ID.get(57))
    },
    { # Q58
        "id": 58,
        "question": "Để thay đổi màu ký tự trong MS Word 2016, trong menu Home, chọn vào:",
        "options": [
            "Font color và chọn màu.",
            "Text highlight color và chọn màu.",
            "Change case và chọn màu.",
            "Font và chọn màu."
        ],
        "correct_option_text": get_correct_text([
            "Font color và chọn màu.",
            "Text highlight color và chọn màu.",
            "Change case và chọn màu.",
            "Font và chọn màu."
        ], CORRECT_ANSWERS_BY_ID.get(58))
    },
    { # Q59
        "id": 59,
        "question": "Trong Word 2016, để đổi chữ thường sang chữ in hoa và ngược lại ta dùng tổ hợp phím nào?",
        "options": ["Shift + F1", "Shift + F3", "Shift + U", "Ctrl + F3"],
        "correct_option_text": get_correct_text(["Shift + F1", "Shift + F3", "Shift + U", "Ctrl + F3"], CORRECT_ANSWERS_BY_ID.get(59))
    },
    { # Q60
        "id": 60,
        "question": "Trong khi soạn thảo văn bản MS Word, nếu muốn ngắt trang (bắt buộc) ta:",
        "options": ["Ấn phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ấn tổ hợp phím Ctrl + Enter", "Word tự động không cần bấm phím"],
        "correct_option_text": get_correct_text(["Ấn phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ấn tổ hợp phím Ctrl + Enter", "Word tự động không cần bấm phím"], CORRECT_ANSWERS_BY_ID.get(60))
    },
    { # Q61
        "id": 61,
        "question": "Trong khi soạn thảo văn bản, nếu kết thúc 1 đoạn (Paragraph) và muốn sang 1 đoạn (Paragraph) mới, ta thực hiện:",
        "options": ["Ấn tổ hợp phím Ctrl - Enter", "Ấn tổ hợp phím Shift - Enter", "Ấn phím Enter", "Word tự động, không cần bấm phím"],
        "correct_option_text": get_correct_text(["Ấn tổ hợp phím Ctrl - Enter", "Ấn tổ hợp phím Shift - Enter", "Ấn phím Enter", "Word tự động, không cần bấm phím"], CORRECT_ANSWERS_BY_ID.get(61))
    },
    { # Q62
        "id": 62,
        "question": "Trong Word để xuống dòng mà không qua đoạn (paragraph) mới thì:",
        "options": ["Ấn tổ hợp phím Ctrl + Enter", "Ấn phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ấn tổ hợp phím Alt + Enter"],
        "correct_option_text": get_correct_text(["Ấn tổ hợp phím Ctrl + Enter", "Ấn phím Enter", "Ấn tổ hợp phím Shift + Enter", "Ấn tổ hợp phím Alt + Enter"], CORRECT_ANSWERS_BY_ID.get(62))
    },
    { # Q63
        "id": 63,
        "question": "Trong MS Word 2016, để canh đều hai bên đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": ["Ctrl + F", "Ctrl + C", "Shift + J", "Ctrl + J"],
        "correct_option_text": get_correct_text(["Ctrl + F", "Ctrl + C", "Shift + J", "Ctrl + J"], CORRECT_ANSWERS_BY_ID.get(63))
    },
    { # Q64
        "id": 64,
        "question": "Trong MS Word 2016, để canh trái đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": ["Ctrl + F", "Ctrl + L", "Shift + L", "Ctrl + J"],
        "correct_option_text": get_correct_text(["Ctrl + F", "Ctrl + L", "Shift + L", "Ctrl + J"], CORRECT_ANSWERS_BY_ID.get(64))
    },
    { # Q65
        "id": 65,
        "question": "Trong MS Word 2016, để canh phải đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": ["Ctrl + R", "Ctrl + L", "Shift + L", "Ctrl + J"],
        "correct_option_text": get_correct_text(["Ctrl + R", "Ctrl + L", "Shift + L", "Ctrl + J"], CORRECT_ANSWERS_BY_ID.get(65))
    },
    { # Q66
        "id": 66,
        "question": "Trong MS Word 2016, để canh giữa đoạn văn bản ta dùng tổ hợp phím nào?",
        "options": ["Ctrl + R", "Ctrl + L", "Shift + L", "Ctrl + E"],
        "correct_option_text": get_correct_text(["Ctrl + R", "Ctrl + L", "Shift + L", "Ctrl + E"], CORRECT_ANSWERS_BY_ID.get(66))
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
        "options": ["Tại menu Home chọn Table", "Tại menu Insert chọn Table", "Tại menu Insert chọn Shapes", "Tại menu Home chọn shapes"],
        "correct_option_text": get_correct_text(["Tại menu Home chọn Table", "Tại menu Insert chọn Table", "Tại menu Insert chọn Shapes", "Tại menu Home chọn shapes"], CORRECT_ANSWERS_BY_ID.get(68))
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
        "options": ["Ctrl + Home", "Ctrl + Alt + Home", "Alt + Home", "Shift + Home"],
        "correct_option_text": get_correct_text(["Ctrl + Home", "Ctrl + Alt + Home", "Alt + Home", "Shift + Home"], CORRECT_ANSWERS_BY_ID.get(70))
    },
    { # Q71
        "id": 71,
        "question": "Trong MS Word, để in văn bản, ta chọn tổ hợp phím nào sau đây:",
        "options": ["Ctrl+P", "Ctrl+Shift+P", "Ctrl+Alt+P", "Alt+P"],
        "correct_option_text": get_correct_text(["Ctrl+P", "Ctrl+Shift+P", "Ctrl+Alt+P", "Alt+P"], CORRECT_ANSWERS_BY_ID.get(71))
    },
    { # Q72
        "id": 72,
        "question": "Trong MS Word, sau khi đã chọn văn bản, ấn tổ hợp phím Ctrl + R là để:",
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
        "options": ["Ctrl + J", "Ctrl + R", "Ctrl + E", "Ctrl + L"],
        "correct_option_text": get_correct_text(["Ctrl + J", "Ctrl + R", "Ctrl + E", "Ctrl + L"], CORRECT_ANSWERS_BY_ID.get(73))
    },
    { # Q74
        "id": 74,
        "question": "Trong MS Word, sau khi đã chọn văn bản, ấn tổ hợp phím Ctrl + B là để:",
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
            "Ấn tổ hợp phím Ctrl + A",
            "Nháy chuột vào từ cần chọn",
            "Nháy chuột phải vào từ cần chọn"
        ],
        "correct_option_text": get_correct_text([
            "Nháy đúp chuột vào từ cần chọn",
            "Ấn tổ hợp phím Ctrl + A",
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
        "options": ["F5", "F2", "F7", "F3"],
        "correct_option_text": get_correct_text(["F5", "F2", "F7", "F3"], CORRECT_ANSWERS_BY_ID.get(77))
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
        "options": ["Replace All", "Replace", "Find Next", "More"],
        "correct_option_text": get_correct_text(["Replace All", "Replace", "Find Next", "More"], CORRECT_ANSWERS_BY_ID.get(79))
    },
    { # Q80
        "id": 80,
        "question": "Trong MS Word, phím Delete có chức năng:",
        "options": [
            "Xóa ký tự phía sau con trỏ soạn thảo",
            "Xóa ký tự phía trước con trỏ soạn thảo",
            "Lùi văn bản vào với một khoảng cách cố định",
            "Di chuyển con trỏ soạn thảo về đầu dòng"
        ],
        "correct_option_text": get_correct_text([
            "Xóa ký tự phía sau con trỏ soạn thảo",
            "Xóa ký tự phía trước con trỏ soạn thảo",
            "Lùi văn bản vào với một khoảng cách cố định",
            "Di chuyển con trỏ soạn thảo về đầu dòng"
        ], CORRECT_ANSWERS_BY_ID.get(80))
    },
    { # Q81
        "id": 81,
        "question": "Trong MS Word, sau khi đã chọn văn bản, ấn tổ hợp phím Ctrl + E là để:",
        "options": [
            "Canh giữa cho văn bản đã chọn",
            "Canh đều lề phải cho văn bản đã chọn",
            "Canh đều lề trái cho văn bản đã chọn",
            "Canh đều cả hai lề (trái và phải) cho văn bản đã chọn"
        ],
        "correct_option_text": get_correct_text([
            "Canh giữa cho văn bản đã chọn",
            "Canh đều lề phải cho văn bản đã chọn",
            "Canh đều lề trái cho văn bản đã chọn",
            "Canh đều cả hai lề (trái và phải) cho văn bản đã chọn"
        ], CORRECT_ANSWERS_BY_ID.get(81))
    },
    { # Q82
        "id": 82,
        "question": "Khi đang soạn thảo văn bản trong MS Word, muốn đánh dấu để chọn toàn bộ nội dung văn bản, ta thực hiện:",
        "options": [
            "Nháy đúp chuột vào từ cần chọn",
            "Ấn tổ hợp phím Ctrl + A",
            "Nháy chuột vào từ cần chọn",
            "Nháy chuột phải vào từ cần chọn"
        ],
        "correct_option_text": get_correct_text([
            "Nháy đúp chuột vào từ cần chọn",
            "Ấn tổ hợp phím Ctrl + A",
            "Nháy chuột vào từ cần chọn",
            "Nháy chuột phải vào từ cần chọn"
        ], CORRECT_ANSWERS_BY_ID.get(82))
    },
    { # Q83
        "id": 83,
        "question": "Khi đang soạn thảo văn bản trong MS Word, ấn tổ hợp phím Ctrl + F là để:",
        "options": [
            "Xuống hàng trong cùng một Paragraph",
            "Xuống hàng và tạo một Paragraph mới",
            "Tìm kiếm từ/cụm từ trong văn bản",
            "Thay thế từ/cụm từ trong văn bản"
        ],
        "correct_option_text": get_correct_text([
            "Xuống hàng trong cùng một Paragraph",
            "Xuống hàng và tạo một Paragraph mới",
            "Tìm kiếm từ/cụm từ trong văn bản",
            "Thay thế từ/cụm từ trong văn bản"
        ], CORRECT_ANSWERS_BY_ID.get(83))
    },
    { # Q84
        "id": 84,
        "question": "Trong Excel 2016, giao của một hàng và một cột được gọi là?",
        "options": ["Dữ liệu", "Ô", "Trường", "Công thức"],
        "correct_option_text": get_correct_text(["Dữ liệu", "Ô", "Trường", "Công thức"], CORRECT_ANSWERS_BY_ID.get(84))
    },
    { # Q85
        "id": 85,
        "question": "Phần mở rộng mặc định của tập tin Excel 2016 là gì?",
        "options": [".EXE", ".XLSX", ".XLS", ".EXCE"],
        "correct_option_text": get_correct_text([".EXE", ".XLSX", ".XLS", ".EXCE"], CORRECT_ANSWERS_BY_ID.get(85))
    },
    { # Q86
        "id": 86,
        "question": "Trong Excel 2016, để nhập dữ liệu sang dòng mới trong cùng một cell (ô), ta nhấn tổ hợp phím nào?",
        "options": ["Shift + Enter", "Alt + Enter", "Ctrl + Enter", "Windows + Enter"],
        "correct_option_text": get_correct_text(["Shift + Enter", "Alt + Enter", "Ctrl + Enter", "Windows + Enter"], CORRECT_ANSWERS_BY_ID.get(86))
    },
    { # Q87
        "id": 87,
        "question": "Trong Excel 2016, muốn sắp xếp danh sách dữ liệu theo thứ tự tăng (hay giảm), ta thực hiện:",
        "options": ["File / Sort", "Formulas / Sort", "Data / Sort", "View / Sort"],
        "correct_option_text": get_correct_text(["File / Sort", "Formulas / Sort", "Data / Sort", "View / Sort"], CORRECT_ANSWERS_BY_ID.get(87))
    },
    { # Q88
        "id": 88,
        "question": "Giả sử có bảng tính Excel. Cần sắp xếp Tiền lương/tháng theo thứ tự giảm dần. Trong bảng lệnh Sort, chọn các thông số nào sau đây để đảm bảo yêu cầu trên?",
        "options": [
            "Column: Sort by: ĐTB; Sort on: Values; Order: Largest to Smallest",
            "Column: Sort by: ĐTB; Sort on: Values; Order: Smallest to Largest",
            "Column: Sort by: TT; Sort on: Values; Order: Smallest to Largest",
            "Column: Sort by: Tên; Sort on: Values; Order: Z to A"
        ],
        "correct_option_text": get_correct_text([
            "Column: Sort by: ĐTB; Sort on: Values; Order: Largest to Smallest",
            "Column: Sort by: ĐTB; Sort on: Values; Order: Smallest to Largest",
            "Column: Sort by: TT; Sort on: Values; Order: Smallest to Largest",
            "Column: Sort by: Tên; Sort on: Values; Order: Z to A"
        ], CORRECT_ANSWERS_BY_ID.get(88))
    },
    { # Q89
        "id": 89,
        "question": "Giả sử có bảng tính Excel. Cần sắp xếp cột Tên theo thứ tự tăng dần (theo thứ tự bảng chữ cái A, B, C,..). Trong bảng lệnh Sort, chọn các thông số nào sau đây để đảm bảo yêu cầu trên?",
        "options": [
            "Column: Sort by: ĐTB; Sort on: Values; Order: Largest to Smallest",
            "Column: Sort by: Tên; Sort on: Values; Order: A to Z",
            "Column: Sort by: TT; Sort on: Values; Order: Smallest to Largest",
            "Column: Sort by: Tên; Sort on: Values; Order: Z to A"
        ],
        "correct_option_text": get_correct_text([
            "Column: Sort by: ĐTB; Sort on: Values; Order: Largest to Smallest",
            "Column: Sort by: Tên; Sort on: Values; Order: A to Z",
            "Column: Sort by: TT; Sort on: Values; Order: Smallest to Largest",
            "Column: Sort by: Tên; Sort on: Values; Order: Z to A"
        ], CORRECT_ANSWERS_BY_ID.get(89))
    },
    { # Q90
        "id": 90,
        "question": "Trong Excel 2016, cho biết kết quả của công thức =AVERAGE(\"AB\";10;15) là gì?",
        "options": ["FALSE", "#VALUE!", "6", "4"],
        "correct_option_text": get_correct_text(["FALSE", "#VALUE!", "6", "4"], CORRECT_ANSWERS_BY_ID.get(90))
    },
    { # Q91
        "id": 91,
        "question": "Trong Excel 2016, cho biết kết quả của công thức =AVERAGE(20;10;15) là gì?",
        "options": ["15", "#VALUE!", "45", "20"],
        "correct_option_text": get_correct_text(["15", "#VALUE!", "45", "20"], CORRECT_ANSWERS_BY_ID.get(91))
    },
    { # Q92
        "id": 92,
        "question": "Trong Excel 2016, cho biết kết quả của công thức =ROUND(10,5534; 1) là:",
        "options": ["10,6", "#VALUE!", "10,5", "10,0"],
        "correct_option_text": get_correct_text(["10,6", "#VALUE!", "10,5", "10,0"], CORRECT_ANSWERS_BY_ID.get(92))
    },
    { # Q93
        "id": 93,
        "question": "Trong Excel 2016, cho biết kết quả của công thức =ROUND(10,69; -1) là:",
        "options": ["10,0", "10,6", "10,7", "11,0"],
        "correct_option_text": get_correct_text(["10,0", "10,6", "10,7", "11,0"], CORRECT_ANSWERS_BY_ID.get(93))
    },
    { # Q94
        "id": 94,
        "question": "Trong Excel 2016, cho biết kết quả của công thức =ROUND(15,445; -1) là:",
        "options": ["20,0", "16,0", "15,5", "15,0"],
        "correct_option_text": get_correct_text(["20,0", "16,0", "15,5", "15,0"], CORRECT_ANSWERS_BY_ID.get(94))
    },
    { # Q95
        "id": 95,
        "question": "Trong Excel 2016, tại ô A2 có sẵn giá trị 0 (số không); Tại ô C2 gõ vào công thức =B2/A2 thì nhận được kết quả:",
        "options": ["0", "#DIV/0!", "5", "#VALUE!"],
        "correct_option_text": get_correct_text(["0", "#DIV/0!", "5", "#VALUE!"], CORRECT_ANSWERS_BY_ID.get(95))
    },
    { # Q96
        "id": 96,
        "question": "Giả sử có dữ liệu bảng tính Excel. Nếu xóa cột C, thì các ô D2, D3 sẽ có kết quả như thế nào?",
        "options": ["#REF!", "FALSE", "#VALUE!", "#NAME?"],
        "correct_option_text": get_correct_text(["#REF!", "FALSE", "#VALUE!", "#NAME?"], CORRECT_ANSWERS_BY_ID.get(96))
    },
    { # Q97
        "id": 97,
        "question": "Giả sử có dữ liệu bảng tính Excel. Tại ô C5, nhập công thức =AVRAGE(C2:C4), xuất hiện kết quả là chuỗi kí tự #NAME? Hãy giải thích vì sao?",
        "options": [
            "Sai tên hàm",
            "Sai địa chỉ ô",
            "Sai cú pháp",
            "Dữ liệu trong khối ô không phù hợp"
        ],
        "correct_option_text": get_correct_text([
            "Sai tên hàm",
            "Sai địa chỉ ô",
            "Sai cú pháp",
            "Dữ liệu trong khối ô không phù hợp"
        ], CORRECT_ANSWERS_BY_ID.get(97))
    },
    { # Q98
        "id": 98,
        "question": "Trong Excel 2016, tại ô A1 chứa công thức =SUM(B5:B7), ô nào sau đây chứa công thức =SUM(C6:C8) khi thực hiện sao chép công thức từ ô A1 qua?",
        "options": ["A2", "B2", "C2", "B1"],
        "correct_option_text": get_correct_text(["A2", "B2", "C2", "B1"], CORRECT_ANSWERS_BY_ID.get(98))
    },
    { # Q99
        "id": 99,
        "question": "Trong Excel có nhiều cột, nhiều dòng. Các cột được ký hiệu theo bảng chữ cái. Vậy cột liền sau cột Z có tên là:",
        "options": ["Z1", "A1", "AB", "AA"],
        "correct_option_text": get_correct_text(["Z1", "A1", "AB", "AA"], CORRECT_ANSWERS_BY_ID.get(99))
    },
    { # Q100
        "id": 100,
        "question": "Trong Excel 2016, khi click vào một ô và nhấn F2 có nghĩa là gì?",
        "options": ["Định dạng ô", "Cho phép sửa nội dung ô đó", "Chọn dữ liệu trong ô để thao tác", "Chèn vào một ô bên trái ô đã chọn"],
        "correct_option_text": get_correct_text(["Định dạng ô", "Cho phép sửa nội dung ô đó", "Chọn dữ liệu trong ô để thao tác", "Chèn vào một ô bên trái ô đã chọn"], CORRECT_ANSWERS_BY_ID.get(100))
    },
    { # Q101
        "id": 101,
        "question": "Trong Excel 2016, chức năng Format Painter trong Excel dùng để làm:",
        "options": ["Copy vùng dữ liệu", "Sao chép định dạng", "Canh trái dữ liệu", "Paste vùng dữ liệu"],
        "correct_option_text": get_correct_text(["Copy vùng dữ liệu", "Sao chép định dạng", "Canh trái dữ liệu", "Paste vùng dữ liệu"], CORRECT_ANSWERS_BY_ID.get(101))
    },
    { # Q102
        "id": 102,
        "question": "Muốn biết trong bảng tính của Excel có bao nhiêu hàng/cột, ta thực hiện:",
        "options": [
            "Di chuyển đến hàng/cột cuối cùng",
            "Có vô số cột, không có cột cuối cùng",
            "Nhấp giữ chuột tại ô vuông giao nhau giữa tên hàng và tên cột",
            "Bôi đen chọn tất cả hàng/cột"
        ],
        "correct_option_text": get_correct_text([
            "Di chuyển đến hàng/cột cuối cùng",
            "Có vô số cột, không có cột cuối cùng",
            "Nhấp giữ chuột tại ô vuông giao nhau giữa tên hàng và tên cột",
            "Bôi đen chọn tất cả hàng/cột"
        ], CORRECT_ANSWERS_BY_ID.get(102))
    },
    { # Q103
        "id": 103,
        "question": "Trong Excel 2016, để gộp nhiều ô thành 1 ô, ta dùng:",
        "options": ["File/Merge & Center", "Insert/Merge & Center", "Home/Merge & Center", "View/Merge & Center"],
        "correct_option_text": get_correct_text(["File/Merge & Center", "Insert/Merge & Center", "Home/Merge & Center", "View/Merge & Center"], CORRECT_ANSWERS_BY_ID.get(103))
    },
    { # Q104
        "id": 104,
        "question": "Trong Excel 2016, tại ô A2 có sẵn giá trị số 25; Tại ô B2 gõ vào công thức =SQRT(A2) thì nhận được kết quả:",
        "options": ["0", "5", "#VALUE!", "#NAME?"],
        "correct_option_text": get_correct_text(["0", "5", "#VALUE!", "#NAME?"], CORRECT_ANSWERS_BY_ID.get(104))
    },
    { # Q105
        "id": 105,
        "question": "Trong Excel 2016, khi ta nhập công thức sau: = LEN(\"ABCDEF\"), kết quả sẽ là:",
        "options": ["9", "7", "6", "8"],
        "correct_option_text": get_correct_text(["9", "7", "6", "8"], CORRECT_ANSWERS_BY_ID.get(105))
    },
    { # Q106
        "id": 106,
        "question": "Trong Excel 2016, công thức = AND(1<3; 5>7) cho kết quả nào?",
        "options": ["TRUE", "1>3", "5>7", "FALSE"],
        "correct_option_text": get_correct_text(["TRUE", "1>3", "5>7", "FALSE"], CORRECT_ANSWERS_BY_ID.get(106))
    },
    { # Q107
        "id": 107,
        "question": "Trong Excel 2016, khi nhập công thức =MOD(12; 24) thì kết quả là bao nhiêu?",
        "options": ["2", "12", "24", "#NAME?"],
        "correct_option_text": get_correct_text(["2", "12", "24", "#NAME?"], CORRECT_ANSWERS_BY_ID.get(107))
    },
    { # Q108
        "id": 108,
        "question": "Trong MS Excel, muốn xóa hàng hay cột trên bảng tính thực hiện:",
        "options": [
            "Nhấp chuột phải vào tên hàng hoặc tên cột cần xóa, chọn Delete",
            "Nhấp chuột vào tên hàng hoặc tên cột cần xóa, nhấn phím Delete",
            "Nhấp chuột vào tên hàng hoặc tên cột cần xóa, chọn Edit / Delete",
            "Click chuột phải, chọn Clear"
        ],
        "correct_option_text": get_correct_text([
            "Nhấp chuột phải vào tên hàng hoặc tên cột cần xóa, chọn Delete",
            "Nhấp chuột vào tên hàng hoặc tên cột cần xóa, nhấn phím Delete",
            "Nhấp chuột vào tên hàng hoặc tên cột cần xóa, chọn Edit / Delete",
            "Click chuột phải, chọn Clear"
        ], CORRECT_ANSWERS_BY_ID.get(108))
    },
    { # Q109
        "id": 109,
        "question": "Trong MS Excel, các ký tự nào sau đây là một địa chỉ tuyệt đối của khối ô?",
        "options": ["$B$1:$C$5", "B1:C5", "$B1:$C5", "B$1:C$5"],
        "correct_option_text": get_correct_text(["$B$1:$C$5", "B1:C5", "$B1:$C5", "B$1:C$5"], CORRECT_ANSWERS_BY_ID.get(109))
    },
    { # Q110
        "id": 110,
        "question": "Trong MS Excel, để chọn các ô liền kề nhau, khi click chuột, ta ấn giữ phím nào?",
        "options": ["Ctrl", "Alt", "Shift", "Tab"],
        "correct_option_text": get_correct_text(["Ctrl", "Alt", "Shift", "Tab"], CORRECT_ANSWERS_BY_ID.get(110))
    },
    { # Q111
        "id": 111,
        "question": "Trong MS Excel, để chọn các ô không liền kề nhau, khi click chuột, ta ấn giữ phím nào?",
        "options": ["Ctrl", "Alt", "Shift", "Tab"],
        "correct_option_text": get_correct_text(["Ctrl", "Alt", "Shift", "Tab"], CORRECT_ANSWERS_BY_ID.get(111))
    },
    { # Q112
        "id": 112,
        "question": "Trong MS Excel, để tính tổng giá trị cho 06 ô (từ A1 đến A3 và từ B1 đến B3), thì công thức nào sau đâu là đúng:",
        "options": ["=(A1:A3) + (B1:B3)", "=(A1+A3+B1+B3)", "=SUM(A1:B3)", "=SUM(A1..A3; B1..B3)"],
        "correct_option_text": get_correct_text(["=(A1:A3) + (B1:B3)", "=(A1+A3+B1+B3)", "=SUM(A1:B3)", "=SUM(A1..A3; B1..B3)"], CORRECT_ANSWERS_BY_ID.get(112))
    },
    { # Q113
        "id": 113,
        "question": "Giả sử ta có bảng tính trong Excel bao gồm các dữ liệu như sau (trong đó: các ô A1, B1, E1 chứa dữ diệu số). Hãy cho biết kết quả của ô A2 khi nhập công thức =COUNT(A1:E1)?",
        "options": ["5", "35", "3", "#VALUE!"],
        "correct_option_text": get_correct_text(["5", "35", "3", "#VALUE!"], CORRECT_ANSWERS_BY_ID.get(113))
    },
    { # Q114
        "id": 114,
        "question": "Giả sử ta có bảng tính trong Excel bao gồm các dữ liệu như sau (trong đó: các ô A1, B1, E1 chứa dữ diệu số). Hãy cho biết kết quả của ô A2 khi nhập công thức =COUNTA(A1:E1)?",
        "options": ["5", "35", "3", "#VALUE!"],
        "correct_option_text": get_correct_text(["5", "35", "3", "#VALUE!"], CORRECT_ANSWERS_BY_ID.get(114))
    },
    { # Q115
        "id": 115,
        "question": "Trong MS Excel, để tìm giá trị nhỏ nhất của 05 ô liền kề (từ A1 đến A5), tại ô A6 ta nhập công thức:",
        "options": ["=MAX(A1:A5)", "=SUM(A1:A5)", "=MIN(A1:A5)", "=COUNT(A1:A5)"],
        "correct_option_text": get_correct_text(["=MAX(A1:A5)", "=SUM(A1:A5)", "=MIN(A1:A5)", "=COUNT(A1:A5)"], CORRECT_ANSWERS_BY_ID.get(115))
    },
    { # Q116
        "id": 116,
        "question": "Trong MS Excel, các ký tự nào sau đây là địa chỉ hỗn hợp của khối ô?",
        "options": ["F1:F2", "B1:D10", "C$2:$C5", "$A$1:$A$10"],
        "correct_option_text": get_correct_text(["F1:F2", "B1:D10", "C$2:$C5", "$A$1:$A$10"], CORRECT_ANSWERS_BY_ID.get(116))
    },
    { # Q117
        "id": 117,
        "question": "Trong bảng tính Excel, ô A1 chứa nội dung \"giáo dục\". Khi thực hiện công thức = LEN(A1) thì giá trị trả về kết quả:",
        "options": ["8", "9", "7", "10"],
        "correct_option_text": get_correct_text(["8", "9", "7", "10"], CORRECT_ANSWERS_BY_ID.get(117))
    },
    { # Q118
        "id": 118,
        "question": "Trong MS Excel, địa chỉ của ô giao nhau giữa hàng thứ 5 và cột thứ 3 là:",
        "options": ["J2", "5C", "2J", "C5"],
        "correct_option_text": get_correct_text(["J2", "5C", "2J", "C5"], CORRECT_ANSWERS_BY_ID.get(118))
    },
    { # Q119
        "id": 119,
        "question": "Trong bảng tính Excel, hàm nào sau đây dùng để tìm kiếm giá trị theo hàng:",
        "options": ["HLOOKUP", "IF", "LEFT", "SUM"],
        "correct_option_text": get_correct_text(["HLOOKUP", "IF", "LEFT", "SUM"], CORRECT_ANSWERS_BY_ID.get(119))
    },
    { # Q120
        "id": 120,
        "question": "Trong MS Excel, muốn ẩn một cột ta thực hiện:",
        "options": [
            "Kích chuột phải lên tên cột cần ẩn, sau đó chọn Hide",
            "Kích chuột phải vào ô bất kỳ trong cột cần ẩn, sau đó chọn Hide",
            "Kích chuột phải lên tên cột cần ẩn, sau đó chọn Delete",
            "Kích chuột phải vào ô bất kỳ trong cột cần ẩn, sau đó chọn Delete"
        ],
        "correct_option_text": get_correct_text([
            "Kích chuột phải lên tên cột cần ẩn, sau đó chọn Hide",
            "Kích chuột phải vào ô bất kỳ trong cột cần ẩn, sau đó chọn Hide",
            "Kích chuột phải lên tên cột cần ẩn, sau đó chọn Delete",
            "Kích chuột phải vào ô bất kỳ trong cột cần ẩn, sau đó chọn Delete"
        ], CORRECT_ANSWERS_BY_ID.get(120))
    },
    { # Q121
        "id": 121,
        "question": "Giả sử ta có bảng tính trong Excel bao gồm các dữ liệu như sau (trong đó: các ô A1, B1, E1 chứa dữ diệu số). Hãy cho biết kết quả của ô A2 khi nhập công thức =SUM(A1:E1)?",
        "options": ["3", "2049", "5", "#VALUE!"],
        "correct_option_text": get_correct_text(["3", "2049", "5", "#VALUE!"], CORRECT_ANSWERS_BY_ID.get(121))
    },
    { # Q122
        "id": 122,
        "question": "Trong PowerPoint 2016, để tạo một slide giống slide hiện hành mà không phải thiết kế lại, ta thực hiện thao tác chọn Slide hiện hành:",
        "options": [
            "Nhấp chuột phải, chọn Duplicate",
            "Nhấp chuột phải, chọn New Slide",
            "Nhấp chuột phải, chọn Duplicate Slide",
            "Nhấp chuột phải, chọn Insert Slide"
        ],
        "correct_option_text": get_correct_text([
            "Nhấp chuột phải, chọn Duplicate",
            "Nhấp chuột phải, chọn New Slide",
            "Nhấp chuột phải, chọn Duplicate Slide",
            "Nhấp chuột phải, chọn Insert Slide"
        ], CORRECT_ANSWERS_BY_ID.get(122))
    },
    { # Q123
        "id": 123,
        "question": "Trong PowerPoint 2016, để thay đổi màu nền cho một slide trong bài trình chiếu ta thực hiện:",
        "options": ["Chọn Home / Format Background", "Chọn Insert / Format Background", "Chọn View / Format Background", "Chọn Design / Format Background"],
        "correct_option_text": get_correct_text(["Chọn Home / Format Background", "Chọn Insert / Format Background", "Chọn View / Format Background", "Chọn Design / Format Background"], CORRECT_ANSWERS_BY_ID.get(123))
    },
    { # Q124
        "id": 124,
        "question": "Trong PowerPoint 2016, để dùng hình ảnh (có trên máy) làm hình nền cho một slide, ta thực hiện: Click chuột phải vào slide, chọn Format Background, sau đó chọn:",
        "options": ["Solid Fill", "Gradient Fill", "Picture and Texture Fill", "Pattern Fill"],
        "correct_option_text": get_correct_text(["Solid Fill", "Gradient Fill", "Picture and Texture Fill", "Pattern Fill"], CORRECT_ANSWERS_BY_ID.get(124))
    },
    { # Q125
        "id": 125,
        "question": "Trong PowerPoint 2016, muốn thay đổi mẫu thiết kế (Theme) của Slide, ta sử dụng menu nào?",
        "options": ["Transitions", "Design", "Home", "Animations"],
        "correct_option_text": get_correct_text(["Transitions", "Design", "Home", "Animations"], CORRECT_ANSWERS_BY_ID.get(125))
    },
    { # Q126
        "id": 126,
        "question": "PowerPoint 2016 cho phép người sử dụng thiết kế một slide chủ chứa các định dạng chung của toàn bộ các slide trong bài trình diễn. Để thực hiện điều này, ta chọn:",
        "options": ["Insert / Slide Master", "Insert / Slide Formatter", "View / Slide Master", "View / Slide Formatter"],
        "correct_option_text": get_correct_text(["Insert / Slide Master", "Insert / Slide Formatter", "View / Slide Master", "View / Slide Formatter"], CORRECT_ANSWERS_BY_ID.get(126))
    },
    { # Q127
        "id": 127,
        "question": "Trong PowerPoint 2016, muốn áp dụng một chủ đề thiết kế (theme) có sẵn vào bài trình chiếu ta chọn:",
        "options": ["Design / Themes", "Insert / Themes", "View / Themes", "Home / Themes"],
        "correct_option_text": get_correct_text(["Design / Themes", "Insert / Themes", "View / Themes", "Home / Themes"], CORRECT_ANSWERS_BY_ID.get(127))
    },
    { # Q128
        "id": 128,
        "question": "Trong PowerPoint 2016, muốn ẩn một silde nào đó trong bài trình chiếu, ta thực hiện:",
        "options": ["Home / Hide Slide", "Edit / Hide Slide", "Design / Hide Slide", "Slide Show / Hide Slide"],
        "correct_option_text": get_correct_text(["Home / Hide Slide", "Edit / Hide Slide", "Design / Hide Slide", "Slide Show / Hide Slide"], CORRECT_ANSWERS_BY_ID.get(128))
    },
    { # Q129
        "id": 129,
        "question": "Trong PowerPoint 2016, đang trình chiếu một bài trình diễn, muốn dừng trình diễn ta bấm phím:",
        "options": ["Tab", "Esc", "Home", "End"],
        "correct_option_text": get_correct_text(["Tab", "Esc", "Home", "End"], CORRECT_ANSWERS_BY_ID.get(129))
    },
    { # Q130
        "id": 130,
        "question": "Trong MS PowerPoint, để thay đổi bố cục cho một slide, ta kích chuột phải vào slide và chọn:",
        "options": ["Layout", "Slide Master", "Reset Slide", "Format Background"],
        "correct_option_text": get_correct_text(["Layout", "Slide Master", "Reset Slide", "Format Background"], CORRECT_ANSWERS_BY_ID.get(130))
    },
    { # Q131
        "id": 131,
        "question": "Trong MS PowerPoint, tại Slide hiện hành ta kích chuột phải chọn New Slide là để:",
        "options": [
            "Chèn thêm một slide mới vào ngay sau slide hiện hành",
            "Chèn thêm một slide mới vào ngay trước slide hiện hành",
            "Chèn thêm một slide mới vào ngay trước slide đầu tiên",
            "Chèn thêm một slide mới vào ngay sau slide cuối cùng"
        ],
        "correct_option_text": get_correct_text([
            "Chèn thêm một slide mới vào ngay sau slide hiện hành",
            "Chèn thêm một slide mới vào ngay trước slide hiện hành",
            "Chèn thêm một slide mới vào ngay trước slide đầu tiên",
            "Chèn thêm một slide mới vào ngay sau slide cuối cùng"
        ], CORRECT_ANSWERS_BY_ID.get(131))
    },
    { # Q132
        "id": 132,
        "question": "Trong PowerPoint, để vẽ một biểu đồ, trước tiên ta cần phải có?",
        "options": ["Bảng số liệu", "Một slide trống", "Các dạng biểu đồ", "Biểu đồ để so sánh"],
        "correct_option_text": get_correct_text(["Bảng số liệu", "Một slide trống", "Các dạng biểu đồ", "Biểu đồ để so sánh"], CORRECT_ANSWERS_BY_ID.get(132))
    },
    { # Q133
        "id": 133,
        "question": "Trong MS PowerPoint, dùng phím tắt gì để tạo mới một bài trình chiếu (Presentation)?",
        "options": ["Ctrl + N", "Ctrl + M", "Ctrl + O", "Ctrl + P"],
        "correct_option_text": get_correct_text(["Ctrl + N", "Ctrl + M", "Ctrl + O", "Ctrl + P"], CORRECT_ANSWERS_BY_ID.get(133))
    },
    { # Q134
        "id": 134,
        "question": "Trong MS PowerPoint, để thực hiện trình chiếu (slide show) bài thuyết trình từ Slide đầu tiên, ta ấn phím:",
        "options": ["F5", "F12", "F2", "F4"],
        "correct_option_text": get_correct_text(["F5", "F12", "F2", "F4"], CORRECT_ANSWERS_BY_ID.get(134))
    },
    { # Q135
        "id": 135,
        "question": "Trong MS PowerPoint, để định dạng nền trang chiếu, nhấp chuột phải vào Slide, chọn:",
        "options": ["Format Background", "Layout", "Duplicate Slide", "Color Slide"],
        "correct_option_text": get_correct_text(["Format Background", "Layout", "Duplicate Slide", "Color Slide"], CORRECT_ANSWERS_BY_ID.get(135))
    },
    { # Q136
        "id": 136,
        "question": "Trong PowerPoint 2016, để trình chiếu từ slide hiện tại trở đi, ta nhấn phím hay tổ hợp phím nào?",
        "options": ["Phím F5", "Ctrl + F5", "Shift + F5", "Alt + F5"],
        "correct_option_text": get_correct_text(["Phím F5", "Ctrl + F5", "Shift + F5", "Alt + F5"], CORRECT_ANSWERS_BY_ID.get(136))
    },
    { # Q137
        "id": 137,
        "question": "Trong PowerPoint 2016, muốn chèn thêm một dòng mới bên dưới dòng đang chọn, ta chọn:",
        "options": ["Layout / Insert Row", "Layout / Insert Below", "Design / Insert Row", "Design / Insert Below"],
        "correct_option_text": get_correct_text(["Layout / Insert Row", "Layout / Insert Below", "Design / Insert Row", "Design / Insert Below"], CORRECT_ANSWERS_BY_ID.get(137))
    },
    { # Q138
        "id": 138,
        "question": "Trong PowerPoint 2016, muốn chèn thêm một cột mới bên trái cột đang chọn, ta chọn:",
        "options": ["Layout / Insert Left", "Layout / Insert Column", "Design / Insert Left", "Design / Insert Column"],
        "correct_option_text": get_correct_text(["Layout / Insert Left", "Layout / Insert Column", "Design / Insert Left", "Design / Insert Column"], CORRECT_ANSWERS_BY_ID.get(138))
    },
    { # Q139
        "id": 139,
        "question": "Trong PowerPoint 2016, giả sử con trỏ soạn thảo đang đặt ở ô cuối cùng trong một bảng, nếu ấn phím Tab sẽ thực hiện việc gì?",
        "options": [
            "Con trỏ chuột nhảy về ô đầu tiên",
            "Con trỏ chuột không nhúc nhích",
            "Thêm một dòng mới",
            "Thêm một cột mới"
        ],
        "correct_option_text": get_correct_text([
            "Con trỏ chuột nhảy về ô đầu tiên",
            "Con trỏ chuột không nhúc nhích",
            "Thêm một dòng mới",
            "Thêm một cột mới"
        ], CORRECT_ANSWERS_BY_ID.get(139))
    },
    { # Q140
        "id": 140,
        "question": "Trong PowerPoint 2016, để di chuyển con trỏ đến một ô kế tiếp trong bảng, ta nhấn phím:",
        "options": ["Tab", "Shift + Tab", "Backspace", "Enter"],
        "correct_option_text": get_correct_text(["Tab", "Shift + Tab", "Backspace", "Enter"], CORRECT_ANSWERS_BY_ID.get(140))
    },
    { # Q141
        "id": 141,
        "question": "Trong PowerPoint 2016, để di chuyển con trỏ soạn thảo về ô liền kề trước đó, ta nhấn phím:",
        "options": ["Tab", "Shift + Tab", "Backspace", "Enter"],
        "correct_option_text": get_correct_text(["Tab", "Shift + Tab", "Backspace", "Enter"], CORRECT_ANSWERS_BY_ID.get(141))
    },
    { # Q142
        "id": 142,
        "question": "Trong PowerPoint 2016, muốn làm cho các cột trong bảng có độ rộng bằng nhau, ta chọn các cột, sau đó vào menu Layout chọn:",
        "options": ["Distribute Rows", "Distribute Columns", "Justify Rows", "Justify Columns"],
        "correct_option_text": get_correct_text(["Distribute Rows", "Distribute Columns", "Justify Rows", "Justify Columns"], CORRECT_ANSWERS_BY_ID.get(142))
    },
    { # Q143
        "id": 143,
        "question": "Trong PowerPoint 2016, muốn ghép hai ô trong bảng lại với nhau, ta chọn hai ô tương ứng rồi vào menu Layout chọn:",
        "options": ["Group Cells", "Merge Cells", "Join Cells", "Split Cells"],
        "correct_option_text": get_correct_text(["Group Cells", "Merge Cells", "Join Cells", "Split Cells"], CORRECT_ANSWERS_BY_ID.get(143))
    },
    { # Q144
        "id": 144,
        "question": "Trong PowerPoint 2016, để điều chỉnh chiều, hướng kí tự trong một ô của bảng, ta chọn ô đó, chọn Layout và chọn:",
        "options": ["Change Text Display", "Distribute Text", "Text Bottom Up", "Text Direction"],
        "correct_option_text": get_correct_text(["Change Text Display", "Distribute Text", "Text Bottom Up", "Text Direction"], CORRECT_ANSWERS_BY_ID.get(144))
    },
    { # Q145
        "id": 145,
        "question": "Trong PowerPoint 2016, muốn thay đổi độ rộng của cột trong bảng, ta thực hiện:",
        "options": [
            "Nhấp chuột vào cột, rồi nhập độ rộng cho cột",
            "Trỏ chuột tại đường biên của cột, khi có mũi tên 2 chiều, rê chuột để thay đổi độ rộng",
            "Trỏ chuột tại đường biên của cột, kéo chuột đến vị trí mới để thay đổi độ rộng",
            "Trỏ chuột tại đường biên xung quanh, khi có mũi tên 2 chiều, rê chuột để thay đổi độ rộng"
        ],
        "correct_option_text": get_correct_text([
            "Nhấp chuột vào cột, rồi nhập độ rộng cho cột",
            "Trỏ chuột tại đường biên của cột, khi có mũi tên 2 chiều, rê chuột để thay đổi độ rộng",
            "Trỏ chuột tại đường biên của cột, kéo chuột đến vị trí mới để thay đổi độ rộng",
            "Trỏ chuột tại đường biên xung quanh, khi có mũi tên 2 chiều, rê chuột để thay đổi độ rộng"
        ], CORRECT_ANSWERS_BY_ID.get(145))
    },
    { # Q146
        "id": 146,
        "question": "Trong PowerPoint 2016, muốn đánh dấu chọn cả một dòng của bảng, ta thực hiện:",
        "options": [
            "Nhấp chuột vào ô đầu tiên của dòng cần chọn",
            "Trỏ chuột vào ô đầu tiên của dòng, khi con trỏ chuột có hình mũi tên màu trắng rồi nhấp chuột",
            "Trỏ chuột vào phía trước ô đầu tiên của dòng, khi con trỏ chuột có hình mũi tên màu đen rồi nhấp chuột",
            "Nhấp chuột phải tại dòng cần đánh dấu, chọn Select Rows"
        ],
        "correct_option_text": get_correct_text([
            "Nhấp chuột vào ô đầu tiên của dòng cần chọn",
            "Trỏ chuột vào ô đầu tiên của dòng, khi con trỏ chuột có hình mũi tên màu trắng rồi nhấp chuột",
            "Trỏ chuột vào phía trước ô đầu tiên của dòng, khi con trỏ chuột có hình mũi tên màu đen rồi nhấp chuột",
            "Nhấp chuột phải tại dòng cần đánh dấu, chọn Select Rows"
        ], CORRECT_ANSWERS_BY_ID.get(146))
    },
    { # Q147
        "id": 147,
        "question": "Trong PowerPoint 2016, để vẽ một biểu đồ, trước tiên ta cần phải có?",
        "options": ["Một slide trống", "Các dạng biểu đồ", "Bảng số liệu", "Biểu đồ để so sánh"],
        "correct_option_text": get_correct_text(["Một slide trống", "Các dạng biểu đồ", "Bảng số liệu", "Biểu đồ để so sánh"], CORRECT_ANSWERS_BY_ID.get(147))
    },
    { # Q148
        "id": 148,
        "question": "Trong PowerPoint 2016, để thay đổi dữ liệu cho một biểu đồ, ta chọn biểu đồ đó và chọn:",
        "options": ["Layout/Edit Data", "Design/Edit Data", "Home/Edit Data", "Chart/Edit Data"],
        "correct_option_text": get_correct_text(["Layout/Edit Data", "Design/Edit Data", "Home/Edit Data", "Chart/Edit Data"], CORRECT_ANSWERS_BY_ID.get(148))
    },
    { # Q149
        "id": 149,
        "question": "Trong PowerPoint 2016, để thay đổi dạng loại biểu đồ, ta nhấp chuột vào biểu đồ rồi chọn:",
        "options": ["Edit/Change Chart Type", "Layout/Change Chart Type", "Design/Change Chart Type", "Chart/Change Chart Type"],
        "correct_option_text": get_correct_text(["Edit/Change Chart Type", "Layout/Change Chart Type", "Design/Change Chart Type", "Chart/Change Chart Type"], CORRECT_ANSWERS_BY_ID.get(149))
    },
    { # Q150
        "id": 150,
        "question": "Trong PowerPoint 2016, để thay đổi màu cho các thành phần trên biểu đồ, ta nhấp vào phần cần thay đổi màu rồi chọn:",
        "options": ["Design / Shape Fill", "Format / Shape Fill", "Layout / Shape Fill", "View / Shape Fill"],
        "correct_option_text": get_correct_text(["Design / Shape Fill", "Format / Shape Fill", "Layout / Shape Fill", "View / Shape Fill"], CORRECT_ANSWERS_BY_ID.get(150))
    },
    { # Q151
        "id": 151,
        "question": "Trong PowerPoint 2016, để ghi số liệu lên biểu đồ, ta nhấp chuột vào biểu đồ rồi chọn:",
        "options": [
            "Insert / Add Chart Element / Data Labels",
            "Design / Add Chart Element / Data Labels",
            "Layout / Add Chart Element / Data Labels",
            "Format / Add Chart Element / Data Labels"
        ],
        "correct_option_text": get_correct_text([
            "Insert / Add Chart Element / Data Labels",
            "Design / Add Chart Element / Data Labels",
            "Layout / Add Chart Element / Data Labels",
            "Format / Add Chart Element / Data Labels"
        ], CORRECT_ANSWERS_BY_ID.get(151))
    },
    { # Q152
        "id": 152,
        "question": "Trong PowerPoint 2016, để vẽ một sơ đồ tổ chức, ta chọn:",
        "options": ["Insert / Smart", "Insert / SmartArt", "Insert / Shape / SmartArt", "Design / SmartArt"],
        "correct_option_text": get_correct_text(["Insert / Smart", "Insert / SmartArt", "Insert / Shape / SmartArt", "Design / SmartArt"], CORRECT_ANSWERS_BY_ID.get(152))
    },
    { # Q153
        "id": 153,
        "question": "Trong PowerPoint 2016, sau khi vẽ một sơ đồ tổ chức, muốn thay đổi một đối tượng xuống cấp thấp hơn, ta chọn thành phần trong bảng danh sách, rồi nhấn phím:",
        "options": ["Ctrl", "Tab", "Shift + Tab", "Ctrl + Tab"],
        "correct_option_text": get_correct_text(["Ctrl", "Tab", "Shift + Tab", "Ctrl + Tab"], CORRECT_ANSWERS_BY_ID.get(153))
    },
    { # Q154
        "id": 154,
        "question": "Trong PowerPoint 2016, sau khi vẽ một sơ đồ tổ chức, muốn thay đổi thành một dạng sơ đồ khác, ta nhấp chuột vào sơ đồ rồi chọn ở mục Smart Tools:",
        "options": ["Design / Add Shape", "Design / Layouts", "Insert / Change", "Format / Change Shape"],
        "correct_option_text": get_correct_text(["Design / Add Shape", "Design / Layouts", "Insert / Change", "Format / Change Shape"], CORRECT_ANSWERS_BY_ID.get(154))
    },
    { # Q155
        "id": 155,
        "question": "Trong PowerPoint 2016, để chèn một hình ảnh có sẵn vào trong Slide, ta thực hiện:",
        "options": ["Home / Picture", "Insert / Picture / From File", "Insert / Picture", "Insert / Picture and Clip Art"],
        "correct_option_text": get_correct_text(["Home / Picture", "Insert / Picture / From File", "Insert / Picture", "Insert / Picture and Clip Art"], CORRECT_ANSWERS_BY_ID.get(155))
    },
    { # Q156
        "id": 156,
        "question": "Trong PowerPoint 2016, để tạo một hình tròn trên Slide, ta thực hiện:",
        "options": ["Home/Shapes", "Insert/Shapes", "Design/Shapes", "View/Shapes"],
        "correct_option_text": get_correct_text(["Home/Shapes", "Insert/Shapes", "Design/Shapes", "View/Shapes"], CORRECT_ANSWERS_BY_ID.get(156))
    },
    { # Q157
        "id": 157,
        "question": "Trong PowerPoint 2016, muốn thay đổi màu nền cho một hình (shape), ta nhấp chuột vào đối tượng đó rồi chọn:",
        "options": ["Home/Shape Fill", "Format/Shape Fill", "Design/Shape Fill", "Layout/Shape Fill"],
        "correct_option_text": get_correct_text(["Home/Shape Fill", "Format/Shape Fill", "Design/Shape Fill", "Layout/Shape Fill"], CORRECT_ANSWERS_BY_ID.get(157))
    },
    { # Q158
        "id": 158,
        "question": "Trong PowerPoint 2016, muốn điều chỉnh đường viền (kích thước viền, kiểu viền, màu viền...) cho một hình (shape), ta nhấp chuột vào đối tượng đó rồi chọn:",
        "options": ["Format/Shape Fill", "Format/Shape Outline", "Design/Shape Effects", "Format/Shape Effects"],
        "correct_option_text": get_correct_text(["Format/Shape Fill", "Format/Shape Outline", "Design/Shape Effects", "Format/Shape Effects"], CORRECT_ANSWERS_BY_ID.get(158))
    },
    { # Q159
        "id": 159,
        "question": "Trong PowerPoint 2016, muốn tạo hiệu ứng đổ bóng cho một hình (shape), ta nhấp chuột vào đối tượng đó rồi chọn:",
        "options": ["Design/Shape Effects", "Home/Shape Effects", "Format/Shape Effects", "Layout/Shape Effects"],
        "correct_option_text": get_correct_text(["Design/Shape Effects", "Home/Shape Effects", "Format/Shape Effects", "Layout/Shape Effects"], CORRECT_ANSWERS_BY_ID.get(159))
    },
    { # Q160
        "id": 160,
        "question": "Trong PowerPoint 2016, giả sử có một hình tròn (shape), muốn sao chép thêm một hình nữa thẳng hàng với hình có sẵn, trong khi kéo chuột ta giữ thêm phím gì?",
        "options": ["Shift", "Ctrl", "Ctrl + Shift", "Alt + Shift"],
        "correct_option_text": get_correct_text(["Shift", "Ctrl", "Ctrl + Shift", "Alt + Shift"], CORRECT_ANSWERS_BY_ID.get(160))
    },
    { # Q161
        "id": 161,
        "question": "Trong PowerPoint 2016, để tạo hiệu ứng 3D cho hình (shape), ta nhấp chuột vào đối tượng đó rồi chọn:",
        "options": ["Format/Shape Fill/3D Rotation", "Format/Shape Outline/3D Rotation", "Format/Shape Effects/3D Rotation", "Design/Shape Effects/3D Rotation"],
        "correct_option_text": get_correct_text(["Format/Shape Fill/3D Rotation", "Format/Shape Outline/3D Rotation", "Format/Shape Effects/3D Rotation", "Design/Shape Effects/3D Rotation"], CORRECT_ANSWERS_BY_ID.get(161))
    },
    { # Q162
        "id": 162,
        "question": "Trong PowerPoint 2016, muốn xoay hình (shape), ta thực hiện:",
        "options": [
            "Click chuột vào hình, một biểu tượng xoay hình hiện lên, Click chuột vào đó và xoay",
            "Click phải chuột vào hình, chọn lệnh Rotation",
            "Click phải chuột vào hình, chọn lệnh: Shape Rotation",
            "Click phải chuột vào hình, chọn lệnh: 3D Rotation"
        ],
        "correct_option_text": get_correct_text([
            "Click chuột vào hình, một biểu tượng xoay hình hiện lên, Click chuột vào đó và xoay",
            "Click phải chuột vào hình, chọn lệnh Rotation",
            "Click phải chuột vào hình, chọn lệnh: Shape Rotation",
            "Click phải chuột vào hình, chọn lệnh: 3D Rotation"
        ], CORRECT_ANSWERS_BY_ID.get(162))
    },
    { # Q163
        "id": 163,
        "question": "Trong PowerPoint 2016, giả sử ta có một hình tròn (shape), muốn nhập văn bản vào hình này, ta thực hiện:",
        "options": [
            "Nhấp chuột vào hình, nhập văn bản",
            "Không có cách nào nhập văn bản vào hình (shape)",
            "Chọn Insert/Add Text",
            "Chọn Design/Add Text"
        ],
        "correct_option_text": get_correct_text([
            "Nhấp chuột vào hình, nhập văn bản",
            "Không có cách nào nhập văn bản vào hình (shape)",
            "Chọn Insert/Add Text",
            "Chọn Design/Add Text"
        ], CORRECT_ANSWERS_BY_ID.get(163))
    },
    { # Q164
        "id": 164,
        "question": "Trong PowerPoint 2016, giả sử ta có nhiều đối tượng hình (shape) trên một trang trình chiếu, ta muốn nhóm chúng lại để dễ di chuyển, sau khi chọn các đối tượng, ta thực hiện:",
        "options": ["Format/Group", "Format/Group/Group", "Design/Group", "Design/Group/Group"],
        "correct_option_text": get_correct_text(["Format/Group", "Format/Group/Group", "Design/Group", "Design/Group/Group"], CORRECT_ANSWERS_BY_ID.get(164))
    },
    { # Q165
        "id": 165,
        "question": "Trong PowerPoint 2016, để chọn nhiều đối tượng trên một trang trình chiếu cùng một lúc, ta giữ phím gì trong khi nhấp chọn:",
        "options": ["Tab", "Ctrl", "Alt", "Space"],
        "correct_option_text": get_correct_text(["Tab", "Ctrl", "Alt", "Space"], CORRECT_ANSWERS_BY_ID.get(165))
    },
    { # Q166
        "id": 166,
        "question": "Trong PowerPoint 2016, muốn bỏ ghép nhóm các đối tượng trên một trang trình chiếu, ta nhấp chuột vào đối tượng đó, rồi chọn:",
        "options": ["Format/UnGroup", "Format/Group/UnGroup", "Design/UnGroup", "Design/ Group/UnGroup"],
        "correct_option_text": get_correct_text(["Format/UnGroup", "Format/Group/UnGroup", "Design/UnGroup", "Design/ Group/UnGroup"], CORRECT_ANSWERS_BY_ID.get(166))
    },
    { # Q167
        "id": 167,
        "question": "Trong PowerPoint 2016, giả sử có nhiều đối tượng hình trên một trang trình chiếu, muốn sắp xếp một đối tượng lên trên cùng, ta chọn đối tượng đó, Click phải và chọn lệnh:",
        "options": ["Bring to Front/Bring to Front", "Bring to Front/Bring Forward", "Send to Back/Send to Back", "Send to Back/Send to Backward"],
        "correct_option_text": get_correct_text(["Bring to Front/Bring to Front", "Bring to Front/Bring Forward", "Send to Back/Send to Back", "Send to Back/Send to Backward"], CORRECT_ANSWERS_BY_ID.get(167))
    },
    { # Q168
        "id": 168,
        "question": "Trong PowerPoint 2016, giả sử có nhiều đối tượng hình trên một trang trình chiếu, muốn sắp xếp một đối tượng đưa xuống dưới cùng, ta nhấp chuột vào đối tượng đó rồi chọn:",
        "options": ["View/Send to Back", "Format/Send to Back", "Home/Send to Back", "Design/Send to Back"],
        "correct_option_text": get_correct_text(["View/Send to Back", "Format/Send to Back", "Home/Send to Back", "Design/Send to Back"], CORRECT_ANSWERS_BY_ID.get(168))
    },
    { # Q169
        "id": 169,
        "question": "Trong PowerPoint 2016, Muốn thiết lập hiệu ứng cho các đối tượng ta chọn menu:",
        "options": ["Animations", "Transition", "View", "Slide show"],
        "correct_option_text": get_correct_text(["Animations", "Transition", "View", "Slide show"], CORRECT_ANSWERS_BY_ID.get(169))
    },
    { # Q170
        "id": 170,
        "question": "Trong PowerPoint 2016, muốn xóa bỏ hiệu ứng trình diễn, ta chọn đối tượng cần xóa bỏ hiệu ứng trong hộp thoại Animation Pane, rồi chọn:",
        "options": ["Delete", "Remove", "Cut", "Copy"],
        "correct_option_text": get_correct_text(["Delete", "Remove", "Cut", "Copy"], CORRECT_ANSWERS_BY_ID.get(170))
    },
    { # Q171
        "id": 171,
        "question": "Trong PowerPoint 2016, muốn xem trước slide khi in cùng với các ghi chú trên slide, ta chọn chế độ xem nào sau đây:",
        "options": ["Slide Sorter", "Normal", "Outline View", "Notes Page"],
        "correct_option_text": get_correct_text(["Slide Sorter", "Normal", "Outline View", "Notes Page"], CORRECT_ANSWERS_BY_ID.get(171))
    },
    { # Q172
        "id": 172,
        "question": "Trong PowerPoint 2016, muốn tạo hiệu ứng khi đối tượng xuất hiện, ta chọn nhóm hiệu ứng nào:",
        "options": ["Entrance", "Emphasis", "Exit", "Motion path"],
        "correct_option_text": get_correct_text(["Entrance", "Emphasis", "Exit", "Motion path"], CORRECT_ANSWERS_BY_ID.get(172))
    },
    { # Q173
        "id": 173,
        "question": "Trong PowerPoint 2016, muốn tạo hiệu ứng khi đối tượng bắt đầu mất khỏi slide, ta chọn nhóm hiệu ứng nào:",
        "options": ["Entrance", "Emphasis", "Exit", "Motion path"],
        "correct_option_text": get_correct_text(["Entrance", "Emphasis", "Exit", "Motion path"], CORRECT_ANSWERS_BY_ID.get(173))
    },
    { # Q174
        "id": 174,
        "question": "Trong PowerPoint 2016, có mấy nhóm hiệu ứng khi chọn hiệu ứng cho đối tượng?",
        "options": ["2 nhóm", "3 nhóm", "4 nhóm", "5 nhóm"],
        "correct_option_text": get_correct_text(["2 nhóm", "3 nhóm", "4 nhóm", "5 nhóm"], CORRECT_ANSWERS_BY_ID.get(174))
    },
    { # Q175
        "id": 175,
        "question": "Trong PowerPoint 2016, Để thêm vào một biểu đồ dạng cột, ta thực hiện:",
        "options": ["Insert/Chart", "Home/Chart", "Design/Chart", "View/Chart"],
        "correct_option_text": get_correct_text(["Insert/Chart", "Home/Chart", "Design/Chart", "View/Chart"], CORRECT_ANSWERS_BY_ID.get(175))
    },
    { # Q176
        "id": 176,
        "question": "Trong PowerPoint 2016, thao tác chọn Animation/Add Animation là để tạo hiệu ứng cho đối tượng nào?",
        "options": [
            "Chỉ cho đối tượng là khối văn bản",
            "Chỉ cho đối tượng là khối biểu tượng",
            "Chỉ cho đối tượng là hình ảnh",
            "Cho tất cả các loại đối tượng được chọn"
        ],
        "correct_option_text": get_correct_text([
            "Chỉ cho đối tượng là khối văn bản",
            "Chỉ cho đối tượng là khối biểu tượng",
            "Chỉ cho đối tượng là hình ảnh",
            "Cho tất cả các loại đối tượng được chọn"
        ], CORRECT_ANSWERS_BY_ID.get(176))
    },
    { # Q177
        "id": 177,
        "question": "Trong PowerPoint 2016, dạng nào sau đây dùng để bắt đầu trình chiếu một slide",
        "options": ["Slide Sorter", "Reading View", "Slide Show", "Normal View"],
        "correct_option_text": get_correct_text(["Slide Sorter", "Reading View", "Slide Show", "Normal View"], CORRECT_ANSWERS_BY_ID.get(177))
    },
    { # Q178
        "id": 178,
        "question": "Trong PowerPoint 2016, để in một tập tin trình chiếu, có thể dùng phím tắt:",
        "options": ["Ctrl + S", "Ctrl + N", "Ctrl + P", "Ctrl + Z"],
        "correct_option_text": get_correct_text(["Ctrl + S", "Ctrl + N", "Ctrl + P", "Ctrl + Z"], CORRECT_ANSWERS_BY_ID.get(178))
    },
    { # Q179
        "id": 179,
        "question": "Khi đang trình diễn trong PowerPoint 2016, muốn kết thúc phiên trình diễn, ta thực hiện:",
        "options": [
            "Click phải chuột, rồi chọn Exit",
            "Click phải chuột, rồi chọn Return",
            "Click phải chuột, rồi chọn End Show",
            "Click phải chuột, rồi chọn Screen"
        ],
        "correct_option_text": get_correct_text([
            "Click phải chuột, rồi chọn Exit",
            "Click phải chuột, rồi chọn Return",
            "Click phải chuột, rồi chọn End Show",
            "Click phải chuột, rồi chọn Screen"
        ], CORRECT_ANSWERS_BY_ID.get(179))
    },
    { # Q180
        "id": 180,
        "question": "Trong PowerPoint 2016, muốn kiểm tra lỗi chính tả ta chọn:",
        "options": ["Home/Spelling", "Slide Show/Spelling", "View/Spelling", "Review/Spelling"],
        "correct_option_text": get_correct_text(["Home/Spelling", "Slide Show/Spelling", "View/Spelling", "Review/Spelling"], CORRECT_ANSWERS_BY_ID.get(180))
    },
    { # Q181
        "id": 181,
        "question": "Trong PowerPoint 2016, muốn quy định kích thước trang slide ta chọn:",
        "options": ["Home / Slide Size", "View / Slide Size", "Design / Slide Size", "Slide Show / Slide Size"],
        "correct_option_text": get_correct_text(["Home / Slide Size", "View / Slide Size", "Design / Slide Size", "Slide Show / Slide Size"], CORRECT_ANSWERS_BY_ID.get(181))
    },
    { # Q182
        "id": 182,
        "question": "Điền cụm từ thích hợp vào dấu \"...\" cho câu sau: Mỗi máy tính khi tham gia vào một mạng máy tính bất kỳ đều phải có ... khác nhau.",
        "options": ["Địa chỉ IP", "Địa chỉ email", "Mã sản phẩm", "Tên miền"],
        "correct_option_text": get_correct_text(["Địa chỉ IP", "Địa chỉ email", "Mã sản phẩm", "Tên miền"], CORRECT_ANSWERS_BY_ID.get(182))
    },
    { # Q183
        "id": 183,
        "question": "Lý do sử dụng tường lửa (Firewall) là:",
        "options": [
            "Để ngăn chặn các thành phần nguy hiểm như hacker, sâu, hay các loại virus trước khi chúng có thể xâm nhập vào máy tính của ta",
            "Quét virus trên hệ thống",
            "Ngăn chặn không cho truy cập các website nước ngoài",
            "Ngăn chặn tất cả các chương trình đang hoạt động trên máy tính"
        ],
        "correct_option_text": get_correct_text([
            "Để ngăn chặn các thành phần nguy hiểm như hacker, sâu, hay các loại virus trước khi chúng có thể xâm nhập vào máy tính của ta",
            "Quét virus trên hệ thống",
            "Ngăn chặn không cho truy cập các website nước ngoài",
            "Ngăn chặn tất cả các chương trình đang hoạt động trên máy tính"
        ], CORRECT_ANSWERS_BY_ID.get(183))
    },
    { # Q184
        "id": 184,
        "question": "Khi soạn thư và gửi file đính kèm trong Gmail, thì file cần gửi phải có kích thước bao nhiêu (không gửi dưới dạng liên kết Google Drive)?",
        "options": ["Nhỏ hơn 1 MB", "Nhỏ hơn 10 MB", "Tối đa 25MB", "Không giới hạn"],
        "correct_option_text": get_correct_text(["Nhỏ hơn 1 MB", "Nhỏ hơn 10 MB", "Tối đa 25MB", "Không giới hạn"], CORRECT_ANSWERS_BY_ID.get(184))
    },
    { # Q185
        "id": 185,
        "question": "Một hoặc nhiều trang web liên quan được tổ chức dưới dạng một địa chỉ truy cập chung gọi là gì?:",
        "options": ["Địa chỉ Web", "Website", "Siêu văn bản", "Trang chủ"],
        "correct_option_text": get_correct_text(["Địa chỉ Web", "Website", "Siêu văn bản", "Trang chủ"], CORRECT_ANSWERS_BY_ID.get(185))
    },
    { # Q186
        "id": 186,
        "question": "Các Web client thường được gọi là gì?",
        "options": ["Netscape Navigator", "Browers", "Mosaic", "HTML interpreter (trình thông dịch HTML)"],
        "correct_option_text": get_correct_text(["Netscape Navigator", "Browers", "Mosaic", "HTML interpreter (trình thông dịch HTML)"], CORRECT_ANSWERS_BY_ID.get(186))
    },
    { # Q187
        "id": 187,
        "question": "Mạng tiền thân của Internet có tên gọi là gì?",
        "options": ["Ethernet", "DECNet", "ARPANET", "TELNET"],
        "correct_option_text": get_correct_text(["Ethernet", "DECNet", "ARPANET", "TELNET"], CORRECT_ANSWERS_BY_ID.get(187))
    },
    { # Q188
        "id": 188,
        "question": "Tên miền nào dưới đây là hợp lệ?",
        "options": ["www.hcmiu.edu,vn", "www.hcmiu@edu.vn", "www.@hcmiu.edu.vn", "www.hcmiu.edu.vn"],
        "correct_option_text": get_correct_text(["www.hcmiu.edu,vn", "www.hcmiu@edu.vn", "www.@hcmiu.edu.vn", "www.hcmiu.edu.vn"], CORRECT_ANSWERS_BY_ID.get(188))
    },
    { # Q189
        "id": 189,
        "question": "Đâu là địa chỉ thư điện tử hợp lệ?",
        "options": ["abc@qnu.edu.vn", "abc.qnu.edu.vn", "abc.qnu#gmail.com", "abc@qnu@edu.vn"],
        "correct_option_text": get_correct_text(["abc@qnu.edu.vn", "abc.qnu.edu.vn", "abc.qnu#gmail.com", "abc@qnu@edu.vn"], CORRECT_ANSWERS_BY_ID.get(189))
    },
    { # Q190
        "id": 190,
        "question": "Ứng dụng nào sau đây thường được sử dụng như một ứng dụng e-mail:",
        "options": ["Microsoft Outlook", "Notepad", "Windows XP", "Google"],
        "correct_option_text": get_correct_text(["Microsoft Outlook", "Notepad", "Windows XP", "Google"], CORRECT_ANSWERS_BY_ID.get(190))
    },
    { # Q191
        "id": 191,
        "question": "Nút nào trên thanh công cụ của trình duyệt web cho phép tải lại nội dung một trang web đang xem?",
        "options": ["Home", "Back", "Refresh", "Next"],
        "correct_option_text": get_correct_text(["Home", "Back", "Refresh", "Next"], CORRECT_ANSWERS_BY_ID.get(191))
    },
    { # Q192
        "id": 192,
        "question": "Nút Forward trên thanh công cụ của trình duyệt Web có tác dụng gì?",
        "options": [
            "Chuyển đến trang Web tiếp theo",
            "Chuyển đến cửa sổ trước đó",
            "Chuyển đến màn hình trước đó",
            "Quay lại trang Web trước đó"
        ],
        "correct_option_text": get_correct_text([
            "Chuyển đến trang Web tiếp theo",
            "Chuyển đến cửa sổ trước đó",
            "Chuyển đến màn hình trước đó",
            "Quay lại trang Web trước đó"
        ], CORRECT_ANSWERS_BY_ID.get(192))
    },
    { # Q193
        "id": 193,
        "question": "Ứng dụng nào sau đây không phải là trình duyệt Web?",
        "options": ["Google Chrome", "Opera", "Safari", "File Explorer"],
        "correct_option_text": get_correct_text(["Google Chrome", "Opera", "Safari", "File Explorer"], CORRECT_ANSWERS_BY_ID.get(193))
    },
    { # Q194
        "id": 194,
        "question": "Cho biết URL viết tắt của cụm từ gì?",
        "options": ["Unique Records List", "Uniform Resource Locator", "Indefined Restricted Learner", "Universal Robot Location"],
        "correct_option_text": get_correct_text(["Unique Records List", "Uniform Resource Locator", "Indefined Restricted Learner", "Universal Robot Location"], CORRECT_ANSWERS_BY_ID.get(194))
    },
    { # Q195
        "id": 195,
        "question": "WWW viết tắt của cụm từ nào?",
        "options": ["World Wide Wed", "World Wide Web", "World Wild Web", "Word Wide Web"],
        "correct_option_text": get_correct_text(["World Wide Wed", "World Wide Web", "World Wild Web", "Word Wide Web"], CORRECT_ANSWERS_BY_ID.get(195))
    },
    { # Q196
        "id": 196,
        "question": "Lệnh PING dùng để?",
        "options": [
            "Kiểm tra địa chỉ IP của máy tính",
            "Kiểm tra các máy tính có hoạt động tốt hay không",
            "Kiểm tra các máy tính trong mạng có liên thông không",
            "Kiểm tra các máy tính có truy cập vào Internet không"
        ],
        "correct_option_text": get_correct_text([
            "Kiểm tra địa chỉ IP của máy tính",
            "Kiểm tra các máy tính có hoạt động tốt hay không",
            "Kiểm tra các máy tính trong mạng có liên thông không",
            "Kiểm tra các máy tính có truy cập vào Internet không"
        ], CORRECT_ANSWERS_BY_ID.get(196))
    },
    { # Q197
        "id": 197,
        "question": "Để xem địa chỉ IP của máy tính bằng Command Prompt, ta sử dụng lệnh nào sau đây?",
        "options": ["ipconfig", "ip address", "ipconfig/release", "ipconfig/renew"],
        "correct_option_text": get_correct_text(["ipconfig", "ip address", "ipconfig/release", "ipconfig/renew"], CORRECT_ANSWERS_BY_ID.get(197))
    },
    { # Q198
        "id": 198,
        "question": "Để 2 mạng có thể trao đổi thông tin với nhau thì cần có các điều kiện gì?",
        "options": [
            "Cần có một thiết bị để kết nối 2 mạng đó",
            "Cần cả thiết bị để kết nối 2 mạng và giao thức để hai mạng trao đổi thông tin",
            "Không thể kết nối 2 mạng",
            "Cần có các giao thức truyền thông để hai mạng trao đổi thông tin"
        ],
        "correct_option_text": get_correct_text([
            "Cần có một thiết bị để kết nối 2 mạng đó",
            "Cần cả thiết bị để kết nối 2 mạng và giao thức để hai mạng trao đổi thông tin",
            "Không thể kết nối 2 mạng",
            "Cần có các giao thức truyền thông để hai mạng trao đổi thông tin"
        ], CORRECT_ANSWERS_BY_ID.get(198))
    },
    { # Q199
        "id": 199,
        "question": "Để truy cập vào một trang Web chúng ta cần phải biết:",
        "options": ["Địa chỉ của trang web", "Hệ điều hành đang sử dụng", "Trang web đó của nước nào", "Địa chỉ IP của máy tính"],
        "correct_option_text": get_correct_text(["Địa chỉ của trang web", "Hệ điều hành đang sử dụng", "Trang web đó của nước nào", "Địa chỉ IP của máy tính"], CORRECT_ANSWERS_BY_ID.get(199))
    }
]


while len(QUIZ_DATA_RAW) < TOTAL_QUESTIONS:
    QUIZ_DATA_RAW.append({
        "id": len(QUIZ_DATA_RAW) + 1,
        "question": f"Câu hỏi mẫu {len(QUIZ_DATA_RAW) + 1}",
        "options": [f"{chr(65+i)}. Đáp án {chr(65+i)}" for i in range(4)],
        "correct_option_text": "A. Đáp án A"
    })

# --- 3. CÁC HÀM XỬ LÝ CHÍNH ---
def calculate_score(exam_questions, answers):
    """Tính điểm và thống kê kết quả bài thi."""
    score = 0
    correct_count = 0
    incorrect_count = 0
    unanswered_count = 0
    results = []

    for q_data in exam_questions:
        q_id = q_data['id']
        question_key = f"q_{q_id}_{q_data['unique_id']}"
        user_answer = answers.get(question_key)
        correct_answer_letter = q_data['correct_letter']
        is_correct = False

        if user_answer:
            if user_answer == correct_answer_letter:
                is_correct = True
                score += (10 / QUESTIONS_PER_EXAM)
                correct_count += 1
            else:
                incorrect_count += 1
        else:
            unanswered_count += 1
            
        # Lưu kết quả chi tiết
        results.append({
            'id': q_id,
            'question': q_data['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer_letter,
            'is_correct': is_correct,
            'options': q_data.get('options_shuffled', q_data.get('options', [])),
            'correct_option_text': q_data['correct_option_text'],
            'unique_id': q_data['unique_id']
        })

    return {
        'Điểm số': round(score, 2),
        'Số câu đúng': correct_count,
        'Số câu sai': incorrect_count,
        'Số câu chưa làm': unanswered_count,
        'Tổng số câu': len(exam_questions)
    }, results

def display_question(q_data, index, mode='Ôn thi', show_answer=False):
    """Hiển thị câu hỏi và xử lý lựa chọn đáp án."""
    q_id = q_data['id']
    question_text = q_data['question']
    
    # Xử lý trường hợp thiếu key 'options'
    if 'options_shuffled' in q_data:
        options = q_data['options_shuffled']
    elif 'options' in q_data:
        options = q_data['options']
    else:
        options = []
    
    correct_letter = q_data.get('correct_letter', '')
    correct_option_text = q_data.get('correct_option_text', '')
    
    # Key duy nhất cho câu hỏi
    unique_id = q_data.get('unique_id', str(q_id))
    question_key = f"q_{q_id}_{unique_id}"

    # Lấy đáp án đã chọn (nếu có)
    user_answer_letter = st.session_state.answers.get(question_key)

    st.markdown(f"**Câu {index + 1}** (ID: {q_id}): {question_text}")

    # Chuẩn bị nhãn hiển thị cho radio button
    option_labels = [f"{chr(65 + i)}. {opt_text}" for i, opt_text in enumerate(options)] if options else []

    # Tìm index của đáp án đã chọn trước đó để hiển thị lại
    index_of_current_answer = None
    if user_answer_letter:
        try:
            index_of_current_answer = ord(user_answer_letter.upper()) - 65
        except:
            index_of_current_answer = None

    # Hiển thị radio button để chọn đáp án (chỉ khi chưa nộp bài trong chế độ thi thử)
    if mode == 'Ôn thi' or (mode == 'Thi thử' and not st.session_state.get('score_submitted', False)):
        selected_option = st.radio(
            label="Chọn đáp án:",
            options=option_labels,
            index=index_of_current_answer,
            key=question_key,
            label_visibility="collapsed"
        )
        
        # Lưu đáp án khi chọn
        if selected_option:
            chosen_letter = selected_option.split('.')[0].strip()
            if chosen_letter != user_answer_letter:
                st.session_state.answers[question_key] = chosen_letter
                if mode == 'Ôn thi':
                    st.rerun()
    else:
        # Trong chế độ xem lại, chỉ hiển thị đáp án đã chọn
        if user_answer_letter and option_labels:
            idx = ord(user_answer_letter.upper()) - 65
            if 0 <= idx < len(option_labels):
                st.info(f"**Đã chọn:** {option_labels[idx]}")

    # Hiển thị kết quả
    if user_answer_letter:
        if mode == 'Ôn thi':
            # Luôn hiển thị đáp án cho chế độ ôn thi
            if user_answer_letter == correct_letter:
                st.success(f"✅ **Đúng!** Đáp án: {correct_letter}. {correct_option_text}")
            else:
                st.error(f"❌ **Sai!** Đáp án đúng: {correct_letter}. {correct_option_text}")
        elif mode == 'Thi thử' and (st.session_state.get('score_submitted', False) or show_answer):
            # Chỉ hiển thị đáp án cho chế độ thi thử sau khi nộp bài
            if user_answer_letter == correct_letter:
                st.success(f"✅ **Đúng!** Đáp án: {correct_letter}. {correct_option_text}")
            else:
                st.error(f"❌ **Sai!** Đáp án đúng: {correct_letter}. {correct_option_text}")
    
    st.markdown("---")

# --- 4. LOGIC TẠO ĐỀ THI THÔNG MINH ---
def generate_smart_exam(exam_index):
    """Tạo đề thi thông minh (30 câu) cho đề thứ 'exam_index'."""
    if exam_index in st.session_state.exam_state:
        return

    all_questions = QUIZ_DATA_RAW
    
    # 1. Phân loại câu hỏi đã dùng và chưa dùng
    unused_questions = [q for q in all_questions if st.session_state.question_usage_count.get(q['id'], 0) == 0]
    used_questions = [q for q in all_questions if st.session_state.question_usage_count.get(q['id'], 0) > 0]
    
    selected_questions = []
    
    # 2. Ưu tiên chọn câu chưa dùng
    if len(unused_questions) >= QUESTIONS_PER_EXAM:
        selected_questions = random.sample(unused_questions, QUESTIONS_PER_EXAM)
    else:
        selected_questions.extend(unused_questions)
        remaining = QUESTIONS_PER_EXAM - len(selected_questions)
        
        # 3. Chọn bổ sung từ các câu đã dùng (ưu tiên ít dùng nhất)
        used_questions_sorted = sorted(used_questions, key=lambda x: st.session_state.question_usage_count.get(x['id'], 0))
        
        if len(used_questions_sorted) >= remaining:
            selected_questions.extend(random.sample(used_questions_sorted, remaining))
        else:
            selected_questions.extend(used_questions_sorted)
            needed_more = QUESTIONS_PER_EXAM - len(selected_questions)
            if needed_more > 0:
                all_used_questions_sorted = sorted(all_questions, key=lambda x: st.session_state.question_usage_count.get(x['id'], 0))
                
                available_for_reuse = [q for q in all_used_questions_sorted if q not in selected_questions or selected_questions.count(q) < 1]

                if len(available_for_reuse) >= needed_more:
                    selected_questions.extend(random.sample(available_for_reuse, needed_more))
                else:
                    selected_questions.extend(random.sample(all_used_questions_sorted, needed_more))
    
    # 4. Đảo thứ tự các câu hỏi trong đề
    random.shuffle(selected_questions)

    # 5. Xử lý đảo đáp án và tăng counter
    shuffled_exam_questions = []
    exam_question_ids = []
    for q in selected_questions:
        # Tạo ID duy nhất cho mỗi câu hỏi trong đề thi này
        unique_id = uuid.uuid4().hex[:8] 
        correct_letter = CORRECT_ANSWERS_BY_ID.get(q['id'], 'A')
        
        # Đảo thứ tự options để tạo sự khác biệt
        options_shuffled = random.sample(q['options'], len(q['options']))
        
        q_copy = q.copy()
        q_copy['options_shuffled'] = options_shuffled
        q_copy['correct_letter'] = correct_letter
        q_copy['unique_id'] = unique_id
        shuffled_exam_questions.append(q_copy)
        
        # Cập nhật số lần sử dụng câu hỏi
        st.session_state.question_usage_count[q['id']] += 1
        exam_question_ids.append(q['id'])

    st.session_state.exam_state[exam_index] = shuffled_exam_questions
    st.session_state.exam_question_ids[exam_index] = exam_question_ids

# --- 5. CÁC HÀM KHỞI TẠO VÀ CHẾ ĐỘ HIỂN THỊ ---
def initialize_session_state():
    """Khởi tạo các biến session state cần thiết."""
    if 'mode' not in st.session_state:
        st.session_state.mode = 'Ôn thi'
    if 'answers' not in st.session_state:
        st.session_state.answers = defaultdict(str)
    if 'exam_state' not in st.session_state:
        st.session_state.exam_state = {}
    if 'current_exam_index' not in st.session_state:
        st.session_state.current_exam_index = 1
    if 'question_usage_count' not in st.session_state:
        st.session_state.question_usage_count = defaultdict(int)
    if 'exam_question_ids' not in st.session_state:
        st.session_state.exam_question_ids = {}
    if 'score_submitted' not in st.session_state:
        st.session_state.score_submitted = False
    if 'show_exam_review' not in st.session_state:
        st.session_state.show_exam_review = False
    if 'show_incorrect_only' not in st.session_state:
        st.session_state.show_incorrect_only = False
    if 'exam_results' not in st.session_state:
        st.session_state.exam_results = {}

# --- 6. CHẾ ĐỘ ÔN THI ---
def render_review_mode():
    st.header("📖 Chế độ Ôn tập (199 câu)")
    st.info("**Lưu ý:** Đáp án đúng/sai sẽ hiển thị **ngay lập tức** sau khi bạn chọn một đáp án.")

    # Lấy tất cả 199 câu hỏi theo thứ tự ID
    review_questions = sorted(QUIZ_DATA_RAW, key=lambda x: x['id'])
    st.subheader(f"Tổng cộng: {len(review_questions)} câu hỏi")

    for i, q in enumerate(review_questions):
        unique_id = str(q['id'])
        correct_letter = CORRECT_ANSWERS_BY_ID.get(q['id'], 'A')
        
        q_data = {
            'id': q['id'],
            'question': q['question'],
            'options': q.get('options', []),
            'correct_letter': correct_letter,
            'correct_option_text': q.get('correct_option_text', ''),
            'unique_id': unique_id
        }
        
        display_question(q_data, i, mode='Ôn thi')

# --- 7. CHẾ ĐỘ THI THỬ ---
def render_exam_mode():
    st.header("📝 Chế độ Thi thử (30 câu/đề)")
    
    # 1. Chọn đề thi
    selected_exam_index = st.selectbox(
        "Chọn Đề thi:",
        range(1, TOTAL_EXAMS + 1),
        index=st.session_state.current_exam_index - 1,
        key='exam_selector'
    )
    
    # Reset state nếu chọn đề thi khác
    if selected_exam_index != st.session_state.current_exam_index:
        st.session_state.current_exam_index = selected_exam_index
        st.session_state.score_submitted = False
        st.session_state.show_exam_review = False
        st.session_state.show_incorrect_only = False
        # Không reset answers để giữ lại câu trả lời của đề thi trước
        st.rerun()

    # Tạo đề thi nếu chưa có
    current_exam_questions = st.session_state.exam_state.get(selected_exam_index)
    if not current_exam_questions:
        generate_smart_exam(selected_exam_index)
        current_exam_questions = st.session_state.exam_state[selected_exam_index]

    # Hiển thị thông tin đề thi
    st.info(f"**Đề thi số {selected_exam_index}** - {len(current_exam_questions)} câu hỏi")

    # --- HIỂN THỊ KẾT QUẢ NẾU ĐÃ NỘP BÀI ---
    if st.session_state.score_submitted:
        # Tính điểm
        stats, results = calculate_score(current_exam_questions, st.session_state.answers)
        
        # Lưu kết quả
        st.session_state.exam_results[selected_exam_index] = {
            'stats': stats,
            'results': results
        }
        
        st.subheader(f"📊 Kết quả Đề thi số {selected_exam_index}")
        
        # Hiển thị điểm số và thống kê
        col1, col2, col3 = st.columns(3)
        col1.metric("Điểm số", f"{stats['Điểm số']}/10", f"({stats['Số câu đúng']} câu đúng)")
        col2.metric("Số câu chưa làm", stats['Số câu chưa làm'])
        col3.metric("Số câu sai", stats['Số câu sai'])

        st.markdown("---")
        
        # Nút làm lại đề thi
        if st.button("🔄 Làm lại đề thi này"):
            # Xóa đáp án của đề thi này
            for q in current_exam_questions:
                question_key = f"q_{q['id']}_{q['unique_id']}"
                if question_key in st.session_state.answers:
                    del st.session_state.answers[question_key]
            st.session_state.score_submitted = False
            st.session_state.show_exam_review = False
            st.rerun()
        
        # Nút xem lại bài làm chi tiết
        st.subheader("Xem lại bài làm")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Xem lại TẤT CẢ câu hỏi"):
                st.session_state.show_exam_review = True
                st.session_state.show_incorrect_only = False
                st.rerun()
        
        with col2:
            if st.button("❌ Chỉ xem câu SAI"):
                st.session_state.show_exam_review = True
                st.session_state.show_incorrect_only = True
                st.rerun()
        
        # Hiển thị bài làm chi tiết
        if st.session_state.get('show_exam_review', False):
            st.markdown("---")
            st.subheader("📋 Bài làm chi tiết")
            
            show_incorrect_only = st.session_state.get('show_incorrect_only', False)
            
            for i, q_data in enumerate(results):
                # Nếu chỉ xem câu sai và câu này đúng, bỏ qua
                if show_incorrect_only and q_data['is_correct']:
                    continue
                
                st.markdown(f"**Câu {i+1}** (ID: {q_data['id']}): {q_data['question']}")
                
                # Hiển thị đáp án đã chọn
                if q_data['user_answer']:
                    user_idx = ord(q_data['user_answer'].upper()) - 65
                    if 0 <= user_idx < len(q_data['options']):
                        st.info(f"**Đã chọn:** {q_data['options'][user_idx]}")
                
                # Hiển thị kết quả
                if q_data['is_correct']:
                    st.success(f"✅ **Đúng!** Đáp án: {q_data['correct_answer']}. {q_data['correct_option_text']}")
                else:
                    st.error(f"❌ **Sai!** Đáp án đúng: {q_data['correct_answer']}. {q_data['correct_option_text']}")
                
                st.markdown("---")
    
    # --- FORM LÀM BÀI VÀ NÚT NỘP BÀI ---
    else:
        st.subheader("📝 Đang làm bài...")
        
        # Form làm bài
        with st.form(key=f'exam_form_{selected_exam_index}'):
            for i, q_data in enumerate(current_exam_questions):
                display_question(q_data, i, mode='Thi thử')
            
            # Nút nộp bài
            col1, col2 = st.columns([1, 3])
            with col1:
                submit_button = st.form_submit_button(label="✅ Nộp bài và Chấm điểm", type="primary")
            
            with col2:
                if st.form_submit_button("🔄 Làm lại từ đầu"):
                    # Xóa đáp án của đề thi này
                    for q in current_exam_questions:
                        question_key = f"q_{q['id']}_{q['unique_id']}"
                        if question_key in st.session_state.answers:
                            del st.session_state.answers[question_key]
                    st.rerun()
            
            if submit_button:
                st.session_state.score_submitted = True
                st.rerun()

# --- CHẠY ỨNG DỤNG CHÍNH ---
def main():
    st.set_page_config(
        page_title="Ôn Thi Chứng Chỉ Ứng Dụng Công Nghệ Thông Tin",
        layout="wide",
        page_icon="📚"
    )
    
    st.title("📚 Ứng dụng Ôn thi Chứng chỉ Ứng dụng Công nghệ Thông tin")
    st.markdown("---")

    with st.sidebar:
        st.header("🛠️ Cấu hình")
        initialize_session_state()

        st.session_state.mode = st.radio(
            "Chọn Chế độ:",
            ['Ôn thi', 'Thi thử'],
            key='mode_selector'
        )
        
        st.markdown("---")
        st.subheader("📊 Thống kê sử dụng câu hỏi")
        
        # Hiển thị thống kê câu hỏi đã dùng bao nhiêu lần
        usage_items = sorted(st.session_state.question_usage_count.items(), key=lambda x: x[1], reverse=True)
        if usage_items:
            st.write(f"**Tổng số câu:** {TOTAL_QUESTIONS}")
            
            # Câu dùng nhiều nhất
            st.write("**Câu dùng nhiều nhất:**")
            for q_id, count in usage_items[:3]:
                st.write(f"- Câu {q_id}: {count} lần")
            
            # Phân phối
            st.write("**Phân phối số lần sử dụng:**")
            max_usage = max(usage_items, key=lambda x: x[1])[1] if usage_items else 0
            for i in range(max_usage + 1):
                count = sum(1 for _, usage in usage_items if usage == i)
                if count > 0:
                    st.write(f"- Dùng {i} lần: {count} câu")
        else:
            st.info("Chưa có dữ liệu thống kê")
        
        st.markdown("---")
        
        # Nút reset progress
        if st.button("🔄 Tạo lại 14 Đề thi thử (Reset Progress)", type="secondary"):
            st.session_state.exam_state = {}
            st.session_state.answers = defaultdict(str)
            st.session_state.score_submitted = False
            st.session_state.question_usage_count = defaultdict(int)
            st.session_state.exam_question_ids = {}
            st.session_state.show_exam_review = False
            st.session_state.show_incorrect_only = False
            st.session_state.exam_results = {}
            st.success("✅ Đã reset tất cả đề thi!")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📖 Hướng dẫn")
        st.markdown("""
        - **Ôn thi:** Xem đáp án ngay sau khi chọn
        - **Thi thử:** Làm bài như thi thật, chấm điểm sau khi nộp
        - Mỗi đề 30 câu, ưu tiên dùng hết 199 câu trước khi lặp
        - Có 14 đề thi thử khác nhau
        """)

    # Hiển thị chế độ tương ứng
    if st.session_state.mode == 'Ôn thi':
        render_review_mode()
    else:
        render_exam_mode()

if __name__ == '__main__':
    main()