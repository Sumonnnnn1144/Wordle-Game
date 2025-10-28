## Wordle - Python Tkinter Edition
## Cấu trúc thư mục

24127183/
│
├── main.py # Giao diện chính và xử lý sự kiện bàn phím
├── wordle_core.py # Logic xử lý game (class WordleGame)
├── allowed.txt # Danh sách các từ được phép đoán (từ hợp lệ)
├── secret.txt # Danh sách các từ có thể được chọn làm từ bí mật
└── README.md # Hướng dẫn chạy chương trình

## Yêu cầu hệ thống

- **Python 3.10+** (đã test ổn định trên 3.12, 3.13).
- Không cần cài thêm thư viện ngoài — chỉ dùng module có sẵn.

## Cách chạy chương trình
Cách 1: 

Sau khi giải nén folder 24127183.zip, nếu đã cài trước python, có thể lựa chọn file **main.py** opens with python sau đó double-click vào file **main.py**.
→ Giao diện trò chơi sẽ hiện lên ngay lập tức, kế bên đó là từ cần đoán hiển thị trên màn hình terminal.

Cách 2: 

1. Mở thư mục chứa project trong Visual Studio Code.

2. Đảm bảo đã cài Python extension (Microsoft).

3. Vào tab Run and Debug (hoặc nhấn Ctrl + Shift + D).

4. Chọn cấu hình: **Python: Current File**

5. Nhấn F5 hoặc nút ▶️ Start Debugging.

6. Cửa sổ trò chơi sẽ xuất hiện, kế bên đó là từ cần đoán hiển thị trên màn hình terminal.

## Bắt đầu chơi:

- Gõ chữ bằng bàn phím.

- Nhấn Enter để xác nhận.

- Nhấn Backspace để xóa chữ.

- Nếu nhập từ không hợp lệ → thông báo “❌ Not in word list” và có thể nhập lại từ, không trừ lượt.

- Trên cùng bên trái là thanh **Menu**, có 2 nút là **Reset Game** và **Exit**.

**Reset Game**: Làm mới toàn bộ bảng + tạo secret mới
**Exit**: Đóng cửa sổ game

## Thông tin sinh viên
Họ tên: Trần Duy Khang
MSSV: 24127183

