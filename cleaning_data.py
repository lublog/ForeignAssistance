# @Time    : 2023/09/28 14:17
# @Author  : lu yao
# @FileName: cleaning_data.py
import glob

import pandas as pd
import Data
import config
import streamlit as st


# 获取指定国家指定年份的HDI(人类发展指数)数据
def get_hdi_index(country_code, year):
    df = pd.read_csv(config.PROJECT_ROOT_URL + 'data/hdi_index.csv')
    columns_name = "hdi_" + str(year)

    # st.write("hdi: ")
    # # 输出国家列表并排列
    # st.write(df['country'].unique().tolist())
    # df按照国家和年份筛选
    return df.loc[(df['iso3'] == country_code), columns_name].values[0]


def get_sdg_index(country_code, year):
    df = pd.read_csv(config.PROJECT_ROOT_URL + 'data/SDG_all.csv')
    # st.write("sdg: ")
    # # 输出国家列表并排列
    # st.write(df['Country'].unique().tolist())

    # 找出SDG Index Score列中的最大值和最小值
    max_value = df['SDG Index Score'].max()
    min_value = df['SDG Index Score'].min()

    # 将year列中的值转换为字符串类型
    df['year'] = df['year'].astype(str)

    # 将SDG Index Score列中的值归一化到0-1之间
    df['SDG Index Score'] = (df['SDG Index Score'] - min_value) / (max_value - min_value)

    # 按照国家和年份筛选
    return df.loc[(df['Country Code ISO3'] == country_code) & (df['year'] == year), 'SDG Index Score'].values[0]


def get_fsi_index(country, year):
    # 初始化一个空的DataFrame，用于存储合并后的数据

    all_data = pd.DataFrame()

    file_paths = glob.glob(config.PROJECT_ROOT_URL + "data/fsi/fsi-20*.csv")
    # 循环读取每个文件并进行合并
    for file_path in file_paths:
        # 只读取需要的列
        cols_to_use = ['Country', 'Year', 'Total']

        df = pd.read_csv(file_path, usecols=cols_to_use)

        df['Year'] = df['Year'].astype(str).str[:4]

        # 将当前DataFrame追加到总DataFrame中
        all_data = pd.concat([all_data, df], ignore_index=True)

    all_data.to_csv(config.PROJECT_ROOT_URL + 'data/fsi_index.csv', index=False)

    max_value = all_data['Total'].max()
    min_value = all_data['Total'].min()

    return (all_data.loc[(all_data['Country'] == country) & (all_data['Year'] == year), 'Total'].values[0],
            (max_value, min_value))


# 计算每个国家每年的经济发展指标(归一化的SDG+HDI/2)
def calc_index_of_economic_development(country_code, year):
    # 获取SDG指数
    sdg_index = get_sdg_index(country_code, year)
    # 获取HDI指数
    hdi_index = get_hdi_index(country_code, year)
    # 计算经济发展指数(保留3位小数)Economic development index
    economic_index = round((sdg_index + hdi_index) / 2, 3)
    return sdg_index, hdi_index, economic_index


# 计算每个国家每年的发展-安全综合指数(归一化的FSI+经济发展指标/2)
@st.cache_data
def calc_index_of_development_and_security(country_name: str, country_code: str, year: str) -> tuple:
    # 获取FSI指数
    fsi_index, (max_value, min_value) = get_fsi_index(country_name, year)
    # st.write("fsi_index: ", fsi_index)
    # 归一化FSI指数
    norm_fsi_index = (fsi_index - min_value) / (max_value - min_value)
    # st.write("normalized fsi_index: ", fsi_index)
    # 获取经济发展指数
    sdg, hdi, economic_development_index = calc_index_of_economic_development(country_code, year)
    # st.write("economic_development_index: ", economic_development_index)
    # 计算发展-安全综合指数(保留3位小数)Composite Index of Development and Security
    # fsi指的是受威胁程度，所以1-fsi_index代表安全指数
    composite_index = round(((1-norm_fsi_index) + economic_development_index) / 2, 3)

    # 返回sdg, hdi, economic, fsi, composite指数
    return sdg, hdi, economic_development_index, fsi_index, composite_index


def get_country_list():
    df = pd.read_csv(config.PROJECT_ROOT_URL + 'data/SDG_all.csv')
    # 使用字典推导式来创建国家代码和国家名称的字典
    config.country_dict = {row['Country']: row['Country Code ISO3'] for index, row in
                    df.drop_duplicates(subset=['Country Code ISO3']).iterrows()}
    # 将索引转换为list
    config.country_list = df['Country'].unique().tolist()

    return config.country_list


def get_amount(country_code: str, year: str):
    df = pd.read_csv(config.PROJECT_ROOT_URL + 'data/amount.csv')
    df['Year'] = df['Year'].astype(str)
    values = df.loc[(df['Country Code'] == country_code) & (df['Year'] == year), 'Amount'].values
    st.write(values)
    return values[0] + values[1]


