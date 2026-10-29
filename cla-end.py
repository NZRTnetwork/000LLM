r"""Close a CLA session ticket: HTML summary to note_public, then status 8 + date_close.

Usage: python cla-end.py --ticket-id 749 --note "<p><strong>Session TS2610-0408 complete.</strong></p>..."
Auth: DOLIBARR_API_KEY env var, else RPO-agt\.env
"""
import argparse, io, os, sys, time
import requests
from dotenv import dotenv_values

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
BASE = "https://erp.nzrtnetwork.com/dolibarr/api/index.php"
ENV = r"C:\RPO-SAI\SYS\PLA\WIN\FRA\FAI\ORG\RPO-NZT\OPS\RPO-agt\.env"

p = argparse.ArgumentParser()
p.add_argument("--ticket-id", type=int, required=True)
p.add_argument("--note", required=True)
a = p.parse_args()

key = os.environ.get("DOLIBARR_API_KEY") or dotenv_values(ENV).get("DOLIBARR_API_KEY", "")
h = {"DOLAPIKEY": key, "Accept": "application/json", "Content-Type": "application/json"}
url = f"{BASE}/tickets/{a.ticket_id}"
print("note_public:", requests.put(url, headers=h, json={"note_public": a.note}, timeout=10).status_code)
print("close:", requests.put(url, headers=h, json={"status": 8, "date_close": int(time.time())}, timeout=10).status_code)
g = requests.get(url, headers=h, timeout=10).json()
print("status:", g.get("status"), "date_close:", g.get("date_close"))
