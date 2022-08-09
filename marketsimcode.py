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


def compute_portvals(
        orders_df,
        prices_df,
        sd,
        ed,
        start_val=100000,
        commission=0.0,
        impact=0.0,
):
    """
    Computes the portfolio values.
    :param orders_df: df of orders of cash desired to invest
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
    # get symbol from orders_df list
    sym = orders_df.columns[0]

    # trim df
    prices_df = prices_df.ix[sd: ed]

    # add 'Cash' column with starting value from orders
    prices_df['Cash'] = orders_df[sym].ix[0]

    # create trades df
    trades = pd.DataFrame(0.0, columns=prices_df.columns, index=prices_df.index)
    # iterate through orders_df to update trades df
    for order in range(orders_df.shape[0]):
        trade_date = orders_df.index[order]

        # determine num of shares possible for cash order
        num_shares = orders_df[sym].ix[order] // prices_df[sym].ix[trade_date]

        # updates trades
        trades[sym].ix[trade_date] += num_shares
        trades['Cash'].ix[trade_date] -= num_shares * prices_df[sym].ix[trade_date] * \
                                         (1 + impact) + commission


    # create holdings df
    holdings = pd.DataFrame(0.0, columns=trades.columns, index=trades.index)
    holdings['Cash'].ix[0] = start_val
    holdings.ix[0] += trades.ix[0]
    for trade_date in range(1, trades.shape[0]):
        holdings.ix[trade_date] = holdings.ix[trade_date - 1] + trades.ix[trade_date]

    # create values df
    values = pd.DataFrame(0.0, columns=holdings.columns, index=holdings.index)
    values = holdings * prices_df

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
    print("May the force be with you")
