"""Download 5 years of daily prices for the dashboard and save them to data/stocks.json.

Run locally:   pip install yfinance && python scripts/fetch_data.py
Runs on GitHub automatically through .github/workflows/update-data.yml
"""
import json
import os
import sys
from datetime import datetime, timezone

import yfinance as yf

# Keep this list in sync with SYMBOLS in index.html (Yahoo Finance tickers).
SYMBOLS = [
    "^NSEI",
    "^BSESN",
    "^NSEBANK",
    "^CNXIT",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "BAJFINANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HCLTECH.NS",
    "WIPRO.NS",
    "RELIANCE.NS",
    "ONGC.NS",
    "NTPC.NS",
    "POWERGRID.NS",
    "COALINDIA.NS",
    "ITC.NS",
    "HINDUNILVR.NS",
    "ASIANPAINT.NS",
    "TITAN.NS",
    "DMART.NS",
    "SUNPHARMA.NS",
    "CIPLA.NS",
    "DRREDDY.NS",
    "TATASTEEL.NS",
    "HINDALCO.NS",
    "JSWSTEEL.NS",
    "BHARTIARTL.NS",
    "MARUTI.NS",
    "LT.NS",
    "ADANIENT.NS",
]

out = {"updated": datetime.now(timezone.utc).isoformat(), "symbols": {}}

for sym in SYMBOLS:
    try:
        df = yf.Ticker(sym).history(period="5y", interval="1d", auto_adjust=False)
        df = df.dropna(subset=["Close"])
        if len(df) < 2:
            print("skipped (no data):", sym)
            continue
        out["symbols"][sym] = {
            "t": [int(ts.timestamp() * 1000) for ts in df.index],
            "c": [round(float(x), 2) for x in df["Close"]],
            "v": [int(x) for x in df["Volume"].fillna(0)],
        }
        print("ok:", sym, len(df), "days")
    except Exception as exc:  # keep going if one ticker fails
        print("failed:", sym, exc)

if not out["symbols"]:
    sys.exit("No data downloaded, leaving the old file untouched.")

os.makedirs("data", exist_ok=True)
with open("data/stocks.json", "w", encoding="utf-8") as f:
    json.dump(out, f, separators=(",", ":"))
print("saved", len(out["symbols"]), "symbols")
