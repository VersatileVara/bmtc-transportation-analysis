import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


df1 = pd.read_csv(r"D:\DataAnalytics\DataAnalyticsProject\Public_Transport\routes_with_coordinates.csv")
print(df1.shape)
print(df1.isnull().sum())
df1 = df1.drop(columns= ['latitude','longitude'])
print("DF1","\n",df1.head())

df2 = pd.read_csv(r"D:\DataAnalytics\DataAnalyticsProject\Public_Transport\routes.csv")
print(df2.shape)
print(df2.isnull().sum())
print(df2.head())
df2 = df2.drop(columns=["route_desc","route_url"])
print(df2.head())
print(df2["agency_id"].value_counts())
print(df2["route_color"].value_counts())
print(df2["route_text_color"].value_counts())
print(df2["route_type"].value_counts())
df2 = df2.drop(columns=["agency_id","route_color","route_text_color","route_type"])
print("DF2","\n",df2.head())

df3 = pd.read_csv(r"D:\DataAnalytics\DataAnalyticsProject\Public_Transport\stop_times.csv")
print(df3.shape)
print(df3.head())
print(df3.isnull().sum())
df3 = df3.drop(columns=["shape_dist_traveled","stop_headsign"])
print(df3.head())
print(df3["drop_off_type"].value_counts())
print(df3["pickup_type"].value_counts())
print(df3["stop_id"].value_counts())
print(df3["stop_sequence"].value_counts())
print(df3["timepoint"].value_counts())
df3 = df3.drop(columns=["drop_off_type","pickup_type","timepoint"])
print("DF3","\n",df3.head())

df4 = pd.read_csv(r"D:\DataAnalytics\DataAnalyticsProject\Public_Transport\stops.csv",index_col=False)
print(df4.shape)
print(df4.head())
print(df4.isnull().sum())
df4 = df4.drop(columns=["location_type","parent_station","stop_code","stop_desc","stop_timezone","stop_url","wheelchair_boarding","zone_id"])
print("DF4","\n",df4.head())

df5 = pd.read_csv(r"D:\DataAnalytics\DataAnalyticsProject\Public_Transport\trips.csv", index_col=False)
print(df5.shape)
print(df5.head())
print(df5.isnull().sum())
df5 = df5.drop(columns=["bikes_allowed","block_id","shape_id","trip_headsign","trip_short_name","wheelchair_accessible"])
print("DF5","\n",df5.head())

busiest_routes = df5["route_id"].value_counts().head(10)
busiest_routes = busiest_routes.reset_index()
busiest_routes = pd.merge(busiest_routes,df2,on="route_id")
print("Busiest Routes","\n",busiest_routes)

busiest_stops = df3["stop_id"].value_counts().head(10)
busiest_stops=busiest_stops.reset_index()
busiest_stops=pd.merge(busiest_stops,df4, on= "stop_id")
busiest_stops=busiest_stops.drop(columns=["stop_lat","stop_lon"])
print("Busiest Stops","\n", busiest_stops)

df3["hour"] = df3["arrival_time"].str.split(':').str[0]
print(df3.head(10))
busiest_hours = df3["hour"].value_counts().head(10)
busiest_hours = busiest_hours.reset_index()
print("Busiest Hours","\n", busiest_hours)

busiest_routes.to_csv('busiest_routes.csv', index=False)
busiest_stops.to_csv('busiest_stops.csv', index=False)
busiest_hours.to_csv('peak_hours.csv', index=False)

#Chart 1: Top 10 Busiest Routes (horizontal bar chart)
plt.figure(figsize=(12,8))
busiest_routes_sorted = busiest_routes.sort_values('count', ascending=True)
colors = cm.Purples(np.linspace(0.2, 0.9, len(busiest_routes_sorted)))
plt.barh(busiest_routes_sorted["route_id"], busiest_routes_sorted['count'], color=colors)
for index, value in enumerate(busiest_routes_sorted['count']):
    plt.text(value, index, f' {value}', va='center')
plt.xlabel("Number of Trips")
plt.title("Top 10 Busiest BMTC Routes")
plt.tight_layout()
plt.savefig('busiest_routes.png', dpi=150, bbox_inches='tight')
plt.show()

#Chart 2: Top 10 Busiest Stops (horizontal bar chart)
plt.figure(figsize=(12,8))
busiest_stops_sorted = busiest_stops.sort_values('count',ascending=True)
colors = cm.Purples(np.linspace(0.2, 0.9, len(busiest_stops_sorted)))
plt.barh(busiest_stops_sorted['stop_name'], busiest_stops_sorted['count'], color=colors)
for index, value in enumerate(busiest_stops_sorted['count']):
    plt.text(value, index, f' {value}', va='center')
plt.xlabel("Number of Trips")
plt.title("Top 10 Busiest BMTC Stops")
plt.tight_layout()
plt.savefig('busiest_stops.png', dpi=150, bbox_inches='tight')
plt.show()

#Chart 3: Busiest Hours
plt.figure(figsize=(12,8))
busiest_hours['hour'] = busiest_hours['hour'].astype(int)
busiest_hours_sorted = busiest_hours.sort_values('hour')
plt.bar(busiest_hours['hour'], busiest_hours['count'], color='steelblue')
plt.xlabel("Hours of a day")
plt.title("Busiest Hours")
plt.savefig('busiest_hours.png', dpi=150, bbox_inches='tight')
plt.show()

import pandas as pd
print(pd.read_csv('busiest_routes.csv').head(2))
print(pd.read_csv('busiest_stops.csv').head(2))
print(pd.read_csv('peak_hours.csv').head(2))