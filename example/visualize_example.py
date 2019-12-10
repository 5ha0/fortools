from fortools import *

# In this example we use event log. But every artifact can be filtered with these functions.
event = EventLog.file_open(r'.\Security.evtx')
event_info = event.get_all_info()

# Visualize type: barchart, piechart, timeline
# Every result was saved in result folder

# In this example, I used the function key_count to create the json data.
cnt = key_count('create Time', event_info[0:10])

# 1. Bar Chart
# how to use: BarChart(json, 'chart name')
BarChart(cnt, 'barchart')

# 2. Timeline
# how to use: Timeline(json, 'chart name')
Timeline(cnt, 'TIMELINE')

# 3. PieChart
# how to use: PieChart(data, label, 'chart name')
PieChart(cnt, 'Pie')

