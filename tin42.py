import streamlit as st
import random
from collections import defaultdict
import time

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

# --- 2. DỮ LIỆU CÂU HỎI ĐẦY ĐỦ (199 CÂU) ---
# Giữ nguyên toàn bộ QUIZ_DATA_RAW như trong mã gốc
# Do giới hạn độ dài, tôi chỉ để placeholder
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
    # ... (giữ nguyên tất cả 199 câu hỏi)
    { # Q199
        "id": 199,
        "question": "Để truy cập vào một trang Web chúng ta cần phải biết:",
        "options": ["Địa chỉ của trang web", "Hệ điều hành đang sử dụng", "Trang web đó của nước nào", "Địa chỉ IP của máy tính"],
        "correct_option_text": get_correct_text(["Địa chỉ của trang web", "Hệ điều hành đang sử dụng", "Trang web đó của nước nào", "Địa chỉ IP của máy tính"], CORRECT_ANSWERS_BY_ID.get(199))
    }
]

# --- 3. CÁC HẰNG SỐ ---
TOTAL_QUESTIONS = 199
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
    if 'exam_history' not in st.session_state:
        st.session_state.exam_history = {}
    if 'form_counter' not in st.session_state:
        st.session_state.form_counter = 0

# --- 5. HÀM TẠO ĐỀ THI THÔNG MINH ---
def generate_smart_exam(exam_index):
    """Tạo đề thi thông minh: ưu tiên sử dụng hết 199 câu trước khi lặp lại"""
    
    # Khởi tạo bộ đếm nếu chưa có
    if not st.session_state.question_usage_count:
        st.session_state.question_usage_count = defaultdict(int)
    
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
            # Nếu vẫn không đủ, lặp lại từ đầu danh sách
            while len(selected_questions) < QUESTIONS_PER_EXAM:
                selected_questions.append(random.choice(all_questions))
    
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
            "correct_option_text": q_data['correct_option_text'],
            "original_options": q_data['options']
        })
        
        # Cập nhật số lần sử dụng
        st.session_state.question_usage_count[q_data['id']] += 1
    
    # Lưu đề vào session
    st.session_state.exam_state[exam_index] = exam_questions
    
    # Lưu lịch sử đề thi
    st.session_state.exam_history[exam_index] = {
        'generated_at': time.time(),
        'question_ids': [q['id'] for q in selected_questions]
    }
    
    return exam_questions

# --- 6. HÀM TẠO LẠI TẤT CẢ ĐỀ THI ---
def regenerate_all_exams():
    """Tạo lại tất cả 14 đề thi"""
    st.session_state.exam_state = {}
    st.session_state.question_usage_count = defaultdict(int)
    st.session_state.exam_history = {}
    st.session_state.form_counter += 1
    
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

# --- 8. HÀM HIỂN THỊ CÂU HỎI (SỬA LỖI KEY TRÙNG) ---
def display_question(q_data, index, mode, form_key_suffix=""):
    q_id = q_data['id']
    question_text = q_data['question']
    options = q_data['options']
    correct_option_text = q_data['correct_option_text']
    
    st.markdown(f"**Câu {index + 1}** (ID: {q_id}): {question_text}")
    
    # Tạo key duy nhất cho mỗi radio button
    if st.session_state.current_exam_index is not None:
        radio_key = f"q_{q_id}_exam_{st.session_state.current_exam_index}_form_{st.session_state.form_counter}_idx_{index}"
    else:
        radio_key = f"q_{q_id}_review_form_{st.session_state.form_counter}_idx_{index}"
    
    # Thêm form_key_suffix nếu có
    if form_key_suffix:
        radio_key += f"_{form_key_suffix}"
    
    selected = st.session_state.answers.get(q_id, "")
    options_with_empty = [""] + options
    
    try:
        default_index = options_with_empty.index(selected) if selected in options_with_empty else 0
    except ValueError:
        default_index = 0

    if st.session_state.score_submitted and mode == 'Thi thử':
        for i, opt in enumerate(options):
            is_correct = opt == correct_option_text
            is_selected = opt == selected
            
            style = "padding: 5px; border-radius: 5px; margin: 2px 0;"
            icon = ""
            if is_correct:
                color = "#d4edda"
                border_color = "#155724"
                icon = "✅"
            elif is_selected and not is_correct:
                color = "#f8d7da"
                border_color = "#721c24"
                icon = "❌"
            else:
                color = "white"
                border_color = "lightgrey"
                
            st.markdown(f'<p style="{style} background-color: {color}; border: 1px solid {border_color}; margin: 2px 0;">{icon} {opt}</p>', unsafe_allow_html=True)
    else:
        # Sửa lỗi format_func
        def format_option(x):
            if not x:
                return " "
            try:
                idx = options.index(x)
                return f"{chr(65 + idx)}. {x}"
            except ValueError:
                return x
        
        selected_option = st.radio(
            "Chọn đáp án:",
            options_with_empty,
            index=default_index,
            key=radio_key,
            format_func=format_option,
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
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Tải đề ôn tập mới"):
            st.session_state.form_counter += 1
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
            st.rerun()

    if 'review_questions' not in st.session_state or not st.session_state.review_questions:
        # Tạo đề ôn tập lần đầu
        all_questions = QUIZ_DATA_RAW.copy()
        random.shuffle(all_questions)
        
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
        st.metric("📊 Tổng câu đã dùng", f"{len(st.session_state.question_usage_count)}/{TOTAL_QUESTIONS}")
    with col2:
        st.metric("🔄 Tổng lượt sử dụng", total_used)
    with col3:
        st.metric("🎯 Độ phủ đề", f"{coverage_percentage:.1f}%")
    
    exam_options = [f"Đề số {i}" for i in range(1, TOTAL_EXAMS + 1)]
    current_index = st.session_state.current_exam_index if st.session_state.current_exam_index is not None else 1
    selected_exam_label = st.selectbox(
        "**Chọn đề thi**",
        options=exam_options,
        index=current_index - 1,
        key='exam_selector'
    )
    
    selected_exam_index = int(selected_exam_label.split()[-1])
    
    if st.session_state.current_exam_index != selected_exam_index:
        st.session_state.current_exam_index = selected_exam_index
        st.session_state.answers = defaultdict(str)
        st.session_state.score_submitted = False
        st.session_state.form_counter += 1

    # Tạo đề nếu chưa có
    if selected_exam_index not in st.session_state.exam_state:
        generate_smart_exam(selected_exam_index)
    
    current_exam_questions = st.session_state.exam_state[selected_exam_index]
    
    st.markdown(f"---")
    st.markdown(f"### Đề thi số {selected_exam_index}")
    st.markdown(f"**Số câu:** {QUESTIONS_PER_EXAM} câu | **Thời gian đề xuất:** 45 phút")
    
    # Hiển thị thông tin về các câu hỏi trong đề
    with st.expander("📋 Xem danh sách câu hỏi trong đề này"):
        question_ids = [q['id'] for q in current_exam_questions]
        st.write(f"**Các câu hỏi:** {', '.join(map(str, sorted(question_ids)))}")
        st.write(f"**Số câu hỏi duy nhất:** {len(set(question_ids))}")
    
    # Nút tạo lại đề thi cụ thể
    if st.button("🔄 Tạo lại đề này"):
        generate_smart_exam(selected_exam_index)
        st.session_state.answers = defaultdict(str)
        st.session_state.score_submitted = False
        st.session_state.form_counter += 1
        st.rerun()
    
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
        
        # Nút làm lại đề
        if st.button("🔄 Làm lại đề này"):
            st.session_state.answers = defaultdict(str)
            st.session_state.score_submitted = False
            st.session_state.form_counter += 1
            st.rerun()
            
    else:
        st.info(f"Đề thi số **{selected_exam_index}** có **{QUESTIONS_PER_EXAM}** câu hỏi. Hãy hoàn thành và nộp bài!")
        st.markdown("---")
        
        # Sử dụng form với submit button đúng cách
        with st.form(key=f"exam_form_{selected_exam_index}_{st.session_state.form_counter}"):
            for i, q_data in enumerate(current_exam_questions):
                display_question(q_data, i, mode='Thi thử', form_key_suffix=f"form_{st.session_state.form_counter}")
            
            st.markdown("---")
            
            # Sử dụng st.form_submit_button đúng cách
            submitted = st.form_submit_button("NỘP BÀI VÀ CHẤM ĐIỂM 🚀")
            
            if submitted:
                answered_count = len(st.session_state.answers)
                if answered_count < QUESTIONS_PER_EXAM:
                    st.warning(f"Bạn mới chỉ trả lời **{answered_count}/{QUESTIONS_PER_EXAM}** câu.")
                    confirm = st.checkbox("Tôi xác nhận muốn nộp bài dù chưa hoàn thành", key=f'confirm_submit_{st.session_state.form_counter}')
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
        mode_selection = st.selectbox(
            "Chọn chế độ",
            ('Ôn thi', 'Thi thử'),
            key='mode_select',
            index=('Ôn thi', 'Thi thử').index(st.session_state.mode)
        )
        st.session_state.mode = mode_selection
        
        st.markdown("---")
        st.markdown("### Thông tin Bài thi")
        st.markdown(f"**Tổng số câu hỏi:** {TOTAL_QUESTIONS} câu")
        st.markdown(f"**Số câu mỗi đề:** {QUESTIONS_PER_EXAM} câu")
        st.markdown(f"**Số đề thi thử:** {TOTAL_EXAMS} đề")
        
        if mode_selection == 'Thi thử':
            st.markdown("---")
            st.markdown("### Quản lý Đề thi")
            if st.button("🔄 Tạo lại tất cả đề thi", use_container_width=True):
                regenerate_all_exams()
                st.session_state.answers = defaultdict(str)
                st.session_state.score_submitted = False
                st.session_state.form_counter += 1
                st.success("✅ Đã tạo lại 14 đề thi mới!")
                st.rerun()
            
            if st.button("📊 Xem thống kê sử dụng câu hỏi", use_container_width=True):
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
                    else:
                        st.info("Chưa có dữ liệu thống kê")
        
        st.markdown("---")
        st.markdown("### Hướng dẫn")
        st.markdown("""
        - **Ôn thi:** Xem đáp án ngay sau khi chọn
        - **Thi thử:** Làm bài như thi thật, chấm điểm sau khi nộp
        - Mỗi đề 30 câu, ưu tiên dùng hết 199 câu trước khi lặp
        """)
    
    # Main content
    if st.session_state.mode == 'Ôn thi':
        render_review_mode()
    elif st.session_state.mode == 'Thi thử':
        render_mock_exam_mode()

if __name__ == "__main__":
    main_app()