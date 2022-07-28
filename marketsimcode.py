"""
Code to determine portfolio values of given df.
Adapted from marketsimcode.py code submitted for Project 8 ML4T
"""

import datetime as dt
import os
import math
import pandas as pd
from SP500_data import SPYdata

def author():
    return 'chirschmann3'


def get_data(sd, ed):
    """Read stock data (adjusted close) for given symbols from SP500_data."""

    # get data from SP500_data
    data_wrang = SPYdata()
    data_df = data_wrang.get_data()
    # print(data_df.info())
    data_df = data_df[(data_df['Date'] >= sd) & (data_df['Date'] <= ed)]

    # index df by dates
    df = pd.DataFrame(data_df['SP500'].values, columns=['SP500'], index=data_df['Date'])

    return df


def compute_portvals(
        orders_df,
        sd,
        ed,
        start_val=100000,
        commission=0.0,
        impact=0.0,
):
    """
    Computes the portfolio values.
    :param orders_df: df of orders_df
    :type orders_df: pandas.Dataframe
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading order in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """
    # get prices of symbols from orders_df list
    sym = orders_df.columns[0]
    date_range = pd.date_range(sd, ed)
    prices = get_data([sym], date_range)
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    # remove SPY column if not in symbols list
    if 'SPY' not in sym: prices.drop('SPY', inplace=True, axis=1)
    # add 'Cash' column
    prices['Cash'] = 1.0

    # create trades df
    trades = pd.DataFrame(0.0, columns=prices.columns, index=prices.index)
    # iterate through orders_df to update trades df
    for order in range(orders_df.shape[0]):
        action = orders_df[sym].ix[order]
        trade_date = orders_df.index[order]
        trades[sym].ix[trade_date] += orders_df[sym].ix[order]
        trades['Cash'].ix[trade_date] -= orders_df[sym].ix[order] * prices[sym].ix[trade_date] * \
                                         (1 + impact) + commission


    # create holdings df
    holdings = pd.DataFrame(0.0, columns=trades.columns, index=trades.index)
    holdings['Cash'].ix[0] = start_val
    holdings.ix[0] += trades.ix[0]
    for trade_date in range(1, trades.shape[0]):
        holdings.ix[trade_date] = holdings.ix[trade_date - 1] + trades.ix[trade_date]

    # create values df
    values = pd.DataFrame(0.0, columns=holdings.columns, index=holdings.index)
    values = holdings * prices

    # get daily portfolio values
    port_vals = values.sum(axis=1)
    port_vals.columns = [sym]

    return port_vals


# function to calculate portfolio stats for test_code below
def find_port_stats(df):
    cum_ret = (df.ix[-1] / df.ix[0]) - 1
    daily_rets = (df / df.shift(1)) - 1
    daily_rets = daily_rets.ix[1:]  # remove 0 that will be first col
    std_daily_ret = daily_rets.std()
    avg_daily_ret = daily_rets.mean()
    sharpe_ratio = math.sqrt(252) * avg_daily_ret / std_daily_ret
    return cum_ret, std_daily_ret, avg_daily_ret, sharpe_ratio


if __name__ == "__main__":
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2010, 12, 31)
    get_data(sd, ed)
