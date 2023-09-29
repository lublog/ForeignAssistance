# @Time    : 2023/09/28 14:08
# @Author  : lu yao
# @FileName: result analysis.py

import streamlit as st
import share
import pandas as pd
import cleaning_data as cd
import plotly.express as px
import config

st.markdown("### 观察每个国家总体发展水平随受援助金额的变化趋势")

country_code, country_name = share.create_country_list()

result = pd.DataFrame(columns=['year', 'Amount', 'SDG', 'HDI', 'economic', 'security', 'composite index'])


'''
分析每个国家的SDG, HDI, 经济发展指标, 安全发展指标, 发展-安全综合指数
随援助金额的变化趋势, 横坐标为时间, 纵坐标为指标值, 采用折线图进行展示
'''

# 选择x轴
y_axis = st.selectbox(
    '请选择你想查看的数据',
    ('SDG', 'Amount', 'HDI', 'economic', 'security', 'composite index')
)

i = 0
# 获取指数数据2006-2023
for year in range(2006, 2022):
        index = cd.calc_index_of_development_and_security(country_name, country_code, str(year))

        amount = cd.get_amount(country_code, str(year))
        # 附加year, amount到index元组中
        value_y = (str(year), amount, index[0], index[1], index[2], index[3], index[4])
        # 将元组转换为词典
        value_d = dict(zip(result.columns, value_y))
        # 将Series追加到result中
        result.loc[i] = value_d
        i += 1


# 绘制plotly图表
fig = px.line(
    result,
    x='year',
    y=y_axis,
    title=f'{country_name}发展水平随受援助金额的变化趋势',
    labels={'year': '年份'},
)

amount_fig = px.bar(
    result,
    x='year',
    y='Amount',
    title=f'{country_name}受援助金额随时间的变化趋势',
    labels={'year': '年份'},

)
st.plotly_chart(fig)
st.plotly_chart(amount_fig)


