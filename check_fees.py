import os, json, requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = "252561990"
LIMITS = {"ERC20": 2.9, "TRC20": 2.9}

url = "https://api.coinex.com/v2/assets/deposit-withdraw-config?ccy=USDT"
chains = requests.get(url, timeout=55).json()["data"]["chains"]
fees = {c["chain"]: float(c["withdrawal_fee"]) for c in chains if c["chain"] in LIMITS}

alerts = [f"{c}: {f} USDT" for c, f in fees.items() if f <= LIMITS[c]]
if alerts:
    msg = "💸 CoinEx fees ↓\n" + "\n".join(alerts)
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": CHAT_ID, "text": msg})
