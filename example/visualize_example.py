from fortools import *

# for example we will use event log. But you can use other artifacts.
path =r'your path'
file = EventLog.file_open(path)

# In this example, i will use date filter. This function returns values within a certain period in json format.
date_fi = file.date('2019-11-01', '2019-11-18')

#  -------------------------- make chart.-------------------------------------
# You need to input json list and name. In this example i made a json variable using the date_count function.
BarChart(date_count("create Time", date_fi), 'name')
Timeline(date_count("create Time", date_fi), 'time')
