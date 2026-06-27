import datetime

def date_transform(date_str):
    '''能把2001-01-01这样的字符串转换为(2001, 1, 1)这样的元组'''
    year, month, day = map(int, date_str.split('-'))
    return (year, month, day)

def key_of_date(date_str):
    '''能把2001-01-01这样的字符串转换为20010101这样的整数'''
    year, month, day = map(int, date_str.split('-'))
    return year * 10000 + month * 100 + day