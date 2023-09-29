from io import StringIO
import streamlit as st
import pandas as pd
import plotly.express as px
import Data
import config
import share


@st.cache_data
def load_data(identifier, **kwargs):
    return Data.get_all_data(identifier, **kwargs)


country_amount = load_data(config.socrata_dataset_identifier,
                           select="country_code, country_name, fiscal_year, transaction_type_name, current_amount",
                           where="fiscal_year >= '2006' AND fiscal_year <= '2023'",
                           order="country_name ASC")
# 筛选出Obligations和Disbursements
country_amount = country_amount[(country_amount['transaction_type_name'] == 'Obligations')
                                |
                                (country_amount['transaction_type_name'] == 'Disbursements')]

st.markdown("### 查看每个国家的受援助金额变化")

country_code, country_name = share.create_country_list()

country_data = country_amount[(country_amount['country_code'] == country_code)]

# 使用 Plotly Express 创建条形图
fig = px.bar(
    country_data,
    x='fiscal_year',
    y='current_amount',
    color='transaction_type_name',
    barmode='group',
    title=f'Aid to {country_name} by Year and assistance type',
    labels={'current_amount': 'Total Aid Amount', 'fiscal_year': 'Year',
            'transaction_type_name': 'Assistance Type'}
)


st.plotly_chart(fig)

# 创建一个 CSV 文件内容的字符串
csv_buffer = StringIO()
country_data.to_csv(csv_buffer, index=False)
csv_str = csv_buffer.getvalue()

# 添加下载按钮
st.download_button(
    label="Download data as CSV",
    data=csv_str,
    file_name=f"{country_name}_aid_data.csv",
    mime="text/csv",
)