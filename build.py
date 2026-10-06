#!/usr/bin/env python3
"""Build and check The RevOps Funnel Equations page.

    python3 build.py           # check the equations, then rewrite index.html
    python3 build.py --check   # check only; fail if index.html is out of date

Edit src/eqstages.py (equations, definitions, example values) and src/eqnames.py (full names and short forms).
Never edit index.html by hand.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))
import equations as E  # noqa: E402
from eqstages import VARS, LINES, SHOWN, WHOLE, FUNNELS  # noqa: E402

fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)


# 1. only + - x / and brackets, and every short form is defined
for l in LINES:
    check(re.sub(r"[a-z_][a-z0-9_]*|\d+|[-+*/() ]", "", l["expr"]) == "", f"{l['result']}: use only + - * / ( )")
    for t in E.ids_in(l["expr"]):
        check(t in VARS, f"{l['result']}: unknown id {t}")
for k, d in VARS.items():
    check(bool(d.get("full")) and bool(d.get("short")), f"{k}: missing full name or short form (src/eqnames.py)")
    check("<" not in d.get("short", ""), f"{k}: short forms are plain capitals, no subscripts")

# 2. six stages per funnel, one metric each, short forms unique within a funnel
for f in FUNNELS:
    check([s for s, _, _ in SHOWN[f]] == ["S1", "S2", "S3", "S4", "S5", "S6"], f"{f}: needs six stages")
    used = set()
    for s, m, res in SHOWN[f]:
        check(m in res, f"{f} {s}: the metric's own line must be shown")
        for r in res:
            l = E.line_for(r, f)
            used |= {r, *E.ids_in(l["expr"])}
    shorts = [VARS[i]["short"] for i in used]
    check(len(shorts) == len(set(shorts)), f"{f}: a short form means two things: {sorted({x for x in shorts if shorts.count(x) > 1})}")
    x = E.VALUES[f]
    check(abs(eval(WHOLE[f], {}, x) - x["c"]) < 1e-9, f"{f}: the whole-funnel line no longer equals the stage chain")
    for _, m, _ in SHOWN[f]:
        check(0 < x[m] < 1, f"{f}: metric {m} should be a rate between 0 and 1 on the example values, got {x[m]}")

# 3. build the page and check the copy rules
style = open(os.path.join(HERE, "src", "base-style.html"), encoding="utf-8").read()
page = E.render_standalone(style)
body = page[page.index("<body>"):]
check("—" not in body and "–" not in body, "no em or en dashes anywhere")
check('href="#' not in body, "no jump links: define everything where it is used")
for client in ("BigHammer", "Neural IT", "Fintech Circle", "Growth Idea", "Motoz", "Bespin", "CRMIT"):
    check(client.lower() not in body.lower(), f"client name {client} must not appear")

out = os.path.join(HERE, "index.html")
current = open(out, encoding="utf-8").read() if os.path.exists(out) else ""
if "--check" in sys.argv:
    check(current == page, "index.html is out of date: run python3 build.py")
for m in fails:
    print("FAIL", m)
if fails:
    sys.exit(1)
if "--check" not in sys.argv and current != page:
    open(out, "w", encoding="utf-8").write(page)
    print("wrote index.html")
for f in FUNNELS:
    print(FUNNELS[f], " · ".join(f"{VARS[m]['short']} {E.VALUES[f][m] * 100:.2f}%" for _, m, _ in SHOWN[f]))
print(f"ok · {len(LINES)} lines · {len(VARS)} short forms")
