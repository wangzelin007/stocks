# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""


def initialize(context):
    set_benchmark('000300.XSHG')
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))

    g.stocknum = 2  # 持股数

    # 根据大盘止损，如不想加入大盘止损，注释此句即可
    run_daily(dapan_stoploss)

    ## 按月调用程序
    run_weekly(Transfer, -1)


def Transfer(context):
    ## 获得Buylist
    Buylist = Check_Stocks(context)
    Buylist = Buylist[:g.stocknum]
    log.info(len(Buylist))
    log.info(Buylist)

    ## 卖出
    if len(context.portfolio.positions) > 0:
        for stock in context.portfolio.positions.keys():
            if stock not in Buylist:
                order_target(stock, 0)

    ## 买入
    if len(Buylist) > 0:
        Num = len(Buylist)
        Cash = context.portfolio.cash / Num
        for stock in Buylist:
            if stock not in context.portfolio.positions.keys():
                order_value(stock, Cash)


def Check_Stocks(context):
    '''
    为防止亏损公司或财务指标异常公司的影响。
    剔除资产报酬率、毛利率、权益报酬率等异常的公司。
    即要求 ROA>0.5%、 adj-ROE>2%、利润总额>0、毛利率>0。
    选取投资收益率 > 0；
    根据PB升序排列，取前30%；
    根据三费占比升序排列，取前30%；
    根据收入现金率降序排列，取前30%；
    '''

    ## 获取财务数据
    df = get_fundamentals(query(
        valuation.code,  # 股票代码
        valuation.pb_ratio,  # 市净率
        income.total_profit,  # 利润总额
        income.total_operating_revenue,  # 营业总收入
        income.total_operating_cost,  # 营业总成本
        income.sale_expense,  # 销售费用
        income.administration_expense,  # 管理费用
        income.financial_expense,  # 财务费用
        income.operating_revenue,  # 主营业务收入
        balance.total_assets,  # 资产总计
        balance.total_liability,  # 负债合计
        balance.account_receivable,  # 应收账款
        balance.accounts_payable,  # 应付账款
        income.investment_income,  # 投资收益
        cash_flow.goods_sale_and_service_render_cash,  # 销售商品、提供劳务收到的现金(
    ).filter(
        # ROA>0.5% (资产报酬率=利润总额/总资产)
        income.total_profit / balance.total_assets > 0.005,
        # adj-ROE>2% (调整的净资产报酬率=利润总额/净资产)
        income.total_profit / (balance.total_assets - balance.total_liability) > 0.02,
        # 利润总额>0
        income.total_profit > 0,
        # 毛利率>0 (（主营业务收入-主营业务成本） / 主营业务收入)
        (income.total_operating_revenue - income.total_operating_cost) / income.total_operating_revenue > 0,
    )).dropna()  # 去除NaN值

    ## 指标计算
    # 三费占比=（销售费用＋管理费用＋财务费用） /主营业务收入
    df['3'] = (df.sale_expense + df.administration_expense + df.financial_expense) / df.operating_revenue
    # 投资收益率 = 投资收益/总资产
    df['tzsy'] = df.investment_income / df.total_assets
    # 收入现金率 = 销售商品提供劳务收到的现金/主营业务收入
    df['srxj'] = df.goods_sale_and_service_render_cash / df.operating_revenue
    #     # 应收账款占比=应收账款/主营业务收入
    # df['ys'] = df.account_receivable / df.operating_revenue
    #     # 应付账款占比=应付账款/主营业务收入
    # df['yf'] = df.accounts_payable / df.operating_revenue

    ## 股票筛选
    # 投资收益率 > 0
    df = df[df.tzsy > 0]
    # 根据PB升序排列，取前30%
    df = df.sort_index(by=['pb_ratio'])
    code1 = list(df.code.head(int(len(df) * 0.3)))
    # 根据三费占比升序排列，取前30%
    df2 = df[df.code.isin(code1)]
    df2 = df2.sort_index(by=['3'])
    code2 = list(df2.code.head(int(len(df2) * 0.3)))
    print len(code2)
    # 根据收入现金率降序排列，取前30%
    df3 = df2[df2.code.isin(code2)]
    df3 = df3.sort_index(by=['srxj'], ascending=False)
    code3 = list(df3.code.head(int(len(df3) * 0.3)))
    print len(code3)
    return code3


def dapan_stoploss(context):
    ## 根据局大盘止损，具体用法详见dp_stoploss函数说明
    stoploss = dp_stoploss(kernel=2, n=10, zs=0.1)
    if stoploss:
        if len(context.portfolio.positions) > 0:
            for stock in list(context.portfolio.positions.keys()):
                order_target(stock, 0)
        return


def dp_stoploss(kernel=2, n=10, zs=0.03):
    '''
    方法1：当大盘N日均线(默认60日)与昨日收盘价构成“死叉”，则发出True信号
    方法2：当大盘N日内跌幅超过zs，则发出True信号
    '''
    # 止损方法1：根据大盘指数N日均线进行止损
    if kernel == 1:
        t = n + 2
        hist = attribute_history('000300.XSHG', t, '1d', 'close', df=False)
        temp1 = sum(hist['close'][1:-1]) / float(n)
        temp2 = sum(hist['close'][0:-2]) / float(n)
        close1 = hist['close'][-1]
        close2 = hist['close'][-2]
        if (close2 > temp2) and (close1 < temp1):
            return True
        else:
            return False
    # 止损方法2：根据大盘指数跌幅进行止损
    elif kernel == 2:
        hist1 = attribute_history('000300.XSHG', n, '1d', 'close', df=False)
        if ((1 - float(hist1['close'][-1] / hist1['close'][0])) >= zs):
            return True
        else:
            return False
