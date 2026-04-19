# Book Translator

Ứng dụng dịch truyện (web/file) sang tiếng Việt bằng Gemini, hỗ trợ tạo EPUB và theo dõi tiến độ dịch theo chương.

## Tính năng chính
- Dịch từ URL truyện hoặc từ file/folder `.txt`.
- Tạo EPUB sau khi dịch xong.
- Cho phép chọn model Gemini trực tiếp trong UI.
- Hỗ trợ model mới (mặc định ưu tiên dòng Gemini 2.5).
- Tự động retry bằng model chất lượng cao khi cần.
- Lưu lịch sử tác vụ và theo dõi tiến độ theo chương.

## Yêu cầu môi trường
- Python 3.10+ (khuyến nghị).
- `pip`.
- API key Gemini (Google AI Studio).

## Cài đặt nhanh
```bash
git clone https://github.com/hoanggiakhoa94/book-translator.git
cd book-translator

python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows (cmd)
# .venv\Scripts\Activate.ps1 # Windows (PowerShell)

pip install -r requirements.txt
```

## Cấu hình API key
Ứng dụng đọc key từ biến môi trường `GEMINI_API_KEY` hoặc bạn có thể nhập trong màn hình Settings.

```bash
export GEMINI_API_KEY="your_key_here"
```

Lưu ý bảo mật:
- Không hardcode key trong code.
- Không commit file chứa key lên git.

## Chạy ứng dụng
### GUI
```bash
python __main__.py
```

### CLI (tuỳ chọn)
```bash
python cli.py \
  --book_url "<url>" \
  --model-name "gemini-2.5-flash" \
  --prompt_style 1 \
  --output_directory "<thu_muc_output>"
```

## Model Gemini
- Mặc định: `gemini-2.5-flash`.
- Retry chất lượng cao: `gemini-2.5-pro`.
- Bạn có thể gõ thủ công model mới trong dropdown nếu Google phát hành model mới.

## Cấu trúc thư mục chính
- `gui/`: giao diện PyQt5.
- `translator/`: logic dịch và quản lý model/prompt.
- `downloader/`: tải chương từ các nguồn web.
- `epub/`: sinh file EPUB.
- `config/`: cấu hình model/prompt/settings.

## Hướng dẫn Git/GitHub (dễ hiểu)
### 1) Đồng bộ mã mới nhất
```bash
git pull
```

### 2) Tạo branch làm việc
```bash
git checkout -b feature/ten-tinh-nang
```

### 3) Commit thay đổi
```bash
git add .
git commit -m "feat: mo ta ngan gon thay doi"
```

### 4) Push branch lên GitHub
```bash
git push -u origin feature/ten-tinh-nang
```

### 5) Mở Pull Request
- Lên GitHub repo, chọn branch vừa push, tạo Pull Request.
- Mô tả rõ: mục tiêu, thay đổi chính, cách test.

## Troubleshooting nhanh
- Lỗi thiếu package: chạy lại `pip install -r requirements.txt` trong `.venv`.
- Lỗi API key: kiểm tra `GEMINI_API_KEY` hoặc nhập lại trong Settings.
- App báo lỗi font trên macOS: cảnh báo này không chặn chạy app.
