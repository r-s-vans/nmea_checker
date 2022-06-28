import io
import pandas as pd
import streamlit as st
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pynmea2


# ファイル名記入
with open("teraterm_0623.log", 'r') as f:
    str_name_log = f.readlines()
    # print(str_name_log)
file = io.StringIO()
file.write("data\n")

list = []
for log_line in str_name_log:
    if (log_line.startswith('$GPZDA')):
        gpzda = (log_line.split(","))
        yyyymmddhhmmssff = datetime.datetime.strptime(gpzda[4] + '/' + gpzda[3] + '/' + gpzda[2] + ' ' + gpzda[1],
                                                      "%Y/%m/%d %H%M%S.%f")
        # print(yyyymmddhhmmssff)
        list.append(yyyymmddhhmmssff)
        # print(list)

df = pd.DataFrame({'data':list})
# print(df)



file2 = io.StringIO()
file2.write("NMEA,Course over ground(t),True,Course over ground(m),Magnetic,Speed over Ground(knots),knots,Speed over Ground(Km/hr),Km/hr,D*checksum\n")

for log_line in str_name_log:
    if log_line.find('$GPVTG') >= 0:
        log_line3 = log_line[:-1]
        # print(log_line3)
        file2.write(log_line3)
        file2.write("\n")
# print(list)
#
file2.seek(0)
df_GPZDA = pd.read_table(file2, sep = ',')

# # print(df_GPZDA)
#
# # fig = go.Figure()
fig1 = make_subplots(rows=4, cols=1, subplot_titles=["course over ground True","course over grounde Magnetic","Speed over ground(knots)","Speed over ground(km/hr)"], shared_xaxes = True, vertical_spacing=0.01, x_title="UTC_time")


fig1.add_trace(
    go.Scatter(x=df["data"], y=df_GPZDA['Course over ground(t)'], mode='lines', name='地表における移動の真方位(度)'), row=1, col=1)
fig1.add_trace(
    go.Scatter(x=df["data"], y=df_GPZDA['Course over ground(m)'], mode='lines', name='地表における移動の磁方位(度)'), row=2, col=1)


fig1.add_trace(
    go.Scatter(x=df["data"], y=df_GPZDA['Speed over Ground(knots)'], mode='lines', name='地表における移動の速度（knot)'), row=3, col=1)

fig1.add_trace(
    go.Scatter(x=df["data"], y=df_GPZDA['Speed over Ground(Km/hr)'], mode='lines', name='地表における移動の速度（km/h)'), row=4, col=1)

st.dataframe(df_GPZDA)
fig1.show()


