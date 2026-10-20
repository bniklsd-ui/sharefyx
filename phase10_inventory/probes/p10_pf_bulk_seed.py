"""Seed fuer die PF-Probe: N Zusatz-Items in alpha der Wegwerf-Instanz (Port 8799, tmp-DATA_ROOT).
Aufruf: env -i HOME=$HOME PATH=$PATH .venv/bin/python phase10_inventory/probes/p10_pf_bulk_seed.py 500
Es wurden 3000 gesaeet (/overview 27 s, zu gross) und auf 500 gekuerzt (~4,4-4,9 s, wie live).
Strg: Server vorher mit p10_wegwerf.py stop beenden, danach start.
"""
import sys, time
sys.path.insert(0, "/home/savefyx/dev/savefxy")
from datetime import datetime, timezone
from storage.store import Store
s = Store("/tmp/opencode/sharefyx-wegwerf-p10/data", now_fn=lambda: datetime.now(timezone.utc), git=False)
t=time.time()
for i in range(int(sys.argv[1])):
    s.create("alpha", type="note" if i%3 else "task", title=f"Bulk {i}", tags=["bulk", f"t{i%20}"], folder=f"B{i%10}", body="x"*400)
s.rebuild_index()
print("seeded", time.time()-t, file=sys.stderr)
