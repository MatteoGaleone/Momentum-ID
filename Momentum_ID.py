import yahoo_fin.stock_info as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
import plotly.express as px



def tickers():
    t = yf.tickers_sp500(include_company_data=False)

    # t = []
    # nt = int(input('Inserire numero di azioni da confrontare:'))
    # for i in range(nt):
    # ticker = str(input('''Inserisci ticker dell'impresa numero ''' + str(i) + ':'))
    # t.append(ticker)
    return t

def Calcolo_Momentum_ID(t):
    Start = datetime.now() - timedelta(days=360)
    End = datetime.now() - timedelta(days=30)
    Interval = '1d'
    Momentum = []
    Information_Discreteness = []
    Ticker = []

    for x in t:
        try:
            Rendimenti = []
            Azione_SS = yf.get_data(x, start_date=Start, end_date=End, interval=Interval)
            Azione_SS = Azione_SS['close']
            primo_prezzo = Azione_SS[1]
            ultimo_prezzo = Azione_SS[-1]

            Momentum_Azione = ultimo_prezzo / primo_prezzo - 1

            for i in range(1, len(Azione_SS)):
                if Azione_SS[i] / Azione_SS[i - 1] - 1 < 0:
                    Rendimenti.append(0)
                else:
                    Rendimenti.append(1)

            giorni_totali = len(Rendimenti)
            giorni_positivi = sum(Rendimenti)
            perc_positivi = giorni_positivi / giorni_totali * 100
            perc_negativi = 100 - perc_positivi

            if Momentum_Azione > 0:
                return_sign = 1
            else:
                return_sign = -1

            ID = return_sign * (perc_negativi - perc_positivi)

            Momentum.append(Momentum_Azione)
            Information_Discreteness.append(ID)
            Ticker.append(x)

        except:
            continue

    Data = {'Ticker': Ticker, 'Momentum': Momentum, 'Information_Discreteness': Information_Discreteness}
    Momentum_ID = pd.DataFrame(Data)

    return Momentum_ID

def Grafico(Momentum_ID):
    fig = px.scatter(Momentum_ID, x="Momentum", y="Information_Discreteness",
                     color='Ticker')
    return fig.show()

def Programma():
    while True:
        t = tickers()
        Momentum_ID = Calcolo_Momentum_ID(t)
        excel = pd.ExcelWriter('Momentum_ID_Azioni.xlsx', engine='xlsxwriter')
        Momentum_ID.to_excel(excel, sheet_name='Azione')
        excel.save()
        Grafico(Momentum_ID)
        while True:
            risposta = str(input('Vuoi visualizzare un nuovo grafico? (si/no): '))
            if risposta in ('si', 'no'):
                break
            print('Input non valido.')
        if risposta == 'si':
            continue
        else:
            print('Ciao')
            break

Programma()