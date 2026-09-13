# Antigravity Remote Control Loop Skill (`remote-control-loop`)

[![npm version](https://img.shields.io/npm/v/antigravity-remote-control.svg)](https://www.npmjs.com/package/antigravity-remote-control)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Skill chuyên dụng cho **Antigravity AI Agent** giúp điều khiển agent từ xa qua giao diện Web di động theo kiến trúc **Event-Driven / Blocking Script Loop**, giúp tiêu tốn **0 Token LLM Usage** trong lúc đứng chờ lệnh.

---

## ⚡ Cài đặt nhanh qua `npx`

Chạy lệnh sau trên terminal để tự động nạp Skill vào Antigravity local của bạn:

```bash
npx antigravity-remote-control
```

Skill sẽ được tự động cài đặt vào thư mục `~/.gemini/config/skills/remote-control-loop/`.

---

## 🚀 Hướng dẫn sử dụng

Sau khi cài đặt, bạn có thể kích hoạt Skill bằng một trong các cách sau:

### Cách 1: Sử dụng Slash Command
Gõ trực tiếp slash command:
```text
/remote-control-loop
```

### Cách 2: Sử dụng câu lệnh tự nhiên
Nhắn trực tiếp trong khung chat:
> *"Bật remote"* hoặc *"Kích hoạt remote skill"*

---

### Quy trình hoạt động tự động:
1. Antigravity sẽ tự động khởi chạy Web Server ngầm ở địa chỉ `http://localhost:8000`.
2. Đi vào trạng thái chờ lệnh `python wait_task.py` (**0 Token LLM Usage**).
3. Mở trình duyệt trên điện thoại/máy tính khác truy cập vào `http://<IP-MÁY-TÍNH>:8000` để gửi prompt và xem phản hồi real-time!

---

## 🛠️ Kiến trúc hệ thống

```text
[ Điện thoại / Máy tính khác ]
              │ (Truy cập Web UI / HTTP REST)
              ▼
┌───────────────────────────────┐
│     remote_server.py          │ ◄── HTTP & Long-polling Server (Port 8000)
└──────────────┬────────────────┘
               │ (Long Polling Response)
               ▼
┌───────────────────────────────┐
│       wait_task.py            │ ◄── Blocking listener (Thoát khi có input)
└──────────────┬────────────────┘
               │ (STDOUT JSON output)
               ▼
┌───────────────────────────────┐
│     Antigravity Session       │ ◄── Nhận prompt & Thực thi tác vụ
└───────────────────────────────┘
```

## 📄 License
MIT © Antigravity Community
