# @Time    : 2023/09/28 14:08
# @Author  : lu yao
# @FileName: result_analysis.py
# @description: 分析每个国家的SDG, HDI, 经济发展指标, 安全发展指标, 发展-安全综合指数随援助金额的变化趋势, 横坐标为时间, 纵坐标为指标值, 采用折线图进行展示

import streamlit as st
import share
import plot

# 打开wide模式
st.set_page_config(layout="wide")
st.markdown("### 观察每个国家总体发展水平随受援助金额的变化趋势")

country_code, country_name = share.create_country_list()
st.write(f'你选择的国家是: {country_name}', f'国家代码是: {country_code}')


# 年度,受援对象国,受援对象国代码,援助类别,经济援助金额(美元),军事援助金额(美元),总援助金额(美元),SDG,HDI,对象国经济发展指标,对象国安全系数指标,对象国发展-安全综合指数
# 选择某种指标关于时间的变化趋势(以上是指标的中文名称)
y_axis = st.selectbox(
    '请选择你想查看的数据',
    ('SDG', 'HDI', '对象国经济发展指标', '对象国安全系数指标', '对象国发展-安全综合指数')
)
col1, col2 = st.columns([1, 1])
# 绘制plotly图表
plot.plot(country_name, y_axis, col1, col2)



