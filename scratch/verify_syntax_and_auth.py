import re

with open(r"c:\c+++\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Check CDNs
assert "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth-compat.js" in content, "Firebase Auth Compat CDN missing!"
assert "https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js" in content, "Firebase App Compat CDN missing!"

# 2. Check Auth handlers
assert "signInWithPopup(provider)" in content, "signInWithPopup missing!"
assert "auth/popup-blocked" in content, "auth/popup-blocked handler missing!"
assert "auth/unauthorized-domain" in content, "auth/unauthorized-domain handler missing!"
assert "createUserWithEmailAndPassword(email, password)" in content, "createUserWithEmailAndPassword missing!"
assert "signInWithEmailAndPassword(email, password)" in content, "signInWithEmailAndPassword missing!"
assert "password.length < 6" in content, "Password validation missing!"
assert "emailRegex" in content, "Email regex validation missing!"
assert "onAuthStateChanged" in content, "onAuthStateChanged missing!"
assert "continueAsGuest" in content, "continueAsGuest missing!"
assert "authModalErrorBox" in content, "authModalErrorBox element missing!"
assert "authModalErrorTitle" in content, "authModalErrorTitle element missing!"
assert "authModalErrorMessage" in content, "authModalErrorMessage element missing!"
assert "pr8848276-arch.github.io" in content, "GitHub Pages domain instructions missing!"

# 3. Check for balanced braces in script
script_start = content.rfind("<script>")
script_end = content.rfind("</script>")
script_content = content[script_start+8:script_end]

# Basic brace stack checker (skipping strings and comments)
in_single_quote = False
in_double_quote = False
in_template = False
in_line_comment = False
in_block_comment = False
stack = []
line = 1
col = 0

i = 0
n = len(script_content)
errors = []

while i < n:
    ch = script_content[i]
    col += 1
    if ch == '\n':
        line += 1
        col = 0
        if in_line_comment:
            in_line_comment = False
        i += 1
        continue
    
    if in_line_comment:
        i += 1
        continue
        
    if in_block_comment:
        if ch == '*' and i + 1 < n and script_content[i+1] == '/':
            in_block_comment = False
            i += 2
            continue
        i += 1
        continue

    # Escape char
    if ch == '\\' and (in_single_quote or in_double_quote or in_template):
        i += 2
        continue

    if in_single_quote:
        if ch == "'":
            in_single_quote = False
        i += 1
        continue

    if in_double_quote:
        if ch == '"':
            in_double_quote = False
        i += 1
        continue

    if in_template:
        if ch == '`':
            in_template = False
        i += 1
        continue

    # Check comment start
    if ch == '/' and i + 1 < n:
        if script_content[i+1] == '/':
            in_line_comment = True
            i += 2
            continue
        elif script_content[i+1] == '*':
            in_block_comment = True
            i += 2
            continue

    if ch == "'":
        in_single_quote = True
    elif ch == '"':
        in_double_quote = True
    elif ch == '`':
        in_template = True
    elif ch in '({[':
        stack.append((ch, line, col))
    elif ch in ')}]':
        matching = {'(': ')', '{': '}', '[': ']'}[stack[-1][0]] if stack else None
        if not stack:
            errors.append(f"Unexpected closing {ch} at line {line}:{col}")
        elif ch != matching:
            errors.append(f"Mismatched {ch} at line {line}:{col}, expected {matching} from {stack[-1]}")
            stack.pop()
        else:
            stack.pop()
    i += 1

if stack:
    errors.append(f"Unclosed open brackets count: {len(stack)}, first unclosed: {stack[0]}")

print("Brace check errors count:", len(errors))
for err in errors[:10]:
    print("  ", err)

assert len(errors) == 0, "Braces/parentheses/brackets are not balanced!"

# 4. Check that IDs referenced by document.getElementById exist in HTML
id_matches = re.findall(r"document\.getElementById\(['\"]([a-zA-Z0-9_-]+)['\"]\)", script_content)
unique_ids = set(id_matches)
missing_ids = []
for el_id in sorted(unique_ids):
    if f'id="{el_id}"' not in content and f"id='{el_id}'" not in content:
        missing_ids.append(el_id)

print(f"Total getElementById targets: {len(unique_ids)}")
print(f"Missing IDs in HTML: {missing_ids}")
assert len(missing_ids) == 0, f"Missing IDs: {missing_ids}"

print("\nALL AUTH AND DOM INTEGRITY CHECKS PASSED PERFECTLY!")
