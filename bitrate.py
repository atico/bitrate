import requests
from lxml import html

def getPrices():
    #
    minfin = requests.get("http://minfin.com.ua/currency/auction/usd/sell/lvov/")
    tree = html.fromstring(minfin.content)
    minfin_price = tree.xpath("/html/body/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div/text()")
    mftemp = minfin_price[1]
    mftemp = mftemp.replace(" ", "")
    minfin_rate = mftemp.split(",")
    minfin_rate_usd = int((minfin_rate[0])[-2:]) + float((minfin_rate[1])[:2])/100
    print "minfin usd/uah rate: " + str(minfin_rate_usd)
    
    #
    coinbase = requests.get("https://www.coinbase.com/charts")
    tree = html.fromstring(coinbase.content)
    coinbase_btc_price = tree.xpath("//*[@id='application_menu']/ul[2]/li[1]/a/text()")
    coinbase_btc_price_x = (coinbase_btc_price[0]).split('$')
    coinbase_btc_price_y = coinbase_btc_price_x[1]
    coinbase_btc_price_ = coinbase_btc_price_y[:7]
    print coinbase_btc_price_
    
    #
    btc_trade = requests.get("https://btc-trade.com.ua/stock", verify=False)
    tree2 = html.fromstring(btc_trade.content)
    
    btc_trade_usd_rate = tree2.xpath("/html/body/div[4]/div/div[2]/div[3]/div[4]/text()")
    btc_trade_usd_rate_ = float(((btc_trade_usd_rate)[0])[1:6])
    
    print "btc-trade usd/uah rate: " + str(btc_trade_usd_rate_)
    
    btc_trade_usd_price = tree2.xpath("//*[@id='btc_uah_top_price']/text()")
    btc_trade_usd_price_ =  float((btc_trade_usd_price)[0])
    print "btc-trade uah price: " + str(btc_trade_usd_price_)
    
    btc_usd_price = btc_trade_usd_price_ / btc_trade_usd_rate_

    print "btc-trade usd price: " + str(btc_usd_price)

    print "Kupyty USD " + str(btc_usd_price * minfin_rate_usd)

    print "Kupyty BTC + 2.75% komisia " + str(btc_trade_usd_price_* 1.0275)
    
    return  "Kantor usd/uah rate --> " + str(minfin_rate_usd) + " | Kupyty USD vartistiu v 1 BTC ->" + str(btc_usd_price * minfin_rate_usd) + " UAH | Kupyty 1 BTC na BTC-TRADE + 2% komisia -> " + str(btc_trade_usd_price_* 1.02) +" UAH | BTC price BTC-TRADE -> " + str(btc_usd_price) + " USD | Coinbase BTC price ->" + str(coinbase_btc_price_) + " USD | Profit kupyty BTC zamist USD -->  " + str(btc_usd_price * minfin_rate_usd - btc_trade_usd_price_* 1.0275) + " UAH"





import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return getPrices()


app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))



