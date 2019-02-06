# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 10:43:30 2019
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def fill_missing_values(df_data):
    """Fill missing values in data frame, in place."""
    df_data.fillna(method="ffill", inplace=True)
    df_data.fillna(method="bfill", inplace=True)


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df_final = pd.DataFrame(index=dates)
    if "SPY" not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, "SPY")

    for symbol in symbols:
        file_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
            usecols=["Date", "Adj Close"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Adj Close": symbol})
        df_final = df_final.join(df_temp)
        if symbol == "SPY":  # drop dates SPY did not trade
            df_final = df_final.dropna(subset=["SPY"])

    return df_final


def plot_data(df_data):
    """Plot stock data with appropriate axis labels."""
    ax = df_data.plot(title="Stock Data", fontsize=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:]/df[:-1].values) -1
    daily_returns.ix[0,:] = 0
    return daily_returns

def test_run():
    """Function called by Test Run."""
    # Read data
    symbol_list = ["JAVA", "FAKE1", "FAKE2"]  # list of symbols
    start_date = "2005-12-31"
    end_date = "2014-12-07"
    dates = pd.date_range(start_date, end_date)  # date range as index
    df = get_data(symbol_list, dates)  # get data for each symbol

    # Fill missing values
    fill_missing_values(df)
    # Computing daily returns
    daily_returns = compute_daily_returns(df)
    # Scatterplot JAVA vs FAKE1
    daily_returns.plot(kind="scatter", x="JAVA", y="FAKE1")
    beta_JAVA, alpha_JAVA = np.polyfit(daily_returns["JAVA"], daily_retuns["FAKE1"],1)
    plt.plot(dauily_retuns["JAVA"], beta_JAVA*daily_retuns["JAVA"] + alpha_JAVA, '-',color='r')
    plt.show()
    
    # Calculate corr
    print(daily_returns.corr(method='pearson'))
    # Plot
    plot_data(df)


if __name__ == "__main__":
    test_run()
