"""Main file to run iterations of FIRE numbers."""

import FIREorders as orders
import marketsimcode as mkt
from SP500_data import SPYdata
import pandas as pd
import datetime as dt


def get_data():
    """Read stock data (adjusted close) for given symbols from SP500_data."""

    # get data from SP500_data
    data_wrang = SPYdata()
    data_df = data_wrang.get_data()
    # print(data_df.info())
    # data_df = data_df[(data_df['Date'] >= sd) & (data_df['Date'] <= ed)]

    # index df by dates
    df = pd.DataFrame(data_df['SP500'].values, columns=['SP500'], index=data_df['Date'])

    return df


def iterate_code(sv, age, mon_inv, ret_age, mon_spend):
    """Runs through iterations of FIREorders for multiple starting years
     and returns statistics on the outcomes
     :param sv: starting value of portfolio
    :param age: current age (must be 30 years or older)
    :param mon_inv: monthly investment until retirement (assumes investing on 1st day of month)
    :param ret_age: age of retirement (assumed retire at current month of year of turning that age)
    :param mon_spend: monthly spend post retirement"""

    # get prices_df for all dates available
    prices_df = get_data()

    # check lastest month that information is available for based on 90 year lifespan
    years2live = 90 - age
    latest_possible_date = prices_df.index[-1] - dt.timedelta(days=(years2live*365))

    # iterate through all years from sd to latest possible date




    # do stats on investments later than above dates and just say amount today?

    return



if __name__ == "__main__":
    iterate_code(500000, 30, 5000, 40, 6000)
