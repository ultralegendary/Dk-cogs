import pandas as pd
import os

data=pd.read_csv("rollnum/resource/db.csv")

print((data.loc[data["r_no"]=='17EUCS001'].iloc[0])["name"])
