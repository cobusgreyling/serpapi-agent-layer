"""Tiny router: send a request to the cheapest layer that can answer it.
private/interactive -> GUI computer use; public lookup -> structured API (SerpApi) via formatted layer."""
import re
PRIVATE = r"\b(my|our|account|inbox|login|log in|portal|dashboard|internal|bank|invoice|order history|submit|book|pay|checkout|upload|fill (in|out))\b"
ENGINES = {"google_flights": r"\bflights?|fly|airfare\b", "google_hotels": r"\bhotels?|stay|accommodation\b",
           "google_jobs": r"\bjobs?|hiring|vacanc", "google_news": r"\bnews|latest|announced\b",
           "google_scholar": r"\bpapers?|arxiv|citations?\b", "google_maps": r"\bnear|restaurants?|directions\b"}

def route(req: str) -> dict:
    r = req.lower()
    if re.search(PRIVATE, r):
        return {"layer": "private-GUI", "why": "needs a logged-in session or a state-changing action"}
    for eng, pat in ENGINES.items():
        if re.search(pat, r):
            return {"layer": "public-structured-API", "engine": eng, "then": "formatted context layer"}
    return {"layer": "public-structured-API", "engine": "google", "then": "formatted context layer"}

if __name__ == "__main__":
    for q in ["Cheapest JNB to AUH flight on 11 Nov", "3 hotels in Abu Dhabi for 11-16 Nov",
              "Who is hiring voice AI developer advocates?", "Latest news on Rasa",
              "Download the invoice from my bank portal", "Submit my leave form in the internal HR tool",
              "Check my order history on Takealot", "Recent arxiv papers on agent harnesses"]:
        print(f"{q:50} -> {route(q)}")
