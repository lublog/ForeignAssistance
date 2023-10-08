# @Time    : 2023/09/29 11:21
# @Author  : lu yao
# @FileName: share.py
import streamlit as st
import config
import pandas as pd


def get_country_list():
    df = pd.read_csv('./cleaned_data/test_all_chinese.csv')
    print(df.columns)
    # 使用字典推导式来创建国家代码和国家名称的字典
    config.country_dict = {row['受援对象国']: row['受援对象国代码'] for index, row in
                    df.drop_duplicates(subset=['受援对象国代码']).iterrows()}
    # 将索引转换为list
    config.country_list = df['受援对象国'].unique().tolist()

    return config.country_list


def create_country_list():
    # 使用 Streamlit 的下拉列表
    selected_country = st.selectbox('选择你想查看的国家:', get_country_list())

    selected_country_code = config.country_dict[selected_country]
    return selected_country_code, selected_country
