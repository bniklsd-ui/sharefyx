import sys, json, time
sys.path.insert(0, "/home/savefyx/dev/savefxy/phase10_inventory/probes")
import p10_pf_eventloop_probe as P
from playwright.sync_api import sync_playwright
creds = json.loads((P.ROOT/"credentials.json").read_text())["users"][0]
with sync_playwright() as pw:
    br = pw.chromium.launch(); ctx = br.new_context(viewport={"width":1440,"height":900}, ignore_https_errors=True); page = ctx.new_page()
    P.login(page, creds)
    n = {"c": 0, "log": []}
    t0 = [0]
    def rq(r):
        if r.url.endswith("/api/v1/overview"):
            n["c"] += 1; n["log"].append(round(time.time() - t0[0], 1))
    page.on("request", rq)
    t0[0] = time.time()
    page.goto(P.BASE + "/ui/"); page.wait_for_selector("button.tree__folder[data-space='alpha']", timeout=60000); time.sleep(6)
    base = n["c"]
    time.sleep(4); k_ruhe = n["c"] - base            # Kontrolle, keine Aktion (t~10-14 s)
    base = n["c"]
    page.evaluate("window.dispatchEvent(new Event('focus'))"); time.sleep(4); k_focus = n["c"] - base   # t~14-18 s
    print(json.dumps({"nach_laden": base, "kontrolle_ruhe_4s": k_ruhe, "focus_event_4s": k_focus, "request_zeiten_s": n["log"]}))
    br.close()
