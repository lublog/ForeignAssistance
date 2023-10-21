# @Time    : 2023/10/08 20:23
# @Author  : lu yao
# @FileName: plot.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot(country, y, board1, board2, save=False):
    result = pd.read_csv("cleaned_data/result_chinese.csv")
    result = result[result['受援对象国'] == country]
    result_fig = px.line(
        result,
        x='年度',
        y=y,
        title=f'{country} {y}随受援助金额的变化趋势'
    )
    result_fig.update_layout(
        autosize=False,
        margin=dict(
            l=0,
            r=50,
            b=20,
            t=100,
            pad=4
        ),
    )
    # 将经济援助金额(美元),军事援助金额(美元),总援助金额(美元)
    # 显示在同一个bar图中
    fig = go.Figure()
    fig.add_trace(go.Line(
        x=result['年度'],
        y=result['经济援助金额(美元)'],
        name='经济援助金额(美元)',
        marker_color='rgb(55, 83, 109)'
    ))
    fig.add_trace(go.Line(
        x=result['年度'],

        y=result['军事援助金额(美元)'],
        name='军事援助金额(美元)',
        marker_color='rgb(26, 118, 255)'
    ))
    fig.add_trace(go.Line(
        x=result['年度'],
        y=result['总援助金额(美元)'],
        name='总援助金额(美元)',
        marker_color='rgb(26, 255, 26)'
    ))

    # 调整图表的大小
    fig.update_layout(
        autosize=False,
            margin=dict(
                l=0,
                r=50,
                b=20,
                t=100,
                pad=4
            ),
    )

    fig.update_layout(title=f'{country} 援助金额分布')


    board1.plotly_chart(result_fig)
    board2.plotly_chart(fig)