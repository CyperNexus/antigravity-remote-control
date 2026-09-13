import http.server
import socketserver
import json
import os
import queue
import time
from urllib.parse import parse_qs, urlparse

PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Shared state in memory
task_queue = queue.Queue()
messages_log = []
is_waiting_for_task = False

class RemoteControlHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence default request logs for clean terminal output
        return

    def do_GET(self):
        global is_waiting_for_task
        parsed_path = urlparse(self.path)

        # Serve API: Wait for Task (Long Polling)
        if parsed_path.path == "/api/wait_task":
            is_waiting_for_task = True
            try:
                # Block for up to 300 seconds waiting for user input from Web UI
                task_text = task_queue.get(timeout=300)
                is_waiting_for_task = False
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {"status": "ok", "prompt": task_text}
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except queue.Empty:
                is_waiting_for_task = False
                self.send_response(208) # Timeout / No content
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {"status": "timeout", "prompt": null}
                self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # Serve API: Status & Messages Log
        elif parsed_path.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "is_waiting": is_waiting_for_task,
                "messages": messages_log
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return

        # Serve Web UI Static Files
        elif parsed_path.path == "/" or parsed_path.path == "/index.html":
            self.path = "/static/index.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        global messages_log
        parsed_path = urlparse(self.path)

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            data = {}

        # API: User sends new prompt from Web UI
        if parsed_path.path == "/api/send_task":
            prompt = data.get("prompt", "").strip()
            if prompt:
                messages_log.append({"sender": "user", "text": prompt, "timestamp": time.time()})
                task_queue.put(prompt)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "queued"}).encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
            return

        # API: Agent reports response back to Web UI
        elif parsed_path.path == "/api/report_status":
            message = data.get("message", "").strip()
            if message:
                messages_log.append({"sender": "agent", "text": message, "timestamp": time.time()})
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "logged"}).encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
            return

        else:
            self.send_error(404, "Endpoint Not Found")

def main():
    os.chdir(os.path.dirname(__file__))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), RemoteControlHTTPRequestHandler) as httpd:
        print(f"==================================================")
        print(f"[+] Antigravity Remote Server active on port {PORT}")
        print(f"[+] Web UI: http://localhost:{PORT}")
        print(f"==================================================")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
