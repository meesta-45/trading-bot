import websocket
import json
import statistics
import threading
from flask import Flask

# ----------------------------
# FLASK SERVER (Render fix)
# ----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Trading Bot is LIVE"

def run_server():
    app.run(host="0.0.0.0", port=10000)


# ----------------------------
# TRADING STATE
# ----------------------------
prices = []

balance = 1000
wins = 0
losses = 0
trades = 0


# ----------------------------
# STRATEGY LOGIC
# ----------------------------
def trade_logic():
    global balance, wins, losses, trades

    if len(prices) < 5:
        return

    recent = prices[-5:]
    avg = statistics.mean(recent)
    current = recent[-1]

    signal = "NO_TRADE"

    if current > avg:
        signal = "BUY"
    elif current < avg:
        signal = "SELL"

    print("Prices:", recent)
    print("Signal:", signal)

    if signal != "NO_TRADE":

        # PAPER TRADE SIMULATION
        import random
        result = random.choice(["WIN", "LOSS"])

        trades += 1

        if result == "WIN":
            balance += 10
            wins += 1
        else:
            balance -= 10
            losses += 1

        print("Balance:", balance)
        print("Wins:", wins, "Losses:", losses)
        print("Trades:", trades)
        print("----------------------")


# ----------------------------
# DERIV WEBSOCKET HANDLERS
# ----------------------------
def on_message(ws, message):
    data = json.loads(message)

    if "tick" in data:
        price = float(data["tick"]["quote"])
        prices.append(price)

        print("Live Price:", price)

        trade_logic()


def on_open(ws):
    print("Connected to Deriv WebSocket")

    req = {
        "ticks": "R_75"
    }

    ws.send(json.dumps(req))


# ----------------------------
# START BOT
# ----------------------------
def start_bot():
    print("Connecting to Deriv...")

    ws = websocket.WebSocketApp(
        "wss://ws.binaryws.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message
    )

    ws.run_forever()


# ----------------------------
# RUN BOTH SERVER + BOT
# ----------------------------
if __name__ == "__main__":

    # Start web server for Render
    threading.Thread(target=run_server).start()

    # Start trading bot
    start_bot()
