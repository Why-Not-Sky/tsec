# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
--------------------------------------------------------------------
1.1     2016/07/26 	    產生crawl2，整理輸入輸出，提供批次



------------------------------------------------------------------------------------------------------------------------------------------
non-function requirement:
    * add unit test
    * implement by etl library: pets, odo, or tab…
    * add exception handling: by AOP framework
    * refactor by inheritance
    * refactor by IoC

------------------------------------------------------------------------------------------------------------------------------------------
feature list:
    * add filter to exclude untracked symbol
    * crawling target
        - personal investment
            > portfolio current stock
            > trading history
            > wish list
        - company: basic/finance/...
            > company revenue...
        - market information
            > news
            > industry/ chain/ group
            >
    * crawling only if the trade market open
    * calculate moving average
    * implement technical analysis library
---------------------------------------------------------------------------------------------------------------------------------------'''

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
import datetime

import requests
from lxml import html

def str_date_to_int(date_str='20160712', esc_char='/'):
    date_str = date_str.replace(esc_char, '')
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:])
    return year, month, day

def str_to_date(date_str='20160712', esc_char=''):
    year, month, day = str_date_to_int(date_str, esc_char)
    return datetime.date(year, month, day)

def to_taiwan_date_str(date_str='20160712', esc_char='/'):
    year, month, day = str_date_to_int(date_str, esc_char)
    taiwan_date = '{0}{esc_ch}{1:02d}{esc_ch}{2:02d}'.format(year - 1911, month, day, esc_ch=esc_char)
    return taiwan_date

def to_century_date_str(self, taiwan_date='105/07/12', esc_char='/'):
    '''in:105/07/12, /  --> 2106/07/12
       in:1050712  --> 20160712
    '''
    taiwan_date = taiwan_date.replace(esc_char, '')
    year = int(taiwan_date[:3]) + 1911
    month = int(taiwan_date[3:5])
    day = int(taiwan_date[5:])
    century_date = '{0}{esc_ch}{1:02d}{esc_ch}{2:02d}'.format(year, month, day, esc_ch=esc_char)
    return century_date

def date_range(start_date, end_date):
    """ date_range(20160701, 20160712) """
    # 若是字串則自動轉換為日期
    start_date = str_to_date(start_date) if isinstance(start_date, str) else start_date
    end_date = str_to_date(end_date)  if isinstance(end_date, str) else end_date

    dlist = (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days))
    return dlist

def download_data_by_url(url, fname):
    # response = urlopen(url)
    # data = response.read()
    r = requests.get(url)
    data = r.content

    # need to use binary to get the data
    # 原先的作法直接從request.response回來，需以binary的方式寫入
    with open(fname, 'wb') as fd:
        fd.write(data)
        fd.close()

class Crawler():
    def __init__(self, prefix="data", origin = "origin"):
        ''' Make directory if not exist when initialize '''
        if not isdir(prefix):
            mkdir(prefix)
        self.prefix = prefix

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
        download_data_by_url(url, fname)

    ''' get the csv directly'''
    def _get_tse_data_raw_simple(self, date_str='20170712'):
        url = self._get_url_of_tse_century(date_str)
        fname = '{}/{}_T.csv'.format(self.origin, date_str)
        download_data_by_url(url, fname)

    def _transform_tse_data(self, taiwan_date_str):
        # Get html page and parse as tree
        date_str = to_century_date_str(taiwan_date_str).replace('/', '')
        infname = self._get_tse_file_name(self.origin, taiwan_date_str)
        infile = open(infname, 'rb')  # 'ab')
        data = infile.read()

        # Parse page
        tree = html.fromstring(data)

        '''for python3 2016/07/19'''
        f = open(self._get_tse_file_name(self.prefix, taiwan_date_str), 'w')  # 'ab')
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
            # f.write(row + "\n")

        f.close()

    def _get_url_of_otc(self, taiwan_date_str):
        return (self.url_otc.format(taiwan_date_str))

    def _get_otc_file_name(self, path='', taiwan_date_str='107/07/12.csv'):
        return '{}/{}_O.csv'.format(path, taiwan_date_str.replace('/', ''))

    def _get_otc_data_raw(self, taiwan_date_str):
        ttime = str(int(time.time() * 100))
        url = self.url_otc.format(taiwan_date_str, ttime)

        fname = self._get_otc_file_name(self.origin, taiwan_date_str)

        download_data_by_url(url, fname)
        return fname

    def _transform_otc_data(self, taiwan_date_str):
        # Get html page and parse as tree
        date_str = to_century_date_str(taiwan_date_str).replace('/', '')
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

        f.close()

    def get_data_all_by_date(self, date_str='20160712'):
        taiwan_date_str = to_taiwan_date_str(date_str, '/')
        #print('Crawling {} by simple format'.format(date_str))
        # to-do: refactoring to general extract method
        #self._get_twse_data_raw_simple(date_str)

        print('Crawling {}'.format(taiwan_date_str))
        self._get_tse_data_raw(taiwan_date_str)
        self._get_otc_data_raw(taiwan_date_str)

        # to-to: transform the original file to expected format
        # _transform
        print('Transform {}'.format(taiwan_date_str))
        self._transform_tse_data(taiwan_date_str)
        self._transform_otc_data(taiwan_date_str)

        # to-do: load into the desired database
        # clean & load (delete the all and insert new one...

    def get_data_all(self, start_date='20160701', end_date='20160715'):
        max_error = 5
        error_times = 0
        # back to download
        from_day = str_to_date(start_date )
        to_day = str_to_date(end_date)

        while error_times < max_error and from_day <= to_day:
            date_str = from_day.strftime('%Y%m%d')
            print('Processing {}'.format(date_str))
            try:
                self.get_data_all_by_date(date_str)
                error_times = 0
            except:
                logging.error('Crawl raise error {}'.format(date_str))
                error_times += 1
                continue
            finally:
                from_day += timedelta(1)

    def _get_during(self):
        start_date = '20160701'
        end_date = '20160731'
        return start_date, end_date

    def _write_execution_log(self):
        pass

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

    # Get arguments of the during
    parser = argparse.ArgumentParser(description='Crawl data at assigned day')
    parser.add_argument('day', type=int, nargs='*',
                        help='assigned day (format: YYYYMMDD), default is today')  # end_date
    parser.add_argument('-b', '--back', action='store_true',
                        help='crawl back from assigned day until 2004/2/11')
    parser.add_argument('-c', '--check', action='store_true',
                        help='crawl back 10 days for check data')

    args = parser.parse_args()

    # Day only accept 0 or 3 arguments
    if len(args.day) == 0:
        from_day = datetime.date.today().strftime('%Y%m%d')
    elif len(args.day) >= 1:
        from_day = str(args.day[0])
    else:
        parser.error('Date should be assigned with (YYYY MM DD) or none')
        return

    to_day = str(args.day[1]) if len(args.day) == 2 else from_day

    crawler = Crawler()
    crawler.get_data_all(from_day, to_day)

def test_download_all(start_date='20160712', end_date='20160712'):
    crawler = Crawler()
    #crawler.get_data_all_by_date(start_date)
    crawler.get_data_all(start_date, end_date)

if __name__ == '__main__':
    main()
    #test_download_all('20160712', '20160713')


