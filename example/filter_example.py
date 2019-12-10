from fortools import *

# In this example we use event log. But every artifact can be filtered with these functions.
event = EventLog.file_open(r'.\Security.evtx')
event_info = event.get_all_info()

# normal filter
# how to use: custom_filter([key, [keyword, keyword], 0], json_list)
filter_data = custom_filter(['eventID', [4624, 4647], 0], event_info)
for i in filter_data:
    print(i)

# regular expression filter
# how to use: custom_filter([key, r'regular expression', 1], json_list)
filter_data = custom_filter(['source', r'Microsoft-Windows-\w+', 1], event_info)
for i in filter_data:
    print(i)

# date filter
# how to use: date_filter(key, ['YYYY-MM-DD', 'YYYY-MM-DD'], json_list)
filter_data = date_filter('create Time', ['2015-03-24', '2015-03-24'], event_info)
for i in filter_data:
    print(i)

# time filter
# how to use: time_filter(key, ['HH:MM:SS', 'HH:MM:SS'], json_list)
filter_data = time_filter('create Time', ['20:00:00', '21:00:00'], event_info)
for i in filter_data:
    print(i)

# day filter
# how to use: day_filter(key, ['YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD HH:MM:SS'], json_list)
filter_data = day_filter('create Time', ['2015-03-24 20:00:00', '2015-03-24 21:00:00'], event_info)
for i in filter_data:
    print(i)

# time sort
# how to use: time_sort(key, json_list)
filter_data = time_sort('create Time', event_info)
for i in filter_data:
    print(i)

# date_count
# how to use: date_count(key, json_list)
filter_data = date_count('create Time', event_info)
print(filter_data)
