from asyncore import write
from copyreg import constructor
import time
from urllib import response
from tda import auth, client
import config
import datetime
import yfinance as yf
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from yahoo_fin import options, stock_info


try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=r'C:\Users\harsh\Desktop\ButterflySpread\chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)

# r = c.get_price_history('AAPL',
#                         period_type=client.Client.PriceHistory.PeriodType.YEAR,
#                         period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#                         frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#                         frequency=client.Client.PriceHistory.Frequency.DAILY)
# assert r.status_code == 200, r.raise_for_status()
# print(json.dumps(r.json(), indent=4))
name = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
filename = str(name)+".txt"
sourceFile = open("./output_files/"+filename, 'w')
sourceFile.truncate(0)
# tickerList = ["OEDV", "AAPL", "BAC", "AMZN", "T", "GOOG", "MO", "DAL", "AA", "AXP", "DD", "BABA", "ABT", "UA", "AMAT", "AMGN", "AAL", "AIG", "ALL", "ADBE", "GOOGL", "ACN", "ABBV", "MT", "LLY", "AGN", "APA", "ADP", "APC", "AKAM", "NLY", "ABX", "ATVI", "ADSK", "ADM", "BMH.AX", "WBA", "ARNA", "LUV", "ACAD", "PANW", "AMD", "AET", "AEP", "ALXN", "CLMS", "AVGO",
#   "EA", "DB", "RAI", "AEM", "APD", "AMBA", "NVS", "APOL", "ANF", "LULU", "RAD", "BRK.AX", "ARRY", "AGNC", "JBLU", "A", "ORLY", "FOLD", "AZO", "ATML", "AN", "AZN", "AES", "GAS", "BUD", "ARR", "BDX", "AKS", "AB", "ACOR", "CS", "AFL", "ADI", "AEGR", "ACIW", "AMP", "AVP", "AMTD", "AEO", "AWK", "NVO", "ALTR", "ALK", "PAA", "MTU.AX", "ARCC", "AAP", "NAT", "FNMA"]

ticker_list = ['AGNC', 'LSI', 'SOFI', 'PTON', 'AAPL', 'AMD', 'NVDA', 'NFLX', 'AAL',
               'MSFT', 'FCEL', 'GRAB', 'LCID', 'INTC', 'DKNG', 'NKLA', 'ZNGA', 'TSLA', 'HBAN']

for ticker in ticker_list:
    # stk = yf.Ticker(ticker)
    # start_date = datetime.datetime.strptime(stk.options[0], '%Y-%m-%d').date()
    # end_date = datetime.datetime.strptime(stk.options[0], '%Y-%m-%d').date()

    # print(c.get_option_chain(ticker, contract_type=c.Options.ContractType.CALL,
    #       strike=12.5, from_date=start_date, to_date=end_date).json())
    try:
        step = options.get_calls(ticker)["Strike"][2] - \
            options.get_calls(ticker)["Strike"][1]
        liveprice = round(stock_info.get_live_price(ticker)) - \
            round(stock_info.get_live_price(ticker)) % step

        for x in range(-5, 5):
            time.sleep(0.5)

            # print(step)

            lower_strike_price_long_call = liveprice+step*x

            strike_price_short_call = lower_strike_price_long_call + step

            higher_strike_price_long_call = strike_price_short_call + step

            sT = np.arange(lower_strike_price_long_call-step*4,
                           higher_strike_price_long_call+step*4, step)

            # print(lower_strike_price_long_call)

            stk = yf.Ticker(ticker)
            start_date = datetime.datetime.strptime(
                stk.options[0], '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(
                stk.options[0], '%Y-%m-%d').date()
            # print(start_date)

            responseLow = c.get_option_chain(ticker, contract_type=c.Options.ContractType.CALL,
                                             strike=lower_strike_price_long_call, from_date=start_date, to_date=end_date).json()

            responseMid = c.get_option_chain(ticker, contract_type=c.Options.ContractType.CALL,
                                             strike=strike_price_short_call, from_date=start_date, to_date=end_date).json()

            responseHigh = c.get_option_chain(ticker, contract_type=c.Options.ContractType.CALL,
                                              strike=higher_strike_price_long_call, from_date=start_date, to_date=end_date).json()

            # print(json.dumps(responseHigh, indent=4))
            # resp = json.loads(responseLow)
            # print(json.dumps(responseLow, indent=4))
            # print("LOWER PRICE:", lower_strike_price_long_call)
            # print(responseHigh['callExpDateMap'])
            try:
                special_dateL = list(responseLow['callExpDateMap'].keys())[0]
                special_dateM = list(responseMid['callExpDateMap'].keys())[0]
                special_dateH = list(responseHigh['callExpDateMap'].keys())[0]
            except:
                continue
            premium_lower_strike_long_call = responseLow['callExpDateMap'][special_dateL][str(
                lower_strike_price_long_call)][0]['mark']

            premium_short_call = responseMid['callExpDateMap'][special_dateM][str(
                strike_price_short_call)][0]['mark']

            premium_higher_strike_long_call = responseHigh['callExpDateMap'][special_dateH][str(
                higher_strike_price_long_call)][0]['mark']

            # print(premium_higher_strike_long_call)
            # print(premium_short_call)
            # print(premium_lower_strike_long_call)

            def call_payoff(sT, strike_price, premium):
                return np.where(sT > strike_price, sT-strike_price, 0)-premium

            lower_strike_long_call_payoff = call_payoff(
                sT, lower_strike_price_long_call, premium_lower_strike_long_call)
            higher_strike_long_call_payoff = call_payoff(
                sT, higher_strike_price_long_call, premium_higher_strike_long_call)
            Short_call_payoff = call_payoff(
                sT, strike_price_short_call, premium_short_call)*-1.0
            Butterfly_spread_payoff = lower_strike_long_call_payoff + \
                higher_strike_long_call_payoff + 2 * Short_call_payoff

            # Range of call option at expiration

            # fig, ax = plt.subplots()
            # ax.spines['bottom'].set_position('zero')
            # ax.plot(sT, Butterfly_spread_payoff,
            #         color='b', label='Butterfly Spread')
            # ax.plot(sT, lower_strike_long_call_payoff, '--',
            #         color='g', label='Lower Strike Long Call')
            # ax.plot(sT, higher_strike_long_call_payoff, '--',
            #         color='g', label='Higher Strike Long Call')
            # ax.plot(sT, Short_call_payoff, '--', color='r', label='Short call')
            # plt.legend()
            # plt.xlabel('Stock Price')
            # plt.ylabel('Profit & Loss')
            # plt.savefig("graph.png")

            profit = max(Butterfly_spread_payoff)
            loss = min(Butterfly_spread_payoff)

            if(profit > 0 and loss > 0.05):
                print(ticker + ": " + str(strike_price_short_call), file=sourceFile)
                print(premium_higher_strike_long_call, file=sourceFile)
                print(premium_short_call, file=sourceFile)
                print(premium_lower_strike_long_call, file=sourceFile)
                print("%.2f" % profit, file=sourceFile)
                print("%.2f" % loss, file=sourceFile)
                print('\n', file=sourceFile)
    except:
        continue

sourceFile.close()
print("done")
