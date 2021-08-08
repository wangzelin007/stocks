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

np.set_printoptions(suppress=True, precision=3)

# valuation.pe_ratio > 0,
# valuation.pe_ratio < 50

def get_income(code, statDate):
    q = query(
            income
            # income.total_profit,  # 利润总额
            # income.total_operating_revenue,  # 营业总收入
            # income.total_operating_cost,  # 营业总成本
            # income.sale_expense,  # 销售费用
            # income.administration_expense,  # 管理费用
            # income.financial_expense,  # 财务费用
            # income.operating_revenue,  # 主营业务收入
            # income.investment_income,  # 投资收益
            # income.total_profit / 1000000,  # 利润总额
            # income.total_operating_revenue / 1000000,  # 营业总收入
            # income.total_operating_cost / 1000000,  # 营业总成本
            # income.sale_expense / 1000000,  # 销售费用
            # income.administration_expense / 1000000,  # 管理费用
            # income.financial_expense / 1000000,  # 财务费用
            # income.operating_revenue / 1000000,  # 主营业务收入
            # income.investment_income / 1000000, # 投资收益
        ).filter(
            income.code == code)
    ref = get_fundamentals(q, statDate=statDate)
    import pdb;pdb.set_trace()
    try:
        # print(pe)
        return ref.total_profit[0],\
               ref.total_operating_revenue[0],\
               ref.total_operating_cost[0],\
               ref.sale_expense[0],\
               ref.administration_expense[0],\
               ref.financial_expense[0],\
               ref.operating_revenue[0],\
               ref.investment_income[0]
    except:
        # print(0)
        return 0, 0, 0, 0, 0, 0, 0, 0

def main(code, year, offset):
    com_name = finance.run_query(query(finance.STK_LIST.name, ).filter(
        finance.STK_LIST.code.in_([code]), )).name[0]
    i1_list = [[] for i in range(offset)]
    i2_list = [[] for i in range(offset)]
    i3_list = [[] for i in range(offset)]
    i4_list = [[] for i in range(offset)]
    i5_list = [[] for i in range(offset)]
    i6_list = [[] for i in range(offset)]
    i7_list = [[] for i in range(offset)]
    i8_list = [[] for i in range(offset)]
    years = [year - i for i in range(offset)]
    date = ['q1', 'q2', 'q3', 'q4', '']
    for y in range(offset):
        for q in range(len(date)):
            i1, i2, i3, i4, i5, i6, i7, i8 = get_income(code, str(year - y) + date[q])
            i1_list[y].append(i1)
            i2_list[y].append(i2)
            i3_list[y].append(i3)
            i4_list[y].append(i4)
            i5_list[y].append(i5)
            i6_list[y].append(i6)
            i7_list[y].append(i7)
            i8_list[y].append(i8)
    data_list = i1_list + i2_list + i3_list + i4_list + i5_list + i6_list + i7_list + i8_list
    # print(data_list)
    df = pd.DataFrame(
        data_list,
        columns=pd.MultiIndex.from_product([[com_name],
                                            ['Q1', 'Q2', 'Q3', 'Q4', 'ALL']]),
        index=pd.MultiIndex.from_product([['利润总额','营业总收入','营业总成本','销售费用','管理费用','财务费用','主营业务收入','投资收益'],years]))
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
