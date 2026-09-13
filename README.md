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

Sau khi cài đặt, bạn chỉ cần mở Antigravity và gõ:
> *"Bật remote"* hoặc *"Kích hoạt remote skill"*

Antigravity sẽ:
1. Tự động khởi chạy Web Server ngầm ở địa chỉ `http://localhost:8000`.
2. Đi vào trạng thái chờ lệnh `python wait_task.py` (0 Token Usage).
3. Mở trình duyệt điện thoại truy cập vào địa chỉ Web để gửi prompt và nhận phản hồi real-time!

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
