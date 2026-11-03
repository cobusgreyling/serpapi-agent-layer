"""Formatted context layer over SerpApi: keep only needed fields, compact records, source URL per fact, simple cache."""
import json, time, hashlib, os, requests
API = "https://serpapi.com/search.json"
_CACHE = {}

def fetch_raw(params, no_cache=True):
    p = dict(params, api_key=os.environ["SERPAPI_API_KEY"])
    if no_cache: p["no_cache"] = "true"   # force SerpApi to run a live search
    t = time.perf_counter(); r = requests.get(API, params=p, timeout=120); dt = time.perf_counter() - t
    r.raise_for_status(); return r.json(), r.text, dt

def _src(d):  # public source URL, api_key stripped
    m = d.get("search_metadata", {})
    return m.get("google_flights_url") or m.get("google_hotels_url") or m.get("prettify_html_file")

def fmt_flights(d, n=5):
    src = _src(d); out = []
    for f in (d.get("best_flights", []) + d.get("other_flights", [])):
        legs = f["flights"]
        out.append({"price": f.get("price"), "airline": "/".join(dict.fromkeys(l["airline"] for l in legs)),
                    "dep": legs[0]["departure_airport"]["time"], "arr": legs[-1]["arrival_airport"]["time"],
                    "stops": len(legs) - 1, "mins": f.get("total_duration"), "src": src})
    out = sorted([o for o in out if o["price"]], key=lambda o: o["price"])[:n]
    return out

def fmt_hotels(d, n=3):
    src = _src(d); out = []
    for h in d.get("properties", []):
        rate = (h.get("rate_per_night") or {}).get("extracted_lowest")
        if rate is None: continue
        out.append({"name": h.get("name"), "rate": rate, "rating": h.get("overall_rating"),
                    "link": h.get("link") or src, "src": src})
    return out[:n]

def to_context(records):
    """Compact pipe-delimited lines: header once, one record per line."""
    if not records: return ""
    keys = list(records[0]); return "\n".join(["|".join(keys)] + ["|".join(str(r[k]) for k in keys) for r in records])

def formatted(params, fmt, use_cache=True):
    key = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()
    t = time.perf_counter()
    if use_cache and key in _CACHE: return _CACHE[key], time.perf_counter() - t, True
    d, _, _ = fetch_raw(params); ctx = to_context(fmt(d)); _CACHE[key] = ctx
    return ctx, time.perf_counter() - t, False
