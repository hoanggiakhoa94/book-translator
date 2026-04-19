# Book Translator

Ứng dụng dịch truyện Trung -> Việt bằng Gemini, hỗ trợ dịch từ web/file, lưu tiến độ theo chương và xuất EPUB.

## 1) Tính năng nổi bật
- Dịch truyện từ URL hoặc file/folder `.txt`.
- Chọn model Gemini trực tiếp trên giao diện.
- Hỗ trợ model Gemini mới: có thể gõ tay model bất kỳ trong ô chọn model.
- Tự động retry với model chất lượng cao khi cần.
- Hỗ trợ nhiều prompt style, giữ ngữ cảnh dịch bằng placeholder:
  - `{source_text}`
  - `{glossary}`
  - `{previous_context}`
  - `{sentences_list}`
- Xuất EPUB và theo dõi tiến độ/lịch sử dịch.

## 2) Yêu cầu
- Python 3.10+
- `pip`
- Gemini API key (tạo tại Google AI Studio)

## 3) Cài đặt nhanh
```bash
git clone https://github.com/hoanggiakhoa94/book-translator.git
cd book-translator

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Cấu hình API key
Ứng dụng đọc key theo thứ tự:
1. Biến môi trường `GEMINI_API_KEY`
2. Key đã lưu trong Settings của app

Ví dụ:
```bash
export GEMINI_API_KEY="your_key_here"
```

## 5) Chạy ứng dụng
### GUI
```bash
./.venv/bin/python __main__.py
```

### CLI (tuỳ chọn)
```bash
./.venv/bin/python cli.py \
  --book_url "<url>" \
  --model-name "gemini-2.5-flash" \
  --prompt_style 1 \
  --output_directory "<thu_muc_output>"
```

## 6) Dùng model Gemini mới hơn
- Trong màn hình dịch, ô model là `editable`.
- Bạn có thể nhập trực tiếp model mới (ví dụ dòng `gemini-2.5-*`) mà không cần sửa code.
- Nếu model retry không khả dụng, hệ thống sẽ fallback về model chính để không dừng job.

## 7) Hướng dẫn Git/GitHub dễ hiểu
### Quy trình chuẩn mỗi lần làm việc
```bash
git pull
git checkout -b feature/ten-tinh-nang
# code...
git add .
git commit -m "feat: mo ta thay doi"
git push -u origin feature/ten-tinh-nang
```

### Đẩy thẳng lên nhánh chính (khi làm repo cá nhân)
```bash
git add .
git commit -m "chore: update project"
git push origin main
```

### Trước khi push, luôn kiểm tra nhanh bảo mật
```bash
rg -n "AIza|GEMINI_API_KEY|API_KEY|SECRET|token"
```
Nếu thấy key thật, xoá ngay khỏi code rồi mới commit.

## 8) `.gitignore` đã chặn file thừa
Đã bỏ qua sẵn:
- `.venv/`, `venv/`
- `__pycache__/`, `*.pyc`
- `.env`, `.env.*`
- `.DS_Store`
- cache/build/log phổ biến

## 9) Cấu trúc thư mục chính
- `gui/`: giao diện PyQt5
- `translator/`: logic dịch, prompt, model manager
- `config/`: cấu hình model/prompt/settings
- `downloader/`: tải nội dung từ nguồn web
- `epub/`: xuất EPUB

## 10) Troubleshooting nhanh
- Thiếu thư viện: chạy lại `pip install -r requirements.txt` trong `.venv`.
- Lỗi API key: kiểm tra `GEMINI_API_KEY` hoặc nhập lại trong Settings.
- Cảnh báo font trên macOS: thường không chặn app chạy.
