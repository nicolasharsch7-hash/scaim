from flask import Flask, render_template_string
import random
import requests

app = Flask(__name__)

users = {
    "demo": {
        "balance": 4520.50,
        "profit": 1320.10,
        "level": 2
    }
}

def price(symbol):
    try:
        return float(requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        ).json()["price"])
    except:
        return 0

HTML = """
<html>
<head>
<title>Quantum Trade Dashboard</title>
<style>
body { background:#0d1117; color:white; font-family:Arial; }
.card { background:#161b22; padding:20px; margin:10px; border-radius:10px; }
</style>
</head>
<body>

<h1>💎 Quantum Trade Dashboard (Demo)</h1>

<div class="card">
💰 Balance: ${{balance}}
📈 Profit: ${{profit}}
🏆 Level: {{level}}
</div>

<div class="card">
₿ BTC: ${{btc}}
Ξ ETH: ${{eth}}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    u = users["demo"]

    return render_template_string(
        HTML,
        balance=u["balance"],
        profit=u["profit"],
        level=u["level"],
        btc=price("BTCUSDT"),
        eth=price("ETHUSDT")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
