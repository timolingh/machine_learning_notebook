
from lxml import html
import requests
import datetime
import pandas as pd
from decimal import Decimal
from df2gspread import df2gspread as d2g


# Parse the text from the HTML
def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')


# Pulls the data from the dividend calendar
def div_forecast(dt):
    
    # The content of the table
    urlstr = 'http://www.nasdaq.com/dividend-stocks/dividend-calendar.aspx?date=' + dt
    page = requests.get(urlstr)
    tree = html.fromstring(page.content)
    
    # Handle no data
    if tree.xpath('//div[@class="notTradingIPO"]'):
        return [['n/a' for i in range(7)]]
    
    # Parse the HTML from the request
    for tbl in tree.xpath('//table[@class="DividendCalendar"]'):
        #header = [text(th) for th in tree.xpath('//th')]
        data = [[text(td) for td in tr.xpath('td')]  
                for tr in tbl.xpath('//tr')] 
        data = [row for row in data if len(row) == 7]
        
    return data


# Pulls the last stock price
def stock_quote(ticker):
        
    # URL
    urlstr = 'http://www.nasdaq.com/aspx/flashquotes.aspx?symbol=' + ticker
    page = requests.get(urlstr)
    tree = html.fromstring(page.content)
    
    data = [text(lb) for lb in tree.xpath("//label[contains(@id, 'lastsale')]")]
        
    #return tree.xpath(ticker_id)
    return [ticker, data[0]]
    
## Main program 
if __name__ == "__main__":
    
    # Get the dividend calendar for the next 2 weeks
    dt_lah = [(datetime.datetime.today() + datetime.timedelta(days=i)).strftime('%Y-%b-%d') for i in range(1,14)]
    out_dt = [div_forecast(dt) for dt in dt_lah]


    # Flatten 1 level
    out_dt = [row for d in out_dt for row in d]

    # to dataframe
    columns = ['company', 'ex_date', 'dividend', 'ann_dividend', 'record_dt', 'announce_dt', 'payment_dt']
    out_pd = pd.DataFrame(out_dt, columns=columns)


    # Parse and add ticker
    co = out_pd['company'].str.extract('(\([A-Z\.]+\)$)').str.extract('([A-Z\.]+)')
    out_pd['symbol'] = co

    # Drop nulls
    out_pd = out_pd.drop(out_pd.index[pd.isnull(out_pd['symbol'])])

    # Most recent quote
    qt = [stock_quote(symbol) for symbol in out_pd['symbol']]

    # Calculate the div yield    
    prc2 = [float(quote[1].strip('$')) for quote in qt]
    out_pd['lastprice'] = prc2
    out_pd['yield_pct'] = (pd.to_numeric(out_pd['ann_dividend']) / pd.to_numeric(out_pd['lastprice'])) * 100.

    # time stamp for sheet name
    now = datetime.datetime.now()
    wks_name = 'Dividend ' + now.strftime("%Y-%m-%d %H:%M")


    # Write to Google sheet
    wks = d2g.upload(out_pd.sort_values(by='yield_pct', ascending=False).
                     sort_values(by='ex_date'), 
                     gfile='/Dividend', wks_name=wks_name)





