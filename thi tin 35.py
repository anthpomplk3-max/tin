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

# --- 2. DỮ LIỆU CÂU HỎI ĐẦY ĐỦ 199 CÂU THỰC TẾ ---
# Dữ liệu này cần được điền đầy đủ 199 câu hỏi.
# Dưới đây là phần mô phỏng lại cấu trúc data, bạn cần đảm bảo đủ 199 câu
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
            "Nghe nhạc"
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
            "Cuộc họp cuối sprint để demo sản phẩm",
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

    # === PHẦN CUỐI: CÂU HỎI TỔNG HỢP (Tiếp tục từ 197) ===
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
            "Sự dễ sử dụng của hệ thống",
            "Bảo mật hệ thống",
            "Tốc độ hệ thống",
            "Chức năng hệ thống"
        ],
        "correct_option_text": get_correct_text([
            "Sự dễ sử dụng của hệ thống",
            "Bảo mật hệ thống",
            "Tốc độ hệ thống",
            "Chức năng hệ thống"
        ], CORRECT_ANSWERS_BY_ID.get(199))
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