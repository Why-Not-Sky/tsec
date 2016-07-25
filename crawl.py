# -*- coding: utf-8 -*-

import argparse
import csv
import logging
import os
import re
import string
import time
from datetime import datetime, timedelta
from os import mkdir
from os.path import isdir
#from urllib import urlopen
from urllib.request import urlopen
import itertools
import json

import requests
from lxml import html

class data():
    def  __init__(self, dtype, url):
        self.type=dtype
        self.url=url

class etl():
    def __init__(self):
        self.source = data('url', 'http:')
        pass

    def _extract(self):
        pass

    def _transformation(self):
        pass

    def _load(self):
        pass

    def run(self):
        self._extract(self)
        self._transform(self)
        self._load(self)

class tse(etl):
    def __init__(self):
        pass


class Crawler():
    def __init__(self, prefix="data", origin = "origin"):
        ''' Make directory if not exist when initialize '''
        if not isdir(prefix):
            mkdir(prefix)
        self.prefix = prefix
        self.output_file = ''

        if not isdir(origin):
            mkdir(origin)
        self.origin = origin

        ''' data source of url to extract'''
        # 上市: query string of the date is a taiwan year:105/07/12
        # http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report201607/A11220160712ALL_1.php&type=csv
        # 上櫃：
        # http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/07/12&s=0,asc,0
        ''''''
        self.url_tse_excel = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report{}/A112{}ALL_1.php&type=csv'
        self.url_tse_csv = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=csv&qdate={}&selectType=ALL"  # .format(taiwan_date_str)'
        self.url_tse = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL"  # .format(taiwan_date_str)'
        self.url_otc_excel = 'http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d={}&s=0,asc,0'
        self.url_otc = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'

        self.fields = ['股號', '日期', '成交股數', '成交金額', '開盤價', '最高價', '最低價', '收盤價', '漲跌價差', '成交筆數']
        # symbol_id,trade_date,volume,amout,open,high,low,close,change,trans

    def _clean_row(self, row):
        ''' Clean comma and spaces '''
        rdict = {}

        for index, content in enumerate(row):
            row[index] = re.sub(",", "", content.strip())
            '''for python3 2016/07/19'''
            # filter() in python 3 does not return a list, but a iterable filter object. Call next() on it to get the first filtered item:
            row[index] = ''.join(list(filter(lambda x: x in string.printable, row[index])))
            #rdict[self.fields[index]] = row[index]

        return row #','.join(row)   #rdict #(zip(self.fields, row))   #row

    def _record(self, stock_id, row):
        ''' Save row to csv file '''
        f = open('{}/{}.csv'.format(self.prefix, stock_id), 'ab')
        cw = csv.writer(f, lineterminator='\n')
        cw.writerow(row)
        f.close()

<<<<<<< HEAD
    def _download_data_by_url(self, url, fname):
        response = urlopen(url)
        fname = '{}/{}.csv'.format(self.prefix, fname)
        data = response.read()

        with open(fname, 'w') as fd:
            fd.write(data)
            fd.close()

    def get_tse_data_all(self, date_str):
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?'
        query_string = 'genpage=genpage/Report{quote_date}/A112?{quote_date}ALL_1.php&type=csv'.format(quote_date=date_str)
        url += query_string

    # 上市：
    # http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report20160623/A11220160623ALL_1.php&type=csv

    # 上櫃：
    # http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/06/23&s=0,asc,0

        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report20160623/A11220160623ALL_1.php&type=csv'

        self._download_data_by_url(url, date_str)
        return
        # Get html page and parse as tree
        #page = requests.post(url, data=query_string)

    def _get_tse_data_to_one_file(self, date_str):
        taiwan_date_str = str(int(date_str[:4])-1911) + date_str[5:]
=======
    def _get_tse_data(self, date_str):
>>>>>>> master
        payload = {
            'download': '',
            'qdate': date_str,
            'selectType': 'ALL'
        }
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
        # http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=''&qdate=20160707&selectType=ALL

        # Get html page and parse as tree
        page = requests.post(url, data=payload)

        if not page.ok:
            logging.error("Can not get TSE data at {}".format(date_str))
            return

        # Parse page
        tree = html.fromstring(page.text)

<<<<<<< HEAD
        f = open('{}/{}_TWSE.csv'.format(self.prefix, date_str), 'ab')
=======
        for tr in tree.xpath('//table[2]/tbody/tr'):
            tds = tr.xpath('td/text()')

            sign = tr.xpath('td/font/text()')
            sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''

            row = self._clean_row([
                date_str,  # 日期
                tds[2],  # 成交股數
                tds[4],  # 成交金額
                tds[5],  # 開盤價
                tds[6],  # 最高價
                tds[7],  # 最低價
                tds[8],  # 收盤價
                sign + tds[9],  # 漲跌價差
                tds[3],  # 成交筆數
            ])

            self._record(tds[0].strip(), row)

    def _get_otc_data(self, date_str):
        ttime = str(int(time.time() * 100))
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'.format(
            date_str, ttime)
        page = requests.get(url)

        if not page.ok:
            logging.error("Can not get OTC data at {}".format(date_str))
            return

        result = page.json()

        if result['reportDate'] != date_str:
            logging.error("Get error date OTC data at {}".format(date_str))
            return

        for table in [result['mmData'], result['aaData']]:
            for tr in table:
                row = self._clean_row([
                    date_str,
                    tr[8],  # 成交股數
                    tr[9],  # 成交金額
                    tr[4],  # 開盤價
                    tr[5],  # 最高價
                    tr[6],  # 最低價
                    tr[2],  # 收盤價
                    tr[3],  # 漲跌價差
                    tr[10]  # 成交筆數
                ])
                self._record(tr[0], row)

    def get_data(self, year, month, day):
        date_str = '{0}/{1:02d}/{2:02d}'.format(year - 1911, month, day)
        print('Crawling {}'.format(date_str))
        self._get_tse_data(date_str)
        self._get_otc_data(date_str)

    def _to_taiwan_date(self, date_str='20160712', esc_char='/'):
        date_str = date_str.replace(esc_char, '')
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:])
        taiwan_date = '{0}{esc_ch}{1:02d}{esc_ch}{2:02d}'.format(year - 1911, month, day, esc_ch=esc_char)
        return taiwan_date

    def _to_century_date(self, taiwan_date='105/07/12', esc_char='/'):
        '''in:105/07/12, /  --> 2106/07/12
           in:1050712  --> 20160712
        '''
        taiwan_date = taiwan_date.replace(esc_char, '')
        year = int(taiwan_date[:3])+1911
        month = int(taiwan_date[3:5])
        day = int(taiwan_date[5:])
        century_date = '{0}{esc_ch}{1:02d}{esc_ch}{2:02d}'.format(year, month, day, esc_ch=esc_char)
        return century_date

    def _download_data_by_url(self, url, fname):
        #response = urlopen(url)
        #fname = '{}/{}.csv'.format(self.prefix, fname)
        #data = response.read()
        r = requests.get(url)
        data = r.content

        # need to use binary to get the data
        # 原先的作法直接從request.response回來，需以binary的方式寫入
        with open(fname, 'wb') as fd:
            fd.write(data)
            fd.close()

    def _get_url_of_tse_century(self, date_str):
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?'
        query_string = 'genpage=genpage/Report{quote_month}/A112{quote_date}ALL_1.php&type=csv'.format(
            quote_month=date_str[:6],
            quote_date=date_str)
        url += query_string

        return (url)

    def _get_url_of_tse(self, taiwan_date_str):
        return (self.url_tse.format(taiwan_date_str))

    def _get_tse_file_name(self, path='', taiwan_date_str='107/07/12.csv'):
        return  '{}/{}_T.csv'.format(path, taiwan_date_str.replace('/', ''))

    def _get_tse_data_raw(self, taiwan_date_str):
        url = self.url_tse.format(taiwan_date_str)
        fname = self._get_tse_file_name(self.origin, taiwan_date_str)

    def _get_tse_data_raw_simple(self, date_str='20170712'):
        url = self._get_url_of_tse_century(date_str)
        fname = '{}/{}_T.csv'.format(self.origin, date_str)
        self._download_data_by_url(url, fname)

    def _transform_tse_data(self, taiwan_date_str):
        # Get html page and parse as tree
        date_str = self._to_century_date(taiwan_date_str).replace('/', '')
        infname = self._get_tse_file_name(self.origin, taiwan_date_str)
        infile = open(infname, 'rb')  # 'ab')
        data = infile.read()

        # Parse page
        tree = html.fromstring(data)

        '''for python3 2016/07/19'''
        f = open(self._get_tse_file_name(self.prefix, taiwan_date_str), 'w')  # 'ab')
>>>>>>> master
        cw = csv.writer(f, lineterminator='\n')

        for tr in tree.xpath('//table[2]/tbody/tr'):
            tds = tr.xpath('td/text()')

            sign = tr.xpath('td/font/text()')
            sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''

            row = self._clean_row([
<<<<<<< HEAD
                tds[0].strip(), # 股票代號
                date_str,  # 成交日期
=======
                tds[0].strip(),  # symbol
                date_str,  # 日期
>>>>>>> master
                tds[2],  # 成交股數
                tds[4],  # 成交金額
                tds[5],  # 開盤價
                tds[6],  # 最高價
                tds[7],  # 最低價
                tds[8],  # 收盤價
                sign + tds[9],  # 漲跌價差
                tds[3],  # 成交筆數
            ])

            cw.writerow(row)
            # f.write(row + "\n")

        f.close()

<<<<<<< HEAD
    def _get_otc_data_to_one_file(self, date_str):
        ttime = str(int(time.time() * 100))
        url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'.format(
            date_str, ttime)
        page = requests.get(url)

        if not page.ok:
            logging.error("Can not get OTC data at {}".format(date_str))
            return

        result = page.json()

        if result['reportDate'] != date_str:
            logging.error("Get error date OTC data at {}".format(date_str))
            return

        f = open('{}/{}_OTC.csv'.format(self.prefix, date_str), 'ab')
        cw = csv.writer(f, lineterminator='\n')

        for table in [result['mmData'], result['aaData']]:
            for tr in table:
                row = self._clean_row([
                    tr[0],  # 股票代號
                    date_str, # 成交日期
                    tr[8],  # 成交股數
                    tr[9],  # 成交金額
                    tr[4],  # 開盤價
                    tr[5],  # 最高價
                    tr[6],  # 最低價
                    tr[2],  # 收盤價
                    tr[3],  # 漲跌價差
                    tr[10]  # 成交筆數
                ])
                self._record(tr[0], row)

    def _get_tse_data(self, date_str):
=======
    def _get_tse_data_all(self, date_str):
        taiwan_date_str = str(int(date_str[:4]) - 1911) + date_str[5:]
>>>>>>> master
        payload = {
            'download': '',
            'qdate': taiwan_date_str,
            'selectType': 'ALL'
        }
        url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
        # http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=''&qdate=20160707&selectType=ALL

        # Get html page and parse as tree
        page = requests.post(url, data=payload)

        if not page.ok:
            logging.error("Can not get TSE data at {}".format(date_str))
            return

        # Parse page
        tree = html.fromstring(page.text)

        '''for python3 2016/07/19'''
        f = open('{}/{}_ALL.csv'.format(self.prefix, date_str), 'w') #'ab')
        cw = csv.writer(f, lineterminator='\n')

        for tr in tree.xpath('//table[2]/tbody/tr'):
            tds = tr.xpath('td/text()')

            sign = tr.xpath('td/font/text()')
            sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''

            row = self._clean_row([
                tds[0].strip(),  # symbol
                date_str,  # 日期
                tds[2],  # 成交股數
                tds[4],  # 成交金額
                tds[5],  # 開盤價
                tds[6],  # 最高價
                tds[7],  # 最低價
                tds[8],  # 收盤價
                sign + tds[9],  # 漲跌價差
                tds[3],  # 成交筆數
            ])

            cw.writerow(row)
            #f.write(row + "\n")

        f.close()

    def _get_url_of_otc(self, taiwan_date_str):
        return (self.url_otc.format(taiwan_date_str))

    def _get_otc_file_name(self, path='', taiwan_date_str='107/07/12.csv'):
        return '{}/{}_O.csv'.format(path, taiwan_date_str.replace('/', ''))

    def _get_otc_data_raw(self, taiwan_date_str):
        ttime = str(int(time.time() * 100))
        url = self.url_otc.format(taiwan_date_str, ttime)

        fname = self._get_otc_file_name(self.origin, taiwan_date_str)

        self._download_data_by_url(url, fname)
        return fname

    def _transform_otc_data(self, taiwan_date_str):
        # Get html page and parse as tree
        date_str = self._to_century_date(taiwan_date_str).replace('/', '')
        infname = self._get_otc_file_name(self.origin, taiwan_date_str)
        infile = open(infname, 'r')  # 'ab')
        data = infile.read()

        # Parse page
        result = json.loads(data)   #data.json()

        if result['reportDate'] != taiwan_date_str:
            logging.error("Get error date OTC data at {}".format(date_str))
            return

        '''for python3 2016/07/21'''
        f = open(self._get_otc_file_name(self.prefix, taiwan_date_str), 'w')  # 'ab')
        cw = csv.writer(f, lineterminator='\n')

        for table in [result['mmData'], result['aaData']]:
            for tr in table:
                row = self._clean_row([
                    tr[0],
                    date_str,
                    tr[8],  # 成交股數
                    tr[9],  # 成交金額
                    tr[4],  # 開盤價
                    tr[5],  # 最高價
                    tr[6],  # 最低價
                    tr[2],  # 收盤價
                    tr[3],  # 漲跌價差
                    tr[10]  # 成交筆數
                ])
                cw.writerow(row)
            # f.write(row + "\n")

<<<<<<< HEAD
    def get_data(self, year, month, day):
        date_str = '{0}/{1:02d}/{2:02d}'.format(year - 1911, month, day)
        print 'Crawling {}'.format(date_str)
        self._get_tse_data_to_one_file(date_str)
        self._get_otc_data_to_one_file(date_str)
=======
        f.close()

    def _get_data_all_by_date(self, date_str='20160712'):
        taiwan_date_str = self._to_taiwan_date(date_str, '/')
        #print('Crawling {} by simple format'.format(date_str))
        # to-do: refactoring to general extract method
        #self._get_twse_data_raw_simple(date_str)

        print('Crawling {} by as default'.format(taiwan_date_str))
        self._get_tse_data_raw(taiwan_date_str)
        self._get_otc_data_raw(taiwan_date_str)

        # self._get_tse_data_all(date_str)
        # self._get_otc_data_all(date_str)
>>>>>>> master

        # to-to: transform the original file to expected format
        # _transform
        print('Transform {} from the default'.format(taiwan_date_str))
        self._transform_tse_data(taiwan_date_str)
        self._transform_otc_data(taiwan_date_str)

        # to-do: load into the desired database
        # clean & load (delete the all and insert new one...

    def get_data_all(self, start_date='20160701', end_date='20160715'):
        self._get_data_all_by_date(start_date)

'''
args: crawl [start_date:yyyymmdd] [end_date:yyyymmdd]
ex: crawl 20160701 20160712
'''
def main():
    # Set logging
    if not os.path.isdir('log'):
        os.makedirs('log')
    logging.basicConfig(filename='log/crawl-error.log',
                        level=logging.ERROR,
                        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    # Get arguments
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    parser.add_argument('day', type=int, nargs='*',
                        help='assigned day (format: YYYY MM DD), default is today')
    parser.add_argument('-b', '--back', action='store_true',
                        help='crawl back from assigned day until 2004/2/11')
    parser.add_argument('-c', '--check', action='store_true',
                        help='crawl back 10 days for check data')

    args = parser.parse_args()

    # Day only accept 0 or 3 arguments
    if len(args.day) == 0:
        first_day = datetime.today()
    elif len(args.day) == 3:
        first_day = datetime(args.day[0], args.day[1], args.day[2])
    else:
        parser.error('Date should be assigned with (YYYY MM DD) or none')
        return

    crawler = Crawler()

    # If back flag is on, crawl till 2004/2/11, else crawl one day
    if args.back or args.check:
        # otc first day is 2007/04/20
        # tse first day is 2004/02/11

        last_day = datetime(2004, 2, 11) if args.back else first_day - timedelta(10)
        max_error = 5
        error_times = 0

        while error_times < max_error and first_day >= last_day:
            try:
                crawler.get_data(first_day.year, first_day.month, first_day.day)
                error_times = 0
            except:
                date_str = first_day.strftime('%Y/%m/%d')
                logging.error('Crawl raise error {}'.format(date_str))
                error_times += 1
                continue
            finally:
                first_day -= timedelta(1)
    else:
        crawler.get_data(first_day.year, first_day.month, first_day.day)

def test_download_all(start_date='20160712', end_date='20160712'):
    crawler = Crawler()
<<<<<<< HEAD
    crawler._get_tse_data_to_one_file(date_str)
    crawler._get_otc_data_to_one_file(date_str)
=======
    crawler.get_data_all(start_date, end_date)
>>>>>>> master

if __name__ == '__main__':
    # main()
    test_download_all('20160712', '20160712')

