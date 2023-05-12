from lxml import html  
import requests
import json
import argparse
from collections import OrderedDict
from time import sleep
import multiprocessing

class TickerPrice:
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price

def scrape(ticker):
	url = "https://finance.yahoo.com/quote/%s"%(ticker)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}
	response = requests.get(url, headers=headers, verify=True)
	parser = html.fromstring(response.text)
	price = parser.xpath("//*[@data-symbol='%s'][@data-field='regularMarketPrice']" % ticker)
	return TickerPrice(ticker, price[0].text)
		
if __name__=="__main__":
	argparser = argparse.ArgumentParser()
	argparser.add_argument('tickers',help = 'Space separated list of tickers', nargs='+')
	args = argparser.parse_args()
	tickers = args.tickers
	pool = multiprocessing.Pool()
	outputs_async = pool.map_async(scrape, tickers)
	outputs = outputs_async.get()
	print(json.dumps([ob.__dict__ for ob in outputs], indent=2))
