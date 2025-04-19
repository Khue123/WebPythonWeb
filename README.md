
# Vietnamese AI Assistant

**Vietnamese AI Assistant** là một ứng dụng desktop được phát triển bằng Python và Tkinter, cho phép người dùng tương tác với API AI của Google Gemini để thực hiện nhiều tác vụ khác nhau. Ứng dụng có giao diện thân thiện, hỗ trợ đa ngôn ngữ (ưu tiên tiếng Việt) và tích hợp nhiều tính năng hữu ích.

---

## ✨ Tính Năng Chính

- **Tóm tắt văn bản**: Tóm tắt nội dung từ văn bản hoặc URL website
- **Chat với AI**: Trò chuyện trực tiếp với mô hình AI của Google Gemini
- **Chuyển văn bản thành giọng nói**: Đọc văn bản với nhiều giọng nói khác nhau
- **Tùy chỉnh cài đặt**: Cài đặt API, chọn mô hình AI và tùy chỉnh giọng nói

---

## 🚀 Yêu Cầu Hệ Thống

- Python 3.7 trở lên
- Các thư viện được liệt kê trong file `requirements.txt`
- Kết nối internet để sử dụng API của Google Gemini
- API Key từ Google AI Studio (Google Gemini)

---

## 📅 Cài Đặt

1. Clone repository hoặc tải mã nguồn về
2. Cài đặt thư viện cần thiết:

```bash
pip install -r requirements.txt
```

3. Tạo file `.env` trong thư mục gốc:

```env
GEMINI_API_KEY=your_api_key_here
```

4. Chạy ứng dụng:

```bash
python app.py
```

---

## 🔍 Hướng Dẫn Sử Dụng

### 📄 Tóm Tắt Văn Bản
- Truy cập tab **"Tóm tắt văn bản"**
- Nhập văn bản hoặc URL website
- Nhấn **"Tóm tắt"**
- Xem kết quả ở phần **"Bản tóm tắt"**
- Nhấn **"Đọc bản tóm tắt"** để nghe

### 🧵 Chat Với AI
- Truy cập tab **"Chat với AI"**
- Nhập yêu cầu và nhấn **"Gửi"** hoặc Enter
- AI sẽ phản hồi trong cửa sổ chat
- Nhấn **"Đọc phản hồi"** để nghe

### 🎙️ Chuyển Văn Bản Thành Giọng Nói
- Truy cập tab **"Chuyển văn bản thành giọng nói"**
- Nhập văn bản
- Tùy chỉnh giọng nói (nếu cần)
- Nhấn **"Đọc"** để nghe
- Nhấn **"Dừng"** để dừng

### 🔧 Cài Đặt
- Truy cập tab **"Cài đặt"**
- Thêm API key của Google Gemini
- Chọn mô hình AI phù hợp
- Tùy chỉnh ngôn ngữ, giới tính, tốc độ giọng nói
- Kiểm tra cài đặt bằng các nút tương ứng

---

## 🗃️ Cấu Trúc Mã Nguồn

- `app.py`: Khởi tạo giao diện chính và các module
- `api_manager.py`: Quản lý kết nối API Gemini
- `voice_manager.py`: Xử lý text-to-speech
- `web_scraper.py`: Trích xuất nội dung từ website
- `summarizer_module.py`: Tóm tắt văn bản
- `chat_module.py`: Trò chuyện với AI
- `tts_module.py`: Chuyển đổi văn bản -> giọng nói
- `settings_module.py`: Cài đặt hệ thống
- `ui_factory.py`: Tạo giao diện đồng nhất

---

## 🚪 Lấy API Key

1. Truy cập [Google AI Studio](https://aistudio.google.com)
2. Đăng nhập tài khoản Google
3. Tạo API Key mới
4. Sao chép và thêm vào file `.env` hoặc giao diện cài đặt

---

## ⚠️ Xử Lý Sự Cố

- **API Key lỗi**: Kiểm tra tính hợp lệ của API Key
- **Lỗi mạng**: Đảm bảo kết nối internet
- **Giọng nói không hoạt động**: Kiểm tra hệ thống có hỗ trợ TTS
- **Ứng dụng không phản hồi**: Khởi động lại hoặc kiểm tra tài nguyên hệ thống

---

## 📝 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Hãy gửi Pull Request hoặc mở Issue nếu bạn có ý tưởng cải tiến.

---

## 📋 Giấy Phép

Phần mềm này được phân phối theo giấy phép MIT.
