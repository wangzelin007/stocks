# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""
# 净利率 > 5
# indicator.net_profit_margin > 5,
# 毛利率 > 70
# indicator.gross_profit_margin > 40
from jqdatasdk import *
auth('18682020262','WzlZxy420107')
# from jqdata import *
import pandas as pd
import numpy as np
import datetime

def get_profit(code, statDate):
    q = query(
            indicator.net_profit_margin,
            indicator.gross_profit_margin,
        ).filter(
            indicator.code == code)
    profit = get_fundamentals(q, statDate=statDate)
    try:
        print(profit.net_profit_margin[0], profit.gross_profit_margin[0])
        return profit.net_profit_margin[0], profit.gross_profit_margin[0]
    except:
        print(0,0)
        return 0,0

def main(code, year, offset):
    com_name = finance.run_query(query(finance.STK_LIST.name, ).filter(
        finance.STK_LIST.code.in_([code]), )).name[0]
    net_list = [[] for i in range(offset)]
    gross_list = [[] for i in range(offset)]
    years = [year - i for i in range(offset)]
    date = ['q1', 'q2', 'q3', 'q4']
    for y in range(offset):
        for q in range(4):
            net, gross = get_profit(code, str(year - y) + date[q])
            net_list[y].append(net)
            gross_list[y].append(gross)
    data_list = net_list + gross_list
    print(data_list)
    df = pd.DataFrame(
        data_list,
        columns=pd.MultiIndex.from_product([[com_name],
                                            ['Q1', 'Q2', 'Q3', 'Q4']]),
        index=pd.MultiIndex.from_product([['净利率', '毛利率'],
                                          years]))
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)


if __name__ == '__main__':
    # get_profit('000002.XSHE', '2019q1')
    # get_profit('000002.XSHE', '2019q2')
    # get_profit('000002.XSHE', '2019q3')
    # get_profit('000002.XSHE', '2019q4')
    # get_profit('000002.XSHE', '2020q1')
    # get_profit('000002.XSHE', '2020q2')
    # get_profit('000002.XSHE', '2020q3')
    # get_profit('000002.XSHE', '2020q4')
    # code = '600519.XSHG'
    code = '600487.XSHG'
    code2 = '000987.XSHE'
    year = 2020
    offset = 5
    main(code, year, offset)
    main(code2, year, offset)
