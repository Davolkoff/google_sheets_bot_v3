from finviz.helper_functions.request_functions import http_request_get
from finviz.main_func import STOCK_URL, STOCK_PAGE
import datetime
import json
import requests
import lxml.html as LH


# сиё творение природы лучше не трогать. это кусок библиотеки, который я переписал
def modified_get_page(ticker):
    global STOCK_PAGE

    if ticker not in STOCK_PAGE:
        STOCK_PAGE[ticker], _ = http_request_get(url=STOCK_URL, payload={'t': ticker}, parse=True)


# это тоже кусок переписанной библиотеки
def modified_get_analyst_price_targets(ticker, last_ratings=5):
    analyst_price_targets = []

    try:
        modified_get_page(ticker)
        page_parsed = STOCK_PAGE[ticker]
        table = page_parsed.cssselect('table[class="fullview-ratings-outer"]')[0]
        ratings_list = [row.xpath('td//text()') for row in table]
        ratings_list = [[val for val in row if val != '\n'] for row in ratings_list] #remove new line entries

        headers = ['date', 'category', 'price_from', 'price_to'] # header names
        count = 0

        for row in ratings_list:
            if count == last_ratings:
                break

            price_from, price_to = 0, 0  # defalut values for len(row) == 4 , that is there is NO price information
            if len(row) == 5:
                strings = row[4].split('→')
                #print(strings)
                if len(strings) == 1:
                    price_to = strings[0].strip(' ').strip('$')   # if only ONE price is avalable then it is 'price_to' value
                else:
                    price_from = strings[0].strip(' ').strip('$')  # both '_from' & '_to' prices available
                    price_to = strings[1].strip(' ').strip('$')

            elements = []  # only take first 4 elements, discard last element if exists
            elements.append(datetime.datetime.strptime(row[0], '%b-%d-%y').strftime('%Y-%m-%d')) # convert date format
            elements.append(row[3].replace('→', '->'))
            elements.append(price_from)
            elements.append(price_to)
            data = dict(zip(headers, elements))
            analyst_price_targets.append(data)
            count += 1
    except Exception as e:
        #print("-> Exception: %s parsing analysts' ratings for ticker %s" % (str(e), ticker))
        pass

    return analyst_price_targets


# получение значения VGM из Zacks API
def vgm(ticker):
    url = f'https://www.zacks.com/stock/quote/{ticker}?q={ticker}'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.106 Safari/537.36'}
    result = requests.get(url, headers=headers)
    tree = LH.document_fromstring(result.content)
    content = tree.xpath('//*[@id="quote_ribbon_v2"]/div[2]/div[2]/p/span[7]/text()')[0]
    return content


# получение значения Zacks Rank из Zacks API
def zacks_rank(ticker):
    answer = requests.get("https://quote-feed.zacks.com/" + ticker).content
    return json.loads(answer)[ticker]["zacks_rank"]


# получение направления
def get_industry(ticker):
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.106 Safari/537.36'}
    answer = requests.get(url, headers=headers).content

    return json.loads(answer)["quoteSummary"]["result"][0]["assetProfile"]["industry"]


# получение отрасли
def get_sector(ticker):
    url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=assetProfile'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/51.0.2704.106 Safari/537.36'}
    answer = requests.get(url, headers=headers).content

    return json.loads(answer)["quoteSummary"]["result"][0]["assetProfile"]["sector"]
