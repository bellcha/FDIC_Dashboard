import requests as rq
import json
import pandas as pd
from dataclasses import dataclass, asdict
import streamlit as st
import plotly.express as px
import yfinance as yf

@dataclass
class BankData:
    REPDTE: str
    ASSET: int
    EEFFQR: float
    NETINC: int
    DEP: int
    LOANS: int
    ROA: float
    ROE: float

ms_banks = {'Amory Federal Savings and Loan Association': '28949', 
    'Bank of Anguilla': '8243', 
    'Bank of Brookhaven': '35439', 
    'Bank of Commerce': '9359', 
    'Bank of England': '13303', 
    'Bank of Franklin': '10594', 
    'Bank of Holly Springs': '8232', 
    'Bank of Kilmichael': '9775', 
    'Bank of Morton': '8556', 
    'Bank of Wiggins': '8250', 
    'Bank of Winona': '12207', 
    'Bank of Yazoo City': '11431', 
    'Bank OZK': '110', 
    'Bank3': '15205', 
    'BankFirst Financial Services': '8870', 
    'BankOkolona': '5902', 
    'BankPlus': '5903', 
    'BNA Bank': '19448', 
    'Cadence Bank': '11813', 
    'CB&S Bank, Inc.': '15310', 
    'Century Bank': '11448', 
    'Citizens Bank': '324', 
    'Citizens Bank & Trust Co.': '9777', 
    'Commerce Bank': '34938', 
    'Commercial Bank & Trust Co.': '8660', 
    'Community Bank of Mississippi': '8879', 
    'Community Spirit Bank': '50', 
    'Concordia Bank & Trust Company': '8527', 
    'Copiah Bank': '8231', 
    'Covington County Bank': '21998', 
    'Delta Bank': '26564', 
    'Evolve Bank & Trust': '1299', 
    'Farmers and Merchants Bank': '15801', 
    'FIDELITY BANK': '28316', 
    'First American National Bank': '19226',
    'First Bank': '5907', 
    'First Choice Bank': '5006', 
    'FIRST COMMERCIAL BANK': '57069', 
    'First Federal Savings and Loan Association': '30812', 
    'First Financial Bank': '28905', 
    'First Horizon Bank': '4977', 
    'First National Bank of Clarksdale': '19070', 
    "First National Banker's Bank": '25247', 
    'First Security Bank': '17120', 
    'First Southern Bank': '31158', 
    'First State Bank': '15663', 
    'FNB Oxford Bank': '5005', 
    'FNB Picayune Bank': '16612', 
    'FSNB, National Association': '16416', 
    'Genesis Bank': '15817', 
    'Grand Bank for Savings, FSB': '31864', 
    'Great Southern Bank': '8552', 
    'Guaranty Bank and Trust Company': '15953', 
    'Hancock Whitney Bank': '12441', 
    'Holmes County Bank': '321', 
    'Home Bank, National Association': '28094', 
    'Home Banking Company': '9196', 
    'JPMorgan Chase Bank, National Association': '628', 
    'Liberty Bank and Trust Company': '20856', 
    'Magnolia State Bank': '22081', 
    'Mechanics Bank': '12206', 
    'Merchants & Marine Bank': '12203', 
    'Merchants and Planters Bank': '327', 
    'Origin Bank': '12614', 
    'Oxford University Bank': '57034', 
    'Paragon Bank': '57874', 
    'Peoples Bank': '9366', 
    'Pike National Bank': '26379', 
    'Pinnacle Bank': '35583', 
    'Planters Bank & Trust Company': '8235', 
    'PriorityOne Bank': '21906', 
    'Regions Bank': '12368', 
    'Renasant Bank': '12437', 
    'Richton Bank & Trust Company': '11817', 
    'RiverHills Bank': '8234', 
    'Southern Bancorp Bank': '1528', 
    'Sycamore Bank': '11423', 
    'The Bank of Forest': '898', 
    'The Bank of Vernon': '51', 
    'The Citizens Bank of Philadelphia, Mississippi': '12204', 
    'The Citizens National Bank of Meridian': '4993', 
    'The Cleveland State Bank': '12201', 
    'The Commercial Bank': '9356', 
    'The First Bank': '34217', 
    'The Jefferson Bank': '11445', 
    'The Peoples Bank': '15871', 
    'The Peoples Bank, Biloxi, Mississippi': '340', 
    'Truist Bank': '9846', 
    'Trustmark National Bank': '4988', 
    'United Mississippi Bank': '21083', 
    'Unity Bank of Mississippi': '11446', 
    'Wells Fargo Bank, National Association': '3511', 
    'Woodforest National Bank': '23220'}

def get_data(bank: str) -> pd.DataFrame:

    url = f'https://banks.data.fdic.gov/api/financials?filters=CERT%3A{bank}&fields=REPDTE%2CASSET%2CEEFFQR%2CDEP%2CNETINC%2CLNLSNET%2CROAQ%2CROEQ&sort_by=REPDTE&sort_order=DESC&limit=10000&offset=0&agg_limit=1&format=json&download=false&filename=data_file'
    data = json.loads(rq.get(url).text)
    bank_df = pd.DataFrame(columns=['REPDTE','ASSET','EEFFQR', 'NETINC', 'DEP', 'LOANS', 'ROA', 'ROE'])

    for d in data['data']:
        results = BankData(REPDTE=d['data']['REPDTE'], ASSET=d['data']['ASSET'], EEFFQR=d['data']['EEFFQR'], NETINC=d['data']['NETINC'], 
                DEP=d['data']['DEP'], LOANS=d['data']['LNLSNET'], ROA=d['data']['ROAQ'], ROE=d['data']['ROEQ'])
        row = pd.DataFrame(asdict(results), index=[0])
        bank_df = pd.concat([bank_df,row], axis=0 ,ignore_index=True)

    return bank_df

def fdic_bar_chart(num_of_records: int, values: pd.DataFrame):
    
    values = values.head(num_of_records)

    values = values.drop(['NETINC','EEFFQR', 'ROA', 'ROE'], axis=1)

    values = pd.melt(values,id_vars=['REPDTE'], var_name='Category', value_name='Total')

    fig = px.bar(data_frame=values , x = 'REPDTE', color='Category', y='Total', barmode='group', title='Total Assets, Loans, and Deposits')
    
    return fig

def get_return_ratios(num_of_records: int, values: pd.DataFrame):

    values = values.head(num_of_records)

    values = values.drop(['ASSET', 'NETINC', 'EEFFQR', 'DEP', 'LOANS'],  axis=1)

    values = pd.melt(values, id_vars=['REPDTE'], var_name='Ratio', value_name = 'Number')

    fig = px.bar(data_frame= values, x='REPDTE', color='Ratio', y='Number', barmode='group', title='ROA and ROE History')

    return fig

def get_stock_history(symbol: str):
    stock = yf.Ticker(symbol)

    stock_history = stock.history(period = 'max')

    stock_history = stock_history.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1)
    
    stock_history = stock_history.reset_index()

    return stock_history

    
def main():
    st.title('FDIC Bank Call Report Dashboard')

    #bank = st.text_input('Enter Bank FDIC Certificate Number:', value=None)

    bank_names = [i for i in ms_banks]

    #with st.form(key = 'columns_in_form'):
        #s1, s2 = st.columns(2)

        #with s1:

            #bank = st.selectbox('Choose a Bank:', bank_names)

        #with s2:

            #num_of_periods = st.number_input('Enter Number of Reporting Periods 1 - 30 (Default is 5)',1 , 30, value= 5)

        #submit_button = st.form_submit_button('Submit')
    
    bank = st.sidebar.selectbox('Choose a Bank:', bank_names)

    num_of_periods = st.sidebar.number_input('Number of Reporting Periods 1 - 30 (Default is 5)', value=5)
    
    cert = ms_banks[bank]

    st.subheader(f'{bank}')
        
    chart_data = get_data(cert)

    fig = fdic_bar_chart(num_of_periods, chart_data)

    st.plotly_chart(fig)

    fig2 = get_return_ratios(num_of_periods, chart_data)

    st.plotly_chart(fig2)
    
    col1, col2 = st.columns(2)
    
    col1.write('Net Income')
    col1.bar_chart(chart_data.head(num_of_periods), x='REPDTE', y='NETINC')

    col2.write('Effiency Ratio')
    col2.bar_chart(chart_data.head(num_of_periods), x='REPDTE', y='EEFFQR')
    
    #st.write(f'Stock Price History')
    #st.line_chart(stock_data, x = 'Date', y = 'Close')

if __name__ == '__main__':

    main()
