import random
import time

balance = 1000
wins = 0
losses = 0
trades = 0

print("Trading Bot Started")

while trades < 10:

    prices = [
        random.randint(100,200),
        random.randint(100,200),
        random.randint(100,200),
        random.randint(100,200),
        random.randint(100,200)
    ]

    up = 0
    down = 0

    for i in range(len(prices)-1):
        if prices[i+1] > prices[i]:
            up += 1
        elif prices[i+1] < prices[i]:
            down += 1

    if up >= 3:
        signal = "BUY"
    elif down >= 3:
        signal = "SELL"
    else:
        signal = "NO_TRADE"

    print("Signal:", signal)

    if signal != "NO_TRADE":

        result = random.choice(["WIN","LOSS"])

        if result == "WIN":
            balance += 10
            wins += 1
        else:
            balance -= 10
            losses += 1

        trades += 1

    time.sleep(1)

print("Balance:", balance)
print("Wins:", wins)
print("Losses:", losses)
