# @Time    : 2023/10/08 18:14
# @Author  : lu yao
# @FileName: cagr.py
# @description: 读取cagr数据, 找出前20名国家和后20名国家

import pandas as pd
import streamlit as st
import plot



num = 20
st.set_page_config(layout="wide")

df = pd.read_csv('./cleaned_data/cagr.csv')

# 创建一个指标选择框
y_axis = st.selectbox(
    '选择一个你想追踪的指标',
    ('SDG', 'HDI', '对象国经济发展指标', '对象国安全系数指标', '对象国发展-安全综合指数')
)

data = df[['受援对象国', y_axis]].sort_values(by=y_axis, ascending=False)

# fsi指数越大, 说明该国家的安全性越低
# 所以我们fsi的值越小, 说明该国家的安全性越高
# 前20名和后20名应该反过来
if y_axis == '对象国安全系数指标':
    top20 = data.tail(20)
    last20 = data.head(20)
else:
    top20 = data.head(20)
    last20 = data.tail(20)


data_plot = st.selectbox(
    '选择一个你想查看的数据',
    ('前20名国家', '后20名国家')
)


col1, col2, col3 = st.columns([0.5,2,2])
if data_plot == '前20名国家':
    selected_data = top20['受援对象国'].tolist()
    st.write(str(selected_data))

else:
    selected_data = last20['受援对象国'].tolist()
    st.write(str(selected_data))

for index, name in enumerate(selected_data):
    # 创建多个按钮, 每个按钮对应一个国家, 默认显示第一个国家的数据
    # 如果点击了某个按钮, 则显示该国家的数据 按钮的名字为序号+国家名字
    last_name = f"{index+1}{name}"
    if col1.button(last_name):
        plot.plot(name, y_axis, col2, col3, save=True)





