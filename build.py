"""SK 2026: build the public static site into ../sk-volby-2026-forecast.

usage: python3 scripts/sk2026/build.py <ai-date> <market-date>
Public series only: AI, Sázky, AI + sázky. Internal series (extremized AI, incumbent baseline)
and paper/real bets are never written to the site.
"""
import csv, html, json, shutil, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = (ROOT / "../sk-volby-2026-forecast").resolve()
sys.path.insert(0, str(Path(__file__).resolve().parent))
import texts  # noqa: E402

RACES = [
    ("vuc-ba", "Bratislavský kraj", "prim-ba", "Bratislava"),
    ("vuc-tt", "Trnavský kraj", "prim-tt", "Trnava"),
    ("vuc-tn", "Trenčiansky kraj", "prim-tn", "Trenčín"),
    ("vuc-nr", "Nitriansky kraj", "prim-nr", "Nitra"),
    ("vuc-za", "Žilinský kraj", "prim-za", "Žilina"),
    ("vuc-bb", "Banskobystrický kraj", "prim-bb", "Banská Bystrica"),
    ("vuc-po", "Prešovský kraj", "prim-po", "Prešov"),
    ("vuc-ke", "Košický kraj", "prim-ke", "Košice"),
]
NAME = {r: n for a, an, b, bn in RACES for r, n in ((a, an), (b, bn))}

CSS = """
:root{--s1:#2a78d6;--s2:#eb6834;--s3:#7a7a72;--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a64;--line:#e4e1d8;--card:#fff;--accent:#2f5d8a;--warn:#9a5b00}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--s1:#3987e5;--s2:#d95926;--s3:#a3a19a;--bg:#151514;--fg:#ecebe6;--muted:#a3a19a;--line:#2e2d2a;--card:#1d1d1b;--accent:#8fb4dc;--warn:#e0a24a}}
:root[data-theme=dark]{--s1:#3987e5;--s2:#d95926;--s3:#a3a19a;--bg:#151514;--fg:#ecebe6;--muted:#a3a19a;--line:#2e2d2a;--card:#1d1d1b;--accent:#8fb4dc;--warn:#e0a24a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.wrap{max-width:1000px;margin:0 auto;padding:24px 16px 64px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:24px}
header a.brand{font-weight:700;color:var(--fg);text-decoration:none;font-size:18px}
nav a{margin-left:14px;color:var(--accent);text-decoration:none;font-size:15px}
h1{font-size:28px;line-height:1.2;margin:8px 0}h2{font-size:20px;margin:32px 0 10px}h3{font-size:16px;margin:0 0 6px}
p.lead{color:var(--muted);margin-top:0}a{color:var(--accent)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:16px 0}
.muted{color:var(--muted)}.warn{color:var(--warn)}code{font-size:13px}
.key i{display:inline-block;width:14px;height:6px;border-radius:3px;vertical-align:middle;margin:0 5px 0 12px}
.sm{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px 26px;margin-top:12px}
.sm figure{margin:0;min-width:0}.sm figcaption{display:flex;justify-content:space-between;gap:8px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:4px;margin-bottom:6px}
.sm figcaption b{font-size:15px}.flag{font-size:11px;color:var(--warn);white-space:nowrap}
.row{display:grid;grid-template-columns:96px 1fr 92px;gap:8px;align-items:center;font-size:13px;margin:3px 0}
.row .n{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.row .v{font-variant-numeric:tabular-nums;text-align:right;color:var(--muted);white-space:nowrap}
.row .v b{color:var(--fg)}.bars{display:flex;flex-direction:column;gap:2px}.bars span{display:block;height:5px;border-radius:3px;min-width:1px}
.b1{background:var(--s1)}.b2{background:var(--s2)}.b3{background:var(--s3);opacity:.6}
.note{font-size:12px;color:var(--muted);margin-top:4px}
table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;padding:7px 6px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.03em}td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.scroll{overflow-x:auto}
footer{margin-top:48px;padding-top:12px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media (max-width:640px){h1{font-size:23px}nav a{margin-left:0;margin-right:12px}}
"""


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def load_names():
    names = {}
    for r in csv.DictReader(open(ROOT / "data/sk-2026/candidates.csv", newline="", encoding="utf-8")):
        full = r["name"].split(",")[0]
        parts = [p for p in full.split() if not p.endswith(".")]
        if not parts:
            continue
        sur = parts[-1]
        names.setdefault(r["race_id"], {})[fold(sur)] = (" ".join(parts), sur, r["incumbent"] == "yes")
    return names


def page(title, body, desc):
    nav = '<a href="index.html">Přehled</a><a href="pravidla.html">Pravidla</a><a href="denik.html">Deník</a>'
    return (f'<!doctype html><html lang="cs"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><style>{CSS}</style></head><body><div class="wrap">'
            f'<header><a class="brand" href="index.html">Slovensko 2026 · forecast</a><nav>{nav}</nav></header>{body}'
            f'<footer>Predikce generuje AI pipeline (Claude) s člověkem ve smyčce. Nejde o sázkové tipy. Obsah CC BY 4.0, kód MIT. · '
            f'<a href="https://github.com/josefslerka/sk-volby-2026-forecast">GitHub</a></footer></div></body></html>')


def pct(p):
    return "<1" if 0 < p < 0.005 else f"{p*100:.0f}"


def figure(race, r, names):
    ai, mk, bl = r["ai"], r["market"] or {}, r["blend"]
    keys = sorted(ai, key=lambda k: -(ai.get(k, 0) + mk.get(k, 0)))
    keys = [k for k in keys if k != "Someone_else" and (ai.get(k, 0) >= 0.015 or mk.get(k, 0) >= 0.015)][:4]
    rows = []
    for k in keys:
        disp, sur, inc = names.get(race, {}).get(k, (k, k, False))
        a, m, b = ai.get(k, 0), mk.get(k, 0), bl.get(k, 0)
        rows.append(
            f'<div class="row"><div class="n" title="{html.escape(disp)}">{html.escape(sur)}{" ★" if inc else ""}</div>'
            f'<div class="bars"><span class="b1" style="width:{a*100:.1f}%"></span><span class="b2" style="width:{m*100:.1f}%"></span>'
            f'<span class="b3" style="width:{b*100:.1f}%"></span></div>'
            f'<div class="v"><b>{pct(a)}</b> · {pct(m)} · {pct(b)}</div></div>')
    flag = '<span class="flag" title="Agent zahlédl titulek o kurzech nebo odkaz na interní poznámku (bez čísel), viz deník">⚠ možné ovlivnění</span>' if r.get("contamination") == "possible" else ""
    note = texts.RACE_NOTES.get(race, "")
    return (f'<figure><figcaption><b>{html.escape(NAME[race])}</b>{flag}</figcaption>{"".join(rows)}'
            f'{f"<div class=note>{note}</div>" if note else ""}</figure>')


def main():
    ai_date, mk_date = sys.argv[1], sys.argv[2]
    names = load_names()
    snap = json.loads((ROOT / f"data/sk-2026/snapshots/{ai_date}-ai.json").read_text())
    contam = {v["race_id"]: v.get("contamination_risk") for v in snap["races"].values()}
    mk = json.loads((ROOT / f"data/sk-2026/market/{mk_date}.json").read_text())
    races = mk["races"]
    for k in races:
        races[k]["contamination"] = contam.get(k)

    OUT.mkdir(exist_ok=True)
    (OUT / "data/snapshots").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / f"data/sk-2026/snapshots/{ai_date}-ai.json", OUT / f"data/snapshots/{ai_date}-ai.json")
    pub = {"date": mk_date, "devig": mk["devig"], "rho": mk["rho"], "ai_snapshot": mk["ai_snapshot"],
           "races": {k: {"market": v["market"], "blend": v["blend"],
                         "books": {b: x["dist"] for b, x in v["books"].items()}} for k, v in races.items()}}
    (OUT / f"data/snapshots/{mk_date}-market.json").write_text(json.dumps(pub, ensure_ascii=False, indent=1))

    key = ('<p class="key muted" style="font-size:14px;margin:6px 0 0"><i class="b1"></i>AI (bez kurzů)'
           '<i class="b2"></i>Sázky<i class="b3"></i>AI + sázky · čísla v pořadí AI · Sázky · AI + sázky, v % · ★ úřadující</p>')
    vuc = "".join(figure(a, races[a], names) for a, _, _, _ in RACES)
    prim = "".join(figure(b, races[b], names) for _, _, b, _ in RACES)
    body = (f"<h1>{texts.TITLE}</h1><p class=lead>{texts.LEAD}</p>{texts.CHANGES_BOX}"
            f"<h2>Předsedové krajů (VÚC)</h2>{key}<div class=sm>{vuc}</div>"
            f"<h2>Primátoři krajských měst</h2>{key}<div class=sm>{prim}</div>{texts.ABOUT}")
    (OUT / "index.html").write_text(page(texts.TITLE, body, texts.LEAD))
    (OUT / "pravidla.html").write_text(page("Pravidla · Slovensko 2026", texts.RULES, "Pravidla vyhodnocení"))
    (OUT / "denik.html").write_text(page("Deník · Slovensko 2026", texts.JOURNAL, "Deník experimentu"))
    (OUT / "data/latest.json").write_text(json.dumps({"ai": f"snapshots/{ai_date}-ai.json", "market": f"snapshots/{mk_date}-market.json"}))
    shutil.copy(Path(__file__).resolve(), OUT / "build.py")
    print("built", OUT)


if __name__ == "__main__":
    main()
