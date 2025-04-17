import streamlit as st
import config
from utils.ai_service import get_ai_response
from utils.tts_service import text_to_speech
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

# Thiết lập cấu hình trang PHẢI ĐẶT TRƯỚC TIÊN
st.set_page_config(
    page_title="Google AI Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo session state và thiết lập sidebar
config.initialize_session_state()
config.setup_sidebar()

def render_chat():
    """Hiển thị giao diện trò chuyện"""

    # Container cho header
    header_container = st.container()
    with header_container:
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/2665/2665038.png", width=60)
        with col2:
            st.header("Trò chuyện với AI")
    
    # Kiểm tra API key
    if not st.session_state.api_key:
        st.info("🔑 Vui lòng nhập Google AI API Key trong phần cài đặt để bắt đầu trò chuyện", icon="ℹ️")
        st.divider()
    
    # Container chính với class để thêm padding
    main_chat_container = st.container()
    with main_chat_container:
        # Nút xóa lịch sử ở trên cùng nếu có tin nhắn
        if st.session_state.chat_history:
            if st.button("🗑️ Xóa lịch sử trò chuyện", use_container_width=True, key="clear_history"):
                st.session_state.chat_history = []
                st.rerun()
        
        # Hiển thị lịch sử chat
        for idx, message in enumerate(st.session_state.chat_history):
            role_icon = "🧑‍💻" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=role_icon):
                st.markdown(message["content"])
                if message["role"] == "assistant":
                    # Thêm nút copy cho mỗi tin nhắn
                    col1, col2 = st.columns([6, 1])
                    with col2:
                        if st.button("📋 Copy", key=f"copy_{idx}", help="Copy nội dung"):
                            import pyperclip
                            pyperclip.copy(message["content"])
                            st.success("✅ Đã copy!", icon="✅")
    
    # Chat input với key duy nhất
    if "chat_input_key" not in st.session_state:
        st.session_state.chat_input_key = 0

    user_input = st.chat_input(
        "Nhập câu hỏi của bạn...", 
        key=f"chat_input_{st.session_state.chat_input_key}"
    )
    
    if user_input:
        if not st.session_state.api_key:
            st.error("⚠️ Bạn cần nhập API Key trước khi gửi tin nhắn", icon="🔒")
            return
            
        # Hiển thị tin nhắn người dùng
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)
        
        # Lưu tin nhắn người dùng
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Hiển thị phản hồi AI
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("AI đang suy nghĩ..."):
                response = get_ai_response(
                    user_input, 
                    st.session_state.selected_model, 
                    st.session_state.api_key
                )
                st.markdown(response)
                # Thêm nút copy cho response mới
                col1, col2 = st.columns([6, 1])
                with col2:
                    if st.button("📋 Copy", key=f"copy_new", help="Copy nội dung"):
                        import pyperclip
                        pyperclip.copy(response)
                        st.success("✅ Đã copy!", icon="✅")
        
        # Lưu phản hồi AI
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": response
        })
        
        # Tăng key cho lần nhập tiếp theo
        st.session_state.chat_input_key += 1
        st.rerun()

def render_summary():
    """Hiển thị giao diện tóm tắt văn bản"""
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665184.png", width=60)
    with col2:
        st.header("Tóm tắt văn bản")
    
    # Tạo tabs cho hai chế độ tóm tắt
    summary_type = st.radio(
        "Chọn nguồn văn bản",
        options=["📝 Nhập văn bản", "🔗 Từ URL"],
        horizontal=True,
        key="summary_type"
    )
    
    st.divider()
    
    # Tab nhập văn bản trực tiếp
    if summary_type == "📝 Nhập văn bản":
        text_to_summarize = st.text_area(
            "Nhập văn bản cần tóm tắt",
            height=200,
            placeholder="Dán văn bản cần tóm tắt vào đây...",
            key="summary_input"
        )
        input_text = text_to_summarize
        
    # Tab nhập URL
    else:
        url_input = st.text_input(
            "Nhập URL cần tóm tắt nội dung",
            placeholder="https://example.com/article",
            key="url_input"
        )
        
        if url_input:
            try:
                with st.spinner("Đang tải nội dung từ URL..."):
                    response = requests.get(url_input)
                    response.raise_for_status()  # Kiểm tra lỗi HTTP
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Loại bỏ các thẻ script và style
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Lấy text từ trang web
                    text = soup.get_text()
                    
                    # Xử lý text: loại bỏ khoảng trắng thừa và dòng trống
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    # Hiển thị preview của nội dung
                    with st.expander("Xem trước nội dung", expanded=False):
                        st.text_area("Nội dung từ URL", value=text, height=200, disabled=True)
                    
                    input_text = text
                    
            except Exception as e:
                st.error(f"❌ Không thể tải nội dung từ URL. Lỗi: {str(e)}")
                return
        else:
            input_text = ""
    
    # Các tùy chọn tóm tắt
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.select_slider(
            "Độ dài",
            options=["Rất ngắn", "Ngắn", "Trung bình", "Dài", "Chi tiết"],
            value="Trung bình",
            key="summary_length"
        )
    with col2:
        summary_style = st.radio(
            "Phong cách",
            options=["Tóm lược", "Điểm chính", "Phân tích"],
            horizontal=True,
            key="summary_style"
        )
    
    # Nút tóm tắt
    summarize_button = st.button(
        "📝 Tóm tắt ngay", 
        use_container_width=True, 
        type="primary", 
        key="summarize_btn"
    )
    
    if summarize_button:
        if not input_text:
            st.warning("⚠️ Vui lòng nhập văn bản hoặc URL cần tóm tắt", icon="📄")
            return
            
        if not st.session_state.api_key:
            st.error("⚠️ Bạn cần nhập API Key trước khi sử dụng tính năng này", icon="🔒")
            return
            
        with st.spinner("AI đang tóm tắt văn bản..."):
            prompt = f"""Hãy tóm tắt văn bản sau với độ dài {summary_length.lower()} 
            theo phong cách {summary_style.lower()}. Đảm bảo giữ lại các ý chính và 
            bỏ qua các chi tiết không quan trọng:\n\n{input_text}"""
            
            summary = get_ai_response(
                prompt, 
                st.session_state.selected_model, 
                st.session_state.api_key
            )
            
            # Lưu summary vào session state
            st.session_state.current_summary = summary
            
    # Hiển thị kết quả nếu có trong session state
    if 'current_summary' in st.session_state and st.session_state.current_summary:
        st.success("✅ Tạo bản tóm tắt thành công!")
        result_container = st.container(border=True)
        with result_container:
            # Tạo header với nút copy
            header_col1, header_col2 = st.columns([5, 1])
            with header_col1:
                st.subheader("📋 Bản tóm tắt")
            with header_col2:
                if st.button("📋 Copy", key="copy_summary", help="Copy nội dung tóm tắt"):
                    import pyperclip
                    pyperclip.copy(st.session_state.current_summary)
                    st.success("✅ Đã copy!", icon="✅")
            
            # Hiển thị nội dung tóm tắt
            st.markdown(st.session_state.current_summary)
            
            # Nút tải xuống
            st.download_button(
                label="📄 Tải xuống văn bản",
                data=st.session_state.current_summary,
                file_name="summary.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_text_btn"
            )

def render_tts():
    """Hiển thị giao diện chuyển văn bản thành giọng nói"""
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665184.png", width=60)
    with col2:
        st.header("Chuyển văn bản thành giọng nói")
    
    st.info(
        f"🔊 Đang sử dụng: "
        f"{config.LANGUAGE_DISPLAY.get(st.session_state.tts_language, st.session_state.tts_language)} | "
        f"Tốc độ: {st.session_state.tts_speed}x", icon="🎛️"
    )
    
    text_for_speech = st.text_area(
        "Nhập văn bản cần chuyển thành giọng nói",
        height=200,
        placeholder="Nhập nội dung bạn muốn chuyển thành giọng nói tại đây...",
        key="tts_input"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        tts_button = st.button("🎤 Chuyển văn bản thành giọng nói", use_container_width=True, type="primary", key="tts_btn")
    with col2:
        clear_button = st.button("🗑️ Xóa", use_container_width=True, key="clear_tts_btn")
        if clear_button:
            st.session_state.text_for_speech = ""
            st.rerun()
    
    if tts_button and text_for_speech:
        with st.spinner("Đang chuyển đổi văn bản thành giọng nói..."):
            audio_path = text_to_speech(
                text_for_speech, 
                st.session_state.tts_language, 
                st.session_state.tts_speed
            )
            
            if audio_path:
                result_container = st.container(border=True)
                with result_container:
                    st.subheader("🎵 Kết quả âm thanh")
                    st.audio(audio_path, format="audio/mp3")
                    
                    # Thêm nút copy cho văn bản
                    col1, col2 = st.columns([5, 1])
                    with col2:
                        if st.button("📋 Copy", key="copy_tts", help="Copy nội dung văn bản"):
                            import pyperclip
                            pyperclip.copy(text_for_speech)
                            st.success("✅ Đã copy!", icon="✅")
                    
                    with open(audio_path, "rb") as file:
                        st.download_button(
                            label="💾 Tải xuống âm thanh",
                            data=file,
                            file_name="speech.mp3",
                            mime="audio/mp3",
                            use_container_width=True,
                            key="download_tts_btn"
                        )

# Thiết lập các tab chức năng với biểu tượng
tab_icons = ["💬", "📝", "🔊"]
tab_names = ["Trò chuyện", "Tóm tắt văn bản", "Chuyển văn bản thành giọng nói"]
tabs = st.tabs([f"{icon} {name}" for icon, name in zip(tab_icons, tab_names)])

# Render các trang chức năng dựa trên tab được chọn
with tabs[0]:
    render_chat()
with tabs[1]:
    render_summary()
with tabs[2]:
    render_tts()