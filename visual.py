import argparse
from influxdb import InfluxDBClient
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Game window stats
width = 700
height = 700

"""Instantiate a connection to the InfluxDB."""

dbname = 'checkers'
dbuser = 'telegraf'
dbuser_password = 'telegraf'
query = 'select * from checkers;'

# client = InfluxDBClient(host, port, user, password, dbname)
client = InfluxDBClient(host='127.0.0.1', port=8086, database=dbname)

print("Switch user: " + dbuser)
client.switch_user(dbuser, dbuser_password)

print("Querying data: " + query)
result = client.query(query)

print("Result: {0}".format(result))

print("Next dataframe")
df = pd.DataFrame(client.query(query).get_points())
print(df.head())

for i in range(12):
    name = df.loc[(df['color'] == 'red') & (df['index'] == i)]
    list_X = name['X'].to_list()
    list_Y = name['Y'].to_list()
    plt.plot(list_X,list_Y,marker="o")
    # plt.xlim(0, 700)
    # plt.ylim(0, 700)
    print(name)
x, y = np.meshgrid(np.linspace(30,670, 8), np.linspace(30, 670, 8))
plt.vlines(x[0], *y[[0,-1],0])
plt.hlines(y[:,0], *x[0, [0,-1]])
plt.title("Red checkers")
#plt.grid(color='r', linestyle='-', linewidth=2)
plt.show()

for i in range(12):
    name = df.loc[(df['color'] == 'blue') & (df['index'] == i)]
    list_X = name['X'].to_list()
    list_Y = name['Y'].to_list()
    plt.plot(list_X, list_Y,marker="o")
    # plt.xlim(0, 700)
    # plt.ylim(0, 700)
    print(name)

x, y = np.meshgrid(np.linspace(30,670, 8), np.linspace(30, 670, 8))
plt.vlines(x[0], *y[[0,-1],0])
plt.hlines(y[:,0], *x[0, [0,-1]])
plt.title("Blue checkers")

#plt.grid(color='r', linestyle='-', linewidth=2)
plt.show()