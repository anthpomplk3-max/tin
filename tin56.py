import streamlit as st
import random
from collections import defaultdict
import uuid

# --- 1. DỮ LIỆU ĐÁP ÁN ĐÚNG CẬP NHẬT TỪ TÀI LIỆU ---
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
    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    idx = mapping.get(correct_letter.upper())
    return options[idx] if idx is not None and 0 <= idx < len(options) else "LỖI: Không tìm thấy đáp án"

# --- 2. DỮ LIỆU CÂU HỎI ĐẦY ĐỦ 199 CÂU THỰC TẾ ---
QUIZ_DATA_RAW = [
    # === PHẦN 1: CƠ BẢN VỀ MÁY TÍNH (Câu 1-30) ===
    {
        "id": 1,
        "question": "Trong các phát biểu sau, phát biểu nào sai khi nói đến bộ nhớ ROM:",
        "options": [
            "Máy tính có thể khởi động mà không cần bộ nhớ ROM.",
            "ROM được viết tắt bởi cụm từ 'Read Only Memory'.",
            "ROM là bộ nhớ chỉ đọc, dữ liệu trong bộ nhớ ROM vẫn duy trì khi nguồn điện bị cắt.",
            "ROM được các nhà sản xuất ghi sẵn các chương trình cơ sở phục vụ cho quá trình khởi động máy."
        ],
        "correct_option_text": get_correct_text([
            "Máy tính có thể khởi động mà không cần bộ nhớ ROM.",
            "ROM được viết tắt bởi cụm từ 'Read Only Memory'.",
            "ROM là bộ nhớ chỉ đọc, dữ liệu trong bộ nhớ ROM vẫn duy trì khi nguồn điện bị cắt.",
            "ROM được các nhà sản xuất ghi sẵn các chương trình cơ sở phục vụ cho quá trình khởi động máy."
        ], CORRECT_ANSWERS_BY_ID.get(1))
    },
    {
        "id": 2,
        "question": "Đơn vị đo thông tin nhỏ nhất trong máy tính là:",
        "options": [
            "Byte",
            "Bit",
            "Kilobyte",
            "Megabyte"
        ],
        "correct_option_text": get_correct_text([
            "Byte",
            "Bit",
            "Kilobyte",
            "Megabyte"
        ], CORRECT_ANSWERS_BY_ID.get(2))
    },
    {
        "id": 3,
        "question": "Phần mềm nào sau đây là hệ điều hành:",
        "options": [
            "Microsoft Word",
            "Windows 10",
            "Google Chrome",
            "Adobe Photoshop"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "Windows 10",
            "Google Chrome",
            "Adobe Photoshop"
        ], CORRECT_ANSWERS_BY_ID.get(3))
    },
    {
        "id": 4,
        "question": "Thiết bị nào sau đây là thiết bị đầu vào:",
        "options": [
            "Màn hình",
            "Máy in",
            "Loa",
            "Bàn phím"
        ],
        "correct_option_text": get_correct_text([
            "Màn hình",
            "Máy in",
            "Loa",
            "Bàn phím"
        ], CORRECT_ANSWERS_BY_ID.get(4))
    },
    {
        "id": 5,
        "question": "1 byte bằng bao nhiêu bit:",
        "options": [
            "4 bit",
            "8 bit",
            "16 bit",
            "32 bit"
        ],
        "correct_option_text": get_correct_text([
            "4 bit",
            "8 bit",
            "16 bit",
            "32 bit"
        ], CORRECT_ANSWERS_BY_ID.get(5))
    },
    {
        "id": 6,
        "question": "Thiết bị nào sau đây dùng để lưu trữ dữ liệu lâu dài:",
        "options": [
            "RAM",
            "CPU",
            "Ổ cứng HDD",
            "ROM"
        ],
        "correct_option_text": get_correct_text([
            "RAM",
            "CPU",
            "Ổ cứng HDD",
            "ROM"
        ], CORRECT_ANSWERS_BY_ID.get(6))
    },
    {
        "id": 7,
        "question": "Phần mềm nào sau đây là phần mềm ứng dụng:",
        "options": [
            "Windows 11",
            "Linux",
            "Microsoft Excel",
            "Android"
        ],
        "correct_option_text": get_correct_text([
            "Windows 11",
            "Linux",
            "Microsoft Excel",
            "Android"
        ], CORRECT_ANSWERS_BY_ID.get(7))
    },
    {
        "id": 8,
        "question": "Chức năng chính của CPU là:",
        "options": [
            "Lưu trữ dữ liệu",
            "Xử lý dữ liệu và điều khiển các thiết bị",
            "Hiển thị thông tin",
            "Nhập dữ liệu"
        ],
        "correct_option_text": get_correct_text([
            "Lưu trữ dữ liệu",
            "Xử lý dữ liệu và điều khiển các thiết bị",
            "Hiển thị thông tin",
            "Nhập dữ liệu"
        ], CORRECT_ANSWERS_BY_ID.get(8))
    },
    {
        "id": 9,
        "question": "Đâu là thiết bị đầu ra:",
        "options": [
            "Bàn phím",
            "Chuột",
            "Máy in",
            "Webcam"
        ],
        "correct_option_text": get_correct_text([
            "Bàn phím",
            "Chuột",
            "Máy in",
            "Webcam"
        ], CORRECT_ANSWERS_BY_ID.get(9))
    },
    {
        "id": 10,
        "question": "RAM là viết tắt của:",
        "options": [
            "Random Access Memory",
            "Read Access Memory",
            "Random Allocation Memory",
            "Read Allocation Memory"
        ],
        "correct_option_text": get_correct_text([
            "Random Access Memory",
            "Read Access Memory",
            "Random Allocation Memory",
            "Read Allocation Memory"
        ], CORRECT_ANSWERS_BY_ID.get(10))
    },
    # Câu 11-30 (tiếp tục phần cơ bản)
    {
        "id": 11,
        "question": "Hệ điều hành nào sau đây là mã nguồn mở:",
        "options": [
            "Windows 10",
            "macOS",
            "Ubuntu Linux",
            "iOS"
        ],
        "correct_option_text": get_correct_text([
            "Windows 10",
            "macOS",
            "Ubuntu Linux",
            "iOS"
        ], CORRECT_ANSWERS_BY_ID.get(11))
    },
    {
        "id": 12,
        "question": "1024 byte bằng:",
        "options": [
            "1 Megabyte",
            "1 Kilobyte",
            "1 Gigabyte",
            "1 Terabyte"
        ],
        "correct_option_text": get_correct_text([
            "1 Megabyte",
            "1 Kilobyte",
            "1 Gigabyte",
            "1 Terabyte"
        ], CORRECT_ANSWERS_BY_ID.get(12))
    },
    {
        "id": 13,
        "question": "Phần mềm diệt virus là loại phần mềm:",
        "options": [
            "Hệ điều hành",
            "Tiện ích",
            "Ứng dụng văn phòng",
            "Lập trình"
        ],
        "correct_option_text": get_correct_text([
            "Hệ điều hành",
            "Tiện ích",
            "Ứng dụng văn phòng",
            "Lập trình"
        ], CORRECT_ANSWERS_BY_ID.get(13))
    },
    {
        "id": 14,
        "question": "Thiết bị nào vừa là đầu vào vừa là đầu ra:",
        "options": [
            "Màn hình cảm ứng",
            "Bàn phím",
            "Máy in",
            "Loa"
        ],
        "correct_option_text": get_correct_text([
            "Màn hình cảm ứng",
            "Bàn phím",
            "Máy in",
            "Loa"
        ], CORRECT_ANSWERS_BY_ID.get(14))
    },
    {
        "id": 15,
        "question": "Phím tắt Ctrl + C dùng để:",
        "options": [
            "Cắt",
            "Copy",
            "Dán",
            "In"
        ],
        "correct_option_text": get_correct_text([
            "Cắt",
            "Copy",
            "Dán",
            "In"
        ], CORRECT_ANSWERS_BY_ID.get(15))
    },
    {
        "id": 16,
        "question": "Phím tắt Ctrl + V dùng để:",
        "options": [
            "Cắt",
            "Copy",
            "Dán",
            "Undo"
        ],
        "correct_option_text": get_correct_text([
            "Cắt",
            "Copy",
            "Dán",
            "Undo"
        ], CORRECT_ANSWERS_BY_ID.get(16))
    },
    {
        "id": 17,
        "question": "Ổ đĩa SSD khác với HDD ở điểm:",
        "options": [
            "Dung lượng nhỏ hơn",
            "Không có phần chuyển động cơ học",
            "Rẻ hơn",
            "Chậm hơn"
        ],
        "correct_option_text": get_correct_text([
            "Dung lượng nhỏ hơn",
            "Không có phần chuyển động cơ học",
            "Rẻ hơn",
            "Chậm hơn"
        ], CORRECT_ANSWERS_BY_ID.get(17))
    },
    {
        "id": 18,
        "question": "Phần mềm nào dùng để nén file:",
        "options": [
            "Microsoft Word",
            "WinRAR",
            "Google Chrome",
            "Adobe Reader"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "WinRAR",
            "Google Chrome",
            "Adobe Reader"
        ], CORRECT_ANSWERS_BY_ID.get(18))
    },
    {
        "id": 19,
        "question": "Đâu là trình duyệt web:",
        "options": [
            "Microsoft Word",
            "Google Chrome",
            "Adobe Photoshop",
            "Excel"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "Google Chrome",
            "Adobe Photoshop",
            "Excel"
        ], CORRECT_ANSWERS_BY_ID.get(19))
    },
    {
        "id": 20,
        "question": "Đơn vị nào lớn nhất:",
        "options": [
            "Megabyte",
            "Gigabyte",
            "Kilobyte",
            "Terabyte"
        ],
        "correct_option_text": get_correct_text([
            "Megabyte",
            "Gigabyte",
            "Kilobyte",
            "Terabyte"
        ], CORRECT_ANSWERS_BY_ID.get(20))
    },
    {
        "id": 21,
        "question": "Phần mở rộng .docx thường là của:",
        "options": [
            "File Excel",
            "File Word",
            "File PowerPoint",
            "File PDF"
        ],
        "correct_option_text": get_correct_text([
            "File Excel",
            "File Word",
            "File PowerPoint",
            "File PDF"
        ], CORRECT_ANSWERS_BY_ID.get(21))
    },
    {
        "id": 22,
        "question": "Phần mở rộng .xlsx thường là của:",
        "options": [
            "File Word",
            "File Excel",
            "File PowerPoint",
            "File hình ảnh"
        ],
        "correct_option_text": get_correct_text([
            "File Word",
            "File Excel",
            "File PowerPoint",
            "File hình ảnh"
        ], CORRECT_ANSWERS_BY_ID.get(22))
    },
    {
        "id": 23,
        "question": "Phần mở rộng .pptx thường là của:",
        "options": [
            "File Word",
            "File Excel",
            "File PowerPoint",
            "File PDF"
        ],
        "correct_option_text": get_correct_text([
            "File Word",
            "File Excel",
            "File PowerPoint",
            "File PDF"
        ], CORRECT_ANSWERS_BY_ID.get(23))
    },
    {
        "id": 24,
        "question": "Phần mở rộng .pdf thường là của:",
        "options": [
            "File Word",
            "File Excel",
            "File PowerPoint",
            "File văn bản di động"
        ],
        "correct_option_text": get_correct_text([
            "File Word",
            "File Excel",
            "File PowerPoint",
            "File văn bản di động"
        ], CORRECT_ANSWERS_BY_ID.get(24))
    },
    {
        "id": 25,
        "question": "Để tạo thư mục mới trong Windows, phím tắt là:",
        "options": [
            "Ctrl + N",
            "Ctrl + Shift + N",
            "Alt + N",
            "Windows + N"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + N",
            "Ctrl + Shift + N",
            "Alt + N",
            "Windows + N"
        ], CORRECT_ANSWERS_BY_ID.get(25))
    },
    {
        "id": 26,
        "question": "Phím tắt để đóng cửa sổ đang mở là:",
        "options": [
            "Ctrl + W",
            "Ctrl + Q",
            "Alt + F4",
            "Ctrl + F4"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + W",
            "Ctrl + Q",
            "Alt + F4",
            "Ctrl + F4"
        ], CORRECT_ANSWERS_BY_ID.get(26))
    },
    {
        "id": 27,
        "question": "Phím tắt để tìm kiếm trong tài liệu là:",
        "options": [
            "Ctrl + F",
            "Ctrl + S",
            "Ctrl + P",
            "Ctrl + H"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + F",
            "Ctrl + S",
            "Ctrl + P",
            "Ctrl + H"
        ], CORRECT_ANSWERS_BY_ID.get(27))
    },
    {
        "id": 28,
        "question": "Phần mềm nào dùng để đọc file PDF:",
        "options": [
            "Microsoft Word",
            "Adobe Acrobat Reader",
            "Google Chrome",
            "Cả B và C"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "Adobe Acrobat Reader",
            "Google Chrome",
            "Cả B và C"
        ], CORRECT_ANSWERS_BY_ID.get(28))
    },
    {
        "id": 29,
        "question": "Tổ hợp phím Ctrl + Alt + Delete dùng để:",
        "options": [
            "Khởi động lại máy",
            "Mở Task Manager",
            "Tắt máy",
            "Đăng xuất"
        ],
        "correct_option_text": get_correct_text([
            "Khởi động lại máy",
            "Mở Task Manager",
            "Tắt máy",
            "Đăng xuất"
        ], CORRECT_ANSWERS_BY_ID.get(29))
    },
    {
        "id": 30,
        "question": "Phần mềm nào là bộ phần mềm văn phòng:",
        "options": [
            "Adobe Creative Cloud",
            "Microsoft Office",
            "Google Chrome",
            "Windows Defender"
        ],
        "correct_option_text": get_correct_text([
            "Adobe Creative Cloud",
            "Microsoft Office",
            "Google Chrome",
            "Windows Defender"
        ], CORRECT_ANSWERS_BY_ID.get(30))
    },
    
    # === PHẦN 2: MICROSOFT WORD (Câu 31-60) ===
    {
        "id": 31,
        "question": "Trong Microsoft Word, phím tắt Ctrl + B dùng để:",
        "options": [
            "In đậm văn bản",
            "In nghiêng văn bản",
            "Gạch chân văn bản",
            "Căn giữa văn bản"
        ],
        "correct_option_text": get_correct_text([
            "In đậm văn bản",
            "In nghiêng văn bản",
            "Gạch chân văn bản",
            "Căn giữa văn bản"
        ], CORRECT_ANSWERS_BY_ID.get(31))
    },
    {
        "id": 32,
        "question": "Trong Microsoft Word, phím tắt Ctrl + I dùng để:",
        "options": [
            "In đậm",
            "In nghiêng",
            "Gạch chân",
            "Căn trái"
        ],
        "correct_option_text": get_correct_text([
            "In đậm",
            "In nghiêng",
            "Gạch chân",
            "Căn trái"
        ], CORRECT_ANSWERS_BY_ID.get(32))
    },
    {
        "id": 33,
        "question": "Trong Microsoft Word, phím tắt Ctrl + U dùng để:",
        "options": [
            "In đậm",
            "In nghiêng",
            "Gạch chân",
            "Undo"
        ],
        "correct_option_text": get_correct_text([
            "In đậm",
            "In nghiêng",
            "Gạch chân",
            "Undo"
        ], CORRECT_ANSWERS_BY_ID.get(33))
    },
    {
        "id": 34,
        "question": "Chức năng Spell Check trong Word dùng để:",
        "options": [
            "Kiểm tra ngữ pháp",
            "Kiểm tra chính tả",
            "Đếm số từ",
            "Tìm và thay thế"
        ],
        "correct_option_text": get_correct_text([
            "Kiểm tra ngữ pháp",
            "Kiểm tra chính tả",
            "Đếm số từ",
            "Tìm và thay thế"
        ], CORRECT_ANSWERS_BY_ID.get(34))
    },
    {
        "id": 35,
        "question": "Để chèn hình ảnh vào Word, ta dùng tab nào:",
        "options": [
            "Home",
            "Insert",
            "Page Layout",
            "Review"
        ],
        "correct_option_text": get_correct_text([
            "Home",
            "Insert",
            "Page Layout",
            "Review"
        ], CORRECT_ANSWERS_BY_ID.get(35))
    },
    {
        "id": 36,
        "question": "Để tạo bảng trong Word, ta dùng:",
        "options": [
            "Insert → Table",
            "Home → Table",
            "Layout → Table",
            "Design → Table"
        ],
        "correct_option_text": get_correct_text([
            "Insert → Table",
            "Home → Table",
            "Layout → Table",
            "Design → Table"
        ], CORRECT_ANSWERS_BY_ID.get(36))
    },
    {
        "id": 37,
        "question": "Phím tắt để lưu tài liệu trong Word là:",
        "options": [
            "Ctrl + N",
            "Ctrl + O",
            "Ctrl + S",
            "Ctrl + P"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + N",
            "Ctrl + O",
            "Ctrl + S",
            "Ctrl + P"
        ], CORRECT_ANSWERS_BY_ID.get(37))
    },
    {
        "id": 38,
        "question": "Phím tắt để mở tài liệu mới trong Word là:",
        "options": [
            "Ctrl + N",
            "Ctrl + O",
            "Ctrl + W",
            "Ctrl + Q"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + N",
            "Ctrl + O",
            "Ctrl + W",
            "Ctrl + Q"
        ], CORRECT_ANSWERS_BY_ID.get(38))
    },
    {
        "id": 39,
        "question": "Để in tài liệu trong Word, phím tắt là:",
        "options": [
            "Ctrl + P",
            "Ctrl + I",
            "Ctrl + O",
            "Ctrl + S"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + P",
            "Ctrl + I",
            "Ctrl + O",
            "Ctrl + S"
        ], CORRECT_ANSWERS_BY_ID.get(39))
    },
    {
        "id": 40,
        "question": "Chức năng Header and Footer nằm ở tab nào:",
        "options": [
            "Home",
            "Insert",
            "Page Layout",
            "View"
        ],
        "correct_option_text": get_correct_text([
            "Home",
            "Insert",
            "Page Layout",
            "View"
        ], CORRECT_ANSWERS_BY_ID.get(40))
    },
    
    # === PHẦN 3: MICROSOFT EXCEL (Câu 41-70) ===
    {
        "id": 41,
        "question": "Trong Excel, một ô được xác định bởi:",
        "options": [
            "Tên cột",
            "Tên hàng",
            "Tên cột và tên hàng",
            "Địa chỉ ô"
        ],
        "correct_option_text": get_correct_text([
            "Tên cột",
            "Tên hàng",
            "Tên cột và tên hàng",
            "Địa chỉ ô"
        ], CORRECT_ANSWERS_BY_ID.get(41))
    },
    {
        "id": 42,
        "question": "Trong Excel, để tính tổng các ô từ A1 đến A10, ta dùng công thức:",
        "options": [
            "=SUM(A1:A10)",
            "=TOTAL(A1:A10)",
            "=ADD(A1:A10)",
            "=SUM(A1+A10)"
        ],
        "correct_option_text": get_correct_text([
            "=SUM(A1:A10)",
            "=TOTAL(A1:A10)",
            "=ADD(A1:A10)",
            "=SUM(A1+A10)"
        ], CORRECT_ANSWERS_BY_ID.get(42))
    },
    {
        "id": 43,
        "question": "Trong Excel, để tính trung bình các ô từ B1 đến B5, ta dùng:",
        "options": [
            "=AVERAGE(B1:B5)",
            "=MEAN(B1:B5)",
            "=AVG(B1:B5)",
            "=MID(B1:B5)"
        ],
        "correct_option_text": get_correct_text([
            "=AVERAGE(B1:B5)",
            "=MEAN(B1:B5)",
            "=AVG(B1:B5)",
            "=MID(B1:B5)"
        ], CORRECT_ANSWERS_BY_ID.get(43))
    },
    {
        "id": 44,
        "question": "Trong Excel, hàm MAX dùng để:",
        "options": [
            "Tìm giá trị lớn nhất",
            "Tìm giá trị nhỏ nhất",
            "Tính trung bình",
            "Đếm số ô"
        ],
        "correct_option_text": get_correct_text([
            "Tìm giá trị lớn nhất",
            "Tìm giá trị nhỏ nhất",
            "Tính trung bình",
            "Đếm số ô"
        ], CORRECT_ANSWERS_BY_ID.get(44))
    },
    {
        "id": 45,
        "question": "Trong Excel, hàm MIN dùng để:",
        "options": [
            "Tìm giá trị lớn nhất",
            "Tìm giá trị nhỏ nhất",
            "Tính tổng",
            "Đếm số ô có giá trị"
        ],
        "correct_option_text": get_correct_text([
            "Tìm giá trị lớn nhất",
            "Tìm giá trị nhỏ nhất",
            "Tính tổng",
            "Đếm số ô có giá trị"
        ], CORRECT_ANSWERS_BY_ID.get(45))
    },
    {
        "id": 46,
        "question": "Trong Excel, hàm COUNT dùng để:",
        "options": [
            "Đếm số ô có chứa số",
            "Đếm tất cả các ô",
            "Đếm số ô trống",
            "Tính tổng các ô"
        ],
        "correct_option_text": get_correct_text([
            "Đếm số ô có chứa số",
            "Đếm tất cả các ô",
            "Đếm số ô trống",
            "Tính tổng các ô"
        ], CORRECT_ANSWERS_BY_ID.get(46))
    },
    {
        "id": 47,
        "question": "Trong Excel, để khóa ô (cố định tham chiếu), ta dùng ký hiệu:",
        "options": [
            "$",
            "#",
            "@",
            "&"
        ],
        "correct_option_text": get_correct_text([
            "$",
            "#",
            "@",
            "&"
        ], CORRECT_ANSWERS_BY_ID.get(47))
    },
    {
        "id": 48,
        "question": "Trong Excel, phím tắt để chèn hàng mới là:",
        "options": [
            "Ctrl + R",
            "Ctrl + +",
            "Ctrl + I",
            "Alt + I + R"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + R",
            "Ctrl + +",
            "Ctrl + I",
            "Alt + I + R"
        ], CORRECT_ANSWERS_BY_ID.get(48))
    },
    {
        "id": 49,
        "question": "Trong Excel, để tạo biểu đồ, ta dùng tab nào:",
        "options": [
            "Home",
            "Insert",
            "Page Layout",
            "Data"
        ],
        "correct_option_text": get_correct_text([
            "Home",
            "Insert",
            "Page Layout",
            "Data"
        ], CORRECT_ANSWERS_BY_ID.get(49))
    },
    {
        "id": 50,
        "question": "Trong Excel, phím F2 có chức năng:",
        "options": [
            "Chỉnh sửa ô đang chọn",
            "Lưu file",
            "Mở file",
            "In file"
        ],
        "correct_option_text": get_correct_text([
            "Chỉnh sửa ô đang chọn",
            "Lưu file",
            "Mở file",
            "In file"
        ], CORRECT_ANSWERS_BY_ID.get(50))
    },
    
    # === PHẦN 4: MICROSOFT POWERPOINT (Câu 51-80) ===
    {
        "id": 51,
        "question": "Trong PowerPoint, để bắt đầu trình chiếu từ đầu, phím tắt là:",
        "options": [
            "F5",
            "F7",
            "Shift + F5",
            "Ctrl + P"
        ],
        "correct_option_text": get_correct_text([
            "F5",
            "F7",
            "Shift + F5",
            "Ctrl + P"
        ], CORRECT_ANSWERS_BY_ID.get(51))
    },
    {
        "id": 52,
        "question": "Trong PowerPoint, để chèn slide mới, phím tắt là:",
        "options": [
            "Ctrl + M",
            "Ctrl + N",
            "Ctrl + S",
            "Ctrl + P"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + M",
            "Ctrl + N",
            "Ctrl + S",
            "Ctrl + P"
        ], CORRECT_ANSWERS_BY_ID.get(52))
    },
    {
        "id": 53,
        "question": "Trong PowerPoint, chế độ nào cho phép xem tất cả slide dưới dạng thu nhỏ:",
        "options": [
            "Normal View",
            "Slide Sorter View",
            "Reading View",
            "Notes Page View"
        ],
        "correct_option_text": get_correct_text([
            "Normal View",
            "Slide Sorter View",
            "Reading View",
            "Notes Page View"
        ], CORRECT_ANSWERS_BY_ID.get(53))
    },
    {
        "id": 54,
        "question": "Để chèn hình ảnh vào slide PowerPoint, ta dùng:",
        "options": [
            "Insert → Picture",
            "Home → Picture",
            "Design → Picture",
            "View → Picture"
        ],
        "correct_option_text": get_correct_text([
            "Insert → Picture",
            "Home → Picture",
            "Design → Picture",
            "View → Picture"
        ], CORRECT_ANSWERS_BY_ID.get(54))
    },
    {
        "id": 55,
        "question": "Trong PowerPoint, để thêm hiệu ứng chuyển tiếp giữa các slide, ta dùng tab:",
        "options": [
            "Animations",
            "Transitions",
            "Slide Show",
            "Design"
        ],
        "correct_option_text": get_correct_text([
            "Animations",
            "Transitions",
            "Slide Show",
            "Design"
        ], CORRECT_ANSWERS_BY_ID.get(55))
    },
    {
        "id": 56,
        "question": "Trong PowerPoint, để thêm hiệu ứng cho đối tượng trên slide, ta dùng tab:",
        "options": [
            "Animations",
            "Transitions",
            "Slide Show",
            "Insert"
        ],
        "correct_option_text": get_correct_text([
            "Animations",
            "Transitions",
            "Slide Show",
            "Insert"
        ], CORRECT_ANSWERS_BY_ID.get(56))
    },
    {
        "id": 57,
        "question": "Phím nào dùng để chuyển sang slide tiếp theo khi trình chiếu:",
        "options": [
            "Spacebar",
            "Enter",
            "Page Down",
            "Tất cả các đáp án trên"
        ],
        "correct_option_text": get_correct_text([
            "Spacebar",
            "Enter",
            "Page Down",
            "Tất cả các đáp án trên"
        ], CORRECT_ANSWERS_BY_ID.get(57))
    },
    {
        "id": 58,
        "question": "Để thoát khỏi chế độ trình chiếu, nhấn phím:",
        "options": [
            "ESC",
            "Enter",
            "Tab",
            "F1"
        ],
        "correct_option_text": get_correct_text([
            "ESC",
            "Enter",
            "Tab",
            "F1"
        ], CORRECT_ANSWERS_BY_ID.get(58))
    },
    {
        "id": 59,
        "question": "Trong PowerPoint, để căn chỉnh văn bản giữa, phím tắt là:",
        "options": [
            "Ctrl + L",
            "Ctrl + E",
            "Ctrl + R",
            "Ctrl + J"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + L",
            "Ctrl + E",
            "Ctrl + R",
            "Ctrl + J"
        ], CORRECT_ANSWERS_BY_ID.get(59))
    },
    {
        "id": 60,
        "question": "Để sao chép slide trong PowerPoint, chọn slide và nhấn:",
        "options": [
            "Ctrl + C",
            "Ctrl + X",
            "Ctrl + D",
            "Ctrl + V"
        ],
        "correct_option_text": get_correct_text([
            "Ctrl + C",
            "Ctrl + X",
            "Ctrl + D",
            "Ctrl + V"
        ], CORRECT_ANSWERS_BY_ID.get(60))
    },
    
    # === PHẦN 5: INTERNET & MẠNG MÁY TÍNH (Câu 61-90) ===
    {
        "id": 61,
        "question": "Giao thức nào dùng để truyền tải trang web:",
        "options": [
            "FTP",
            "HTTP",
            "SMTP",
            "POP3"
        ],
        "correct_option_text": get_correct_text([
            "FTP",
            "HTTP",
            "SMTP",
            "POP3"
        ], CORRECT_ANSWERS_BY_ID.get(61))
    },
    {
        "id": 62,
        "question": "Giao thức nào dùng để gửi email:",
        "options": [
            "POP3",
            "IMAP",
            "SMTP",
            "HTTP"
        ],
        "correct_option_text": get_correct_text([
            "POP3",
            "IMAP",
            "SMTP",
            "HTTP"
        ], CORRECT_ANSWERS_BY_ID.get(62))
    },
    {
        "id": 63,
        "question": "Giao thức nào dùng để nhận email:",
        "options": [
            "SMTP",
            "HTTP",
            "FTP",
            "POP3"
        ],
        "correct_option_text": get_correct_text([
            "SMTP",
            "HTTP",
            "FTP",
            "POP3"
        ], CORRECT_ANSWERS_BY_ID.get(63))
    },
    {
        "id": 64,
        "question": "Địa chỉ IP phiên bản 4 có bao nhiêu phần:",
        "options": [
            "2",
            "3",
            "4",
            "6"
        ],
        "correct_option_text": get_correct_text([
            "2",
            "3",
            "4",
            "6"
        ], CORRECT_ANSWERS_BY_ID.get(64))
    },
    {
        "id": 65,
        "question": "WWW là viết tắt của:",
        "options": [
            "World Wide Web",
            "World Web Wide",
            "Wide World Web",
            "Web World Wide"
        ],
        "correct_option_text": get_correct_text([
            "World Wide Web",
            "World Web Wide",
            "Wide World Web",
            "Web World Wide"
        ], CORRECT_ANSWERS_BY_ID.get(65))
    },
    {
        "id": 66,
        "question": "Trình duyệt web nào sau đây do Microsoft phát triển:",
        "options": [
            "Google Chrome",
            "Mozilla Firefox",
            "Microsoft Edge",
            "Safari"
        ],
        "correct_option_text": get_correct_text([
            "Google Chrome",
            "Mozilla Firefox",
            "Microsoft Edge",
            "Safari"
        ], CORRECT_ANSWERS_BY_ID.get(66))
    },
    {
        "id": 67,
        "question": "URL là viết tắt của:",
        "options": [
            "Uniform Resource Locator",
            "Universal Resource Locator",
            "Uniform Resource Link",
            "Universal Resource Link"
        ],
        "correct_option_text": get_correct_text([
            "Uniform Resource Locator",
            "Universal Resource Locator",
            "Uniform Resource Link",
            "Universal Resource Link"
        ], CORRECT_ANSWERS_BY_ID.get(67))
    },
    {
        "id": 68,
        "question": "Phần mở rộng .com thường là:",
        "options": [
            "Trang web thương mại",
            "Trang web giáo dục",
            "Trang web chính phủ",
            "Trang web tổ chức"
        ],
        "correct_option_text": get_correct_text([
            "Trang web thương mại",
            "Trang web giáo dục",
            "Trang web chính phủ",
            "Trang web tổ chức"
        ], CORRECT_ANSWERS_BY_ID.get(68))
    },
    {
        "id": 69,
        "question": "Phần mở rộng .edu thường là:",
        "options": [
            "Trang web thương mại",
            "Trang web giáo dục",
            "Trang web chính phủ",
            "Trang web tổ chức"
        ],
        "correct_option_text": get_correct_text([
            "Trang web thương mại",
            "Trang web giáo dục",
            "Trang web chính phủ",
            "Trang web tổ chức"
        ], CORRECT_ANSWERS_BY_ID.get(69))
    },
    {
        "id": 70,
        "question": "Công cụ tìm kiếm phổ biến nhất hiện nay là:",
        "options": [
            "Bing",
            "Yahoo",
            "Google",
            "DuckDuckGo"
        ],
        "correct_option_text": get_correct_text([
            "Bing",
            "Yahoo",
            "Google",
            "DuckDuckGo"
        ], CORRECT_ANSWERS_BY_ID.get(70))
    },
    
    # === PHẦN 6: BẢO MẬT & VIRUS (Câu 71-100) ===
    {
        "id": 71,
        "question": "Phần mềm độc hại được gọi là:",
        "options": [
            "Malware",
            "Freeware",
            "Shareware",
            "Adware"
        ],
        "correct_option_text": get_correct_text([
            "Malware",
            "Freeware",
            "Shareware",
            "Adware"
        ], CORRECT_ANSWERS_BY_ID.get(71))
    },
    {
        "id": 72,
        "question": "Loại virus lây lan qua email được gọi là:",
        "options": [
            "Worm",
            "Trojan",
            "Spyware",
            "Ransomware"
        ],
        "correct_option_text": get_correct_text([
            "Worm",
            "Trojan",
            "Spyware",
            "Ransomware"
        ], CORRECT_ANSWERS_BY_ID.get(72))
    },
    {
        "id": 73,
        "question": "Chương trình giả dạng phần mềm hữu ích nhưng thực chất là độc hại được gọi là:",
        "options": [
            "Worm",
            "Trojan",
            "Virus",
            "Spyware"
        ],
        "correct_option_text": get_correct_text([
            "Worm",
            "Trojan",
            "Virus",
            "Spyware"
        ], CORRECT_ANSWERS_BY_ID.get(73))
    },
    {
        "id": 74,
        "question": "Phần mềm gián điệp thu thập thông tin người dùng được gọi là:",
        "options": [
            "Adware",
            "Spyware",
            "Ransomware",
            "Worm"
        ],
        "correct_option_text": get_correct_text([
            "Adware",
            "Spyware",
            "Ransomware",
            "Worm"
        ], CORRECT_ANSWERS_BY_ID.get(74))
    },
    {
        "id": 75,
        "question": "Loại phần mềm độc hại mã hóa dữ liệu và đòi tiền chuộc là:",
        "options": [
            "Spyware",
            "Adware",
            "Ransomware",
            "Trojan"
        ],
        "correct_option_text": get_correct_text([
            "Spyware",
            "Adware",
            "Ransomware",
            "Trojan"
        ], CORRECT_ANSWERS_BY_ID.get(75))
    },
    {
        "id": 76,
        "question": "Firewall là:",
        "options": [
            "Tường lửa bảo vệ mạng",
            "Phần mềm diệt virus",
            "Phần mềm chống spam",
            "Công cụ tìm kiếm"
        ],
        "correct_option_text": get_correct_text([
            "Tường lửa bảo vệ mạng",
            "Phần mềm diệt virus",
            "Phần mềm chống spam",
            "Công cụ tìm kiếm"
        ], CORRECT_ANSWERS_BY_ID.get(76))
    },
    {
        "id": 77,
        "question": "Mật khẩu mạnh nên có:",
        "options": [
            "Ít nhất 6 ký tự",
            "Chỉ chữ cái",
            "Kết hợp chữ hoa, chữ thường, số và ký tự đặc biệt",
            "Tên người dùng"
        ],
        "correct_option_text": get_correct_text([
            "Ít nhất 6 ký tự",
            "Chỉ chữ cái",
            "Kết hợp chữ hoa, chữ thường, số và ký tự đặc biệt",
            "Tên người dùng"
        ], CORRECT_ANSWERS_BY_ID.get(77))
    },
    {
        "id": 78,
        "question": "Phishing là hình thức:",
        "options": [
            "Đánh cắp thông tin qua email giả mạo",
            "Tấn công từ chối dịch vụ",
            "Lây lan virus",
            "Mã hóa dữ liệu"
        ],
        "correct_option_text": get_correct_text([
            "Đánh cắp thông tin qua email giả mạo",
            "Tấn công từ chối dịch vụ",
            "Lây lan virus",
            "Mã hóa dữ liệu"
        ], CORRECT_ANSWERS_BY_ID.get(78))
    },
    {
        "id": 79,
        "question": "Phần mềm diệt virus nên được:",
        "options": [
            "Cài đặt một lần và không cập nhật",
            "Cập nhật thường xuyên",
            "Không cần thiết nếu có firewall",
            "Chỉ cần cho máy tính công cộng"
        ],
        "correct_option_text": get_correct_text([
            "Cài đặt một lần và không cập nhật",
            "Cập nhật thường xuyên",
            "Không cần thiết nếu có firewall",
            "Chỉ cần cho máy tính công cộng"
        ], CORRECT_ANSWERS_BY_ID.get(79))
    },
    {
        "id": 80,
        "question": "Sao lưu dữ liệu (backup) nên được thực hiện:",
        "options": [
            "Chỉ khi máy tính bị hỏng",
            "Định kỳ thường xuyên",
            "Không cần thiết",
            "Chỉ một lần khi mua máy"
        ],
        "correct_option_text": get_correct_text([
            "Chỉ khi máy tính bị hỏng",
            "Định kỳ thường xuyên",
            "Không cần thiết",
            "Chỉ một lần khi mua máy"
        ], CORRECT_ANSWERS_BY_ID.get(80))
    },
    
    # === PHẦN 7: PHẦN MỀM & HỆ ĐIỀU HÀNH (Câu 81-110) ===
    {
        "id": 81,
        "question": "Hệ điều hành nào sau đây của Apple:",
        "options": [
            "Windows",
            "macOS",
            "Linux",
            "Android"
        ],
        "correct_option_text": get_correct_text([
            "Windows",
            "macOS",
            "Linux",
            "Android"
        ], CORRECT_ANSWERS_BY_ID.get(81))
    },
    {
        "id": 82,
        "question": "Hệ điều hành mã nguồn mở phổ biến nhất là:",
        "options": [
            "Windows",
            "macOS",
            "Linux",
            "iOS"
        ],
        "correct_option_text": get_correct_text([
            "Windows",
            "macOS",
            "Linux",
            "iOS"
        ], CORRECT_ANSWERS_BY_ID.get(82))
    },
    {
        "id": 83,
        "question": "Hệ điều hành di động phổ biến nhất hiện nay:",
        "options": [
            "iOS",
            "Android",
            "Windows Mobile",
            "Blackberry OS"
        ],
        "correct_option_text": get_correct_text([
            "iOS",
            "Android",
            "Windows Mobile",
            "Blackberry OS"
        ], CORRECT_ANSWERS_BY_ID.get(83))
    },
    {
        "id": 84,
        "question": "Phần mềm mã nguồn mở là phần mềm:",
        "options": [
            "Miễn phí và có thể sửa đổi mã nguồn",
            "Chỉ miễn phí sử dụng",
            "Chỉ dành cho doanh nghiệp",
            "Không thể sao chép"
        ],
        "correct_option_text": get_correct_text([
            "Miễn phí và có thể sửa đổi mã nguồn",
            "Chỉ miễn phí sử dụng",
            "Chỉ dành cho doanh nghiệp",
            "Không thể sao chép"
        ], CORRECT_ANSWERS_BY_ID.get(84))
    },
    {
        "id": 85,
        "question": "Phần mềm thương mại là phần mềm:",
        "options": [
            "Miễn phí hoàn toàn",
            "Có bản quyền và phải trả phí",
            "Chỉ dùng thử",
            "Không có hỗ trợ"
        ],
        "correct_option_text": get_correct_text([
            "Miễn phí hoàn toàn",
            "Có bản quyền và phải trả phí",
            "Chỉ dùng thử",
            "Không có hỗ trợ"
        ], CORRECT_ANSWERS_BY_ID.get(85))
    },
    {
        "id": 86,
        "question": "Phần mềm shareware là phần mềm:",
        "options": [
            "Miễn phí vĩnh viễn",
            "Dùng thử trong thời gian nhất định",
            "Chỉ dành cho giáo dục",
            "Không có bản quyền"
        ],
        "correct_option_text": get_correct_text([
            "Miễn phí vĩnh viễn",
            "Dùng thử trong thời gian nhất định",
            "Chỉ dành cho giáo dục",
            "Không có bản quyền"
        ], CORRECT_ANSWERS_BY_ID.get(86))
    },
    {
        "id": 87,
        "question": "Task Manager trong Windows dùng để:",
        "options": [
            "Quản lý file",
            "Quản lý tiến trình và ứng dụng",
            "Cài đặt phần mềm",
            "Quản lý mạng"
        ],
        "correct_option_text": get_correct_text([
            "Quản lý file",
            "Quản lý tiến trình và ứng dụng",
            "Cài đặt phần mềm",
            "Quản lý mạng"
        ], CORRECT_ANSWERS_BY_ID.get(87))
    },
    {
        "id": 88,
        "question": "Control Panel trong Windows dùng để:",
        "options": [
            "Chơi game",
            "Soạn thảo văn bản",
            "Cấu hình hệ thống",
            "Lướt web"
        ],
        "correct_option_text": get_correct_text([
            "Chơi game",
            "Soạn thảo văn bản",
            "Cấu hình hệ thống",
            "Lướt web"
        ], CORRECT_ANSWERS_BY_ID.get(88))
    },
    {
        "id": 89,
        "question": "Để gỡ cài đặt phần mềm trong Windows, ta dùng:",
        "options": [
            "Control Panel → Programs and Features",
            "My Computer",
            "Task Manager",
            "Command Prompt"
        ],
        "correct_option_text": get_correct_text([
            "Control Panel → Programs and Features",
            "My Computer",
            "Task Manager",
            "Command Prompt"
        ], CORRECT_ANSWERS_BY_ID.get(89))
    },
    {
        "id": 90,
        "question": "Phím tắt Windows + E dùng để:",
        "options": [
            "Mở File Explorer",
            "Mở trình duyệt web",
            "Mở Control Panel",
            "Mở Task Manager"
        ],
        "correct_option_text": get_correct_text([
            "Mở File Explorer",
            "Mở trình duyệt web",
            "Mở Control Panel",
            "Mở Task Manager"
        ], CORRECT_ANSWERS_BY_ID.get(90))
    },
    
    # === PHẦN 8: THỦ THUẬT & MẸO VẶT (Câu 91-120) ===
    {
        "id": 91,
        "question": "Phím tắt để chụp ảnh màn hình toàn bộ là:",
        "options": [
            "Print Screen",
            "Alt + Print Screen",
            "Windows + Print Screen",
            "Ctrl + Print Screen"
        ],
        "correct_option_text": get_correct_text([
            "Print Screen",
            "Alt + Print Screen",
            "Windows + Print Screen",
            "Ctrl + Print Screen"
        ], CORRECT_ANSWERS_BY_ID.get(91))
    },
    {
        "id": 92,
        "question": "Phím tắt để chụp ảnh cửa sổ đang hoạt động là:",
        "options": [
            "Print Screen",
            "Alt + Print Screen",
            "Windows + Print Screen",
            "Ctrl + Alt + Print Screen"
        ],
        "correct_option_text": get_correct_text([
            "Print Screen",
            "Alt + Print Screen",
            "Windows + Print Screen",
            "Ctrl + Alt + Print Screen"
        ], CORRECT_ANSWERS_BY_ID.get(92))
    },
    {
        "id": 93,
        "question": "Phím tắt Windows + D có chức năng:",
        "options": [
            "Hiển thị desktop",
            "Mở hộp thoại Run",
            "Khóa máy tính",
            "Mở File Explorer"
        ],
        "correct_option_text": get_correct_text([
            "Hiển thị desktop",
            "Mở hộp thoại Run",
            "Khóa máy tính",
            "Mở File Explorer"
        ], CORRECT_ANSWERS_BY_ID.get(93))
    },
    {
        "id": 94,
        "question": "Phím tắt Windows + L có chức năng:",
        "options": [
            "Khóa máy tính",
            "Đăng xuất",
            "Tắt máy",
            "Khởi động lại"
        ],
        "correct_option_text": get_correct_text([
            "Khóa máy tính",
            "Đăng xuất",
            "Tắt máy",
            "Khởi động lại"
        ], CORRECT_ANSWERS_BY_ID.get(94))
    },
    {
        "id": 95,
        "question": "Phím tắt Ctrl + Z có chức năng:",
        "options": [
            "Undo (hoàn tác)",
            "Redo (làm lại)",
            "Copy",
            "Cut"
        ],
        "correct_option_text": get_correct_text([
            "Undo (hoàn tác)",
            "Redo (làm lại)",
            "Copy",
            "Cut"
        ], CORRECT_ANSWERS_BY_ID.get(95))
    },
    {
        "id": 96,
        "question": "Phím tắt Ctrl + Y có chức năng:",
        "options": [
            "Undo",
            "Redo",
            "Save",
            "Print"
        ],
        "correct_option_text": get_correct_text([
            "Undo",
            "Redo",
            "Save",
            "Print"
        ], CORRECT_ANSWERS_BY_ID.get(96))
    },
    {
        "id": 97,
        "question": "Phím tắt Ctrl + A có chức năng:",
        "options": [
            "Chọn tất cả",
            "Cắt",
            "Sao chép",
            "Dán"
        ],
        "correct_option_text": get_correct_text([
            "Chọn tất cả",
            "Cắt",
            "Sao chép",
            "Dán"
        ], CORRECT_ANSWERS_BY_ID.get(97))
    },
    {
        "id": 98,
        "question": "Phím tắt để thu nhỏ tất cả cửa sổ là:",
        "options": [
            "Windows + M",
            "Windows + D",
            "Alt + Tab",
            "Ctrl + M"
        ],
        "correct_option_text": get_correct_text([
            "Windows + M",
            "Windows + D",
            "Alt + Tab",
            "Ctrl + M"
        ], CORRECT_ANSWERS_BY_ID.get(98))
    },
    {
        "id": 99,
        "question": "Phím tắt Alt + Tab có chức năng:",
        "options": [
            "Chuyển đổi giữa các ứng dụng",
            "Đóng ứng dụng",
            "Mở Task Manager",
            "Chụp màn hình"
        ],
        "correct_option_text": get_correct_text([
            "Chuyển đổi giữa các ứng dụng",
            "Đóng ứng dụng",
            "Mở Task Manager",
            "Chụp màn hình"
        ], CORRECT_ANSWERS_BY_ID.get(99))
    },
    {
        "id": 100,
        "question": "Phím tắt Ctrl + Shift + Esc có chức năng:",
        "options": [
            "Mở Task Manager",
            "Mở Control Panel",
            "Khóa máy tính",
            "Đăng xuất"
        ],
        "correct_option_text": get_correct_text([
            "Mở Task Manager",
            "Mở Control Panel",
            "Khóa máy tính",
            "Đăng xuất"
        ], CORRECT_ANSWERS_BY_ID.get(100))
    },
    
    # === PHẦN 9: LÝ THUYẾT NÂNG CAO (Câu 101-130) ===
    {
        "id": 101,
        "question": "Ngôn ngữ lập trình nào được dùng để phát triển web frontend:",
        "options": [
            "Python",
            "Java",
            "HTML/CSS/JavaScript",
            "C++"
        ],
        "correct_option_text": get_correct_text([
            "Python",
            "Java",
            "HTML/CSS/JavaScript",
            "C++"
        ], CORRECT_ANSWERS_BY_ID.get(101))
    },
    {
        "id": 102,
        "question": "Cơ sở dữ liệu quan hệ sử dụng ngôn ngữ nào để truy vấn:",
        "options": [
            "Java",
            "Python",
            "SQL",
            "HTML"
        ],
        "correct_option_text": get_correct_text([
            "Java",
            "Python",
            "SQL",
            "HTML"
        ], CORRECT_ANSWERS_BY_ID.get(102))
    },
    {
        "id": 103,
        "question": "Phần mềm nào sau đây là hệ quản trị cơ sở dữ liệu:",
        "options": [
            "Microsoft Word",
            "Microsoft Excel",
            "MySQL",
            "Photoshop"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "Microsoft Excel",
            "MySQL",
            "Photoshop"
        ], CORRECT_ANSWERS_BY_ID.get(103))
    },
    {
        "id": 104,
        "question": "Cloud Computing là:",
        "options": [
            "Điện toán đám mây",
            "Lập trình di động",
            "Phát triển web",
            "Bảo mật mạng"
        ],
        "correct_option_text": get_correct_text([
            "Điện toán đám mây",
            "Lập trình di động",
            "Phát triển web",
            "Bảo mật mạng"
        ], CORRECT_ANSWERS_BY_ID.get(104))
    },
    {
        "id": 105,
        "question": "Dịch vụ lưu trữ đám mây phổ biến:",
        "options": [
            "Google Drive",
            "Microsoft Word",
            "Adobe Photoshop",
            "Windows Media Player"
        ],
        "correct_option_text": get_correct_text([
            "Google Drive",
            "Microsoft Word",
            "Adobe Photoshop",
            "Windows Media Player"
        ], CORRECT_ANSWERS_BY_ID.get(105))
    },
    {
        "id": 106,
        "question": "AI là viết tắt của:",
        "options": [
            "Artificial Intelligence",
            "Automated Interface",
            "Advanced Internet",
            "Application Integration"
        ],
        "correct_option_text": get_correct_text([
            "Artificial Intelligence",
            "Automated Interface",
            "Advanced Internet",
            "Application Integration"
        ], CORRECT_ANSWERS_BY_ID.get(106))
    },
    {
        "id": 107,
        "question": "IoT là viết tắt của:",
        "options": [
            "Internet of Things",
            "Internet of Technology",
            "Integrated Online Tools",
            "International Online Transfer"
        ],
        "correct_option_text": get_correct_text([
            "Internet of Things",
            "Internet of Technology",
            "Integrated Online Tools",
            "International Online Transfer"
        ], CORRECT_ANSWERS_BY_ID.get(107))
    },
    {
        "id": 108,
        "question": "Big Data là:",
        "options": [
            "Dữ liệu nhỏ",
            "Dữ liệu lớn",
            "Cơ sở dữ liệu",
            "Phần mềm phân tích"
        ],
        "correct_option_text": get_correct_text([
            "Dữ liệu nhỏ",
            "Dữ liệu lớn",
            "Cơ sở dữ liệu",
            "Phần mềm phân tích"
        ], CORRECT_ANSWERS_BY_ID.get(108))
    },
    {
        "id": 109,
        "question": "Blockchain được sử dụng chủ yếu cho:",
        "options": [
            "Tiền điện tử (Cryptocurrency)",
            "Soạn thảo văn bản",
            "Chỉnh sửa ảnh",
            "Phát triển game"
        ],
        "correct_option_text": get_correct_text([
            "Tiền điện tử (Cryptocurrency)",
            "Soạn thảo văn bản",
            "Chỉnh sửa ảnh",
            "Phát triển game"
        ], CORRECT_ANSWERS_BY_ID.get(109))
    },
    {
        "id": 110,
        "question": "Machine Learning là:",
        "options": [
            "Học máy",
            "Lập trình web",
            "Thiết kế đồ họa",
            "Quản lý mạng"
        ],
        "correct_option_text": get_correct_text([
            "Học máy",
            "Lập trình web",
            "Thiết kế đồ họa",
            "Quản lý mạng"
        ], CORRECT_ANSWERS_BY_ID.get(110))
    },
    
    # === PHẦN 10: THIẾT BỊ & PHẦN CỨNG (Câu 111-140) ===
    {
        "id": 111,
        "question": "Thiết bị nào kết nối máy tính với Internet qua đường dây điện thoại:",
        "options": [
            "Router",
            "Modem",
            "Switch",
            "Hub"
        ],
        "correct_option_text": get_correct_text([
            "Router",
            "Modem",
            "Switch",
            "Hub"
        ], CORRECT_ANSWERS_BY_ID.get(111))
    },
    {
        "id": 112,
        "question": "Thiết bị nào phân phối tín hiệu mạng đến nhiều máy tính:",
        "options": [
            "Modem",
            "Router",
            "USB",
            "CPU"
        ],
        "correct_option_text": get_correct_text([
            "Modem",
            "Router",
            "USB",
            "CPU"
        ], CORRECT_ANSWERS_BY_ID.get(112))
    },
    {
        "id": 113,
        "question": "Cổng USB 3.0 có tốc độ:",
        "options": [
            "Chậm hơn USB 2.0",
            "Nhanh hơn USB 2.0",
            "Bằng USB 2.0",
            "Không tương thích với USB 2.0"
        ],
        "correct_option_text": get_correct_text([
            "Chậm hơn USB 2.0",
            "Nhanh hơn USB 2.0",
            "Bằng USB 2.0",
            "Không tương thích với USB 2.0"
        ], CORRECT_ANSWERS_BY_ID.get(113))
    },
    {
        "id": 114,
        "question": "Wi-Fi là công nghệ:",
        "options": [
            "Kết nối có dây",
            "Kết nối không dây",
            "Truyền dữ liệu qua cáp",
            "Kết nối Bluetooth"
        ],
        "correct_option_text": get_correct_text([
            "Kết nối có dây",
            "Kết nối không dây",
            "Truyền dữ liệu qua cáp",
            "Kết nối Bluetooth"
        ], CORRECT_ANSWERS_BY_ID.get(114))
    },
    {
        "id": 115,
        "question": "Bluetooth dùng để:",
        "options": [
            "Kết nối mạng Internet",
            "Kết nối không dây tầm ngắn",
            "Truyền dữ liệu qua cáp",
            "Kết nối máy in có dây"
        ],
        "correct_option_text": get_correct_text([
            "Kết nối mạng Internet",
            "Kết nối không dây tầm ngắn",
            "Truyền dữ liệu qua cáp",
            "Kết nối máy in có dây"
        ], CORRECT_ANSWERS_BY_ID.get(115))
    },
    {
        "id": 116,
        "question": "SSD so với HDD có ưu điểm:",
        "options": [
            "Giá rẻ hơn",
            "Tốc độ đọc/ghi nhanh hơn",
            "Dung lượng lớn hơn cùng giá tiền",
            "Tuổi thọ ngắn hơn"
        ],
        "correct_option_text": get_correct_text([
            "Giá rẻ hơn",
            "Tốc độ đọc/ghi nhanh hơn",
            "Dung lượng lớn hơn cùng giá tiền",
            "Tuổi thọ ngắn hơn"
        ], CORRECT_ANSWERS_BY_ID.get(116))
    },
    {
        "id": 117,
        "question": "RAM DDR4 so với DDR3 có:",
        "options": [
            "Tốc độ chậm hơn",
            "Điện năng tiêu thụ cao hơn",
            "Tốc độ nhanh hơn và điện năng tiêu thụ thấp hơn",
            "Không tương thích với mainboard hiện đại"
        ],
        "correct_option_text": get_correct_text([
            "Tốc độ chậm hơn",
            "Điện năng tiêu thụ cao hơn",
            "Tốc độ nhanh hơn và điện năng tiêu thụ thấp hơn",
            "Không tương thích với mainboard hiện đại"
        ], CORRECT_ANSWERS_BY_ID.get(117))
    },
    {
        "id": 118,
        "question": "Card đồ họa rời (GPU) giúp:",
        "options": [
            "Tăng tốc độ xử lý đồ họa",
            "Tăng dung lượng RAM",
            "Tăng tốc độ Internet",
            "Tăng dung lượng ổ cứng"
        ],
        "correct_option_text": get_correct_text([
            "Tăng tốc độ xử lý đồ họa",
            "Tăng dung lượng RAM",
            "Tăng tốc độ Internet",
            "Tăng dung lượng ổ cứng"
        ], CORRECT_ANSWERS_BY_ID.get(118))
    },
    {
        "id": 119,
        "question": "Nguồn máy tính (PSU) có chức năng:",
        "options": [
            "Cung cấp điện cho các linh kiện",
            "Xử lý đồ họa",
            "Lưu trữ dữ liệu",
            "Kết nối mạng"
        ],
        "correct_option_text": get_correct_text([
            "Cung cấp điện cho các linh kiện",
            "Xử lý đồ họa",
            "Lưu trữ dữ liệu",
            "Kết nối mạng"
        ], CORRECT_ANSWERS_BY_ID.get(119))
    },
    {
        "id": 120,
        "question": "Mainboard (bo mạch chủ) có chức năng:",
        "options": [
            "Kết nối các linh kiện với nhau",
            "Xử lý dữ liệu",
            "Lưu trữ dữ liệu",
            "Hiển thị hình ảnh"
        ],
        "correct_option_text": get_correct_text([
            "Kết nối các linh kiện với nhau",
            "Xử lý dữ liệu",
            "Lưu trữ dữ liệu",
            "Hiển thị hình ảnh"
        ], CORRECT_ANSWERS_BY_ID.get(120))
    },
    
    # === PHẦN 11: ĐỊNH DẠNG FILE & PHẦN MỀM (Câu 121-150) ===
    {
        "id": 121,
        "question": "Định dạng file nén phổ biến nhất:",
        "options": [
            ".docx",
            ".xlsx",
            ".zip",
            ".mp3"
        ],
        "correct_option_text": get_correct_text([
            ".docx",
            ".xlsx",
            ".zip",
            ".mp3"
        ], CORRECT_ANSWERS_BY_ID.get(121))
    },
    {
        "id": 122,
        "question": "Định dạng file hình ảnh không nén:",
        "options": [
            ".jpg",
            ".png",
            ".gif",
            ".bmp"
        ],
        "correct_option_text": get_correct_text([
            ".jpg",
            ".png",
            ".gif",
            ".bmp"
        ], CORRECT_ANSWERS_BY_ID.get(122))
    },
    {
        "id": 123,
        "question": "Định dạng file hình ảnh hỗ trợ trong suốt (transparency):",
        "options": [
            ".jpg",
            ".bmp",
            ".png",
            ".tiff"
        ],
        "correct_option_text": get_correct_text([
            ".jpg",
            ".bmp",
            ".png",
            ".tiff"
        ], CORRECT_ANSWERS_BY_ID.get(123))
    },
    {
        "id": 124,
        "question": "Định dạng file video phổ biến:",
        "options": [
            ".mp3",
            ".mp4",
            ".docx",
            ".pdf"
        ],
        "correct_option_text": get_correct_text([
            ".mp3",
            ".mp4",
            ".docx",
            ".pdf"
        ], CORRECT_ANSWERS_BY_ID.get(124))
    },
    {
        "id": 125,
        "question": "Định dạng file âm thanh phổ biến:",
        "options": [
            ".mp4",
            ".avi",
            ".mp3",
            ".wav"
        ],
        "correct_option_text": get_correct_text([
            ".mp4",
            ".avi",
            ".mp3",
            ".wav"
        ], CORRECT_ANSWERS_BY_ID.get(125))
    },
    {
        "id": 126,
        "question": "Phần mềm chỉnh sửa ảnh chuyên nghiệp:",
        "options": [
            "Microsoft Paint",
            "Adobe Photoshop",
            "Windows Photo Viewer",
            "Google Photos"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Paint",
            "Adobe Photoshop",
            "Windows Photo Viewer",
            "Google Photos"
        ], CORRECT_ANSWERS_BY_ID.get(126))
    },
    {
        "id": 127,
        "question": "Phần mềm chỉnh sửa video phổ biến:",
        "options": [
            "Adobe Premiere Pro",
            "Microsoft Word",
            "Windows Media Player",
            "VLC Media Player"
        ],
        "correct_option_text": get_correct_text([
            "Adobe Premiere Pro",
            "Microsoft Word",
            "Windows Media Player",
            "VLC Media Player"
        ], CORRECT_ANSWERS_BY_ID.get(127))
    },
    {
        "id": 128,
        "question": "Phần mềm nghe nhạc, xem video miễn phí:",
        "options": [
            "Windows Media Player",
            "Adobe Premiere",
            "Microsoft Excel",
            "Photoshop"
        ],
        "correct_option_text": get_correct_text([
            "Windows Media Player",
            "Adobe Premiere",
            "Microsoft Excel",
            "Photoshop"
        ], CORRECT_ANSWERS_BY_ID.get(128))
    },
    {
        "id": 129,
        "question": "VLC Media Player có thể:",
        "options": [
            "Chỉ xem video",
            "Chỉ nghe nhạc",
            "Xem nhiều định dạng video/audio khác nhau",
            "Chỉnh sửa video"
        ],
        "correct_option_text": get_correct_text([
            "Chỉ xem video",
            "Chỉ nghe nhạc",
            "Xem nhiều định dạng video/audio khác nhau",
            "Chỉnh sửa video"
        ], CORRECT_ANSWERS_BY_ID.get(129))
    },
    {
        "id": 130,
        "question": "Phần mềm mã nguồn mở để thay thế Microsoft Office:",
        "options": [
            "Google Docs",
            "LibreOffice",
            "Adobe Acrobat",
            "WinRAR"
        ],
        "correct_option_text": get_correct_text([
            "Google Docs",
            "LibreOffice",
            "Adobe Acrobat",
            "WinRAR"
        ], CORRECT_ANSWERS_BY_ID.get(130))
    },
    
    # === PHẦN 12: TỔNG HỢP & ỨNG DỤNG (Câu 131-160) ===
    {
        "id": 131,
        "question": "Phần mềm giả lập máy tính để bàn trên điện thoại gọi là:",
        "options": [
            "Remote Desktop",
            "Virtual Machine",
            "Cloud Storage",
            "VPN"
        ],
        "correct_option_text": get_correct_text([
            "Remote Desktop",
            "Virtual Machine",
            "Cloud Storage",
            "VPN"
        ], CORRECT_ANSWERS_BY_ID.get(131))
    },
    {
        "id": 132,
        "question": "VPN dùng để:",
        "options": [
            "Tăng tốc độ Internet",
            "Bảo mật kết nối mạng",
            "Nén file",
            "Chỉnh sửa ảnh"
        ],
        "correct_option_text": get_correct_text([
            "Tăng tốc độ Internet",
            "Bảo mật kết nối mạng",
            "Nén file",
            "Chỉnh sửa ảnh"
        ], CORRECT_ANSWERS_BY_ID.get(132))
    },
    {
        "id": 133,
        "question": "TeamViewer dùng để:",
        "options": [
            "Chỉnh sửa video",
            "Điều khiển máy tính từ xa",
            "Lướt web",
            "Nghe nhạc"
        ],
        "correct_option_text": get_correct_text([
            "Chỉnh sửa video",
            "Điều khiển máy tính từ xa",
            "Lướt web",
            "Nghe nhac"
        ], CORRECT_ANSWERS_BY_ID.get(133))
    },
    {
        "id": 134,
        "question": "Phần mềm quản lý dự án phổ biến:",
        "options": [
            "Microsoft Project",
            "Windows Calculator",
            "Paint",
            "Notepad"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Project",
            "Windows Calculator",
            "Paint",
            "Notepad"
        ], CORRECT_ANSWERS_BY_ID.get(134))
    },
    {
        "id": 135,
        "question": "GIMP là phần mềm mã nguồn mở thay thế cho:",
        "options": [
            "Microsoft Word",
            "Adobe Photoshop",
            "Microsoft Excel",
            "Windows Media Player"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "Adobe Photoshop",
            "Microsoft Excel",
            "Windows Media Player"
        ], CORRECT_ANSWERS_BY_ID.get(135))
    },
    {
        "id": 136,
        "question": "Phần mềm thiết kế đồ họa vector:",
        "options": [
            "Adobe Photoshop",
            "Adobe Illustrator",
            "Adobe Premiere",
            "Microsoft Paint"
        ],
        "correct_option_text": get_correct_text([
            "Adobe Photoshop",
            "Adobe Illustrator",
            "Adobe Premiere",
            "Microsoft Paint"
        ], CORRECT_ANSWERS_BY_ID.get(136))
    },
    {
        "id": 137,
        "question": "Phần mềm thiết kế 3D phổ biến:",
        "options": [
            "Microsoft Word",
            "Blender",
            "Windows Calculator",
            "Notepad"
        ],
        "correct_option_text": get_correct_text([
            "Microsoft Word",
            "Blender",
            "Windows Calculator",
            "Notepad"
        ], CORRECT_ANSWERS_BY_ID.get(137))
    },
    {
        "id": 138,
        "question": "Visual Studio Code là:",
        "options": [
            "Trình duyệt web",
            "Trình soạn thảo code",
            "Phần mềm diệt virus",
            "Phần mềm chỉnh sửa ảnh"
        ],
        "correct_option_text": get_correct_text([
            "Trình duyệt web",
            "Trình soạn thảo code",
            "Phần mềm diệt virus",
            "Phần mềm chỉnh sửa ảnh"
        ], CORRECT_ANSWERS_BY_ID.get(138))
    },
    {
        "id": 139,
        "question": "Git là công cụ để:",
        "options": [
            "Quản lý phiên bản mã nguồn",
            "Chỉnh sửa ảnh",
            "Xem video",
            "Nghe nhạc"
        ],
        "correct_option_text": get_correct_text([
            "Quản lý phiên bản mã nguồn",
            "Chỉnh sửa ảnh",
            "Xem video",
            "Nghe nhạc"
        ], CORRECT_ANSWERS_BY_ID.get(139))
    },
    {
        "id": 140,
        "question": "Docker dùng để:",
        "options": [
            "Chỉnh sửa video",
            "Đóng gói và phân phối ứng dụng trong container",
            "Lướt web",
            "Nghe nhạc"
        ],
        "correct_option_text": get_correct_text([
            "Chỉnh sửa video",
            "Đóng gói và phân phối ứng dụng trong container",
            "Lướt web",
            "Nghe nhạc"
        ], CORRECT_ANSWERS_BY_ID.get(140))
    },
    
    # === PHẦN 13: KIẾN THỨC TỔNG HỢP (Câu 141-170) ===
    {
        "id": 141,
        "question": "ASCII là bảng mã:",
        "options": [
            "Mã hóa ký tự cho máy tính",
            "Ngôn ngữ lập trình",
            "Phần mềm diệt virus",
            "Giao thức mạng"
        ],
        "correct_option_text": get_correct_text([
            "Mã hóa ký tự cho máy tính",
            "Ngôn ngữ lập trình",
            "Phần mềm diệt virus",
            "Giao thức mạng"
        ], CORRECT_ANSWERS_BY_ID.get(141))
    },
    {
        "id": 142,
        "question": "Binary (hệ nhị phân) sử dụng các chữ số:",
        "options": [
            "0-9",
            "0-1",
            "0-7",
            "0-9 và A-F"
        ],
        "correct_option_text": get_correct_text([
            "0-9",
            "0-1",
            "0-7",
            "0-9 và A-F"
        ], CORRECT_ANSWERS_BY_ID.get(142))
    },
    {
        "id": 143,
        "question": "Hexadecimal (hệ thập lục phân) sử dụng các chữ số:",
        "options": [
            "0-9",
            "0-1",
            "0-9 và A-F",
            "Chỉ A-F"
        ],
        "correct_option_text": get_correct_text([
            "0-9",
            "0-1",
            "0-9 và A-F",
            "Chỉ A-F"
        ], CORRECT_ANSWERS_BY_ID.get(143))
    },
    {
        "id": 144,
        "question": "Thuật toán là:",
        "options": [
            "Phần cứng máy tính",
            "Tập hợp các bước để giải quyết vấn đề",
            "Ngôn ngữ lập trình",
            "Phần mềm ứng dụng"
        ],
        "correct_option_text": get_correct_text([
            "Phần cứng máy tính",
            "Tập hợp các bước để giải quyết vấn đề",
            "Ngôn ngữ lập trình",
            "Phần mềm ứng dụng"
        ], CORRECT_ANSWERS_BY_ID.get(144))
    },
    {
        "id": 145,
        "question": "Compiler (trình biên dịch) có chức năng:",
        "options": [
            "Chạy chương trình",
            "Dịch mã nguồn sang mã máy",
            "Soạn thảo văn bản",
            "Quản lý file"
        ],
        "correct_option_text": get_correct_text([
            "Chạy chương trình",
            "Dịch mã nguồn sang mã máy",
            "Soạn thảo văn bản",
            "Quản lý file"
        ], CORRECT_ANSWERS_BY_ID.get(145))
    },
    {
        "id": 146,
        "question": "Debugging là quá trình:",
        "options": [
            "Viết code",
            "Tìm và sửa lỗi trong chương trình",
            "Biên dịch chương trình",
            "Chạy chương trình"
        ],
        "correct_option_text": get_correct_text([
            "Viết code",
            "Tìm và sửa lỗi trong chương trình",
            "Biên dịch chương trình",
            "Chạy chương trình"
        ], CORRECT_ANSWERS_BY_ID.get(146))
    },
    {
        "id": 147,
        "question": "API là viết tắt của:",
        "options": [
            "Application Programming Interface",
            "Advanced Programming Interface",
            "Application Process Integration",
            "Automated Programming Interface"
        ],
        "correct_option_text": get_correct_text([
            "Application Programming Interface",
            "Advanced Programming Interface",
            "Application Process Integration",
            "Automated Programming Interface"
        ], CORRECT_ANSWERS_BY_ID.get(147))
    },
    {
        "id": 148,
        "question": "Framework trong lập trình là:",
        "options": [
            "Ngôn ngữ lập trình",
            "Bộ thư viện và công cụ hỗ trợ phát triển",
            "Phần mềm diệt virus",
            "Hệ điều hành"
        ],
        "correct_option_text": get_correct_text([
            "Ngôn ngữ lập trình",
            "Bộ thư viện và công cụ hỗ trợ phát triển",
            "Phần mềm diệt virus",
            "Hệ điều hành"
        ], CORRECT_ANSWERS_BY_ID.get(148))
    },
    {
        "id": 149,
        "question": "Agile là:",
        "options": [
            "Ngôn ngữ lập trình",
            "Phương pháp phát triển phần mềm linh hoạt",
            "Phần mềm diệt virus",
            "Hệ điều hành"
        ],
        "correct_option_text": get_correct_text([
            "Ngôn ngữ lập trình",
            "Phương pháp phát triển phần mềm linh hoạt",
            "Phần mềm diệt virus",
            "Hệ điều hành"
        ], CORRECT_ANSWERS_BY_ID.get(149))
    },
    {
        "id": 150,
        "question": "DevOps là sự kết hợp giữa:",
        "options": [
            "Development và Operations",
            "Design và Operations",
            "Development và Optimization",
            "Design và Optimization"
        ],
        "correct_option_text": get_correct_text([
            "Development và Operations",
            "Design và Operations",
            "Development và Optimization",
            "Design và Optimization"
        ], CORRECT_ANSWERS_BY_ID.get(150))
    },
    
    # === PHẦN 14: CÂU HỎI CUỐI CÙNG (Câu 151-199) ===
    {
        "id": 151,
        "question": "UI là viết tắt của:",
        "options": [
            "User Interface",
            "Universal Interface",
            "User Integration",
            "Universal Integration"
        ],
        "correct_option_text": get_correct_text([
            "User Interface",
            "Universal Interface",
            "User Integration",
            "Universal Integration"
        ], CORRECT_ANSWERS_BY_ID.get(151))
    },
    {
        "id": 152,
        "question": "UX là viết tắt của:",
        "options": [
            "User Experience",
            "Universal Experience",
            "User Extension",
            "Universal Extension"
        ],
        "correct_option_text": get_correct_text([
            "User Experience",
            "Universal Experience",
            "User Extension",
            "Universal Extension"
        ], CORRECT_ANSWERS_BY_ID.get(152))
    },
    {
        "id": 153,
        "question": "Responsive Web Design là thiết kế web:",
        "options": [
            "Chỉ hoạt động trên desktop",
            "Tự động thích ứng với kích thước màn hình",
            "Chỉ hoạt động trên mobile",
            "Không hỗ trợ mobile"
        ],
        "correct_option_text": get_correct_text([
            "Chỉ hoạt động trên desktop",
            "Tự động thích ứng với kích thước màn hình",
            "Chỉ hoạt động trên mobile",
            "Không hỗ trợ mobile"
        ], CORRECT_ANSWERS_BY_ID.get(153))
    },
    {
        "id": 154,
        "question": "SEO là viết tắt của:",
        "options": [
            "Search Engine Optimization",
            "System Engine Optimization",
            "Search Engine Operation",
            "System Engine Operation"
        ],
        "correct_option_text": get_correct_text([
            "Search Engine Optimization",
            "System Engine Optimization",
            "Search Engine Operation",
            "System Engine Operation"
        ], CORRECT_ANSWERS_BY_ID.get(154))
    },
    {
        "id": 155,
        "question": "CMS là viết tắt của:",
        "options": [
            "Content Management System",
            "Computer Management System",
            "Content Marketing System",
            "Computer Marketing System"
        ],
        "correct_option_text": get_correct_text([
            "Content Management System",
            "Computer Management System",
            "Content Marketing System",
            "Computer Marketing System"
        ], CORRECT_ANSWERS_BY_ID.get(155))
    },
    {
        "id": 156,
        "question": "WordPress là một:",
        "options": [
            "Hệ điều hành",
            "CMS phổ biến",
            "Ngôn ngữ lập trình",
            "Phần mềm diệt virus"
        ],
        "correct_option_text": get_correct_text([
            "Hệ điều hành",
            "CMS phổ biến",
            "Ngôn ngữ lập trình",
            "Phần mềm diệt virus"
        ], CORRECT_ANSWERS_BY_ID.get(156))
    },
    {
        "id": 157,
        "question": "E-commerce là:",
        "options": [
            "Thương mại điện tử",
            "Email thương mại",
            "Mạng xã hội",
            "Công cụ tìm kiếm"
        ],
        "correct_option_text": get_correct_text([
            "Thương mại điện tử",
            "Email thương mại",
            "Mạng xã hội",
            "Công cụ tìm kiếm"
        ], CORRECT_ANSWERS_BY_ID.get(157))
    },
    {
        "id": 158,
        "question": "SaaS là viết tắt của:",
        "options": [
            "Software as a Service",
            "System as a Service",
            "Software as a System",
            "System as a Software"
        ],
        "correct_option_text": get_correct_text([
            "Software as a Service",
            "System as a Service",
            "Software as a System",
            "System as a Software"
        ], CORRECT_ANSWERS_BY_ID.get(158))
    },
    {
        "id": 159,
        "question": "PaaS là viết tắt của:",
        "options": [
            "Platform as a Service",
            "Program as a Service",
            "Platform as a System",
            "Program as a System"
        ],
        "correct_option_text": get_correct_text([
            "Platform as a Service",
            "Program as a Service",
            "Platform as a System",
            "Program as a System"
        ], CORRECT_ANSWERS_BY_ID.get(159))
    },
    {
        "id": 160,
        "question": "IaaS là viết tắt của:",
        "options": [
            "Infrastructure as a Service",
            "Internet as a Service",
            "Infrastructure as a System",
            "Internet as a System"
        ],
        "correct_option_text": get_correct_text([
            "Infrastructure as a Service",
            "Internet as a Service",
            "Infrastructure as a System",
            "Internet as a System"
        ], CORRECT_ANSWERS_BY_ID.get(160))
    },
    # Câu 161-199 (các câu còn lại với nội dung tương tự)
    {
        "id": 161,
        "question": "Công nghệ nào cho phép chạy nhiều hệ điều hành trên một máy tính vật lý:",
        "options": [
            "Virtualization",
            "Cloud Computing",
            "Big Data",
            "Blockchain"
        ],
        "correct_option_text": get_correct_text([
            "Virtualization",
            "Cloud Computing",
            "Big Data",
            "Blockchain"
        ], CORRECT_ANSWERS_BY_ID.get(161))
    },
    {
        "id": 162,
        "question": "Hypervisor là phần mềm dùng để:",
        "options": [
            "Tạo và chạy máy ảo",
            "Chỉnh sửa ảnh",
            "Lập trình web",
            "Quản lý mạng"
        ],
        "correct_option_text": get_correct_text([
            "Tạo và chạy máy ảo",
            "Chỉnh sửa ảnh",
            "Lập trình web",
            "Quản lý mạng"
        ], CORRECT_ANSWERS_BY_ID.get(162))
    },
    {
        "id": 163,
        "question": "Container khác với Virtual Machine ở điểm:",
        "options": [
            "Container chia sẻ kernel với host",
            "Container có hệ điều hành riêng",
            "Container nặng hơn VM",
            "Container khởi động chậm hơn VM"
        ],
        "correct_option_text": get_correct_text([
            "Container chia sẻ kernel với host",
            "Container có hệ điều hành riêng",
            "Container nặng hơn VM",
            "Container khởi động chậm hơn VM"
        ], CORRECT_ANSWERS_BY_ID.get(163))
    },
    {
        "id": 164,
        "question": "Kubernetes dùng để:",
        "options": [
            "Quản lý container",
            "Chỉnh sửa video",
            "Lập trình game",
            "Thiết kế đồ họa"
        ],
        "correct_option_text": get_correct_text([
            "Quản lý container",
            "Chỉnh sửa video",
            "Lập trình game",
            "Thiết kế đồ họa"
        ], CORRECT_ANSWERS_BY_ID.get(164))
    },
    {
        "id": 165,
        "question": "Microservices là kiến trúc:",
        "options": [
            "Chia ứng dụng thành các dịch vụ nhỏ độc lập",
            "Xây dựng ứng dụng nguyên khối",
            "Chỉ dành cho ứng dụng desktop",
            "Không thể mở rộng"
        ],
        "correct_option_text": get_correct_text([
            "Chia ứng dụng thành các dịch vụ nhỏ độc lập",
            "Xây dựng ứng dụng nguyên khối",
            "Chỉ dành cho ứng dụng desktop",
            "Không thể mở rộng"
        ], CORRECT_ANSWERS_BY_ID.get(165))
    },
    {
        "id": 166,
        "question": "RESTful API là:",
        "options": [
            "Giao diện đồ họa",
            "Kiến trúc API sử dụng HTTP methods",
            "Ngôn ngữ lập trình",
            "Cơ sở dữ liệu"
        ],
        "correct_option_text": get_correct_text([
            "Giao diện đồ họa",
            "Kiến trúc API sử dụng HTTP methods",
            "Ngôn ngữ lập trình",
            "Cơ sở dữ liệu"
        ], CORRECT_ANSWERS_BY_ID.get(166))
    },
    {
        "id": 167,
        "question": "GraphQL là:",
        "options": [
            "Ngôn ngữ lập trình",
            "Ngôn ngữ truy vấn cho API",
            "Cơ sở dữ liệu",
            "Framework frontend"
        ],
        "correct_option_text": get_correct_text([
            "Ngôn ngữ lập trình",
            "Ngôn ngữ truy vấn cho API",
            "Cơ sở dữ liệu",
            "Framework frontend"
        ], CORRECT_ANSWERS_BY_ID.get(167))
    },
    {
        "id": 168,
        "question": "NoSQL là cơ sở dữ liệu:",
        "options": [
            "Không quan hệ",
            "Chỉ quan hệ",
            "Chỉ SQL",
            "Không hỗ trợ truy vấn"
        ],
        "correct_option_text": get_correct_text([
            "Không quan hệ",
            "Chỉ quan hệ",
            "Chỉ SQL",
            "Không hỗ trợ truy vấn"
        ], CORRECT_ANSWERS_BY_ID.get(168))
    },
    {
        "id": 169,
        "question": "MongoDB là cơ sở dữ liệu:",
        "options": [
            "Quan hệ",
            "NoSQL dạng document",
            "Chỉ lưu trữ bảng tính",
            "Không thể mở rộng"
        ],
        "correct_option_text": get_correct_text([
            "Quan hệ",
            "NoSQL dạng document",
            "Chỉ lưu trữ bảng tính",
            "Không thể mở rộng"
        ], CORRECT_ANSWERS_BY_ID.get(169))
    },
    {
        "id": 170,
        "question": "Redis là cơ sở dữ liệu:",
        "options": [
            "Quan hệ",
            "NoSQL dạng key-value",
            "Chỉ lưu trữ file",
            "Không hỗ trợ bộ nhớ cache"
        ],
        "correct_option_text": get_correct_text([
            "Quan hệ",
            "NoSQL dạng key-value",
            "Chỉ lưu trữ file",
            "Không hỗ trợ bộ nhớ cache"
        ], CORRECT_ANSWERS_BY_ID.get(170))
    },
    {
        "id": 171,
        "question": "CI/CD là viết tắt của:",
        "options": [
            "Continuous Integration/Continuous Deployment",
            "Computer Integration/Computer Deployment",
            "Continuous Interface/Continuous Design",
            "Computer Interface/Computer Design"
        ],
        "correct_option_text": get_correct_text([
            "Continuous Integration/Continuous Deployment",
            "Computer Integration/Computer Deployment",
            "Continuous Interface/Continuous Design",
            "Computer Interface/Computer Design"
        ], CORRECT_ANSWERS_BY_ID.get(171))
    },
    {
        "id": 172,
        "question": "Jenkins là công cụ dùng cho:",
        "options": [
            "CI/CD",
            "Chỉnh sửa ảnh",
            "Lập trình game",
            "Thiết kế web"
        ],
        "correct_option_text": get_correct_text([
            "CI/CD",
            "Chỉnh sửa ảnh",
            "Lập trình game",
            "Thiết kế web"
        ], CORRECT_ANSWERS_BY_ID.get(172))
    },
    {
        "id": 173,
        "question": "GitHub là nền tảng:",
        "options": [
            "Lưu trữ và quản lý mã nguồn",
            "Chỉnh sửa video",
            "Thiết kế đồ họa",
            "Quản lý dự án offline"
        ],
        "correct_option_text": get_correct_text([
            "Lưu trữ và quản lý mã nguồn",
            "Chỉnh sửa video",
            "Thiết kế đồ họa",
            "Quản lý dự án offline"
        ], CORRECT_ANSWERS_BY_ID.get(173))
    },
    {
        "id": 174,
        "question": "GitLab là nền tảng:",
        "options": [
            "Chỉ public repository",
            "DevOps lifecycle hoàn chỉnh",
            "Chỉ private repository",
            "Chỉ quản lý issue"
        ],
        "correct_option_text": get_correct_text([
            "Chỉ public repository",
            "DevOps lifecycle hoàn chỉnh",
            "Chỉ private repository",
            "Chỉ quản lý issue"
        ], CORRECT_ANSWERS_BY_ID.get(174))
    },
    {
        "id": 175,
        "question": "Jira là công cụ quản lý:",
        "options": [
            "Dự án và issue tracking",
            "Chỉnh sửa ảnh",
            "Lập trình",
            "Thiết kế đồ họa"
        ],
        "correct_option_text": get_correct_text([
            "Dự án và issue tracking",
            "Chỉnh sửa ảnh",
            "Lập trình",
            "Thiết kế đồ họa"
        ], CORRECT_ANSWERS_BY_ID.get(175))
    },
    {
        "id": 176,
        "question": "Slack là công cụ:",
        "options": [
            "Chat và cộng tác nhóm",
            "Chỉnh sửa video",
            "Lập trình",
            "Quản lý cơ sở dữ liệu"
        ],
        "correct_option_text": get_correct_text([
            "Chat và cộng tác nhóm",
            "Chỉnh sửa video",
            "Lập trình",
            "Quản lý cơ sở dữ liệu"
        ], CORRECT_ANSWERS_BY_ID.get(176))
    },
    {
        "id": 177,
        "question": "Trello là công cụ quản lý dự án theo phương pháp:",
        "options": [
            "Kanban",
            "Waterfall",
            "Scrum",
            "Agile"
        ],
        "correct_option_text": get_correct_text([
            "Kanban",
            "Waterfall",
            "Scrum",
            "Agile"
        ], CORRECT_ANSWERS_BY_ID.get(177))
    },
    {
        "id": 178,
        "question": "Scrum là framework:",
        "options": [
            "Waterfall",
            "Agile",
            "Kanban",
            "Traditional"
        ],
        "correct_option_text": get_correct_text([
            "Waterfall",
            "Agile",
            "Kanban",
            "Traditional"
        ], CORRECT_ANSWERS_BY_ID.get(178))
    },
    {
        "id": 179,
        "question": "Sprint trong Scrum là:",
        "options": [
            "Giai đoạn phát triển ngắn (2-4 tuần)",
            "Cuộc họp hàng ngày",
            "Tài liệu yêu cầu",
            "Bản release cuối cùng"
        ],
        "correct_option_text": get_correct_text([
            "Giai đoạn phát triển ngắn (2-4 tuần)",
            "Cuộc họp hàng ngày",
            "Tài liệu yêu cầu",
            "Bản release cuối cùng"
        ], CORRECT_ANSWERS_BY_ID.get(179))
    },
    {
        "id": 180,
        "question": "Product Owner trong Scrum có trách nhiệm:",
        "options": [
            "Phát triển code",
            "Quản lý Product Backlog",
            "Điều phối cuộc họp",
            "Test sản phẩm"
        ],
        "correct_option_text": get_correct_text([
            "Phát triển code",
            "Quản lý Product Backlog",
            "Điều phối cuộc họp",
            "Test sản phẩm"
        ], CORRECT_ANSWERS_BY_ID.get(180))
    },
    {
        "id": 181,
        "question": "Scrum Master có vai trò:",
        "options": [
            "Phát triển code chính",
            "Đảm bảo team tuân theo Scrum",
            "Quyết định tính năng sản phẩm",
            "Test sản phẩm"
        ],
        "correct_option_text": get_correct_text([
            "Phát triển code chính",
            "Đảm bảo team tuân theo Scrum",
            "Quyết định tính năng sản phẩm",
            "Test sản phẩm"
        ], CORRECT_ANSWERS_BY_ID.get(181))
    },
    {
        "id": 182,
        "question": "Daily Standup trong Scrum là:",
        "options": [
            "Cuộc họp hàng tuần",
            "Cuộc họp hàng ngày 15 phút",
            "Cuộc họp hàng tháng",
            "Buổi training"
        ],
        "correct_option_text": get_correct_text([
            "Cuộc họp hàng tuần",
            "Cuộc họp hàng ngày 15 phút",
            "Cuộc họp hàng tháng",
            "Buổi training"
        ], CORRECT_ANSWERS_BY_ID.get(182))
    },
    {
        "id": 183,
        "question": "Sprint Review trong Scrum là:",
        "options": [
            "Cuộc họp đầu sprint",
            "Cuộc họp cuối sprint để demo sản phẩm",
            "Cuộc họp hàng ngày",
            "Buổi training"
        ],
        "correct_option_text": get_correct_text([
            "Cuộc họp đầu sprint",
            "Cuộh họp cuối sprint để demo sản phẩm",
            "Cuộc họp hàng ngày",
            "Buổi training"
        ], CORRECT_ANSWERS_BY_ID.get(183))
    },
    {
        "id": 184,
        "question": "Sprint Retrospective trong Scrum là:",
        "options": [
            "Cuộc họp cải tiến quy trình",
            "Cuộc họp demo sản phẩm",
            "Cuộc họp lập kế hoạch",
            "Cuộc họp hàng ngày"
        ],
        "correct_option_text": get_correct_text([
            "Cuộc họp cải tiến quy trình",
            "Cuộc họp demo sản phẩm",
            "Cuộc họp lập kế hoạch",
            "Cuộc họp hàng ngày"
        ], CORRECT_ANSWERS_BY_ID.get(184))
    },
    {
        "id": 185,
        "question": "Waterfall là mô hình phát triển:",
        "options": [
            "Linh hoạt",
            "Tuần tự",
            "Lặp đi lặp lại",
            "Tăng trưởng"
        ],
        "correct_option_text": get_correct_text([
            "Linh hoạt",
            "Tuần tự",
            "Lặp đi lặp lại",
            "Tăng trưởng"
        ], CORRECT_ANSWERS_BY_ID.get(185))
    },
    {
        "id": 186,
        "question": "Kanban là phương pháp:",
        "options": [
            "Visual workflow management",
            "Chỉ dùng trong manufacturing",
            "Không có board visual",
            "Không giới hạn work in progress"
        ],
        "correct_option_text": get_correct_text([
            "Visual workflow management",
            "Chỉ dùng trong manufacturing",
            "Không có board visual",
            "Không giới hạn work in progress"
        ], CORRECT_ANSWERS_BY_ID.get(186))
    },
    {
        "id": 187,
        "question": "WIP Limit trong Kanban là:",
        "options": [
            "Giới hạn công việc đang thực hiện",
            "Không giới hạn công việc",
            "Chỉ áp dụng cho team nhỏ",
            "Không quan trọng"
        ],
        "correct_option_text": get_correct_text([
            "Giới hạn công việc đang thực hiện",
            "Không giới hạn công việc",
            "Chỉ áp dụng cho team nhỏ",
            "Không quan trọng"
        ], CORRECT_ANSWERS_BY_ID.get(187))
    },
    {
        "id": 188,
        "question": "TDD là viết tắt của:",
        "options": [
            "Test-Driven Development",
            "Technical Design Document",
            "Test Design Document",
            "Technical-Driven Development"
        ],
        "correct_option_text": get_correct_text([
            "Test-Driven Development",
            "Technical Design Document",
            "Test Design Document",
            "Technical-Driven Development"
        ], CORRECT_ANSWERS_BY_ID.get(188))
    },
    {
        "id": 189,
        "question": "BDD là viết tắt của:",
        "options": [
            "Behavior-Driven Development",
            "Business Design Document",
            "Behavior Design Document",
            "Business-Driven Development"
        ],
        "correct_option_text": get_correct_text([
            "Behavior-Driven Development",
            "Business Design Document",
            "Behavior Design Document",
            "Business-Driven Development"
        ], CORRECT_ANSWERS_BY_ID.get(189))
    },
    {
        "id": 190,
        "question": "Unit Test là test:",
        "options": [
            "Toàn bộ hệ thống",
            "Từng đơn vị code nhỏ",
            "Giao diện người dùng",
            "Hiệu năng hệ thống"
        ],
        "correct_option_text": get_correct_text([
            "Toàn bộ hệ thống",
            "Từng đơn vị code nhỏ",
            "Giao diện người dùng",
            "Hiệu năng hệ thống"
        ], CORRECT_ANSWERS_BY_ID.get(190))
    },
    {
        "id": 191,
        "question": "Integration Test là test:",
        "options": [
            "Từng module riêng lẻ",
            "Tương tác giữa các module",
            "Chỉ giao diện người dùng",
            "Chỉ database"
        ],
        "correct_option_text": get_correct_text([
            "Từng module riêng lẻ",
            "Tương tác giữa các module",
            "Chỉ giao diện người dùng",
            "Chỉ database"
        ], CORRECT_ANSWERS_BY_ID.get(191))
    },
    {
        "id": 192,
        "question": "System Test là test:",
        "options": [
            "Toàn bộ hệ thống hoàn chỉnh",
            "Chỉ từng function",
            "Chỉ giao diện",
            "Chỉ database"
        ],
        "correct_option_text": get_correct_text([
            "Toàn bộ hệ thống hoàn chỉnh",
            "Chỉ từng function",
            "Chỉ giao diện",
            "Chỉ database"
        ], CORRECT_ANSWERS_BY_ID.get(192))
    },
    {
        "id": 193,
        "question": "UAT là viết tắt của:",
        "options": [
            "Unit Acceptance Testing",
            "User Acceptance Testing",
            "Universal Acceptance Testing",
            "User Access Testing"
        ],
        "correct_option_text": get_correct_text([
            "Unit Acceptance Testing",
            "User Acceptance Testing",
            "Universal Acceptance Testing",
            "User Access Testing"
        ], CORRECT_ANSWERS_BY_ID.get(193))
    },
    {
        "id": 194,
        "question": "Regression Test là test:",
        "options": [
            "Chức năng mới",
            "Đảm bảo chức năng cũ vẫn hoạt động",
            "Chỉ performance",
            "Chỉ security"
        ],
        "correct_option_text": get_correct_text([
            "Chức năng mới",
            "Đảm bảo chức năng cũ vẫn hoạt động",
            "Chỉ performance",
            "Chỉ security"
        ], CORRECT_ANSWERS_BY_ID.get(194))
    },
    {
        "id": 195,
        "question": "Performance Test là test:",
        "options": [
            "Chức năng hệ thống",
            "Tốc độ và khả năng mở rộng",
            "Bảo mật hệ thống",
            "Giao diện người dùng"
        ],
        "correct_option_text": get_correct_text([
            "Chức năng hệ thống",
            "Tốc độ và khả năng mở rộng",
            "Bảo mật hệ thống",
            "Giao diện người dùng"
        ], CORRECT_ANSWERS_BY_ID.get(195))
    },
    {
        "id": 196,
        "question": "Security Test là test:",
        "options": [
            "Tốc độ hệ thống",
            "Bảo mật và lỗ hổng",
            "Chức năng hệ thống",
            "Giao diện người dùng"
        ],
        "correct_option_text": get_correct_text([
            "Tốc độ hệ thống",
            "Bảo mật và lỗ hổng",
            "Chức năng hệ thống",
            "Giao diện người dùng"
        ], CORRECT_ANSWERS_BY_ID.get(196))
    },
    {
        "id": 197,
        "question": "Load Test là test:",
        "options": [
            "Hệ thống dưới tải bình thường",
            "Hệ thống dưới tải cao",
            "Chỉ chức năng đơn lẻ",
            "Chỉ bảo mật"
        ],
        "correct_option_text": get_correct_text([
            "Hệ thống dưới tải bình thường",
            "Hệ thống dưới tải cao",
            "Chỉ chức năng đơn lẻ",
            "Chỉ bảo mật"
        ], CORRECT_ANSWERS_BY_ID.get(197))
    },
    {
        "id": 198,
        "question": "Stress Test là test:",
        "options": [
            "Hệ thống dưới tải bình thường",
            "Hệ thống vượt quá giới hạn",
            "Chỉ chức năng cơ bản",
            "Chỉ giao diện"
        ],
        "correct_option_text": get_correct_text([
            "Hệ thống dưới tải bình thường",
            "Hệ thống vượt quá giới hạn",
            "Chỉ chức năng cơ bản",
            "Chỉ giao diện"
        ], CORRECT_ANSWERS_BY_ID.get(198))
    },
    {
        "id": 199,
        "question": "Usability Test là test:",
        "options": [
            "Tốc độ hệ thống",
            "Độ dễ sử dụng của giao diện",
            "Bảo mật hệ thống",
            "Chức năng backend"
        ],
        "correct_option_text": get_correct_text([
            "Tốc độ hệ thống",
            "Độ dễ sử dụng của giao diện",
            "Bảo mật hệ thống",
            "Chức năng backend"
        ], CORRECT_ANSWERS_BY_ID.get(199))
    }
]
for i in range(2, 200):
    QUIZ_DATA_RAW.append({
        "id": i,
        "question": f"Câu hỏi mẫu số {i} về Tin học cơ bản:",
        "options": [
            f"Đáp án A cho câu {i}",
            f"Đáp án B cho câu {i}",
            f"Đáp án C cho câu {i}",
            f"Đáp án D cho câu {i}"
        ],
        "correct_option_text": get_correct_text([
            f"Đáp án A cho câu {i}",
            f"Đáp án B cho câu {i}",
            f"Đáp án C cho câu {i}",
            f"Đáp án D cho câu {i}"
        ], CORRECT_ANSWERS_BY_ID.get(i, 'A'))
    })

# --- 3. CÁC HẰNG SỐ ---
# --- 3. CÁC HẰNG SỐ ---
TOTAL_QUESTIONS = len(QUIZ_DATA_RAW)
QUESTIONS_PER_EXAM = 30
TOTAL_EXAMS = 14

# --- 4. HÀM KHỞI TẠO SESSION ---
def initialize_session_state():
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
    if 'review_questions' not in st.session_state:
        st.session_state.review_questions = []
    if 'question_usage_count' not in st.session_state:
        st.session_state.question_usage_count = defaultdict(int)
    if 'exam_question_ids' not in st.session_state:
        st.session_state.exam_question_ids = {}
    if 'radio_keys' not in st.session_state:
        st.session_state.radio_keys = {}
    if 'exam_forms' not in st.session_state:
        st.session_state.exam_forms = {}

# --- 5. HÀM TẠO ĐỀ THI THÔNG MINH ---
def generate_smart_exam(exam_index):
    """Tạo đề thi thông minh: ưu tiên sử dụng hết 199 câu trước khi lặp lại"""
    
    if exam_index not in st.session_state.exam_state:
        # Lấy tất cả câu hỏi
        all_questions = QUIZ_DATA_RAW.copy()
        
        # Phân chia thành 2 nhóm: chưa dùng và đã dùng
        unused_questions = []
        used_questions = []
        
        for q in all_questions:
            usage_count = st.session_state.question_usage_count.get(q['id'], 0)
            if usage_count == 0:
                unused_questions.append(q)
            else:
                used_questions.append(q)
        
        # Ưu tiên chọn câu chưa dùng
        selected_questions = []
        
        # Nếu còn đủ câu chưa dùng cho 30 câu
        if len(unused_questions) >= QUESTIONS_PER_EXAM:
            selected_questions = random.sample(unused_questions, QUESTIONS_PER_EXAM)
        else:
            # Lấy tất cả câu chưa dùng
            selected_questions = unused_questions.copy()
            remaining = QUESTIONS_PER_EXAM - len(selected_questions)
            
            # Sắp xếp câu đã dùng theo số lần sử dụng (ưu tiên câu ít dùng nhất)
            used_questions_sorted = sorted(used_questions, 
                                          key=lambda x: st.session_state.question_usage_count.get(x['id'], 0))
            
            # Thêm câu ít dùng nhất
            if remaining > 0 and len(used_questions_sorted) >= remaining:
                selected_questions.extend(used_questions_sorted[:remaining])
            elif remaining > 0:
                # Nếu vẫn không đủ, lặp lại từ đầu danh sách (tạm thời, nhưng với 199 câu thì 14x30=420 cần)
                # Vì cần 420 câu cho 14 đề, sẽ có lặp lại nhưng ưu tiên câu ít dùng nhất
                all_questions_sorted = sorted(all_questions, 
                                             key=lambda x: st.session_state.question_usage_count.get(x['id'], 0))
                while len(selected_questions) < QUESTIONS_PER_EXAM:
                    for q in all_questions_sorted:
                        if q not in selected_questions:
                            selected_questions.append(q)
                            if len(selected_questions) >= QUESTIONS_PER_EXAM:
                                break
        
        # Lưu ID các câu hỏi được chọn cho đề này
        st.session_state.exam_question_ids[exam_index] = [q['id'] for q in selected_questions]
        
        # Đảo thứ tự câu hỏi trong đề
        random.shuffle(selected_questions)
        
        # Tạo đề với đáp án đã đảo
        exam_questions = []
        for q_data in selected_questions:
            shuffled_options = q_data['options'].copy()
            random.shuffle(shuffled_options)
            
            exam_questions.append({
                "id": q_data['id'],
                "question": q_data['question'],
                "options": shuffled_options,
                "correct_option_text": q_data['correct_option_text']
            })
            
            # Cập nhật số lần sử dụng
            st.session_state.question_usage_count[q_data['id']] += 1
        
        st.session_state.exam_state[exam_index] = exam_questions
    
    return st.session_state.exam_state[exam_index]

# --- 6. HÀM TẠO LẠI TẤT CẢ ĐỀ THI ---
def regenerate_all_exams():
    """Tạo lại tất cả 14 đề thi"""
    st.session_state.exam_state = {}
    st.session_state.question_usage_count = defaultdict(int)
    st.session_state.exam_question_ids = {}
    st.session_state.answers = defaultdict(str)
    st.session_state.score_submitted = False
    st.session_state.radio_keys = {}
    st.session_state.exam_forms = {}
    
    for exam_index in range(1, TOTAL_EXAMS + 1):
        generate_smart_exam(exam_index)

# --- 7. HÀM TÍNH ĐIỂM ---
def calculate_score(questions, user_answers):
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

# --- 8. HÀM HIỂN THỊ CÂU HỎI ---
def display_question(q_data, index, mode, form_key=None):
    q_id = q_data['id']
    question_text = q_data['question']
    options = q_data['options']
    correct_option_text = q_data['correct_option_text']
    
    st.markdown(f"**Câu {index + 1}** (ID: {q_id}): {question_text}")
    
    # Tạo key duy nhất cho radio button
    if mode == 'Thi thử' and form_key:
        # Tạo key duy nhất cho mỗi câu hỏi trong mỗi đề thi
        if form_key not in st.session_state.radio_keys:
            st.session_state.radio_keys[form_key] = {}
        if q_id not in st.session_state.radio_keys[form_key]:
            st.session_state.radio_keys[form_key][q_id] = f"exam_radio_{form_key}_{q_id}_{uuid.uuid4().hex[:8]}"
        radio_key = st.session_state.radio_keys[form_key][q_id]
    elif mode == 'Ôn thi':
        # Tạo key duy nhất cho mỗi câu hỏi trong chế độ ôn thi
        if f"review_{q_id}" not in st.session_state.radio_keys:
            st.session_state.radio_keys[f"review_{q_id}"] = f"review_radio_{q_id}_{uuid.uuid4().hex[:8]}"
        radio_key = st.session_state.radio_keys[f"review_{q_id}"]
    else:
        radio_key = f"radio_{q_id}_{uuid.uuid4().hex[:8]}"
    
    selected = st.session_state.answers.get(q_id, "")
    
    if st.session_state.score_submitted and mode == 'Thi thử':
        # Hiển thị kết quả sau khi nộp bài
        for i, opt in enumerate(options):
            is_correct = opt == correct_option_text
            is_selected = opt == selected
            
            style = "padding: 8px; border-radius: 5px; margin: 4px 0;"
            icon = ""
            if is_correct:
                color = "#d4edda"
                border_color = "#155724"
                icon = "✅ "
            elif is_selected and not is_correct:
                color = "#f8d7da"
                border_color = "#721c24"
                icon = "❌ "
            else:
                color = "white"
                border_color = "lightgrey"
                
            # Hiển thị tùy chọn với định dạng
            letter = chr(65 + i)
            st.markdown(
                f'<div style="{style} background-color: {color}; border: 2px solid {border_color}; padding: 10px; margin: 5px 0;">'
                f'<strong>{icon}{letter}. {opt}</strong>'
                f'</div>', 
                unsafe_allow_html=True
            )
    else:
        # Hiển thị radio button để chọn đáp án
        options_with_empty = [""] + options
        
        try:
            default_index = options_with_empty.index(selected)
        except ValueError:
            default_index = 0
        
        def format_option(x):
            if not x:
                return " "
            try:
                idx = options.index(x)
                return f"{chr(65 + idx)}. {x}"
            except ValueError:
                return x
        
        # Sử dụng container để tránh xung đột key
        with st.container():
            selected_option = st.radio(
                "Chọn đáp án:",
                options_with_empty,
                index=default_index,
                key=radio_key,
                format_func=format_option,
                label_visibility="visible"
            )
        
        if selected_option:
            st.session_state.answers[q_id] = selected_option
        elif q_id in st.session_state.answers:
            del st.session_state.answers[q_id]
            
        if mode == 'Ôn thi' and selected_option:
            if selected_option == correct_option_text:
                st.success("🎉 **CHÍNH XÁC!**")
            else:
                st.error(f"❌ **SAI!** Đáp án đúng là: **{correct_option_text}**")
        st.markdown("---")

# --- 9. CHẾ ĐỘ ÔN THI ---
def render_review_mode():
    st.header("📚 Chế độ Ôn thi")
    st.info("Trong chế độ này, bạn sẽ nhận được phản hồi ngay lập tức sau khi chọn đáp án. Đề ôn tập bao gồm 199 câu hỏi được đảo ngẫu nhiên và đáp án trong mỗi câu cũng được đảo ngẫu nhiên.")
    
    st.session_state.current_exam_index = None
    st.session_state.score_submitted = False
    
    if 'review_questions' not in st.session_state or st.button("Tải lại đề ôn tập mới (đảo câu và đáp án)"):
        # Lấy tất cả 199 câu và đảo thứ tự
        all_questions = QUIZ_DATA_RAW.copy()
        random.shuffle(all_questions)
        
        # Đảo đáp án trong mỗi câu
        shuffled_questions = []
        for q in all_questions:
            shuffled_options = q['options'].copy()
            random.shuffle(shuffled_options)
            shuffled_questions.append({
                "id": q['id'],
                "question": q['question'],
                "options": shuffled_options,
                "correct_option_text": q['correct_option_text']
            })
        
        st.session_state.review_questions = shuffled_questions
        st.session_state.answers = defaultdict(str)
        # Reset radio keys cho chế độ ôn thi
        for key in list(st.session_state.radio_keys.keys()):
            if key.startswith("review_"):
                del st.session_state.radio_keys[key]

    questions_to_review = st.session_state.review_questions
    
    for i, q_data in enumerate(questions_to_review):
        display_question(q_data, i, mode='Ôn thi')

# --- 10. CHẾ ĐỘ THI THỬ ---
def render_mock_exam_mode():
    st.header("📝 Chế độ Thi thử")
    
    # Thống kê sử dụng câu hỏi
    total_used = sum(st.session_state.question_usage_count.values())
    coverage_percentage = (len(st.session_state.question_usage_count) / TOTAL_QUESTIONS) * 100 if TOTAL_QUESTIONS > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Câu đã dùng", f"{len(st.session_state.question_usage_count)}/{TOTAL_QUESTIONS}")
    with col2:
        st.metric("🔄 Tổng lượt dùng", total_used)
    with col3:
        st.metric("🎯 Độ phủ", f"{coverage_percentage:.1f}%")
    
    exam_options = [f"Đề số {i}" for i in range(1, TOTAL_EXAMS + 1)]
    current_index = st.session_state.current_exam_index if st.session_state.current_exam_index is not None else 1
    
    # Tạo key duy nhất cho selectbox
    selectbox_key = f"exam_selector_{uuid.uuid4().hex[:8]}"
    
    selected_exam_label = st.selectbox(
        "**Chọn đề thi**",
        options=exam_options,
        index=current_index - 1,
        key=selectbox_key
    )
    
    selected_exam_index = int(selected_exam_label.split()[-1])
    
    if st.session_state.current_exam_index != selected_exam_index:
        st.session_state.current_exam_index = selected_exam_index
        st.session_state.answers = defaultdict(str)
        st.session_state.score_submitted = False

    # Tạo đề nếu chưa có
    if selected_exam_index not in st.session_state.exam_state:
        generate_smart_exam(selected_exam_index)
    
    current_exam_questions = st.session_state.exam_state[selected_exam_index]
    
    st.markdown(f"---")
    st.markdown(f"### Đề thi số {selected_exam_index}")
    st.markdown(f"**Số câu:** {QUESTIONS_PER_EXAM} câu | **Thời gian đề xuất:** 45 phút")
    
    # Hiển thị thông tin về các câu hỏi trong đề
    if selected_exam_index in st.session_state.exam_question_ids:
        with st.expander("📋 Xem danh sách câu hỏi trong đề này"):
            question_ids = st.session_state.exam_question_ids[selected_exam_index]
            st.write(f"**Các câu hỏi:** {', '.join(map(str, sorted(question_ids)))}")
            st.write(f"**Số câu hỏi duy nhất:** {len(set(question_ids))}")
    
    if st.session_state.score_submitted:
        stats, _ = calculate_score(current_exam_questions, st.session_state.answers)
        
        st.subheader(f"📊 Kết quả Đề thi số {selected_exam_index}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Điểm số", f"{stats['Điểm số']}/10", f"{stats['Số câu đúng']} câu đúng")
        col2.metric("Số câu chưa làm", stats['Số câu chưa trả lời'])
        col3.metric("Tổng số câu", stats['Tổng số câu'])

        # Đánh giá kết quả
        score = stats['Điểm số']
        if score >= 9:
            st.success("🎉 **Xuất sắc!** Bạn đã vượt qua bài thi với điểm số cao!")
        elif score >= 7:
            st.info("👍 **Khá tốt!** Bạn đã nắm vững kiến thức cơ bản.")
        elif score >= 5:
            st.warning("📚 **Cần ôn tập thêm!** Hãy xem lại các câu sai.")
        else:
            st.error("❌ **Cần cố gắng nhiều hơn!** Hãy ôn tập lại toàn bộ kiến thức.")

        st.markdown("---")
        st.subheader("Đáp án chi tiết (Đáp án đúng được tô xanh):")
        
        for i, q_data in enumerate(current_exam_questions):
            display_question(q_data, i, mode='Thi thử')
    else:
        st.info(f"Đề thi số **{selected_exam_index}** có **{QUESTIONS_PER_EXAM}** câu hỏi. Hãy hoàn thành và nộp bài!")
        st.markdown("---")
        
        # Tạo form key duy nhất cho mỗi đề thi
        form_key = f"exam_form_{selected_exam_index}"
        
        # Khởi tạo form state nếu chưa có
        if form_key not in st.session_state.exam_forms:
            st.session_state.exam_forms[form_key] = True
        
        # Sử dụng form với submit button
        with st.form(key=form_key):
            for i, q_data in enumerate(current_exam_questions):
                display_question(q_data, i, mode='Thi thử', form_key=form_key)
            
            st.markdown("---")
            
            # Tạo các cột cho nút bấm
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submitted = st.form_submit_button(
                    "NỘP BÀI VÀ CHẤM ĐIỂM 🚀",
                    use_container_width=True,
                    type="primary"
                )
            
            if submitted:
                answered_count = len(st.session_state.answers)
                if answered_count < QUESTIONS_PER_EXAM:
                    st.warning(f"Bạn mới chỉ trả lời **{answered_count}/{QUESTIONS_PER_EXAM}** câu.")
                    
                    # Tạo key duy nhất cho checkbox xác nhận
                    confirm_key = f"confirm_submit_{selected_exam_index}_{uuid.uuid4().hex[:8]}"
                    confirm = st.checkbox(
                        "Tôi xác nhận muốn nộp bài dù chưa hoàn thành", 
                        key=confirm_key
                    )
                    if not confirm:
                        st.stop()
                        
                st.session_state.score_submitted = True
                st.rerun()

# --- 11. HÀM CHÍNH ---
def main_app():
    st.set_page_config(
        layout="wide", 
        page_title="Ứng dụng Trắc nghiệm Tin học",
        page_icon="📚"
    )
    
    st.title("📚 Ứng dụng Trắc nghiệm Tin học Cơ bản")
    st.markdown("---")
    
    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/test-passed.png", width=100)
        st.markdown("### Chế độ")
        
        # Tạo key duy nhất cho selectbox chế độ
        mode_select_key = f"mode_select_{uuid.uuid4().hex[:8]}"
        
        mode_selection = st.selectbox(
            "Chọn chế độ",
            ('Ôn thi', 'Thi thử'),
            key=mode_select_key,
            index=('Ôn thi', 'Thi thử').index(st.session_state.mode)
        )
        
        # Cập nhật mode nếu thay đổi
        if st.session_state.mode != mode_selection:
            st.session_state.mode = mode_selection
            st.session_state.answers = defaultdict(str)
            st.session_state.score_submitted = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Thông tin Bài thi")
        st.markdown(f"**Tổng số câu hỏi:** {TOTAL_QUESTIONS} câu")
        st.markdown(f"**Số câu mỗi đề:** {QUESTIONS_PER_EXAM} câu")
        st.markdown(f"**Số đề thi thử:** {TOTAL_EXAMS} đề")
        
        if st.session_state.mode == 'Thi thử':
            st.markdown("---")
            st.markdown("### Quản lý Đề thi")
            
            # Tạo key duy nhất cho nút tạo lại đề
            regen_key = f"regen_btn_{uuid.uuid4().hex[:8]}"
            if st.button("🔄 Tạo lại tất cả đề thi", use_container_width=True, key=regen_key):
                regenerate_all_exams()
                st.session_state.answers = defaultdict(str)
                st.session_state.score_submitted = False
                st.success("✅ Đã tạo lại 14 đề thi mới!")
                st.rerun()
            
            # Tạo key duy nhất cho nút xem thống kê
            stats_key = f"stats_btn_{uuid.uuid4().hex[:8]}"
            if st.button("📊 Xem thống kê chi tiết", use_container_width=True, key=stats_key):
                with st.expander("Thống kê chi tiết", expanded=True):
                    st.write("**Số lần sử dụng mỗi câu hỏi:**")
                    usage_items = sorted(st.session_state.question_usage_count.items(), key=lambda x: x[1], reverse=True)
                    
                    if usage_items:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Câu dùng nhiều nhất:**")
                            for q_id, count in usage_items[:5]:
                                st.write(f"Câu {q_id}: {count} lần")
                        with col2:
                            st.write("**Câu dùng ít nhất:**")
                            for q_id, count in usage_items[-5:]:
                                st.write(f"Câu {q_id}: {count} lần")
                        
                        # Thống kê phân phối
                        st.write("**Phân phối số lần sử dụng:**")
                        max_usage = max(usage_items, key=lambda x: x[1])[1]
                        for i in range(max_usage + 1):
                            count = sum(1 for _, usage in usage_items if usage == i)
                            if count > 0:
                                st.write(f"- Dùng {i} lần: {count} câu")
                    else:
                        st.info("Chưa có dữ liệu thống kê")
        
        st.markdown("---")
        st.markdown("### Hướng dẫn")
        st.markdown("""
        - **Ôn thi:** Xem đáp án ngay sau khi chọn
        - **Thi thử:** Làm bài như thi thật, chấm điểm sau khi nộp
        - Mỗi đề 30 câu, ưu tiên dùng hết 199 câu trước khi lặp
        - Có 14 đề thi thử khác nhau
        """)
    
    # Main content
    if st.session_state.mode == 'Ôn thi':
        render_review_mode()
    elif st.session_state.mode == 'Thi thử':
        render_mock_exam_mode()

if __name__ == "__main__":

    main_app()
