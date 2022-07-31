"""
price: acquisition price
average_price: average acquisition price
current_price: current price of the coin
total_cost: total cost of acquisition
fee: trading fees
average_cost: average cost of acquistion
amount: acquisition amount in one trade
total amount: total amount of my own coin

average_cost = total_cost / total_amount
cost = price * amount + fee

In my case, opening balance of btc is -0.0024 because I lost the amount of btc by trading with ltc/btc.
"""

import requests
import pandas as pd

def get_current_price(symbol):
    url = "https://public.bitbank.cc/" + symbol + "/ticker"
    r = requests.get(url, timeout=10)
    r = r.json()
    current_price = r["data"]["last"]
    
    return current_price


def trade_cost(row):
    side = row[4]
    amount = row[5]
    price = row[6]
    fee = row[7]

    if side == "buy":
        cost = amount * price + fee
        flag = True

    elif side == "sell":
        cost = fee
        flag = False

    return cost, amount, flag
    

def average_trade_cost(trade_histyory, opening_balance=0):

    total_cost = 0
    total_amount = 0
    current_amount = opening_balance

    for row in trade_histyory.values:
        cost, amount, flag = trade_cost(row)
        
        if flag:
            total_cost += cost
            total_amount += amount
            current_amount += amount
            average_cost = total_cost / total_amount

        else:
            total_cost += cost
            current_amount -= amount
            average_cost = total_cost / total_amount

    return average_cost, current_amount


def btc_trade_result(trade_df, symbol):

    symbols = trade_df["通貨ペア"].unique()

    if symbol == "btc_jpy":
        btc_symbols = [btc_symbol for btc_symbol in symbols if '_btc' in btc_symbol]

        pl = 0 # amount of profit and loss
        for btc_symbol in btc_symbols:
            df = trade_df[trade_df["通貨ペア"] == btc_symbol].copy()
            df["cost"] = df["数量"] * df["価格"]
            pl += df[df["売/買"] == "sell"]["cost"].sum() - df[df["売/買"] == "buy"]["cost"].sum() - df["手数料"].sum()
        
        return pl

    else:
        btc_symbol = symbol.split('_')[0] + "_btc"
        df = trade_df[trade_df["通貨ペア"] == btc_symbol]
        pl = df[df["売/買"] == "buy"]["数量"].sum() - df[df["売/買"] == "sell"]["数量"].sum()

        return pl


if __name__ == '__main__':

    # csv_path = "trade_history_20220724095343.csv"
    symbol = "btc_jpy"
    # df = pd.read_csv(csv_path, header=0)
    # symbols = df["通貨ペア"].unique()