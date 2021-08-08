# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""
from jqdatasdk import *
auth('18682020262','WzlZxy420107')
# from jqdata import *
import pandas as pd
import numpy as np
import datetime

# indicator.roe
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)

def get_roe(code, statDate):
    q = query(
            indicator,
            # indicator.roe,
    ).filter(
            indicator.code == code)
    roe = get_fundamentals(q, statDate=statDate)
    # import pdb;pdb.set_trace()
    try:
        # print(roe)
        # print(roe.roe[0])
        return roe.roe[0]
    except:
        # print(0)
        return 0

def main(code, year, offset):
    com_name = finance.run_query(query(finance.STK_LIST.name, ).filter(
        finance.STK_LIST.code.in_([code]), )).name[0]
    data_list = [[] for i in range(offset)]
    years = [year - i for i in range(offset)]
    date = ['q1', 'q2', 'q3', 'q4', '']
    for y in range(offset):
        for q in range(5):
            fzl = get_roe(code, str(year - y) + date[q])
            data_list[y].append(fzl)
    # print(data_list)
    df = pd.DataFrame(
        data_list,
        columns=pd.MultiIndex.from_product([[com_name],
                                            ['Q1', 'Q2', 'Q3', 'Q4', 'ALL']]),
        index=pd.MultiIndex.from_product([['ROE'],years]))
    print(df)


if __name__ == '__main__':
    # get_roe('600519.XSHG', '2019')
    # get_roe('600519.XSHG', '2018')
    # get_roe('600519.XSHG', '2017')
    # get_roe('600519.XSHG', '2016')
    # get_roe('600519.XSHG', '2019q1')
    # get_roe('600519.XSHG', '2019q2')
    # get_roe('600519.XSHG', '2019q3')
    # get_roe('600519.XSHG', '2019q4')
    # get_roe('600519.XSHG', '2020q1')
    # get_roe('600519.XSHG', '2020q2')
    # get_roe('600519.XSHG', '2020q3')
    # get_roe('600519.XSHG', '2020q4')
    # code = '600519.XSHG'
    # code = '000987.XSHE'
    code = '600487.XSHG'
    year = 2020
    offset = 5
    main(code, year, offset)