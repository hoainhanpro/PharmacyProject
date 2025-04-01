# 🏥 Hệ Thống Quản Lý Nhà Thuốc (Pharmacy Management System)

Hệ thống quản lý nhà thuốc kết hợp chatbot hỗ trợ chẩn đoán sức khỏe, được phát triển bằng Python, Flask và Rasa.

## 📚 Giới thiệu

Dự án **PharmacyProject** là một hệ thống tích hợp nhiều tính năng giúp quản lý toàn diện hoạt động của nhà thuốc, bao gồm:

- 💊 Quản lý thuốc và sản phẩm
- 👨‍⚕️ Quản lý nhân viên
- 🛒 Hệ thống bán hàng và giỏ hàng
- 🧾 Quản lý hóa đơn
- 🚚 Quản lý giao hàng
- 🤖 Chatbot tư vấn sức khỏe và hỗ trợ chẩn đoán bệnh

## 🧰 Công nghệ sử dụng

- **Python 3.x**: Ngôn ngữ lập trình chính
- **Flask**: Framework web cho giao diện người dùng
- **Rasa**: Framework xây dựng chatbot AI
- **MySQL**: Cơ sở dữ liệu
- **Scikit-learn**: Thư viện học máy cho việc dự đoán bệnh
- **Bootstrap**: Framework CSS cho giao diện

## 🛠️ Cài đặt

### Yêu cầu hệ thống

- Python 3.x
- MySQL Server
- Pip (Package Installer for Python)

### Các bước cài đặt

1. **Clone dự án**

```bash
git clone <repository-url>
cd PharmacyProject
```

2. **Tạo và kích hoạt môi trường ảo**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Cài đặt các thư viện**

```bash
pip install -r requirements.txt
```

4. **Cấu hình cơ sở dữ liệu**

Tạo file `.env` tại thư mục gốc của dự án với nội dung:

```
HOST=<database-host>
USER=<database-user>
PASSWORD=<database-password>
DATABASE=<database-name>
SSL_CA_PATH=<path-to-ssl-certificate>
```

5. **Khởi động Rasa server**

```bash
# Đào tạo mô hình Rasa nếu chưa có
rasa train

# Khởi động Rasa server
rasa run --enable-api
```

6. **Khởi động Rasa Action server**

```bash
rasa run actions
```

7. **Khởi động ứng dụng Flask**

```bash
cd app
python app.py
```

Sau khi hoàn tất, ứng dụng web sẽ được khởi chạy tại địa chỉ `http://localhost:5000`.

## 📋 Cấu trúc dự án

```
PharmacyProject/
├── actions/                # Custom actions cho Rasa
│   └── actions.py         # Các action tùy chỉnh cho chatbot
├── app/                    # Ứng dụng Flask
│   ├── routes/            # Các route của ứng dụng
│   ├── services/          # Các service như kết nối database
│   ├── static/            # CSS, JS, hình ảnh
│   ├── templates/         # HTML templates
│   └── app.py             # Entry point của ứng dụng Flask
├── data/                   # Dữ liệu cho Rasa
│   ├── nlu.yml            # Dữ liệu NLU training
│   ├── rules.yml          # Rules cho conversational flow
│   ├── stories.yml        # Stories cho conversational flow
│   ├── dataset.csv        # Dataset cho mô hình dự đoán bệnh
│   └── disease_description.csv  # Mô tả về các loại bệnh
├── models/                 # Mô hình đã đào tạo
├── tests/                  # Unit tests
├── config.yml              # Cấu hình Rasa
├── credentials.yml         # Credentials cho Rasa channels
├── domain.yml              # Domain cho Rasa
├── endpoints.yml           # Endpoints cho Rasa
└── requirements.txt        # Các thư viện cần thiết
```

## 👥 Vai trò người dùng

Hệ thống hỗ trợ ba vai trò chính:

1. **QUANLY (Quản lý)**:
   - Quản lý dataset và đào tạo mô hình
   - Quản lý nhân viên
   - Quản lý thuốc và sản phẩm
   - Xem danh sách hóa đơn và chi tiết

2. **NHANVIENGIAOHANG (Nhân viên giao hàng)**:
   - Xem danh sách đơn hàng cần giao
   - Nhận đơn giao hàng
   - Cập nhật trạng thái đơn hàng

3. **khachhang (Khách hàng)**:
   - Xem danh sách sản phẩm
   - Thêm sản phẩm vào giỏ hàng
   - Thanh toán đơn hàng
   - Xem lịch sử đơn hàng
   - Tương tác với chatbot để tư vấn sức khỏe

## 🤖 Chatbot hỗ trợ chẩn đoán sức khỏe

Chatbot tích hợp trong hệ thống có khả năng:
- Tiếp nhận triệu chứng từ người dùng
- Dự đoán bệnh dựa trên các triệu chứng
- Cung cấp thông tin về bệnh và cách phòng ngừa
- Lưu trữ các triệu chứng và kết quả chẩn đoán vào cơ sở dữ liệu

## 🔒 Bảo mật

- Hệ thống kiểm soát quyền truy cập dựa trên vai trò người dùng
- Mật khẩu được mã hóa trước khi lưu vào cơ sở dữ liệu
- Phiên làm việc được bảo vệ với secret key

## 📝 Sử dụng

1. **Đăng nhập vào hệ thống**:
   - Truy cập `http://localhost:5000/login`
   - Nhập thông tin đăng nhập tương ứng với vai trò

2. **Sử dụng chatbot**:
   - Chatbot được tích hợp trong giao diện người dùng
   - Nhập triệu chứng bạn đang gặp phải
   - Chatbot sẽ hỏi thêm thông tin và đưa ra dự đoán về bệnh

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork dự án
2. Tạo nhánh tính năng mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi (`git commit -m 'Add some amazing feature'`)
4. Push lên nhánh (`git push origin feature/amazing-feature`)
5. Tạo Pull Request mới

## 📜 Giấy phép

Phân phối theo giấy phép MIT. Xem `LICENSE` để biết thêm thông tin. 