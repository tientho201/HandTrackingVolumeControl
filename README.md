# Hand Tracking Control

Ứng dụng điều khiển máy tính bằng cử chỉ tay sử dụng thư viện MediaPipe và OpenCV.

## Tính năng

- Nhận diện và theo dõi bàn tay trong thời gian thực sử dụng MediaPipe
- Điều khiển âm lượng hệ thống bằng cử chỉ tay
- Giao diện trực quan với thanh hiển thị âm lượng
- Hỗ trợ nhận diện nhiều bàn tay cùng lúc (tối đa 2 bàn tay)
- Hiển thị 21 điểm mốc trên bàn tay

## Yêu cầu hệ thống

- Python 3.x
- Webcam
- Windows OS (cho tính năng điều khiển âm lượng)

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/your-repo/Hand_Tracking_Control.git
cd Hand_Tracking_Control
```
2. Cài đặt môi trường ảo
```bash
python -m venv .venv
```

3. Chạy môi trường ảo
```bash
.\.venv\Scripts\activate
```

4. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Cách sử dụng

1. Chạy chương trình:
```bash
python src/main.py
```

2. Các thao tác:
- Đưa bàn tay vào khung hình camera
- Để điều chỉnh âm lượng:
  - Sử dụng ngón cái (landmark 4) và ngón trỏ (landmark 8)
  - Khoảng cách giữa hai ngón tay sẽ quyết định mức âm lượng
  - Khoảng cách càng lớn, âm lượng càng cao
  - Khoảng cách < 30px sẽ hiển thị màu khác để báo hiệu
- Nhấn 'q' để thoát chương trình

## Cấu trúc dự án

```
Hand_Tracking_Control/
├── src/
│   ├── hand_tracking.py    # Module nhận diện bàn tay
│   └── volume_control.py   # Module điều khiển âm lượng
├── main.py                 # File chính chạy ứng dụng
├── requirements.txt        # Danh sách thư viện cần thiết
└── README.md               # Tài liệu hướng dẫn
```

## Chi tiết kỹ thuật

### Hand Tracking Module
- Sử dụng MediaPipe Hands để nhận diện bàn tay
- Có thể nhận diện tối đa 2 bàn tay cùng lúc
- Độ chính xác nhận diện: 70% (detectionCon = 0.7)
- Độ chính xác theo dõi: 50% (trackCon = 0.5)
- Hiển thị 21 điểm mốc trên bàn tay với các màu sắc khác nhau

### Volume Control Module
- Sử dụng PyCAW để điều khiển âm lượng hệ thống Windows
- Khoảng cách điều chỉnh âm lượng:
  - Tối thiểu: 20px
  - Tối đa: 200px
- Thanh hiển thị âm lượng:
  - Vị trí: (50, 200) đến (85, 400)
  - Hiển thị phần trăm âm lượng bên dưới thanh

## Công nghệ sử dụng

- OpenCV: Xử lý hình ảnh và video
- MediaPipe: Nhận diện và theo dõi bàn tay
- PyCAW: Điều khiển âm lượng hệ thống Windows
- NumPy: Xử lý dữ liệu số và tính toán

## Lưu ý

- Đảm bảo có đủ ánh sáng khi sử dụng
- Giữ bàn tay trong khung hình camera
- Có thể điều chỉnh các thông số sau trong code:
  - `maxHand`: Số lượng bàn tay tối đa có thể nhận diện
  - `detectionCon`: Độ chính xác nhận diện
  - `trackCon`: Độ chính xác theo dõi
  - `min_dist`, `max_dist`: Khoảng cách điều chỉnh âm lượng
  - `minBar`, `maxBar`: Kích thước thanh hiển thị âm lượng


## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request để đóng góp.

