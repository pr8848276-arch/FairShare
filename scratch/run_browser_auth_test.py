import subprocess
import time
import json
import urllib.request
import sys
import websocket

# Launch Edge headless on port 9222
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    "http://localhost:8080/index.html"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2)

def cdp_eval(ws, expression):
    msg_id = int(time.time() * 1000) % 100000
    req = {
        "id": msg_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        }
    }
    ws.send(json.dumps(req))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id:
            result = resp.get("result", {})
            if "exceptionDetails" in result:
                raise RuntimeError(result["exceptionDetails"])
            return result.get("result", {}).get("value")

try:
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    pages = json.loads(req.read().decode())
    target = next((p for p in pages if "localhost:8080" in p.get("url", "")), None)
    assert target, "Target page http://localhost:8080/index.html not found!"
    ws_url = target["webSocketDebuggerUrl"]

    ws = websocket.create_connection(ws_url, timeout=5)

    # 1. Enable console and runtime
    ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
    ws.send(json.dumps({"id": 2, "method": "Console.enable"}))

    # Give page 1 second to execute DOMContentLoaded
    time.sleep(1)

    print("--- 1. Testing Firebase SDK Presence ---")
    fb_defined = cdp_eval(ws, "typeof firebase !== 'undefined'")
    print("firebase defined:", fb_defined)
    assert fb_defined, "Firebase global object is not defined!"

    fb_auth_fn = cdp_eval(ws, "typeof firebase.auth === 'function'")
    print("firebase.auth function defined:", fb_auth_fn)
    assert fb_auth_fn, "firebase.auth is not a function!"

    print("--- 2. Testing getFirebaseAuth() Instance ---")
    auth_check = cdp_eval(ws, "Boolean(getFirebaseAuth())")
    print("getFirebaseAuth() returns instance:", auth_check)
    assert auth_check, "getFirebaseAuth() failed to return auth instance!"

    print("--- 3. Testing Auth Modal Elements & Helper Functions ---")
    modal_exists = cdp_eval(ws, "Boolean(document.getElementById('authModal'))")
    err_box = cdp_eval(ws, "Boolean(document.getElementById('authModalErrorBox'))")
    google_btn = cdp_eval(ws, "Boolean(document.getElementById('googleSignInBtn'))")
    guest_btn = cdp_eval(ws, "Boolean(document.querySelector('button[onclick*=\"continueAsGuest\"]'))")
    print("Modal elements check:", {
        "authModal": modal_exists,
        "authModalErrorBox": err_box,
        "googleSignInBtn": google_btn,
        "continueAsGuestBtn": guest_btn
    })
    assert modal_exists and err_box and google_btn and guest_btn, "Missing required auth UI elements!"

    print("--- 4. Testing Error Box UI Rendering ---")
    cdp_eval(ws, "showAuthModalError('Domain Authorization Error', 'auth/unauthorized-domain test')")
    err_box_hidden = cdp_eval(ws, "document.getElementById('authModalErrorBox').classList.contains('hidden')")
    err_title = cdp_eval(ws, "document.getElementById('authModalErrorTitle').textContent")
    err_msg = cdp_eval(ws, "document.getElementById('authModalErrorMessage').textContent")
    print("Error box state:", {"hidden": err_box_hidden, "title": err_title, "msg": err_msg})
    assert not err_box_hidden, "Error box should be visible!"
    assert err_title == "Domain Authorization Error", f"Unexpected title: {err_title}"

    # Hide error box
    cdp_eval(ws, "hideAuthModalError()")
    err_box_hidden_after = cdp_eval(ws, "document.getElementById('authModalErrorBox').classList.contains('hidden')")
    print("Error box hidden after hideAuthModalError():", err_box_hidden_after)
    assert err_box_hidden_after, "Error box should be hidden!"

    print("--- 5. Testing Email Validation in handleEmailAuthSubmit ---")
    # Set invalid email
    cdp_eval(ws, "document.getElementById('authEmailInput').value = 'invalid-email'")
    cdp_eval(ws, "document.getElementById('authPasswordInput').value = '123'")
    cdp_eval(ws, "handleEmailAuthSubmit({ preventDefault: () => {} })")
    val_title = cdp_eval(ws, "document.getElementById('authModalErrorTitle').textContent")
    print("Validation error title for bad email:", val_title)
    assert "Invalid Email Address" in val_title, f"Expected Invalid Email Address error, got: {val_title}"

    # Set valid email but short password
    cdp_eval(ws, "document.getElementById('authEmailInput').value = 'test@example.com'")
    cdp_eval(ws, "document.getElementById('authPasswordInput').value = '123'")
    cdp_eval(ws, "handleEmailAuthSubmit({ preventDefault: () => {} })")
    pwd_title = cdp_eval(ws, "document.getElementById('authModalErrorTitle').textContent")
    print("Validation error title for short password:", pwd_title)
    assert "Password Too Short" in pwd_title, f"Expected Password Too Short error, got: {pwd_title}"

    print("--- 6. Testing auth/configuration-not-found Error Prompt Handling ---")
    cdp_eval(ws, "showAuthModalError('Firebase Auth Not Configured (auth/configuration-not-found)', 'Test config prompt'); showAuthConfigPrompt();")
    prompt_visible = not cdp_eval(ws, "document.getElementById('authConfigPromptBox').classList.contains('hidden')")
    paste_input_exists = cdp_eval(ws, "Boolean(document.getElementById('authConfigPasteInput'))")
    print("Configuration prompt box visible:", prompt_visible, "Paste input exists:", paste_input_exists)
    assert prompt_visible and paste_input_exists, "Configuration-not-found prompt box should be visible!"

    print("--- 7. Testing Continue as Guest Fallback & Working Local Session ---")
    cdp_eval(ws, "continueAsGuest()")
    time.sleep(0.3)
    is_guest = cdp_eval(ws, "appState.isGuest")
    session_guest = cdp_eval(ws, "sessionStorage.getItem('fairshare_is_guest')")
    auth_user = cdp_eval(ws, "appState.authUser")
    modal_closed = cdp_eval(ws, "document.getElementById('authModal').classList.contains('hidden')")
    prompt_hidden_now = cdp_eval(ws, "document.getElementById('authConfigPromptBox').classList.contains('hidden')")
    print("Guest mode state:", {
        "isGuest": is_guest,
        "sessionStorage": session_guest,
        "modalClosed": modal_closed,
        "promptHidden": prompt_hidden_now,
        "authUser": auth_user
    })
    assert is_guest is True, "appState.isGuest should be True!"
    assert session_guest == "true", "sessionStorage fairshare_is_guest should be 'true'!"
    assert modal_closed is True, "authModal should be closed!"
    assert prompt_hidden_now is True, "authConfigPromptBox should be hidden after continuing as guest!"
    assert auth_user and auth_user.get("isGuest") is True, "appState.authUser should be populated with guest session!"
    assert auth_user.get("displayName") in ["Rahul", "Amit", "Pooja"], f"Expected guest displayName in group members, got {auth_user.get('displayName')}"

    print("\n[SUCCESS] ALL FIREBASE AUTH & CONFIGURATION-NOT-FOUND TESTS PASSED WITH 100% SUCCESS!")

    ws.close()

except Exception as e:
    print("TEST FAILED:", e)
    sys.exit(1)
finally:
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
