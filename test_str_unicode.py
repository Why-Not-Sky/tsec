# coding=UTF-8
# http://www.codedata.com.tw/python/python-tutorial-the-1st-class-4-unicode-support-basic-input-output/

str = '測試'
print str, type(str), len(str)  # 顯示 "<type 'str'>", 6

strU = str.decode('utf8')

print strU, type(strU), len(strU)  # 顯示 "<type 'unicode'>", 2

backToBytes = strU.encode('utf8')

print backToBytes, type(backToBytes), len(backToBytes)  # 顯示 "<type 'str'>", 6

# print str.encode('big5')   #err: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128) 
# print str.encode('utf-8')  #err: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)


print '----------------------'


utext = u'測試'
print utext, type(utext),  len(utext)  # 顯示 "<type 'unicode'>", 2

strU = utext.encode('utf8')
backToBytes = strU.decode('utf8')

print 'utext.encode()', strU, type(strU), len(strU) # 顯示 "<type 'str'>", 2
print 'strU.decode()', backToBytes, type(backToBytes), len(backToBytes) # 顯示 "<type 'unicode'>", 2

