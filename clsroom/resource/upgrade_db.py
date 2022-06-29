import os

import pandas as pd

data = pd.read_csv("sk_data_v3.csv")
# data = pd.read_csv("db.csv")

data['Rno']=data['Rno'].str.upper()
data.to_csv('sk_data_v4.csv')

