# @Time    : 2023/10/08 09:42
# @Author  : lu yao
# @FileName: process_data.py

"""
处理all.csv数据, 生成最终的数据集result.csv
"""

# 1. 导入需要的库
import pandas as pd

# 2. 读取数据
data = pd.read_csv('cleaned_data/all.csv', encoding='utf-8')


# 3. 数据处理
# 将assistance_type列展开为两个不同的列（economic和military）
# 通过pivot方法将assistance_type列展开
pivot_df = data.pivot(index=['year', 'country_name', 'country_code', 'fsi_index', 'hdi_index', 'sdg_index'],
                      columns='assistance_type',
                      values='amount')

# 重置索引和列名称以获得所需的格式
pivot_df.reset_index(inplace=True)
pivot_df.columns.name = None
pivot_df.columns = ['year', 'country_name', 'country_code', 'fsi_index', 'hdi_index', 'sdg_index',
                    'economic', 'military']
pivot_df = pivot_df.sort_values(by=['country_name', 'year'], ascending=[True, True])
# 将economic和military列中的NaN值替换为0
pivot_df['economic'] = pivot_df['economic'].fillna(0)
pivot_df['military'] = pivot_df['military'].fillna(0)

# 4. 计算每个国家每年的总援助金额
pivot_df['total'] = pivot_df['economic'] + pivot_df['military']

# 5. 计算每个国家2006-2021年经济援助金额和军事援助金额
country_list = pivot_df['country_name'].unique().tolist()
for cl in country_list:
    df = pivot_df[pivot_df['country_name'] == cl]
    economic_amount = df['economic'].sum()
    military_amount = df['military'].sum()
    total_amount = df['total'].sum()


pivot_df = pivot_df.convert_dtypes()

# 6. 根据规则判断援助类型
# pivot_df['assistance_type'] = pivot_df['economic_ratio'].apply(lambda x: 'economic' if x >= 0.5 else 'military')


# 定义一个函数，用于判断援助类型
def classify_aid(country_data):
    # 计算总体比例
    total_economic_amount = country_data['economic'].sum()
    total_military_amount = country_data['military'].sum()
    total_amount = total_economic_amount + total_military_amount

    # 检查援助类型条件
    if total_economic_amount / total_amount > 0.7:
        return 'Economic'
    elif total_military_amount / total_amount > 0.7:
        return 'Military'
    elif abs(total_economic_amount - total_military_amount) / total_amount < 0.1:
        return 'Balanced'
    else:
        return 'Other'


# 将数据按国家分组，并应用classify_aid函数
aid_type_series = pivot_df.groupby('country_name').apply(classify_aid)

# 将得到的Series转换为DataFrame，以便与原始数据合并
aid_type_df = aid_type_series.reset_index()
aid_type_df.columns = ['country_name', 'assistance_type']

# 合并到原始数据
pivot_df = pivot_df.merge(aid_type_df, on='country_name', how='left')

# 7. 计算每个国家每年的经济发展指标(归一化的SDG+HDI/2)
# 计算sdg归一化指标
max_value = pivot_df['sdg_index'].max()
min_value = pivot_df['sdg_index'].min()


pivot_df['economic_index'] = ((pivot_df['sdg_index'] - min_value) / (max_value - min_value) + pivot_df['hdi_index']) / 2

# 8.计算每个国家每年的发展-安全综合指数(归一化的FSI+经济发展指标/2)
# 计算fsi归一化指标
max_value = pivot_df['fsi_index'].max()
min_value = pivot_df['fsi_index'].min()

pivot_df['security_economic_index'] = (1 - (pivot_df['fsi_index'] - min_value) / (max_value - min_value)
                                       + pivot_df['economic_index']) / 2

pivot_df.to_csv('cleaned_data/test_result.csv', index=False, encoding='utf-8')

# 9. 删除奇异值
# 有的国家的数据只有一条，这样的数据没有意义，需要删除


# 导出一个中文列名的csv文件用于提交
# 先将列名转换为中文
# 年度
# 受援对象国
# 援助类别
# 经济援助金额(美元)
# 军事援助金额(美元)
# 总援助金额(美元)
# SDG
# HDI
# 对象国经济发展指标
# 对象国安全系数指标
# 对象国发展-安全综合指数
pivot_df.columns = ['年度', '受援对象国', '受援对象国代码', '对象国安全系数指标', 'HDI', 'SDG',
                    '经济援助金额(美元)', '军事援助金额(美元)', '总援助金额(美元)',
                     '援助类别', '对象国经济发展指标', '对象国发展-安全综合指数']
pivot_df = pivot_df[['年度', '受援对象国', '受援对象国代码', '援助类别', '经济援助金额(美元)', '军事援助金额(美元)', '总援助金额(美元)',
                     'SDG', 'HDI', '对象国经济发展指标', '对象国安全系数指标', '对象国发展-安全综合指数']]
pivot_df.to_csv('cleaned_data/result.csv', index=False, encoding='utf-8')


