import urllib.request
import urllib.error
import json
import sys
import time

SERVER_URL = "http://localhost:8000/api/wait_task"

def main():
    while True:
        try:
            req = urllib.request.Request(SERVER_URL, headers={"User-Agent": "Antigravity-WaitTask/1.0"})
            with urllib.request.urlopen(req, timeout=310) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    prompt = data.get("prompt")
                    if prompt:
                        # Output prompt as JSON to stdout for Antigravity to capture
                        print(json.dumps({"status": "received", "prompt": prompt}, ensure_ascii=False))
                        sys.exit(0)
                elif response.status == 208:
                    # Timeout long polling, loop again
                    continue
        except urllib.error.URLError as e:
            # Server not running yet or connection refused, wait 2 seconds and retry
            time.sleep(2)
        except Exception as e:
            print(json.dumps({"status": "error", "error": str(e)}), file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
