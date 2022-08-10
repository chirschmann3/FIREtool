"""Main file to run iterations of FIRE numbers."""

import FIREorders as FIRE
import marketsimcode as mkt
from SP500_data import SPYdata
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdts


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


def plot_values(df):
    ax = df.plot(label='Portfolio Value over Time')
    plt.show()
    plt.title('Portfolio Performance Over Time')
    plt.xlabel('Date')
    xformat = mdts.DateFormatter('%b-%y')
    ax.xaxis.set_major_formatter(xformat)
    ax.legend()

    # save graph as png
    filename = "port_perform.png"
    plt.savefig(filename)
    plt.clf()


def get_mean(arr1, arr2, arr3):
    a1_mean = np.mean(arr1)
    a2_mean = np.mean(arr2)
    a3_mean = np.mean(arr3)
    return a1_mean, a2_mean, a3_mean

def get_std(ar1, ar2, ar3):
    a1_std = np.std(ar1)
    a2_std = np.std(ar2)
    a3_std = np.std(ar3)
    return a1_std, a2_std, a3_std

def get_10perctl(ar1, ar2, ar3):
    a1_pct = np.percentile(ar1, 10)
    a2_pct = np.percentile(ar2, 10)
    a3_pct = np.percentile(ar3, 10)
    return a1_pct, a2_pct, a3_pct


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

    # check latest month that information is available for based on 90 year lifespan
    years2live = 90 - age
    latest_possible_date = prices_df.index[-1] - relativedelta(years=years2live)

    # create empty arrays to track results for later statistics
    retire_values = np.empty([1,1])
    FIRE_ages = np.empty([1, 1])
    EOL_values = np.empty([1,1])

    # iterate through all years from data sd to latest possible date
    earliest_date = prices_df.index[0]
    possible_years = pd.date_range(earliest_date, latest_possible_date, freq='YS')
    for start_year in possible_years:
        # get retire year and death year based on start_year
        year_retire = start_year + relativedelta(years=(ret_age - age))
        end_year = start_year + relativedelta(years=years2live)

        # get orders and portfolio values
        orders = FIRE.get_orders(sv, age, mon_inv, ret_age, mon_spend, start_year)
        port_val = mkt.compute_portvals(orders, prices_df, start_year, end_year)

        # plot potfolio values over time
        plot_values(port_val)

        # get when hit FIRE number
        FIRE_num = mon_spend * 12 * 25
    #     sym = port_val.columns[0]
    #     FIRE_month = port_val[port_val[sym] >= FIRE_num].index[0]
    #     FIRE_age = FIRE_month.year - start_year + age
    #
    #     # update arrays for later stats
    #     retire_values.append(port_val.ix[year_retire])
    #     FIRE_ages.append(FIRE_age)
    #     EOL_values.append(port_val.ix[end_year])
    #
    # # trim first empty value
    # retire_values = retire_values.ix[1:]
    # FIRE_ages = FIRE_ages.index[1:]
    # EOL_values = EOL_values.ix[1:]
    #
    # # perform stats of interest on values
    # retire_mean_val, FIRE_mean_month, EOL_mean_val = get_mean(retire_values, FIRE_ages, EOL_values)
    # retire_std_val, FIRE_std_year, EOL_std_val = get_std(retire_values, FIRE_ages, EOL_values)
    # retire_10pct_val, FIRE_10pct_year, EOL_10pct_val = get_10perctl(retire_values, FIRE_ages, EOL_values)
    #
    # print('Your avg net worth at retirement is: ' + str(retire_mean_val))
    # print('Your avg age of reaching FIRE is : ' + str(FIRE_mean_month))
    # print('Your avg net worth at end of life is: ' + str(EOL_mean_val))
    # print('The std of your net worth at retirement is: ' + str(retire_std_val))
    # print("The std of age you reach FIRE is:  " + str(FIRE_std_year))
    # print('The std of your net worth at death is: ' + str(EOL_std_val))
    # print('The 10th percentile of net worth at retirement is: ' + str(retire_10pct_val))
    # print('The 10th percentile of your age you FIRE is: ' + str(FIRE_10pct_year))
    # print('The 10th percentile of your net worth at death is: ' + str(EOL_10pct_val))

    return



if __name__ == "__main__":
    iterate_code(500000, 30, 5000, 40, 6000)
