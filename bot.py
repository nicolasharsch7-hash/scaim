import os
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔐 TOKEN (mejor desde variables de entorno)
TOKEN = ("8656921886:AAGOdVdXeb8s0CMwacYY1PC7OK8ohMFhCo0")

# ---------------- USERS ----------------
users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {
            "balance": round(random.uniform(1000, 9000), 2),
            "profit": 0,
            "level": 1,
            "referrals": 0
        }
    return users[uid]

# ---------------- PRICE ----------------
def price(symbol):
    try:
        r = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}",
            timeout=5
        )
        return float(r.json()["price"])
    except:
        return 0.0

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user.id)

    await update.message.reply_text(f"""
💎 Quantum Trade

💰 Balance: ${u['balance']:.2f}
📊 Nivel: {u['level']}

Comandos:
/panel /trade /market /dashboard
""")

# ---------------- PANEL ----------------
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user.id)

    await update.message.reply_text(f"""
📊 DASHBOARD

💰 Balance: ${u['balance']:.2f}
📈 Profit: ${u['profit']:.2f}
🏆 Nivel: {u['level']}
👥 Referidos: {u['referrals']}
""")

# ---------------- TRADE ----------------
async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user.id)

    profit = round(random.uniform(5, 3276), 2)
    win = random.choice([True, False])

    if win:
        u["balance"] += profit
        u["profit"] += profit
    else:
        u["balance"] -= profit * 0.3

    await update.message.reply_text(
        f"📈 {'WIN ✅' if win else 'LOSS ❌'} | ${profit}"
    )

# ---------------- MARKET ----------------
async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btc = price("BTCUSDT")
    eth = price("ETHUSDT")

    await update.message.reply_text(f"""
📊 MARKET LIVE

₿ BTC: ${btc:.2f}
Ξ ETH: ${eth:.2f}
""")

# ---------------- DASHBOARD LINK ----------------
async def dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Panel web:\nhttp://localhost:10000 (demo local)"
    )

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("panel", panel))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(CommandHandler("market", market))
app.add_handler(CommandHandler("dashboard", dashboard))

print("🚀 Quantum Trade FULL activo")

app.run_polling(drop_pending_updates=True)