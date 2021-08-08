# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""
# 标题 价值投资
# 作者：剑胆琴心up
from jqdatasdk import *
auth('18682020262','WzlZxy420107')
# from jqdata import *
import pandas as pd
import numpy as np
import datetime

global g
g = {}

import logging as log

logger = log.getLogger(__name__)
log.basicConfig(level=log.WARNING,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger.setLevel(level=log.DEBUG)
# use logging
log.info('this is a loggging info message')
log.debug('this is a loggging debug message')
log.warning('this is loggging a warning message')
log.error('this is an loggging error message')
log.critical('this is a loggging critical message')

# 初始化函数，设定基准等等
def initialize():
    set_param()
    # run_monthly(main, 1, time='9:30')
    main()


def main():
    one_stock_study('600449.XSHG')

def one_stock_study(code):
    compinfo = finance.run_query(query(
        finance.STK_LIST,
    # id/code/name/short_name/category/exchange/start_date/end_date/company_id
    # company_name ipo_shares/book_price/per_value/state_id/state
    ).filter(
        finance.STK_LIST.code.in_([code]),
    ))
    # finance.run_query(query(finance.STK_LIST).filter(finance.STK_LIST.code.in_([call_stks])))
    # log.warning('compinfo: {}'.format(compinfo))
    q = query(
        income
    ).filter(
        income.code.in_([code]),
    )
    rets = get_fundamentals(q)
    # log.warning('rets: {}'.format(rets))
    import pdb;pdb.set_trace()
    q2 = query(
        indicator
    ).filter(
        # 排除300
        indicator.code.notlike('300%'),
        # 排除688
        indicator.code.notlike('688%'),
        # 净资产收益率roe大于0 %
        # 销售净利率net_profit_margin大于5 %
        # 销售毛利率gross_profit_margin大于90 %
        indicator.roe > 0,
        indicator.net_profit_margin > 5,
        indicator.gross_profit_margin > 90,
    )
    rets2 = get_fundamentals(q2)
    log.warning('rets2: {}'.format(rets2))

def set_param():
    g['bten'] = []
    g['bfive'] = []
    g['stock_num'] = 5
    g['fin'] = pd.DataFrame()
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)

    # 其他指数：https://www.joinquant.com/help/api/help?name=index
    # 设定沪深300作为基准
    # set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    # set_option('use_real_price', True)


    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    # set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')

if __name__ == '__main__':
    from jqdatasdk import *
    auth('18682020262', 'WzlZxy420107')
    import pprint
    count = get_query_count()
    pprint.pprint(count)
    initialize()