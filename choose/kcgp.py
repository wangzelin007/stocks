# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""
import fcff
import fzl
# 科创板不支持
# 深交所股票代码后缀为 XSHE
# 如000001.XSHE 平安银行
# 上交所股票代码后缀为 XSHG
# 如600000.XSHG 浦发银行
stocks = [
    '000002.XSHE', # 万科A
    '600036.XSHG', # 招商银行
    '000001.XSHE', # 平安银行
    '601318.XSHG', # 中国平安
    '002511.XSHE', # 中顺洁柔
    # '300750.XSHG', # 宁德时代
    '002594.XSHE', # 比亚迪
    '600276.XSHG', # 恒瑞医药
    '601933.XSHG', # 永辉超市
    '603708.XSHG', # 家家悦
    '600009.XSHG', # 上海机场
    '600585.XSHG', # 海螺水泥
    '002372.XSHE', # 伟星新材
    '603288.XSHG', # 海天味业
    '600887.XSHG', # 伊利股份
    '002304.XSHE', # 洋河股份
    '603589.XSHG', # 口子窖
    '000596.XSHE', # 古井贡酒
    '600519.XSHG', # 茅台
    '000858.XSHE', # 五粮液
    '000568.XSHE', # 泸州老窖
    '603899.XSHG', # 晨光文具
    '002415.XSHE', # 海康威视
    '002960.XSHE', # 青鸟消防
    '002352.XSHE', # 顺丰控股
    '002120.XSHE', # 韵达股份
    '000651.XSHE', # 格力电器
    '600482.XSHG', # 中国动力
]
for i in stocks:
#     fcff.main(i, 2020, 5)
    fzl.main(i, 2020, 5)
# fcff.main(stocks[0], 2020, 5)
