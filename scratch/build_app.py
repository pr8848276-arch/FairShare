import os

from parts_head import HEAD_HTML
from parts_header_and_main import BODY_TOP
from parts_tabs import TABS_HTML
from parts_modals import MODALS_HTML
from parts_js import JS_CODE

full_html = HEAD_HTML + "\n" + BODY_TOP + "\n" + TABS_HTML + "\n" + MODALS_HTML + "\n" + JS_CODE

# Output destinations
target_root = r"c:\c+++\index.html"
target_sub = r"c:\c+++\expense-splitter\index.html"

with open(target_root, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"Successfully wrote {len(full_html)} bytes to {target_root}")

with open(target_sub, "w", encoding="utf-8") as f:
    f.write(full_html)
print(f"Successfully wrote {len(full_html)} bytes to {target_sub}")
