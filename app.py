import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang Web
st.set_page_config(page_title="Trợ lý AI của Trung", page_icon="🤖")
st.title("🤖 Chat với AI - By Trung")

# 2. Lấy API Key từ hệ thống bảo mật (Secrets)
# (Lát nữa mình sẽ hướng dẫn bạn điền key này trên web, KHÔNG điền trực tiếp vào đây)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Chưa tìm thấy API Key. Vui lòng cấu hình trong phần Secrets!")
    st.stop()

# 3. Cấu hình Model (Bạn có thể đổi tên model nếu muốn)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Khởi tạo lịch sử chat (Để AI nhớ nội dung cũ)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Hiển thị lịch sử chat lên màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Xử lý khi người dùng nhập liệu
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    # Hiện câu hỏi của người dùng
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gọi Google AI trả lời
    try:
        response = model.generate_content(prompt)
        text_response = response.text
        
        # Hiện câu trả lời của AI
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "assistant", "content": text_response})
        
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")