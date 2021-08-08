# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""
# 毛利率

from kuanke.wizard import *
from jqdata import *
import numpy as np
import talib
import datetime

##################################  选股函数群 ##################################

## 财务指标筛选函数
def financial_statements_filter():
    security_list = indicator.gross_profit_margin, 70)

    # 返回列表
    print(security_list)
    return security_list

if __name__ == '__main__':
    financial_statements_filter()