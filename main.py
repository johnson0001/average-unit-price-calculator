import pandas as pd

import module


# read trade history file
csv_path = "trade_history_20220724095343.csv"
trade_df = pd.read_csv(csv_path, header=0)
trade_df["取引日時"] = pd.to_datetime(trade_df["取引日時"], infer_datetime_format=True)
trade_df = trade_df.sort_values(by="取引日時", ascending=True)
symbols = trade_df["通貨ペア"].unique()
jpy_symbols = [symbol for symbol in symbols if '_jpy' in symbol]


# prepare result dataframe
columns = ['Symbol', 'Amount', 'Avg Price', 'Current Price', 'Evaluated', 'Unrealized', "Unrealized (%)"]
result_df = pd.DataFrame([], columns=columns)


# for each jpy symbols
for i, symbol in enumerate(jpy_symbols):

    # get current price
    current_price = module.get_current_price(symbol)

    # calculate btc trading cost
    btc_trade_pl = module.btc_trade_result(trade_df, symbol)

    # get new df by symbol
    df = trade_df[trade_df["通貨ペア"] == symbol]

    # calculate average trading cost
    average_cost, current_amount = module.average_trade_cost(df, btc_trade_pl)
    if current_amount <= 0:
        continue
    evaluated = float(current_price) * current_amount
    unrealized = (float(current_price) - average_cost) * current_amount
    unrealized_per = (float(current_price) - average_cost) / average_cost * 100

    # add data to result df
    data = [symbol, current_amount, average_cost, current_price, evaluated, unrealized, unrealized_per]
    result_df.loc[i, :] = data
    
print(result_df)