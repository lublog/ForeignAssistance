# @Time    : 2023/09/29 11:21
# @Author  : lu yao
# @FileName: share.py
import streamlit as st
import cleaning_data
import config


def create_country_list():
    # 使用 Streamlit 的下拉列表
    selected_country = st.selectbox('Select a country:', cleaning_data.get_country_list())

    selected_country_code = config.country_dict[selected_country]
    return selected_country_code, selected_country