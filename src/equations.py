#!/usr/bin/env python3
"""The RevOps Funnel Equations, version 3: one metric per stage, per funnel shape.

    python3 workshop-plan/build/equations.py          # rewrite every EQ block, the JSON, the app model and the lead magnet
    python3 workshop-plan/build/equations.py --check  # fail if any output is stale

Source: build/eqstages.py (short forms, definitions, lines). Engine: build/eqmodel.js (runs the same lines).
"""
from __future__ import annotations

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WP = os.path.dirname(HERE)
ROOT = os.path.dirname(WP)
PLAYBOOK = os.path.join(WP, "playbook.html")
sys.path.insert(0, HERE)
from eqstages import VARS, LINES, SHOWN, WHOLE, STAGE_TITLES, FUNNELS, W, R, K  # noqa: E402

OPS = {"*": "×", "/": "÷", "+": "+", "-": "−", "(": "(", ")": ")"}


def ids_in(expr):
    return re.findall(r"[a-z_][a-z0-9_]*", expr)


def line_for(result, f):
    return next(l for l in LINES if l["result"] == result and f in l["fn"])


def show(expr):
    out = []
    for t in re.findall(r"[a-z_][a-z0-9_]*|\d+|[-+*/()]", expr):
        out.append(OPS.get(t) or (VARS[t]["short"] if t in VARS else t))
    return " ".join(out).replace("( ", "(").replace(" )", ")")


def compute(f, x=None):
    v = {k: d["value"] for k, d in VARS.items() if d["value"] is not None}
    v.update(x or {})
    for l in LINES:
        if f in l["fn"]:
            try:
                v[l["result"]] = eval(l["expr"], {}, v)
            except ZeroDivisionError:
                v[l["result"]] = 0
    return v


VALUES = {f: compute(f) for f in FUNNELS}


# ------------------------------------------------------------------------------------------------ the document
STOP = {"of", "the", "a", "an", "from", "on", "by", "to", "for", "and", "per"}


def meaning(d):
    """The part of the definition that adds something to the full name."""
    text = d["text"]
    if ":" in text:
        return text.split(":", 1)[1].strip()
    words = {w for w in re.findall(r"[a-z0-9.]+", text.lower()) if w not in STOP}
    name = {w for w in re.findall(r"[a-z0-9.]+", d["full"].lower()) if w not in STOP}
    return "" if words <= name else text


def key_line(i):
    d = VARS[i]
    m = meaning(d)
    return f'<li><b>{d["short"]}</b><span><i>{html.escape(d["full"])}</i>{": " + html.escape(m) if m else ""}</span></li>'


def stage_block(f, n, st, metric, results):
    lines = [line_for(r, f) for r in results]
    eqs = "".join(f'<div class="eqs-l"><b>{VARS[l["result"]]["short"]}</b> = {show(l["expr"])}</div>' for l in lines)
    seen = []
    for l in lines:
        for t in [l["result"]] + ids_in(l["expr"]):
            if t in VARS and t not in seen:
                seen.append(t)
    keys = "".join(key_line(t) for t in seen)
    m = VARS[metric]
    return (f'<div class="eqs" id="eq-{f}-{st.lower()}"><div class="eqs-h"><span>Stage {n}</span> {STAGE_TITLES[st]}</div>'
            f'<p class="eqs-m">Metric: <b>{m["short"]}</b> ({html.escape(m["full"])}) = {html.escape(meaning(m))}</p>'
            f'<div class="eqs-eq">{eqs}</div><ul class="eqs-k">{keys}</ul></div>')


def whole_block(f):
    ids = ["c"]
    for t in ids_in(WHOLE[f]):
        if t not in ids:
            ids.append(t)
    keys = "".join(key_line(t) for t in ids)
    return (f'<div class="eqs eqs-w"><div class="eqs-h">Whole Funnel</div>'
            f'<div class="eqs-eq"><div class="eqs-l"><b>OC</b> = {show(WHOLE[f])}</div></div>'
            f'<ul class="eqs-k">{keys}</ul></div>')


def funnel_section(f, heading="h3"):
    parts = [f'<{heading} id="eq-{f}">{FUNNELS[f]}</{heading}>', whole_block(f)]
    parts += [stage_block(f, i, st, m, res) for i, (st, m, res) in enumerate(SHOWN[f], 1)]
    return "\n      ".join(parts)


def metrics_table():
    rows = []
    for i, st in enumerate(STAGE_TITLES, 1):
        cells = []
        for f in FUNNELS:
            m = next(mm for s, mm, _ in SHOWN[f] if s == st)
            cells.append(f'<td data-label="{FUNNELS[f]}"><b>{VARS[m]["short"]}</b> {html.escape(VARS[m]["full"])}</td>')
        rows.append(f'<tr><td data-label="Stage">{i}. {STAGE_TITLES[st]}</td>{"".join(cells)}</tr>')
    return ('<div class="tbl stack"><table><thead><tr><th>Stage</th>' + "".join(f"<th>{FUNNELS[f]}</th>" for f in FUNNELS) +
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def block_intro():
    keys = "".join(key_line(t) for t in ("c", "r", "su", "br", "cl"))
    return ('<h3>The One Equation to Memorize</h3>\n'
            '      <p>Each funnel has six stages, and each stage has one metric that says how well it works. Multiply them and you get customers:</p>\n'
            '      <div class="eqs-eq"><div class="eqs-l"><b>OC</b> = R × SUR × BR × CR</div></div>\n'
            f'      <ul class="eqs-k">{keys}</ul>\n'
            '      <p>That is the webinar. The reverse squeeze page and the workshop series use their own metrics; all three are in The Funnel Equations.</p>')


def block_chapter(section_open='<section class="reveal" id="equations">', h2="The Funnel Equations", sub_h="h3"):
    parts = [section_open,
             '<div class="chap"><span class="no">The Equations</span><span class="tag">One Metric per Stage</span></div>' if "reveal" in section_open else "",
             f"<h2>{h2}</h2>" if h2 else "",
             "<p>One metric per stage, per funnel. Each stage's equation shows what that metric is made of, channel by channel. Every rate is one count divided by another.</p>",
             metrics_table()]
    parts += [funnel_section(f, sub_h) for f in FUNNELS]
    parts.append("</section>")
    return "\n      ".join(p for p in parts if p)


def block_stage(st):
    items = []
    for f in FUNNELS:
        m = next(mm for s, mm, _ in SHOWN[f] if s == st)
        items.append(f'<li>{FUNNELS[f]}: <b>{VARS[m]["short"]}</b> {html.escape(VARS[m]["full"])} = {html.escape(meaning(VARS[m]))}</li>')
    return f'<div class="box tip"><div class="h">The Metric for This Stage</div><ul class="eqlist">{"".join(items)}</ul></div>'


def block_dashboard():
    rows = []
    for i, st in enumerate(STAGE_TITLES, 1):
        names = sorted({re.sub("<[^>]+>", "", VARS[t]["short"]) for f in FUNNELS for s, _, res in SHOWN[f] if s == st
                        for r in res for t in ids_in(line_for(r, f)["expr"]) if VARS[t]["value"] is not None})
        rows.append(f'<li><b>Stage {i}:</b> {", ".join(names)}</li>')
    return ('<div class="box tip"><div class="h">The Columns, Stage by Stage</div>'
            f'<p>One column for every input in The Funnel Equations.</p><ul>{"".join(rows)}</ul></div>')


def block_model():
    return '<div class="eqmodel" data-funnel="webinar"></div>'


CSS = r"""
.eqs{border-top:1px solid var(--line);padding:16px 0 14px;max-width:820px}
.eqs-h{font-size:17px;font-weight:750;color:var(--ink);margin-bottom:6px}.eqs-h span{color:var(--ink-3);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase;margin-right:6px}
.eqs-m{margin:0 0 10px;font-size:15.5px;color:var(--ink)}
.eqs-eq{background:var(--panel-2);border-radius:12px;padding:10px 14px;margin:0 0 10px;max-width:820px}
.eqs-l{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14.5px;line-height:1.75;color:var(--ink);overflow-wrap:anywhere}
.eqs-l sub,.eqs-k sub,.eqs-m sub,td sub{font-size:.72em}
.eqs-k{list-style:none;margin:0;padding:0;columns:2 300px;column-gap:28px;max-width:820px}
.eqs-k li{display:grid;grid-template-columns:64px minmax(0,1fr);margin:0 0 4px;padding:0;font-size:14px;line-height:1.45;color:var(--ink-2);break-inside:avoid}.eqs-k li::before{content:none;display:none}
.eqs-k i{font-style:normal;color:var(--ink);font-weight:600}.eqs-k b{color:var(--ink);font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:13.5px}
.eqs-w{border-top:2px solid var(--ink)}
.eqlist{margin:8px 0 0;padding-left:18px}.eqlist li{margin:5px 0;font-size:15px}
.eqmodel{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:20px;margin:24px 0;font-size:14.5px}
.eqm-top{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;align-items:center;margin-bottom:14px}
.eqm-tabs{display:flex;flex-wrap:wrap;gap:6px}.eqm-tabs button,.eqm-reset{font:inherit;font-size:14px;border:1px solid var(--line-2);background:var(--panel-2);color:var(--ink-2);border-radius:999px;padding:8px 15px;cursor:pointer;min-height:40px}
.eqm-tabs button[aria-selected=true]{background:var(--ink);color:var(--bg);border-color:var(--ink)}.eqm-reset{background:none}
.eqm-chain{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
.eqm-t{border:1px solid var(--line);border-radius:12px;padding:10px;display:flex;flex-direction:column;gap:2px;min-width:0}
.eqm-t b{font-size:22px;font-variant-numeric:tabular-nums;color:var(--ink)}.eqm-t span{font-size:12.5px;color:var(--ink-2);line-height:1.3}.eqm-t small{font-size:12px;color:var(--ink-3)}
.eqm-t .eqm-s{font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-3)}
.eqm-econ{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin-top:10px}.eqm-econ div{padding:4px 2px}.eqm-econ span{display:block;font-size:12px;color:var(--ink-3);line-height:1.3}.eqm-econ b{font-size:17px;font-variant-numeric:tabular-nums}
.eqm-h{font-size:12px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3);margin:18px 0 8px}
.eqm-list{margin:0;padding-left:22px}.eqm-list li{margin:6px 0;font-size:14.5px}
.eqm-st{border-top:1px solid var(--line);padding:8px 0}.eqm-st>summary{cursor:pointer;font-weight:650;padding:6px 0}.eqm-st>summary span{color:var(--ink-3);font-weight:500}
.eqm-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px 16px;margin-top:8px}
.eqm-in{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13.5px;color:var(--ink-2)}.eqm-l{min-width:0}
.eqm-v{display:flex;align-items:center;gap:4px;flex:none}.eqm-v input{width:88px;font:inherit;font-size:14px;padding:6px 8px;border:1px solid var(--line-2);border-radius:8px;background:var(--bg);color:var(--ink);text-align:right}
.eqm-v i{font-style:normal;color:var(--ink-3);width:12px}
@media(max-width:760px){.eqm-chain,.eqm-econ{grid-template-columns:repeat(2,minmax(0,1fr))}.eqs-k{columns:1}}
"""


def render_css_into(pb):
    a, b = "/* EQ-CSS:START (generated by build/equations.py) */", "/* EQ-CSS:END */"
    return re.sub(re.escape(a) + r".*?" + re.escape(b), lambda _: a + CSS + b, pb, count=1, flags=re.S)


# ------------------------------------------------------------------------------------------------ the model
COUNTS = {"v", "r", "p", "a", "h", "h_1", "q", "b", "bd", "fb", "c", "l", "b_y", "c_y", "d_1", "d_2", "d_3"}


def kind(i):
    if i.startswith("n_") or i in COUNTS or i.startswith("ar"):
        return "count"
    if i.startswith("sn_") or i == "ns":
        return "number"
    return "rate"


def model_data():
    tiles = {f: [[f"Stage {i}", m] for i, (_, m, _) in enumerate(SHOWN[f], 1)] for f in FUNNELS}
    counts = {W: ["v", "r", "a", "b", "c", "c_y"], R: ["v", "p", "h", "b", "c", "c_y"], K: ["v", "r", "q", "b", "c", "c_y"]}
    def nm(d):
        t = d["text"].split(":")[0]
        return t[:1].upper() + t[1:]
    return {"vars": {k: {"name": d.get("full") or nm(d), "short": d["short"], "full": d.get("full", ""), "kind": kind(k), "value": d["value"], "rng": d["rng"],
                         "low": False, "fix": ""} for k, d in VARS.items()},
            "eqs": LINES, "stages": {k: f"Stage {i}: {v}" for i, (k, v) in enumerate(STAGE_TITLES.items(), 1)},
            "funnels": FUNNELS, "tiles": tiles, "counts": counts}


def model_json():
    md = model_data()
    return {"version": 3, "about": "One metric per stage, per funnel. Only + - * /. Every rate is one count divided by another.",
            "funnels": FUNNELS, "stages": STAGE_TITLES, "variables": VARS, "equations": LINES, "whole": WHOLE,
            "metrics": {f: [{"stage": s, "metric": m, "shown": res} for s, m, res in SHOWN[f]] for f in FUNNELS},
            "tiles": md["tiles"], "counts": md["counts"]}


def engine_js():
    return open(os.path.join(HERE, "eqmodel.js")).read()


def script_tag():
    return ("<script>/* EQ-ENGINE generated by build/equations.py */\n" + engine_js() + "\nwindow.EQ_MODEL=" +
            json.dumps(model_data(), ensure_ascii=False) + ";\n</script>")


MARKERS = {"INTRO": block_intro, "CHAPTER": block_chapter, "DASH": block_dashboard, "MODEL": block_model,
           **{f"S{i}": (lambda i=i: block_stage(f"S{i}")) for i in range(1, 7)}}


def render_playbook(src):
    src = render_css_into(src)
    for name, fn in MARKERS.items():
        a, b = f"<!-- EQ-{name}:START (generated by build/equations.py) -->", f"<!-- EQ-{name}:END -->"
        pat = re.compile(re.escape(f"<!-- EQ-{name}:START") + r".*?" + re.escape(b), re.S)
        assert pat.search(src), f"place the EQ-{name} markers in playbook.html first"
        src = pat.sub(lambda _: a + "\n" + fn() + "\n" + b, src, count=1)
    pat = re.compile(r"<script>/\* EQ-ENGINE.*?</script>", re.S)
    return pat.sub(lambda _: script_tag(), src, count=1)


def render_ts():
    return ("// GENERATED by workshop-plan/build/equations.py from build/eqmodel.js + build/eqstages.py. Do not edit.\n/* eslint-disable */\n// @ts-nocheck\n"
            + engine_js() + "\nexport const EQ_MODEL = " + json.dumps(model_data(), ensure_ascii=False) + ";\n"
            "export { funnelCompute, funnelLeverage, funnelInputs, mountFunnelModel };\n")


def render_css(pb):
    tokens = (".eqm-wrap{--panel:transparent;--panel-2:color-mix(in srgb,currentColor 5%,transparent);--line:color-mix(in srgb,currentColor 14%,transparent);"
              "--line-2:color-mix(in srgb,currentColor 24%,transparent);--ink-3:color-mix(in srgb,currentColor 58%,transparent);--bg:#fff}\n")

    def scope(block):
        return "".join(",".join(".eqm-wrap " + x.strip() for x in sel.split(",")) + "{" + body + "}\n" for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", block))
    out, i, flat = "", 0, CSS.replace("\n", "")
    while i < len(flat):
        j = flat.find("{", i)
        if j < 0:
            break
        head = flat[i:j].strip()
        if head.startswith("@media"):
            depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(flat[k], 0)
                k += 1
            out += head + "{\n" + scope(flat[j + 1:k - 1]) + "}\n"
            i = k
        else:
            k = flat.index("}", j)
            out += scope(flat[i:k + 1])
            i = k + 1
    return "/* GENERATED by workshop-plan/build/equations.py. */\n" + tokens + out


CLI = r"""#!/usr/bin/env node
// The RevOps Funnel Equations CLI (generated). Usage: node equations/run.mjs <webinar|rsp|workshop> measured.json
// measured.json: { "id": value } with rates as fractions (0.35). Ids are the keys of "variables" in funnel-equations.json.
import fs from "node:fs";
import { funnelLeverage } from "./model.mjs";
const here = new URL(".", import.meta.url);
const EQ = JSON.parse(fs.readFileSync(new URL("../funnel-equations.json", here), "utf8"));
const MODEL = { vars: Object.fromEntries(Object.entries(EQ.variables).map(([k, d]) => [k, { ...d, kind: "rate", fix: "" }])), eqs: EQ.equations };
const [funnel = "webinar", file] = process.argv.slice(2);
const measured = file ? JSON.parse(fs.readFileSync(file, "utf8")) : {};
const { base, rows } = funnelLeverage(MODEL, funnel, measured);
console.log(`# ${EQ.funnels[funnel]}: one metric per stage`);
for (const m of EQ.metrics[funnel]) console.log(`${m.stage} ${EQ.stages[m.stage]}: ${(base[m.metric] * 100).toFixed(2)}%  (${EQ.variables[m.metric].text})`);
console.log(`Calls booked ${Math.round(base.b)} · onboarded customers ${Math.round(base.c)} · plus ${Math.round(base.c_y)} from the 52 weeks`);
console.log("\nRaise first (customers added if this input reaches the top of its typical range):");
rows.slice(0, 8).forEach((r, i) => console.log(`${i + 1}. ${EQ.variables[r.id].text}: ${(r.from * 100).toFixed(2)}% to ${(r.to * 100).toFixed(2)}% adds ${r.dCustomers.toFixed(2)} customers${measured[r.id] === undefined ? " (not measured yet)" : ""}`));
"""


def render_pack():
    data = json.dumps(model_json(), ensure_ascii=False, indent=1)
    files = [{"name": "funnel-os/funnel-equations.json", "text": data + "\n"},
             {"name": "funnel-os/equations/model.mjs", "text": engine_js() + "\nexport { funnelCompute, funnelLeverage, funnelInputs };\n"},
             {"name": "funnel-os/equations/run.mjs", "text": CLI}]
    return ("// GENERATED by workshop-plan/build/equations.py. Files the Funnel OS pack ships so the attendee's AI computes with the same equations.\n"
            "export const EQ_FILES: { name: string; text: string }[] = " + json.dumps(files, ensure_ascii=False, indent=0) + ";\n")


STANDALONE_URL = "https://revops-funnel-equations.growthcluborg.workers.dev/"
WORKSHOP_URL = "https://adisuja.github.io/tantra-workshop-live/site/workshop/"
# The Apps Script receiver every funnel form posts to (app/src/lib/form-log.ts). Public by nature: the browser calls it.
# The live receiver accepts six form keys, so a lead magnet sign-up goes in as a registration row with
# source=funnel-equations; ops/tracker_sync.py lifts those rows into the Tantra Tracker's own Funnel Equations tab.
LEAD_WEBHOOK = "https://script.google.com/macros/s/AKfycbxgZiV7RLX8t5cE8fR8TN8a2tMe_0ufQnMsc5OpCJJU6CsVns__QS7qNWhoESTHiiKAnw/exec"
LEAD_SOURCE = "funnel-equations"
LEAD_KEY = "rfe_unlocked"

GATE_CSS = ("<style>.eqgate{max-width:440px;margin-top:8px}.eqgate p{margin:0 0 20px;color:var(--ink-2)}"
            ".eqgate label{display:block;font-size:14px;font-weight:600;margin:0 0 6px}"
            ".eqgate input{display:block;width:100%;box-sizing:border-box;font:inherit;color:var(--ink);background:var(--panel-2);"
            "border:1px solid var(--line-2);border-radius:8px;padding:11px 13px;margin:0 0 16px}"
            ".eqgate input:focus-visible,.eqgate button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}"
            ".eqgate button{font:inherit;font-weight:700;color:#fff;background:var(--accent);border:0;border-radius:8px;"
            "padding:12px 20px;min-height:46px;cursor:pointer}.eqgate button:hover{background:var(--accent-ink)}"
            ".eqgate .eqerr{color:#b3261e;font-size:14px;margin:12px 0 0}.eqgate .eqerr:empty{display:none}"
            ".eqcta{margin:0 0 8px;color:var(--ink-2)}.eqcta a{color:var(--accent);font-weight:700}"
            ".eqlocked .eqopen{display:none}html:not(.eqlocked) .eqgate{display:none}</style>")

# runs in <head>, before paint, so a returning reader never sees the form flash
GATE_HEAD_JS = ("<script>(function(){var d=document.documentElement;try{if(localStorage.getItem(\"%s\"))return}catch(e){}"
                "d.classList.add(\"eqlocked\")})();</script>" % LEAD_KEY)

GATE_FORM = """<form class="eqgate" id="eqgate" novalidate>
    <p>Enter your name, email and WhatsApp number and the equations open on this page.</p>
    <label for="eq-name">Name</label>
    <input id="eq-name" name="name" type="text" autocomplete="name" required>
    <label for="eq-email">Email</label>
    <input id="eq-email" name="email" type="email" autocomplete="email" inputmode="email" required>
    <label for="eq-phone">WhatsApp Number</label>
    <input id="eq-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required>
    <button type="submit">Show Me the Equations</button>
    <p class="eqerr" id="eq-err" role="alert"></p>
  </form>"""

GATE_JS = """<script>
(function () {
  var form = document.getElementById("eqgate");
  if (!form) return;
  var err = document.getElementById("eq-err");
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var name = form.elements.name.value.trim();
    var email = form.elements.email.value.trim();
    var phone = form.elements.phone.value.trim();
    var bad = !name ? ["name", "Enter your name."]
      : !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email) ? ["email", "Enter a valid email address."]
      : phone.replace(/\\D/g, "").length < 7 ? ["phone", "Enter your WhatsApp number with the country code."]
      : null;
    if (bad) {
      err.textContent = bad[1];
      form.elements[bad[0]].focus();
      return;
    }
    var parts = name.split(/\\s+/);
    var row = {
      form: "free_registration",
      first_name: parts[0],
      last_name: parts.slice(1).join(" "),
      email: email,
      phone: phone,
      lane: "lead-magnet",
      source: "%(source)s",
      page: "/revops-funnel-equations",
      via: "apps-script"
    };
    var q = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_content"].forEach(function (k) {
      var v = q.get(k);
      if (v) row[k] = v.slice(0, 200);
    });
    try {
      // text/plain keeps this a simple request: no CORS preflight, which Apps Script cannot answer
      fetch("%(hook)s", { method: "POST", mode: "no-cors", keepalive: true,
        headers: { "Content-Type": "text/plain;charset=utf-8" }, body: JSON.stringify(row) }).catch(function () {});
    } catch (e) {}
    try { localStorage.setItem("%(key)s", "1"); } catch (e) {}
    document.documentElement.classList.remove("eqlocked");
    window.scrollTo(0, 0);
  });
})();
</script>""" % {"source": LEAD_SOURCE, "hook": LEAD_WEBHOOK, "key": LEAD_KEY}


def render_standalone(pb):
    style = pb[pb.index("<style>"):pb.index("</style>") + 8]
    desc = "One metric per stage for a webinar, a reverse squeeze page and a workshop series, with the equation for each stage and every short form defined."
    body = block_chapter('<section id="equations">', "", "h2")
    solo = ("<style>.shell.eqsolo{grid-template-columns:minmax(0,1fr);max-width:900px}.eqsolo main{max-width:none;padding-top:40px}"
            ".eqsolo h2{margin-top:44px}@media(max-width:560px){h1{font-size:32px}}</style>")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The RevOps Funnel Equations</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="The RevOps Funnel Equations">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{STANDALONE_URL}">
<link rel="canonical" href="{STANDALONE_URL}">
{style}
{solo}
{GATE_CSS}
{GATE_HEAD_JS}
</head>
<body>
<div class="shell eqsolo"><main>
  <h1>The RevOps Funnel Equations</h1>
  {GATE_FORM}
  <div class="eqopen">
  <p class="eqcta">Want these numbers built into your own funnel? <a href="{WORKSHOP_URL}">Join the free 3-Day AI RevOps Workshop</a>.</p>
  {body}
  </div>
</main></div>
{GATE_JS}
</body>
</html>
"""


def main():
    check = "--check" in sys.argv
    pb = render_playbook(open(PLAYBOOK, encoding="utf-8").read())
    outs = {
        PLAYBOOK: pb,
        os.path.join(WP, "funnel-equations.json"): json.dumps(model_json(), ensure_ascii=False, indent=1) + "\n",
        os.path.join(ROOT, "app/public/materials/funnel-equations.json"): json.dumps(model_json(), ensure_ascii=False, indent=1) + "\n",
        os.path.join(ROOT, "app/src/generated/funnel-model.ts"): render_ts(),
        os.path.join(ROOT, "app/src/generated/funnel-model.css"): render_css(pb),
        os.path.join(ROOT, "cloud/src/generated/pack-equations.ts"): render_pack(),
        os.path.join(WP, "revops-funnel-equations/index.html"): render_standalone(pb),
    }
    stale = []
    for p, txt in outs.items():
        cur = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if cur != txt:
            stale.append(os.path.relpath(p, ROOT))
            if not check:
                open(p, "w", encoding="utf-8").write(txt)
    print(("stale: " if check else "wrote: ") + (", ".join(stale) or "nothing"), f"· {len(LINES)} lines · {len(VARS)} short forms")
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
