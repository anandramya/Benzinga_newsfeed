import requests
import json
import re
import csv
import datetime

import pandas as pd

from Tickers import *

from datetime import datetime

from datetime import timedelta

Column1= ["Ticker", ]

Daily_DF = pd.DataFrame(columns=Column1,)


api_token = '60d276220ee248e1b461341c1ea05ac2'
api_url_base = 'https://api.benzinga.com/api/v1'
query = '/signal/option_activity?pagesize=1000&parameters%5Bdate_from%5D='
fromDate = datetime.now().strftime("%Y-%m-%d")
toDatepre = '&parameters%5Bdate_to%5D='
toDate = datetime.now().strftime("%Y-%m-%d")
ticker_pre = '&parameters%5Btickers%5D='
ticker = 'NFLX'
token = '&token='

filename = "Daily SP500 Full" + " "+ datetime.now().strftime("%I:%M%p on %B %d, %Y")+ ".csv"

csvobj = open(filename, 'w')

writefile = csv.writer(csvobj, dialect='excel')

writefile.writerow(["Ticker","date","time", "Option activity description", "sentiment","Option bet in millions"])

headers = {'accept': 'application/json'}

#print(api_url_base+query+fromDate+toDatepre+toDate+ticker_pre+ticker+token+api_token)

for x in SP500_List:


    response = requests.get(api_url_base+query+fromDate+toDatepre+toDate+ticker_pre+x+token+api_token, headers=headers)

    #print(response.status_code)

    #print(json.loads(response.content.decode('utf-8')))

    Main_Dict=json.loads(response.content.decode('utf-8'))

    try :
        Main_List = Main_Dict['option_activity']

        Short_bull_cnt = 0
        Short_bear_cnt = 0

        Short_bull_bet = 0
        Short_bear_bet = 0

        Long_bull_cnt = 0
        Long_bear_cnt = 0

        Long_bull_bet = 0
        Long_bear_bet = 0

        for activity in Main_List:

            #print(activity["sentiment"])

            Desc_list = activity["description"].split(":")

            Second = re.split('\s',Desc_list[1].rstrip().lstrip())
            Third = re.split('\s', Desc_list[2].rstrip().lstrip())

            #print(Third)

            contracts = float(Third[0])
            price= float(Third[2][1:])

            writefile.writerow([x,activity["date"],activity["time"], activity["description"], activity["sentiment"],contracts * price * 100 / 1000000])

            csvobj.flush()

            if Second[0] == 'Fri':

                if activity["sentiment"] == 'BULLISH':
                    Short_bull_cnt = Short_bull_cnt + 1
                    Short_bull_bet = Short_bull_bet + contracts*price*100/1000000
                if activity["sentiment"] == 'BEARISH':
                    Short_bear_cnt =  Short_bear_cnt + 1
                    Short_bear_bet = Short_bear_bet + contracts * price * 100 / 1000000

            else:

                if activity["sentiment"] == 'BULLISH':
                    Long_bull_cnt = Long_bull_cnt + 1
                    Long_bull_bet = Long_bull_bet + contracts * price * 100 / 1000000
                if activity["sentiment"] == 'BEARISH':
                    Long_bear_cnt =  Long_bear_cnt + 1
                    Long_bear_bet = Long_bear_bet + contracts * price * 100 / 1000000
    except:
        print("Except")
        continue
    print("Ticker: "+x)

    print("")

    print('Short Term Total Bulls = ', Short_bull_cnt)
    print('Short Term Total bears = ', Short_bear_cnt)

    print("")

    print('Short Term Total Bulls bet in millions = ',  format(Short_bull_bet, '.3f'))
    print('Short Term Total bears bet in millions = ',  format(Short_bear_bet, '.3f'))

    print("")

    print('Long Term Total Bulls = ', Long_bull_cnt)
    print('Long Term Total bears = ', Long_bear_cnt)

    print('Long Term Total Bulls bet in millions = ', format(Long_bull_bet, '.3f'))
    print('Long Term Total bears bet in millions = ', format(Long_bear_bet, '.3f'))

    data_dict = {"Ticker": x, "Short_bull":Short_bull_cnt,"Short_bull_bet":format(Short_bull_bet, '.3f'),"Short_bear":Short_bear_cnt,"Short_bear_bet":format(Short_bear_bet, '.3f'), "Long_bull":Long_bull_cnt,"Long_bull_bet":format(Long_bull_bet, '.3f'), "Long_bear":Long_bear_cnt, "Long_bear_bet":format(Long_bear_bet, '.3f') }
    Daily_DF = Daily_DF.append(data_dict, ignore_index=True)


Daily_DF.to_csv("Daily_SP500_summary"+datetime.now().strftime("%I:%M%p on %B %d, %Y") +".csv", index=None ,header=True)

csvobj.close()

