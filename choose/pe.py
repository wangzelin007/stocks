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

# valuation.pe_ratio > 0,
# valuation.pe_ratio < 50

def get_pe(code, statDate):
    q = query(
            valuation.pe_ratio,  # price/earnings 市(价)盈(利)率
            valuation.pb_ratio,  # price/book value 市(价)净(资产)率
        ).filter(
            valuation.code == code)
    pe = get_fundamentals(q, statDate=statDate)
    try:
        # print(pe)
        return pe.pe_ratio[0], pe.pb_ratio[0]
    except:
        # print(0)
        return 0, 0

def main(code, year, offset):
    com_name = finance.run_query(query(finance.STK_LIST.name, ).filter(
        finance.STK_LIST.code.in_([code]), )).name[0]
    pe_list = [[] for i in range(offset)]
    pb_list = [[] for i in range(offset)]
    years = [year - i for i in range(offset)]
    date = ['q1', 'q2', 'q3', 'q4']
    for y in range(offset):
        for q in range(4):
            pe, pb = get_pe(code, str(year - y) + date[q])
            pe_list[y].append(pe)
            pb_list[y].append(pb)
    data_list = pe_list + pb_list
    # print(data_list)
    df = pd.DataFrame(
        data_list,
        columns=pd.MultiIndex.from_product([[com_name],
                                            ['Q1', 'Q2', 'Q3', 'Q4']]),
        index=pd.MultiIndex.from_product([['PE','PB'],years]))
    print(df)


if __name__ == '__main__':
    # get_pe('600519.XSHG', '2019q1')
    # get_pe('600519.XSHG', '2019q2')
    # get_pe('600519.XSHG', '2019q3')
    # get_pe('600519.XSHG', '2019q4')
    # get_pe('600519.XSHG', '2020q1')
    # get_pe('600519.XSHG', '2020q2')
    # get_pe('600519.XSHG', '2020q3')
    # get_pe('600519.XSHG', '2020q4')
    # code = '600519.XSHG'
    # code = '000987.XSHE'
    code = '600487.XSHG'
    year = 2020
    offset = 5
    main(code, year, offset)