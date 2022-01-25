import pandas as pd
from yahoo_fin import options
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import seaborn

pd.set_option("display.max_columns", None)

stock = "bbby"
# stk = yf.Ticker(stock)
# output = stk.option_chain(date=stk.options[0])

# print(stk.options[0])
# print(output)
# print(stk.info)
# expirationDates = options.get_expiration_dates(stock)
# calls = options.get_calls(stock, expirationDates[0])

# output = calls

# h = pd.DataFrame(output, columns=["Strike", "Ask"])
# # print(output["Strike"]output["Ask"])
# # print(h)
# print(output)
print(options.get_calls(stock)["Strike"][2] -
      options.get_calls(stock)["Strike"][1])
# def call_payoff(sT, strike_price, premium):
#     return np.where(sT > strike_price, sT-strike_price, 0)-premium


# sT = np.arange(100, 130, 1)

# lower_strike_price_long_call = 110
# premium_lower_strike_long_call = 24.85

# higher_strike_price_long_call = 120
# premium_higher_strike_long_call = 15.05

# strike_price_short_call = 115
# premium_short_call = 20.25

# lower_strike_long_call_payoff = call_payoff(
#     sT, lower_strike_price_long_call, premium_lower_strike_long_call)
# higher_strike_long_call_payoff = call_payoff(
#     sT, higher_strike_price_long_call, premium_higher_strike_long_call)
# Short_call_payoff = call_payoff(
#     sT, strike_price_short_call, premium_short_call)*-1.0
# Butterfly_spread_payoff = lower_strike_long_call_payoff + \
#     higher_strike_long_call_payoff + 2 * Short_call_payoff


# # Range of call option at expiration


# fig, ax = plt.subplots()
# ax.spines['bottom'].set_position('zero')
# ax.plot(sT, Butterfly_spread_payoff, color='b', label='Butterfly Spread')
# ax.plot(sT, lower_strike_long_call_payoff, '--',
#         color='g', label='Lower Strike Long Call')
# ax.plot(sT, higher_strike_long_call_payoff, '--',
#         color='g', label='Higher Strike Long Call')
# ax.plot(sT, Short_call_payoff, '--', color='r', label='Short call')
# plt.legend()
# plt.xlabel('Stock Price')
# plt.ylabel('Profit & Loss')
# plt.savefig("graph.png")

# profit = max(Butterfly_spread_payoff)
# loss = min(Butterfly_spread_payoff)

# print("%.2f" % profit)
# print("%.2f" % loss)
