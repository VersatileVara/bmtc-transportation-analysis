import pandas as pd

df1 = pd.read_csv(r'D:\DataAnalytics\DataAnalyticsProject\Public_Transport\routes_with_coordinates.csv') 
df2 = pd.read_csv(r'D:\DataAnalytics\DataAnalyticsProject\Public_Transport\routes.csv') 
print(df1.shape)
print(df1.columns.tolist())
print(df1.head())
print(df2.shape)
print(df2.columns.to_list())
print(df2.head())