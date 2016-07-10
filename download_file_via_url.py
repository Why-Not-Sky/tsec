# -*- coding: utf-8 -*-
# http://www.blog.pythonlibrary.org/2012/06/07/python-101-how-to-download-a-file/
import urllib
import urllib2
import requests
import io

url = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
# http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=''&qdate=20160707&selectType=ALL
# 上市：
# http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report20160623/A11220160623ALL_1.php&type=csv
# 上櫃：
# http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/06/23&s=0,asc,0

url = 'http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/06/23&s=0,asc,0'

print "downloading with urllib"
urllib.urlretrieve(url, "1.csv")

print "downloading with urllib2"
f = urllib2.urlopen(url)
data = f.read()
with open("2.csv", "wb") as code:
    code.write(data)

print "downloading with requests"
r = requests.get(url)
with open("3.csv", "wb") as code:
    code.write(r.content)

f = urllib2.urlopen(url)
data = f.read()
with io.open("4.csv", "w", encoding="utf8") as code:
    code.write(data.encode('utf8'))


