import json, statistics as st, csv, tiktoken, layer
enc = tiktoken.get_encoding("o200k_base"); tok = lambda s: len(enc.encode(s))
FL = dict(engine="google_flights", departure_id="JNB", arrival_id="AUH", outbound_date="2026-11-11",
          return_date="2026-11-16", type="1", currency="USD", hl="en", gl="za")
HO = dict(engine="google_hotels", q="Abu Dhabi hotels", check_in_date="2026-11-11", check_out_date="2026-11-16",
          adults="1", currency="USD", hl="en", gl="za")
rows, runs = [], {"raw": [], "fmt_uncached": [], "fmt_cached": []}
for i in range(3):
    fd, ftxt, fdt = layer.fetch_raw(FL); hd, htxt, hdt = layer.fetch_raw(HO)
    # raw as fed to a model: compact JSON dump of the full responses
    raw_ctx = json.dumps(fd, separators=(",", ":")) + json.dumps(hd, separators=(",", ":"))
    runs["raw"].append(dict(lat=fdt + hdt, fl=fdt, hl=hdt, bytes=len(ftxt) + len(htxt), tok=tok(raw_ctx)))
    layer._CACHE.clear()
    c1, t1, _ = layer.formatted(FL, layer.fmt_flights); c2, t2, _ = layer.formatted(HO, layer.fmt_hotels)
    ctx = c1 + "\n\n" + c2
    runs["fmt_uncached"].append(dict(lat=t1 + t2, bytes=len(ctx.encode()), tok=tok(ctx)))
    c1, t1, h1 = layer.formatted(FL, layer.fmt_flights); c2, t2, h2 = layer.formatted(HO, layer.fmt_hotels)
    assert h1 and h2
    runs["fmt_cached"].append(dict(lat=t1 + t2, bytes=len(ctx.encode()), tok=tok(ctx)))
    print(i, {k: v[-1] for k, v in runs.items()}, flush=True)
open("sample_context.txt", "w").write(ctx)
json.dump(runs, open("runs.json", "w"), indent=1)
med = lambda k, f: st.median(r[f] for r in runs[k])
with open("results.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["metric", "computer use (GUI)", "raw SerpApi JSON", "formatted layer (uncached)", "formatted layer (cached)"])
    w.writerow(["median_latency_s", "", *(round(med(k, "lat"), 3 if k != "fmt_cached" else 6) for k in runs)])
    w.writerow(["median_context_tokens", "", *(med(k, "tok") for k in runs)])
    w.writerow(["median_context_bytes", "", *(med(k, "bytes") for k in runs)])
    w.writerow(["runs", "", 3, 3, 3])
print(open("results.csv").read())
