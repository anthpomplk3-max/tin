import streamlit as st
import random

def load_questions(content):
    questions = []
    lines = content.split("\n")
    current_question = {}
    current_text = []
    options = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("Câu"):
            # Lưu câu hỏi trước đó nếu có
            if current_question:
                current_question["question"] = "\n".join(current_text)
                current_question["options"] = options
                questions.append(current_question)
            
            # Bắt đầu câu hỏi mới
            current_question = {}
            current_text = [line]
            options = []
        elif line.startswith(("A.", "B.", "C.", "D.")):
            options.append(line)
        elif line and not line.startswith("=====") and not line.startswith("SỞ Y TẾ"):
            if not current_text:  # Nếu chưa có phần câu hỏi
                current_text.append(line)
            elif options:  # Đã có đáp án, dòng này là phần tiếp theo của đáp án cuối
                options[-1] += " " + line
            else:  # Phần mô tả câu hỏi tiếp theo
                current_text.append(line)
    
    # Thêm câu hỏi cuối cùng
    if current_question:
        current_question["question"] = "\n".join(current_text)
        current_question["options"] = options
        questions.append(current_question)
    
    return questions

def shuffle_questions_and_options(questions):
    # Tạo bản sao để không ảnh hưởng đến danh sách gốc
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)
    
    for question in shuffled_questions:
        # Tráo đáp án
        options = question["options"]
        # Tách nhãn và nội dung
        labeled_options = []
        for opt in options:
            if opt.startswith(("A.", "B.", "C.", "D.")):
                labeled_options.append((opt[0], opt[2:].strip()))
        
        # Tráo thứ tự
        random.shuffle(labeled_options)
        
        # Gán lại nhãn mới
        new_labels = ["A.", "B.", "C.", "D."]
        new_options = []
        for new_label, (old_label, content) in zip(new_labels, labeled_options):
            new_options.append(f"{new_label} {content}")
        
        question["options"] = new_options
    
    return shuffled_questions

def main():
    st.set_page_config(page_title="Đề Thi Tin Học", layout="wide")
    
    st.title("📚 Tạo Đề Thi Tin Học Cơ Bản")
    st.markdown("---")
    
    # Đọc nội dung từ file
    content = ""
    with open("Noi dung on tap Tin hoc co ban_2025.pdf", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Tải câu hỏi
    questions = load_questions(content)
    
    st.sidebar.header("Cấu hình đề thi")
    exam_number = st.sidebar.selectbox("Chọn đề số:", list(range(1, 11)))
    
    # Tạo seed ngẫu nhiên dựa trên đề số để đảm bảo mỗi đề khác nhau
    random.seed(exam_number)
    
    # Tráo câu hỏi và đáp án
    shuffled_questions = shuffle_questions_and_options(questions)
    
    # Hiển thị đề thi
    st.header(f"ĐỀ THI SỐ {exam_number}")
    st.markdown("---")
    
    for i, question in enumerate(shuffled_questions, 1):
        with st.container():
            st.subheader(f"Câu {i}:")
            st.markdown(f"**{question['question']}**")
            
            for option in question["options"]:
                st.markdown(f"- {option}")
            
            st.markdown("---")

if __name__ == "__main__":
    main()