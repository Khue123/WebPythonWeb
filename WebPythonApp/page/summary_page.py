import streamlit as st
from utils.ai_service import get_ai_response
from utils.tts_service import text_to_speech

def render():
    """Hiển thị trang tóm tắt văn bản"""
    # Đầu trang có biểu tượng hấp dẫn
    col1, col2 = st.columns([1, 9])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2665/2665093.png", width=60)
    with col2:
        st.header("Tóm tắt văn bản")
    
    # Hiển thị thông báo nếu chưa cung cấp API key
    if not st.session_state.api_key:
        st.info("🔑 Vui lòng nhập Google AI API Key trong phần cài đặt để sử dụng tính năng tóm tắt", icon="ℹ️")
    
    # Vùng nhập văn bản với placeholder hữu ích
    text_to_summarize = st.text_area(
        "Nhập văn bản cần tóm tắt",
        height=250,
        placeholder="Dán văn bản dài của bạn vào đây để AI tóm tắt thành những ý chính...",
        key="summary_input"
    )
    
    # Các tùy chọn tóm tắt
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.select_slider(
            "Độ dài bản tóm tắt",
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
    
    # Nút tóm tắt đẹp hơn
    summarize_button = st.button("📝 Tóm tắt ngay", use_container_width=True, type="primary", key="summarize_btn")
    
    # Xử lý khi nhấn nút tóm tắt
    if summarize_button:
        if not text_to_summarize:
            st.warning("⚠️ Vui lòng nhập văn bản cần tóm tắt", icon="📄")
            return
            
        if not st.session_state.api_key:
            st.error("⚠️ Bạn cần nhập API Key trước khi sử dụng tính năng này", icon="🔒")
            return
            
        with st.spinner("AI đang tóm tắt văn bản..."):
            # Tạo prompt dựa trên các tùy chọn người dùng
            prompt = f"""Hãy tóm tắt văn bản sau với độ dài {summary_length.lower()} 
            theo phong cách {summary_style.lower()}. Đảm bảo giữ lại các ý chính và 
            bỏ qua các chi tiết không quan trọng:\n\n{text_to_summarize}"""
            
            summary = get_ai_response(
                prompt, 
                st.session_state.selected_model, 
                st.session_state.api_key
            )
            
            # Hiển thị kết quả trong một container đẹp mắt
            st.success("✅ Tạo bản tóm tắt thành công!")
            result_container = st.container(border=True)
            with result_container:
                st.subheader("📋 Bản tóm tắt")
                st.markdown(summary)
                
                # Chuyển bản tóm tắt thành giọng nói
                with st.spinner("Đang chuyển đổi thành giọng nói..."):
                    audio_path = text_to_speech(
                        summary, 
                        st.session_state.tts_language, 
                        st.session_state.tts_speed
                    )
                    if audio_path:
                        st.audio(audio_path, format="audio/mp3")
                        
                        # Tạo nút tải xuống văn bản và âm thanh
                        col1, col2 = st.columns(2)
                        with col1:
                            with open(audio_path, "rb") as file:
                                st.download_button(
                                    label="🔊 Tải xuống âm thanh",
                                    data=file,
                                    file_name="summary.mp3",
                                    mime="audio/mp3",
                                    use_container_width=True,
                                    key="download_audio_btn"
                                )
                        with col2:
                            st.download_button(
                                label="📄 Tải xuống văn bản",
                                data=summary,
                                file_name="summary.txt",
                                mime="text/plain",
                                use_container_width=True,
                                key="download_text_btn"
                            )