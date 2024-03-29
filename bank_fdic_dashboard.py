import requests as rq
import json
import pandas as pd
from fdic_data import BankData
from fdic_bank import BankInformation
import streamlit as st
import plotly.express as px
import yfinance as yf
import redis
from typing import List
from functools import partial


states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]


client = redis.Redis(host="redis", port=6379, db=0)


def get_state_bank_info(state: str) -> dict:

    url = "https://banks.data.fdic.gov/api/institutions"

    params = {
        "filters": f'STNAME:"{state}" AND ACTIVE:1',
        "fields": "CERT,NAME",
        "sort_by": "OFFICES",
        "sort_order": "DESC",
        "limit": "10000",
        "offset": "0",
        "format": "json",
    }

    raw_data = rq.get(url, params=params).text

    data = BankInformation(**json.loads(raw_data))

    bank_dict = {}

    for bank in data.data:
        bank_dict[bank.data.name] = str(bank.data.cert)

    return bank_dict


def get_redis_data(bank: str) -> pd.DataFrame:

    url = "https://banks.data.fdic.gov/api/financials"

    params = {
        "filters": f"CERT:{bank}",
        "fields": "REPDTE,ASSET,EEFFR,DEP,NETINC,LNLSNET,ROAQ,ROEQ,EQ,EQCCOMPI",
        "sort_by": "REPDTE",
        "sort_order": "DESC",
        "limit": "10000",
        "offset": "0",
        "agg_limit": "1",
        "format": "json",
    }

    try:

        raw_data = client.get(bank)

        if raw_data is None:
            print("Getting data from API to load into Redis")
            raw_data = rq.get(url, params=params).text
            client.set(bank, raw_data, px=86400)

    except Exception as e:

        print(e)

        raw_data = rq.get(url, params=params).text

    bank_df = pd.DataFrame(
        columns=[
            "repdte",
            "asset",
            "eeffr",
            "netinc",
            "dep",
            "lnlsnet",
            "roaq",
            "roeq",
            "eq",
            "eqccompi",
            "id",
        ]
    )

    bank_data = BankData(**json.loads(raw_data))

    for d in bank_data.data:
        row = pd.DataFrame(d.data.dict(), index=[0])
        bank_df = pd.concat([bank_df, row], axis=0, ignore_index=True)

    bank_df["repdte"] = pd.to_datetime(bank_df["repdte"], format="%Y%m%d")

    bank_df = bank_df.sort_values(by="repdte", ascending=False)

    return bank_df


def fdic_bar_chart(num_of_records: int, values: pd.DataFrame):

    values = values.head(num_of_records)

    values = values.drop(
        ["netinc", "eeffr", "roaq", "roeq", "eq", "eqccompi", "id"], axis=1
    )

    values = pd.melt(
        values, id_vars=["repdte"], var_name="Category", value_name="Total"
    )

    fig = px.bar(
        data_frame=values,
        x="repdte",
        color="Category",
        y="Total",
        barmode="group",
        title="Total Assets, Deposits, and Loans",
    )

    fig.update_layout(xaxis_title="Report Date")

    fig.update_xaxes(tickformat="%m/%d/%y", tickvals = values["repdte"])
    return fig


def get_return_ratios(num_of_records: int, values: pd.DataFrame):

    values = values.head(num_of_records)

    values = values.drop(
        ["asset", "netinc", "eeffr", "dep", "lnlsnet", "eq", "eqccompi", "id"], axis=1
    )

    values = pd.melt(values, id_vars=["repdte"], var_name="Ratio", value_name="Number")

    fig = px.bar(
        data_frame=values,
        x="repdte",
        color="Ratio",
        y="Number",
        barmode="group",
        title="ROA and ROE History",
    )

    fig.update_layout(xaxis_title="Report Date")

    fig.update_xaxes(tickformat="%m/%d/%y", tickvals = values["repdte"])
    return fig


def get_ratios_bar_chart(
    num_of_records: int, values: pd.DataFrame, data_cols: List[str]
):

    values = values.head(num_of_records)

    values_to_drop = [c for c in values.columns.values.tolist() if c not in data_cols]

    values = values.drop(values_to_drop, axis=1)

    values = pd.melt(values, id_vars=["repdte"], var_name="Ratio", value_name="Number")

    fig = px.bar(
        data_frame=values,
        x="repdte",
        # color="Ratio",
        y="Number",
        height=360,
        width=360,
    )

    fig.update_layout(xaxis_title="Report Date")
    fig.update_xaxes(tickformat="%m/%d/%y", tickvals = values["repdte"])
    return fig


def get_stock_history(symbol: str):
    stock = yf.Ticker(symbol)

    stock_history = stock.history(period="max")

    stock_history = stock_history.drop(
        ["Open", "High", "Low", "Volume", "Dividends", "Stock Splits"], axis=1
    )

    stock_history = stock_history.reset_index()

    return stock_history


def main():
    st.title("FDIC Bank Call Report Dashboard")

    state = st.sidebar.selectbox("Select a State: ", states)

    bank_dict = get_state_bank_info(state)

    bank = st.sidebar.selectbox("Choose a Bank:", sorted(bank_dict.keys()))

    num_of_periods = st.sidebar.number_input(
        "Number of Reporting Periods 1 - 30 (Default is 5)", value=5
    )

    cert = bank_dict[bank]

    st.subheader(f"{bank}")

    chart_data = get_redis_data(cert)

    fig = fdic_bar_chart(num_of_periods, chart_data)

    st.plotly_chart(fig)

    fig2 = get_return_ratios(num_of_periods, chart_data)

    st.plotly_chart(fig2)

    col1, col2 = st.columns(2)

    bar_chart = partial(get_ratios_bar_chart, num_of_periods, chart_data)

    col1.write("Net Income")
    ni_chart = bar_chart(["repdte", "netinc"])
    col1.write(ni_chart)

    col2.write("Effiency Ratio")
    eff_ratio_chart = bar_chart(["repdte", "eeffr"])
    col2.write(eff_ratio_chart)

    col3, col4 = st.columns(2)

    col3.write("Total Equity Capital")
    capital_chart = bar_chart(["repdte", "eq"])
    col3.write(capital_chart)

    col4.write("Other Comprehensive Income")
    oci_chart = bar_chart(["repdte", "eqccompi"])
    col4.write(oci_chart)

    # Keeping here in case I want to get stock price data again.
    # st.write(f'Stock Price History')
    # st.line_chart(stock_data, x = 'Date', y = 'Close')


if __name__ == "__main__":

    main()
