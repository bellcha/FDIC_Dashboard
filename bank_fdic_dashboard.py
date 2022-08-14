import requests as rq
import json
import pandas as pd
from dataclasses import dataclass, asdict
import streamlit as st
import plotly.express as px

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



def get_data() -> pd.DataFrame:

    url = 'https://banks.data.fdic.gov/api/financials?filters=CERT%3A12203&fields=REPDTE%2CASSET%2CEEFFQR%2CDEP%2CNETINC%2CLNLSNET%2CROAQ%2CROEQ&sort_by=REPDTE&sort_order=DESC&limit=10000&offset=0&agg_limit=1&format=json&download=false&filename=data_file'
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

    values = values.drop(['NETINC','EEFFQR'], axis=1)

    values = pd.melt(values,id_vars=['REPDTE'], var_name='Category', value_name='Total')

    fig = px.bar(data_frame=values , x = 'REPDTE', color='Category', y='Total', barmode='group', title='Total Assets, Loans, and Deposits')
    
    return fig

def get_return_ratios(num_of_records: int, values: pd.DataFrame):

    values = values.head(num_of_records)

    values = values.drop(['ASSET', 'NETINC', 'EEFFQR', 'DEP', 'LOANS'],  axis=1)

    values = pd.melt(values, id_vars=['REPDTE'], var_name='Ratio', value_name = 'Number')

    fig = px.bar(data_frame= values, x='REPDTE', color='Ratio', y='Number', barmode='group', title='ROA and ROE History')

    return fig

    
def main():
    st.title('Merchants & Marine Bank')

    chart_data = get_data()
    
    num_of_periods = st.number_input('Enter Number of Periods',0, 30)

    if num_of_periods <= 0:
        num_of_periods = 5

    fig = fdic_bar_chart(num_of_periods, chart_data)

    st.plotly_chart(fig)

    fig2 = get_return_ratios(num_of_periods, chart_data)

    st.plotly_chart(fig2)
    
    col1, col2 = st.columns(2)
    
    col1.write('Net Income')
    col1.bar_chart(chart_data.head(num_of_periods), x='REPDTE', y='NETINC')

    col2.write('Effiency Ratio')
    col2.bar_chart(chart_data.head(num_of_periods), x='REPDTE', y='EEFFQR')

if __name__ == '__main__':

    main()
