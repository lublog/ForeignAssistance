# @Time    : 2023/09/26 16:17
# @Author  : lu yao
# @FileName: Data.py

import pandas as pd
from sodapy import Socrata


def get_all_data(identifier, **kwargs):
    client = Socrata("data.usaid.gov", "7wQTG5bIYVjjEUv5JZ3KLJvEg")
    results = client.get_all(identifier, **kwargs)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    client.close()
    return results_df

