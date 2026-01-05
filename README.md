# 🎣 Web Fishing Game

**Web Fishing Game** là một trò chơi câu cá chạy trên nền web được xây dựng bằng **Python (Flask)** cho phía server và **HTML/CSS/JS** cho giao diện người dùng. Người chơi sẽ vào vai một ngư dân, thực hiện các minigame để câu cá, bán lấy vàng và nâng cấp trang bị.

---

## 📋 1. Yêu Cầu Hệ Thống

* **Python**: Phiên bản 3.x trở lên.
* **Hệ điều hành**: Windows, macOS, hoặc Linux.
* **Trình duyệt web**: Chrome, Firefox, Edge, Safari, v.v.

---

## 📂 2. Cấu Trúc Dự Án

Cấu trúc thư mục của dự án được chia tách rõ ràng:

* **`backend/`**: Chứa mã nguồn server (Flask API, Database Model, Logic game).
    * `run.py`: File khởi động server.
    * `instance/fishing.db`: Database SQLite (tự động tạo khi chạy lần đầu).
* **`frontend/`**: Chứa giao diện người dùng.
    * `templates/`: Các file HTML.
    * `static/`: Các file CSS, JavaScript, hình ảnh.

---

## ⚙️ 3. Hướng Dẫn Cài Đặt

Làm theo các bước sau để thiết lập môi trường chạy game:

### Bước 1: Mở terminal tại thư mục gốc
Đảm bảo bạn đang đứng ở thư mục chứa cả 2 thư mục con là `backend` và `frontend`.

### Bước 2: Tạo môi trường ảo (Virtual Environment) - *Khuyên dùng*
Giúp tránh xung đột thư viện với các dự án khác.

* **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
* **macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### Bước 3: Cài đặt các thư viện cần thiết
Chạy lệnh sau để cài đặt Flask và các thư viện hỗ trợ (được liệt kê trong `requirements.txt`):

```bash
pip install -r backend/requirements.txt

🚀 4. Hướng Dẫn Chạy Game
Mỗi khi muốn chơi, bạn thực hiện các bước sau:

Di chuyển vào thư mục backend:

Bash

cd backend
Khởi chạy Server:

Bash

python run.py
Lưu ý: Lần chạy đầu tiên, hệ thống sẽ tự động tạo Database và nạp dữ liệu cá mẫu (Cá Rô, Cá Trắm, Cá Mập...) nên bạn không cần cấu hình DB thủ công.

Vào game:

Mở trình duyệt và truy cập địa chỉ: http://127.0.0.1:5000

Nếu chưa có tài khoản, hãy nhấn Đăng ký để tạo nhân vật mới (bạn sẽ được tặng 100 Vàng và Cần câu Lv.1).

🎮 5. Hướng Dẫn Chơi (Gameplay)
Trò chơi mô phỏng việc câu cá thông qua 2 giai đoạn minigame phản xạ:

Bước 1: Quăng Cần (Giai đoạn Nhảy Nút)
Sau khi bấm "QUĂNG CẦN", một chuỗi mũi tên sẽ hiện ra. Bạn dùng 4 phím mũi tên trên bàn phím để thao tác:

🟢 Mũi tên Xanh (Lá/Dương): Bấm phím mũi tên CÙNG CHIỀU với hình hiển thị.

🔴 Mũi tên Đỏ (TRAP): Đây là bẫy! Bạn phải bấm phím mũi tên NGƯỢC CHIỀU (Ví dụ: Thấy ⬆️ Đỏ thì phải bấm ⬇️).

Nếu bấm sai, cá sẽ chạy mất ngay lập tức!

Bước 2: Giật Cá (Giai đoạn Canh Lực - Space)
Nếu vượt qua Bước 1, một thanh trượt (slider) sẽ xuất hiện.

Một con trỏ sẽ chạy qua chạy lại liên tục.

Nhiệm vụ: Bấm phím Space (Cách) đúng lúc con trỏ nằm trong vùng màu vàng.

Cá càng hiếm, thanh trượt chạy càng nhanh hoặc vùng vàng càng nhỏ.

Bước 3: Thu Hoạch & Bán Cá
Nếu thành công cả 2 bước, bạn sẽ nhận được cá và điểm kinh nghiệm (EXP).

Cá câu được sẽ nằm trong Túi Đồ (bên dưới màn hình chơi).

Bạn có thể bấm nút Bán ở từng con cá để đổi lấy Vàng.

🛠️ Xử Lý Lỗi Thường Gặp
Lỗi ModuleNotFoundError: Do chưa cài đủ thư viện. Hãy kiểm tra lại Bước 3 phần Cài đặt.

Lỗi no such table: Thường do DB chưa khởi tạo kịp hoặc bị lỗi file. Hãy xóa file backend/instance/fishing.db đi, sau đó chạy lại lệnh python run.py để server tự tạo lại DB mới sạch sẽ.

Lỗi không tìm thấy template/static: Đảm bảo bạn đang chạy file run.py từ bên trong thư mục backend, và cấu trúc thư mục frontend nằm đúng vị trí ngang hàng với backend.