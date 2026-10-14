import subprocess
import time
import json
import urllib.request
import sys

# Start Edge with remote debugging
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "http://localhost:8080/index.html"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("Started Edge, waiting for CDP...")
time.sleep(2)

try:
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    pages = json.loads(req.read().decode())
    print("CDP Connected! Pages:", [p.get("title", "") for p in pages])
    target = next((p for p in pages if "localhost:8080" in p.get("url", "")), pages[0] if pages else None)
    if target:
        ws_url = target.get("webSocketDebuggerUrl")
        print("Target page found:", target.get("url"), "WS:", ws_url)
    else:
        print("No target page found")
except Exception as e:
    print("Error connecting to CDP:", e)
finally:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
