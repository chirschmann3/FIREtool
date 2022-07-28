import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

"""Creates df of orders to feed through marketsimcode
to determine performance for given datas and contributions/spend."""

def get_orders(sv, age, mon_inv, ret_age, mon_spend):
    """Get orders df to feed through marketsimcode and retrieve portfolio performance.
    :param sv: starting value of portfolio
    :param age: current age
    :param mon_inv: monthly investment until retirement (assumes investing on 1st day of month)
    :param ret_age: age of retirement (assumed at first of year of turning that age)
    :param mon_spend: monthly spend post retirement
    :return orders: orders df through age 90"""

    # get info for iterating through investing and selling period
    months2invest = (ret_age - age) * 12
    months2spend = (90 - ret_age) * 12

    # create df of NaN values for all months from now until 90 to fill in with orders
    # will be trimmed later
    date_range = pd.date_range(dt.date.today(), (dt.date.today() + relativedelta(years=(90-age))), freq='MS')
    orders = pd.DataFrame(np.nan, columns=['SP500'], index=date_range)

    # add starting investment value
    orders.ix[0] = sv

    # loop through investing years and add buy orders to df
    for month in range(1, months2invest+1):
        orders.ix[month] = mon_inv

    # loop through spending years and add sell orders to df
    for month in range(months2invest+1, months2invest+months2spend+1):
        orders.ix[month] = -mon_spend


    return orders