"""SK 2026: parse raw bookmaker files, power de-vig, consensus, blend with AI snapshot.

usage: python3 scripts/sk2026/market.py <date> [<ai-snapshot-date>]
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forecast_math import power_fair, blend_dist  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MKT = ROOT / "data/sk-2026/market"
RHO = 0.55


def parse_raw(path):
    out = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        race, rest = line.split(":", 1)
        odds = {}
        for item in rest.split("|")[0].split(";"):
            m = re.match(r"\s*(\S+)\s+([0-9.]+)", item)
            if m:
                odds[m.group(1)] = float(m.group(2))
        out[race.strip()] = odds
    return out


def to_keys(fair, keys):
    d = {k: 0.0 for k in keys}
    for name, p in fair.items():
        d[name if name in d else "Someone_else"] = d.get(name if name in d else "Someone_else", 0.0) + p
    return d


def main():
    date = sys.argv[1]
    ai_date = sys.argv[2] if len(sys.argv) > 2 else date
    ai = json.loads((ROOT / f"data/sk-2026/snapshots/{ai_date}-ai.json").read_text())["races"]
    ai = {v["race_id"]: v["dist"] for v in ai.values()}
    books = {p.stem.split("-")[1]: parse_raw(p) for p in sorted(MKT.glob(f"raw-*-{date}.txt"))}
    res = {}
    for race, dist in sorted(ai.items()):
        keys = list(dist)
        if "Someone_else" not in keys:
            keys.append("Someone_else")
        per_book = {}
        for b, races in books.items():
            if race in races and len(races[race]) > 1:
                fair = power_fair(races[race])
                per_book[b] = {"margin": round(sum(1 / o for o in races[race].values()) - 1, 4),
                               "dist": to_keys(fair, keys)}
        if not per_book:
            res[race] = {"ai": dist, "market": None, "blend": dist, "books": {}}
            continue
        cons = {k: sum(pb["dist"][k] for pb in per_book.values()) / len(per_book) for k in keys}
        aid = {k: dist.get(k, 0.0) for k in keys}
        res[race] = {"ai": dist, "books": per_book, "market": cons, "blend": blend_dist(aid, cons, RHO)}
    out = MKT / f"{date}.json"
    out.write_text(json.dumps({"date": date, "ai_snapshot": ai_date, "rho": RHO, "devig": "power",
                               "races": res}, ensure_ascii=False, indent=1))
    print(f"{'race':8} {'AI fav':24} {'Market fav':24} {'Blend fav':24} books")
    for race, r in res.items():
        f = lambda d: (lambda k: f"{k} {d[k]*100:.0f}")(max(d, key=d.get)) if d else "-"
        print(f"{race:8} {f(r['ai']):24} {f(r['market']):24} {f(r['blend']):24} {','.join(r['books'])}")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
