from app import create_app, db
from app.models import FishConfig
import os

app = create_app()

def check_and_seed_data():
    """Hàm tự động kiểm tra Database và nạp dữ liệu mẫu nếu thiếu"""
    
    # 1. Tự động tạo bảng nếu chưa có (Fix lỗi 'no such table')
    db.create_all()
    print("[INFO] Đã kiểm tra cấu trúc Database.")

    # 2. Kiểm tra xem đã có dữ liệu cá chưa
    # Nếu chưa có con cá nào thì nạp danh sách mẫu vào
    if not FishConfig.query.first():
        print("--- [INFO] Database chưa có dữ liệu cá. Đang nạp mẫu... ---")
        
        # Danh sách cá mẫu (Lấy từ init_db.py sang)
        fish_list = [
            # Cá thường (Rarity 1)
            {"name": "Cá Rô Phi", "image": "ca_ro.png", "rarity": 1, "price": 10, "diff": 1},
            {"name": "Cá Diếc", "image": "ca_diec.png", "rarity": 1, "price": 15, "diff": 1},
            
            # Cá hiếm (Rarity 2-3)
            {"name": "Cá Trắm Đen", "image": "ca_tram.png", "rarity": 2, "price": 50, "diff": 2},
            {"name": "Cá Hồi", "image": "ca_hoi.png", "rarity": 3, "price": 120, "diff": 3},
            
            # Cá huyền thoại (Rarity 4-5)
            {"name": "Cá Ngừ Đại Dương", "image": "ca_ngu.png", "rarity": 4, "price": 300, "diff": 4},
            {"name": "Cá Mập Trắng", "image": "ca_map.png", "rarity": 5, "price": 1000, "diff": 5},
        ]

        for fish_data in fish_list:
            new_fish = FishConfig(
                name=fish_data["name"],
                image_url=fish_data["image"],
                rarity=fish_data["rarity"],
                base_price=fish_data["price"],
                difficulty=fish_data["diff"]
            )
            db.session.add(new_fish)
        
        db.session.commit()
        print("--- [SUCCESS] Đã khởi tạo Database và nạp cá thành công! ---")
    else:
        print("--- [INFO] Database đã có dữ liệu. Sẵn sàng chiến! ---")

if __name__ == '__main__':
    # Chạy lệnh kiểm tra DB trong ngữ cảnh ứng dụng trước khi bật server
    with app.app_context():
        check_and_seed_data()

    # Debug=True giúp server tự reload khi sửa code
    print("--- [START] Đang khởi động Server... ---")
    app.run(debug=True, port=5000)