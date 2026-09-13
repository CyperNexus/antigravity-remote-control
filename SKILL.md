---
name: remote-control-loop
description: Kích hoạt chế độ điều khiển từ xa qua Web Interface di động theo kiến trúc Event-Driven / Blocking Script Loop. Giúp Antigravity nhận và thực thi lệnh từ xa mà không tiêu tốn token usage khi ở trạng thái chờ.
---

# Remote Control Loop Skill (`remote-control-loop`)

Skill này cho phép Antigravity kết nối và nhận lệnh từ xa thông qua giao diện Web di động (WebUI) theo mô hình **Event-Driven / Blocking Script Loop**.

## 🎯 Điểm nổi bật
- **0 Token Usage khi chờ:** Antigravity sử dụng một blocking script Python (`wait_task.py`) để tạm dừng tiến trình, không tốn Token/Credit LLM trong lúc người dùng chưa gửi yêu cầu.
- **Web UI Tiện Lợi:** Giao diện web responsive nhẹ nhàng trên cổng `8000` (truy cập qua Wi-Fi local hoặc `ngrok`/`localtunnel`).

---

## 🚀 Hướng Dẫn Vận Hành Vòng Lặp (Agent Protocol)

Khi người dùng kích hoạt lệnh `/remote` hoặc yêu cầu "bật remote điều khiển từ xa":

### 1. Khởi động Web Server (Nếu chưa chạy)
Kiểm tra hoặc chạy `remote_server.py` ở chế độ Daemon (chạy ngầm background):
```powershell
python C:\Users\ygxjd\.gemini\config\skills\remote-control-loop\scripts\remote_server.py
```
*(Có thể dùng `run_command` với `IsDaemon: true` hoặc khởi chạy qua background process).*

### 2. Bắt đầu Vòng lặp Chờ Lệnh (`wait_task.py`)
Gửi thông báo ngắn gọn cho người dùng local về đường dẫn Web UI (ví dụ `http://localhost:8000` hoặc IP mạng LAN), sau đó thực thi lệnh blocking:
```powershell
python C:\Users\ygxjd\.gemini\config\skills\remote-control-loop\scripts\wait_task.py
```
*(Script này sẽ giữ kết nối và CHỜ cho đến khi người dùng gửi prompt từ Web UI).*

### 3. Đọc Prompt thu được & Thực thi Task
Khi `wait_task.py` nhận được input từ WebUI, nó sẽ trả về kết quả dạng JSON dạng:
```json
{"status": "received", "prompt": "Nội dung yêu cầu từ người dùng..."}
```
1. Đọc nội dung `prompt`.
2. Thực thi các tác vụ theo yêu cầu (sửa code, chạy test, build, phân tích...).

### 4. Báo cáo Trạng thái lại Web UI (Optional)
Gửi phản hồi báo cáo lại Web UI để người dùng di động biết kết quả qua API:
```powershell
curl -X POST http://localhost:8000/api/report_status -H "Content-Type: application/json" -d "{\"message\": \"Đã hoàn tất công việc X!\"}"
```

### 5. Tiếp tục Vòng lặp
Quay lại **Bước 2** bằng cách gọi lại `python wait_task.py` để đứng chờ câu lệnh tiếp theo từ người dùng.
