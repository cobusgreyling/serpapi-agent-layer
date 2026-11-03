import json, statistics as st, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
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
fig,ax=plt.subplots(figsize=(10,6)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,10)
for y,c,t,s in [(0.5,"#ff5c7a","GUI layer  (computer use)","private / logged-in / interactive  ·  screenshots + clicks  ·  slow, token-heavy"),
               (3.8,"#f5a623","Structured public data layer  (SerpApi)","Flights · Hotels · Jobs · News · Scholar · Maps  ->  JSON  (~80k tokens here)"),
               (7.1,"#29d3c3","Formatted context layer","keep needed fields · compact records · source URL per fact · cache  (~900 tokens)")]:
    ax.add_patch(FancyBboxPatch((0.5,y),9,2.2,boxstyle="round,pad=0.1",fc=c+"22",ec=c,lw=2))
    ax.text(5,y+1.4,t,ha="center",fontsize=15,color=c,weight="bold"); ax.text(5,y+0.6,s,ha="center",fontsize=10,color="#ddd")
ax.annotate("",xy=(9.75,9.3),xytext=(9.75,0.6),arrowprops=dict(arrowstyle="->",color="#888"))
ax.text(9.9,5,"cheaper, faster",rotation=90,va="center",color="#888")
ax.set_title("Route each request to the cheapest layer that can answer it",fontsize=13)
plt.tight_layout(); plt.savefig("architecture.svg")
