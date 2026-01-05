<div align="center">

# 🎣 WEB FISHING GAME

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Trò chơi câu cá giả lập phản xạ, xây dựng trên nền tảng Flask Framework.**

[Giới Thiệu](#-giới-thiệu) •
[Cài Đặt](#-cài-đặt) •
[Cách Chơi](#-cách-chơi) •
[Cấu Trúc](#-cấu-trúc-dự-án)

</div>

---

## 📖 Giới Thiệu

**Web Fishing Game** đưa người chơi vào vai một ngư dân tài ba. Không chỉ là click chuột, bạn cần sự tập trung cao độ và phản xạ nhanh nhạy để chinh phục những loài thủy quái hiếm có.

**Tính năng nổi bật:**

- 🎮 **Minigame kép:** Kết hợp giữa _Nhảy Audition_ (Mũi tên) và _Canh lực_ (Timing).
- 🎒 **Hệ thống túi đồ:** Lưu trữ chiến lợi phẩm, bán cá kiếm Vàng.
- 📈 **Nâng cấp:** Tích lũy kinh nghiệm (EXP) và tiền vàng (Gold).
- 🔒 **Hệ thống tài khoản:** Đăng ký/Đăng nhập bảo mật, lưu progress người chơi.

---

## 📸 Hình Ảnh Demo

_(Khu vực này để bạn chèn ảnh chụp màn hình game sau này)_

|                                    Màn Hình Chờ                                    |                                     Minigame Câu Cá                                      |
| :--------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| <img src="https://placehold.co/600x400?text=Sanh+Cho" alt="Sảnh Chờ" width="100%"> | <img src="https://placehold.co/600x400?text=Minigame+Arrow" alt="Minigame" width="100%"> |

---

## 🛠 Cài Đặt & Chạy Game

### 1. Yêu Cầu

- Python 3.x
- Git (Tùy chọn)

### 2. Các Bước Cài Đặt

**B1: Clone hoặc tải dự án về máy**
```bash
git clone [https://github.com/USERNAME/web-fishing-game.git](https://github.com/USERNAME/web-fishing-game.git)
cd web-fishing-game
```

**B2: Thiết lập môi trường ảo**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**B3: Cài đặt thư viện**
pip install -r backend/requirements.txt

### 3. Khởi Chạy
Di chuyển vào thư mục backend và chạy server:
```bash
cd backend
python run.py
```

🔥 Lưu ý: Lần chạy đầu tiên, hệ thống sẽ tự động tạo Database và nạp dữ liệu cá mẫu. Bạn không cần setup gì thêm!

Truy cập game tại: http://127.0.0.1:5000

🎮 Cách Chơi
**Quy trình câu cá gồm 2 giai đoạn thử thách:**
### Giai Đoạn 1: Phản Xạ (Arrow Phase) Nhìn kỹ màu sắc của mũi tên xuất hiện trên màn hình:Loại Mũi Tên, Màu Sắc, Hành Động Cần Làm
* Ví Dụ:
- Bình Thường🟢 Xanh Lá / 🔵 Lam Bấm CÙNG CHIỀU - Thấy ⬆️ bấm ⬆️
- Cạm Bẫy (TRAP)🔴 Đỏ Bấm NGƯỢC CHIỀU Thấy ⬆️ bấm ⬇️

### Giai Đoạn 2: Canh Lực (Timing Phase)
- Thanh trượt (Slider) sẽ chạy qua lại liên tục.
- Bấm phím Space (Cách) khi con trỏ nằm trong Vùng Màu Vàng.

```bash
web-fishing-game/
├── backend/                  # Xử lý Logic & API
│   ├── app/
│   │   ├── models.py         # Cấu trúc Database (User, Fish, Inventory)
│   │   ├── routes/           # Định nghĩa đường dẫn (URL)
│   │   └── __init__.py       # Khởi tạo Flask App
│   ├── instance/             # Chứa file Database SQLite
│   ├── run.py                # File khởi chạy Server
│   └── requirements.txt      # Danh sách thư viện
│
├── frontend/                 # Giao diện người dùng
│   ├── static/
│   │   ├── css/              # Giao diện đẹp (Style)
│   │   └── js/               # Xử lý hiệu ứng động
│   └── templates/            # Các file HTML (Login, Game...)
│
└── README.md                 # Hướng dẫn sử dụng
````

Code by Trương Khuynh Hàn