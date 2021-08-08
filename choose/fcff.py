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

# FCFF：自由现金流计算

# 经营性现金流=息税前利润 折旧-当期税款
# 计算息税前利润(息税前利润=净利润+所得税+利息费用)
def EBIT(code, report_date):
    # 从合并利润表中获取净利润、所得税、利息费用数据
    df = finance.run_query(query(
        finance.STK_INCOME_STATEMENT.code,
        finance.STK_INCOME_STATEMENT.report_type,
        finance.STK_INCOME_STATEMENT.net_profit,
        finance.STK_INCOME_STATEMENT.income_tax,
        finance.STK_INCOME_STATEMENT.interest_expense,
        finance.STK_INCOME_STATEMENT.report_date
    ).filter(
        finance.STK_INCOME_STATEMENT.code == code,
        finance.STK_INCOME_STATEMENT.report_date == report_date,
        ))
    df = df.fillna(0)
    df = df[df['report_type'] == 0]
    df['EBIT'] = df['net_profit'] + df['income_tax'] + df['interest_expense']
    # 息税前利润=净利润 所得税 利息费用
    return df['EBIT'][1]


# 计算本期折旧(本期折旧=本期累计折旧-上期累计折旧)
def depreciation(code, report_date):
    # 从合并现金流量表中获取折旧数据
    df_depreciation = finance.run_query(query(
        finance.STK_CASHFLOW_STATEMENT.code,
        finance.STK_CASHFLOW_STATEMENT.report_type,
        finance.STK_CASHFLOW_STATEMENT.fixed_assets_depreciation).filter(
        finance.STK_CASHFLOW_STATEMENT.code == code,
        finance.STK_CASHFLOW_STATEMENT.report_date == report_date))
    df_depreciation = df_depreciation.fillna(0)
    # 本期折旧=本期累计折旧-上期累计折旧
    depreciation = df_depreciation[(df_depreciation.report_type == 0)]['fixed_assets_depreciation'][1] - \
                   df_depreciation[(df_depreciation.report_type == 1)]['fixed_assets_depreciation'][0]
    return depreciation


# 计算当期税款(当期税款=所得税-递延所得税)
def current_tax(code, report_date):
    # 从合并利润表中获取所得税数据
    df = finance.run_query(query(
        finance.STK_INCOME_STATEMENT.code,
        finance.STK_INCOME_STATEMENT.report_type,
        finance.STK_INCOME_STATEMENT.income_tax).filter(
        finance.STK_INCOME_STATEMENT.code == code,
        finance.STK_INCOME_STATEMENT.report_date == report_date))
    df = df.fillna(0)
    df = df[df['report_type'] == 0]
    current_tax = df['income_tax'][1] - deferred_income_taxes(code, report_date)  # 当期税款=所得税-递延所得税
    return current_tax


# 计算递延所得税(递延所得税=递延所得税资产的减少+递延所得税负债的增加)
def deferred_income_taxes(code, report_date):
    # 从合并现金流量表中获取递延所得税资产的减少、递延所得税负债的增加数据
    df = finance.run_query(query(
        finance.STK_CASHFLOW_STATEMENT.code,
        finance.STK_CASHFLOW_STATEMENT.report_type,
        finance.STK_CASHFLOW_STATEMENT.deffered_tax_asset_decrease,
        finance.STK_CASHFLOW_STATEMENT.deffered_tax_liability_increase).filter(
        finance.STK_CASHFLOW_STATEMENT.code == code,
        finance.STK_CASHFLOW_STATEMENT.report_date == report_date))
    df = df.fillna(0)
    df = df[df['report_type'] == 0]
    df['deferred_income_taxes'] = df['deffered_tax_asset_decrease'] + df['deffered_tax_liability_increase']
    # 递延所得税=递延所得税资产的减少+递延所得税负债的增加
    return df['deferred_income_taxes'][1]


# 计算资本性支出(资本性支出=期末固定资产净额-期初固定资产净额+折旧)
def capital_expenditure(code, report_date):
    # 从合并资产负债表中获取固定资产净额数据
    df_fixed_assets = finance.run_query(query(
        finance.STK_BALANCE_SHEET.code,
        finance.STK_BALANCE_SHEET.report_type,
        finance.STK_BALANCE_SHEET.fixed_assets).filter(
        finance.STK_BALANCE_SHEET.code == code,
        finance.STK_BALANCE_SHEET.report_date == report_date))
    df_fixed_assets = df_fixed_assets.fillna(0)
    fix_assets = df_fixed_assets[(df_fixed_assets.report_type == 0)]['fixed_assets'][1] - \
                 df_fixed_assets[(df_fixed_assets.report_type == 1)]['fixed_assets'][0]
    depreciation_ = depreciation(code, report_date)
    capital_expenditure = fix_assets + depreciation_
    # 资本性支出=期末固定资产净额-期初固定资产净额+本期折旧
    return capital_expenditure


# 计算净营运资本增加额(期末净营运资本-期初净营运资本     其中：净营运资本=流动资产-流动负债)
def net_working_capital_increment(code, report_date):
    # 从合并资产负债表中获取本期和上期的流动资产&流动负债数据
    df = finance.run_query(query(
        finance.STK_BALANCE_SHEET.code,
        finance.STK_BALANCE_SHEET.report_type,
        finance.STK_BALANCE_SHEET.total_current_assets,
        finance.STK_BALANCE_SHEET.total_current_liability).filter(
        finance.STK_BALANCE_SHEET.code == code,
        finance.STK_BALANCE_SHEET.report_date == report_date))
    df = df.fillna(0)
    end_working_capital = df[(df.report_type == 0)]['total_current_assets'][1] - \
                          df[(df.report_type == 0)]['total_current_liability'][1]
    begin_working_capital = df[(df.report_type == 1)]['total_current_assets'][0] - \
                            df[(df.report_type == 1)]['total_current_liability'][0]
    net_working_capital_increment = end_working_capital - begin_working_capital  # 净营运资本增加额=期末净营运资本-期初净营运资本
    return net_working_capital_increment


# 计算FCFF自由现金流(自由现金流=息税前利润-当期税款-资本性支出-净营运资本增加额 折旧)
def FCFF(code, report_date):
    # 自由现金流=息税前利润-当期税款-资本性支出-净营运资本增加额+折旧
    try:
        FCFF = EBIT(code, report_date) - current_tax(code, report_date) - capital_expenditure(code, report_date) - net_working_capital_increment(code, report_date) + depreciation(code, report_date)
        # print('自由现金流 {}'.format(FCFF/100000000))
        return FCFF/100000000
    except:
        # print ('自由现金流 0')
        return 0

def main(code, year, offset):
    # import pdb;pdb.set_trace()
    com_name = finance.run_query(query(finance.STK_LIST.name,).filter(
        finance.STK_LIST.code.in_([code]),)).name[0]
    data_list = [[] for i in range(offset)]
    years = [year-i for i in range(offset)]
    date = ['-03-31', '-06-30', '-09-30', '-12-31']
    for y in range(offset):
        for q in range(4):
            fcff = FCFF(code, str(year-y)+date[q])
            data_list[y].append(fcff)
    # print(data_list)
    # data_list = [[-1.4304344770001602, 270.1678320675998, 272.70733148540006, 0], [1.9071140488998413, 198.05974670659984, 201.2814201058001, 216.58207870310008], [3.5308122424000357, 168.2392891695001, 169.17596594619994, 165.64596191480013], [-3.8652993581000232, 85.07303135979997, 88.11251978660007, 81.80290417569992], [7.420652542099915, 89.28589482450005, 88.82341421739994, 62.18844505489996]]
    df = pd.DataFrame(
        data_list,
        columns=pd.MultiIndex.from_product([[com_name],
                                            ['Q1', 'Q2', 'Q3', 'ALL']]),
        index=pd.MultiIndex.from_product([years]))
    print(df)
    # df4 = pd.DataFrame(np.random.randint(0, 150, size=(8, 12)),
    #                 columns=pd.MultiIndex.from_product([['模拟考', '正式考'],
    #                                                     ['数学', '语文', '英语', '物理', '化学', '生物']]),
    #                 index=pd.MultiIndex.from_product([['期中', '期末'],
    #                                                   ['雷军', '李斌'],
    #                                                   ['测试一', '测试二']]))
    # print(df4)


if __name__ == '__main__':
    # 年\季度 Q1 Q2 Q3 全年
    # 2020   x  x  x  x
    # 2019   x  x  x  x
    #data = {'Q1': {'2020': 3, '2019': 2, '2018': 5},
    #        'Q2': {'2020': 3, '2019': 2, '2018': 5},
    #        'Q3': {'2020': 3, '2019': 2, '2018': 5},
    #        'ALL': {'2020': 3, '2019': 2, '2018': 5}}
    # code = '600519.XSHG'
    # code = '000987.XSHE'
    code = '600487.XSHG'
    year = 2020
    offset = 5
    main(code, year, offset)
    # print('2019年')
    # FCFF('600519.XSHG', '2019-12-31')
    # print('2018年')
    # FCFF('600519.XSHG', '2018-12-31')
    # print('2017年')
    # FCFF('600519.XSHG', '2017-12-31')
    # print('2016年')
    # FCFF('600519.XSHG', '2016-12-31')
    # print('2015年')
    # FCFF('600519.XSHG', '2015-12-31')
    # print('2014年')
    # FCFF('600519.XSHG', '2014-12-31')
    # print('2020年1季度')
    # FCFF('600519.XSHG', '2020-03-31')
    # print('2020年2季度')
    # FCFF('600519.XSHG', '2020-06-30')
    # print('2020年3季度')
    # FCFF('600519.XSHG', '2020-09-30')
    # print('2020年全年')
    # FCFF('600519.XSHG', '2020-12-31')

