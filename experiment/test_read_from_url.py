# -*- coding: utf-8 -*-
# http://quickteckiteasy.blogspot.tw/2009/03/python-string-and-unicode-string.html

import urllib2
import sys
import locale

print sys.getdefaultencoding()
print locale.getpreferredencoding()

# sys.setdefaultencoding("utf-8")
# locale -a in terminal to get the localization list
locale.setlocale(locale.LC_ALL, 'zh_TW.UTF-8')
print 'locale.getpreferredencoding', locale.getpreferredencoding()
print 'locale.getlocale', locale.getlocale()

url = 'http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/06/23&s=0,asc,0'
f = urllib2.urlopen(url)
data = f.read()
d8 = data[:64]
print d8, type(d8), len(d8)

print d8.encode('utf-8')

ud8 = d8.decode('utf-8')
print ud8, type(d8), len(d8)

#print d8.decode('utf8')
