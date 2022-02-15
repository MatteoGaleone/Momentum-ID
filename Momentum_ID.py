import yahoo_fin.stock_info as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
import plotly.express as px



def tickers():
    #t = yf.tickers_sp500(include_company_data=False)

    t = []
    nt = int(input('Insert stock number:'))
    for i in range(nt):
        ticker = str(input('Insert ticker of the stock number ' + str(i) + ':'))
        t.append(ticker)
    return t

def Calculation_Momentum_ID(t):
    Start = datetime.now() - timedelta(days=360)
    End = datetime.now() - timedelta(days=30)
    Interval = '1d'
    Momentum = []
    Information_Discreteness = []
    Ticker = []

    for x in t:
        try:
            Yield = []
            Stock_TS = yf.get_data(x, start_date=Start, end_date=End, interval=Interval)
            Stock_TS = Stock_TS['close']
            first_price = Stock_TS[1]
            last_price = Stock_TS[-1]

            Momentum_Stock = last_price / first_price - 1

            for i in range(1, len(Stock_TS)):
                if Stock_TS[i] / Stock_TS[i - 1] - 1 < 0:
                    Yield.append(0)
                else:
                    Yield.append(1)

            total_days = len(Yield)
            positive_days = sum(Yield)
            perc_positive = positive_days / total_days * 100
            perc_negative = 100 - perc_positive

            if Momentum_Stock > 0:
                return_sign = 1
            else:
                return_sign = -1

            ID = return_sign * (perc_negative - perc_positive)

            Momentum.append(Momentum_Stock)
            Information_Discreteness.append(ID)
            Ticker.append(x)

        except:
            continue

    Data = {'Ticker': Ticker, 'Momentum': Momentum, 'Information_Discreteness': Information_Discreteness}
    Momentum_ID = pd.DataFrame(Data)

    return Momentum_ID

def Graphic(Momentum_ID):
    fig = px.scatter(Momentum_ID, x="Momentum", y="Information_Discreteness",
                     color='Ticker')
    return fig.show()

def Program():
    while True:
        t = tickers()
        Momentum_ID = Calculation_Momentum_ID(t)
        excel = pd.ExcelWriter('Momentum_ID_Stocks.xlsx', engine='xlsxwriter')
        Momentum_ID.to_excel(excel, sheet_name='Stocks')
        excel.save()
        Graphic(Momentum_ID)
        while True:
            response = str(input('You want to see a new graphic? (yes/no): '))
            if response in ('yes', 'no'):
                break
            print('Input not valid.')
        if response == 'yes':
            continue
        else:
            print('Bye')
            break

Program()
