# -*- coding: utf-8 -*-
"""
    :author: Wang Zelin (王泽霖)
    :url: 
    :copyright: © 2018 Wang Zelin <1064534588@qq.com>
    :license: MIT, see LICENSE for more details.
"""
# fzl 负债率
# balance.total_liability / balance.total_assets

from jqdatasdk import *
auth('18682020262','WzlZxy420107')
# from jqdata import *
import pandas as pd
import numpy as np
import datetime

def get_fzl(code, statDate):
    # ['code', 'id', 'day', 'pubDate', 'statDate', 'cash_equivalents', 'settlement_provi', 'lend_capital', 'trading_assets', 'bill_receivable', 'account_receivable', 'advance_payment', 'insurance_receivables', 'reinsurance_receivables', 'reinsurance_contract_reserves_receivable', 'interest_receivable', 'dividend_receivable', 'other_receivable', 'bought_sellback_assets', 'inventories', 'non_current_asset_in_one_year', 'other_current_assets', 'total_current_assets', 'loan_and_advance', 'hold_for_sale_assets', 'hold_to_maturity_investments', 'longterm_receivable_account', 'longterm_equity_invest', 'investment_property', 'fixed_assets', 'constru_in_process', 'construction_materials', 'fixed_assets_liquidation', 'biological_assets', 'oil_gas_assets', 'intangible_assets', 'development_expenditure', 'good_will', 'long_deferred_expense', 'deferred_tax_assets', 'other_non_current_assets', 'total_non_current_assets', 'total_assets', 'shortterm_loan', 'borrowing_from_centralbank', 'deposit_in_interbank', 'borrowing_capital', 'trading_liability', 'notes_payable', 'accounts_payable', 'advance_peceipts', 'sold_buyback_secu_proceeds', 'commission_payable', 'salaries_payable', 'taxs_payable', 'interest_payable', 'dividend_payable', 'other_payable', 'reinsurance_payables', 'insurance_contract_reserves', 'proxy_secu_proceeds', 'receivings_from_vicariously_sold_securities', 'non_current_liability_in_one_year', 'other_current_liability', 'total_current_liability', 'longterm_loan', 'bonds_payable', 'longterm_account_payable', 'specific_account_payable', 'estimate_liability', 'deferred_tax_liability', 'other_non_current_liability', 'total_non_current_liability', 'total_liability', 'paidin_capital', 'capital_reserve_fund', 'treasury_stock', 'specific_reserves', 'surplus_reserve_fund', 'ordinary_risk_reserve_fund', 'retained_profit', 'foreign_currency_report_conv_diff', 'equities_parent_company_owners', 'minority_interests', 'total_owner_equities', 'total_sheet_owner_equities']
    q = query(
            balance.total_liability / balance.total_assets,
        ).filter(
            balance.code == code)
    fzl = get_fundamentals(q, statDate=statDate)
    try:
        # print(fzl.anon_1[0])
        return fzl.anon_1[0]
    except:
        # print(0)
        return 0

def main(code, year, offset):
    com_name = finance.run_query(query(finance.STK_LIST.name, ).filter(
        finance.STK_LIST.code.in_([code]), )).name[0]
    data_list = [[] for i in range(offset)]
    years = [year - i for i in range(offset)]
    date = ['q1', 'q2', 'q3', 'q4']
    for y in range(offset):
        for q in range(4):
            fzl = get_fzl(code, str(year - y) + date[q])
            data_list[y].append(fzl)
    # print(data_list)
    df = pd.DataFrame(
        data_list,
        columns=pd.MultiIndex.from_product([[com_name],
                                            ['Q1', 'Q2', 'Q3', 'Q4']]),
        index=pd.MultiIndex.from_product([years]))
    print(df)


if __name__ == '__main__':
    # get_fzl('000002.XSHE', '2019q1')
    # get_fzl('000002.XSHE', '2019q2')
    # get_fzl('000002.XSHE', '2019q3')
    # get_fzl('000002.XSHE', '2019q4')
    # get_fzl('000002.XSHE', '2020q1')
    # get_fzl('000002.XSHE', '2020q2')
    # get_fzl('000002.XSHE', '2020q3')
    # get_fzl('000002.XSHE', '2020q4')
    # code = '600519.XSHG'
    # code = '000987.XSHE'
    code = '600487.XSHG'
    year = 2020
    offset = 5
    main(code, year, offset)
