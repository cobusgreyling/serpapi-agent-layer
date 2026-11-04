import json, statistics as st, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.style.use("dark_background"); R=json.load(open("runs.json")); m=lambda k,f: st.median(x[f] for x in R[k])
L=["raw SerpApi JSON","formatted (uncached)","formatted (cached)"]; K=["raw","fmt_uncached","fmt_cached"]; C=["#f5a623","#29d3c3","#7cff9b"]
fig,ax=plt.subplots(figsize=(9,5)); v=[m(k,"tok") for k in K]; b=ax.bar(L,v,color=C); ax.set_yscale("log")
ax.bar_label(b,[f"{int(x):,}" for x in v]); ax.set_title("Context tokens fed to the model (o200k_base, median of 3)"); ax.set_ylabel("tokens (log)")
plt.tight_layout(); plt.savefig("chart_tokens.svg")
fig,ax=plt.subplots(figsize=(9,5)); L2=["browser agent\n(DOM read, est.)"]+L; v=[105]+[m(k,"lat") for k in K]
b=ax.bar(L2,v,color=["#ff5c7a"]+C); ax.set_yscale("log")
ax.bar_label(b,["~90-120 s"]+[f"{x:.2f} s" if x>0.01 else f"{x*1e6:.1f} µs" for x in v[1:]])
ax.set_title("Wall-clock latency, flights + hotels (median of 3; GUI = 1 run)"); ax.set_ylabel("seconds (log)")
plt.tight_layout(); plt.savefig("chart_latency.svg")
