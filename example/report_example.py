from fortools import *

# In this example we use event log. But every artifact can be filtered with these functions.
event = EventLog.file_open(r'.\Security.evtx')
event_info = event.get_all_info()

# You can make report with md or word file.
# Every report exported by fortools saved in result folder

# 1. MD File Report

# 1) Make report.
# how to use: MdExport(report name)
md = MdExport('my_report')

# 2) Add table.
# how to use: var.add_table(json_list)
md.add_table(event_info)

# 3) Add text.
# how to use: var.add_text(string)
md.add_text('It\'s my report')

# 4) Close file.
# how to use: var.save()
md.save()


# 2. Word File Report

# 1) Make report.
# how to use: MdExport()
word = DocxExport()

# 2) Add table.
# This feature may take a long time depending on the amount of material.
# how to use: var.add_table(json_list)
word.add_table(event_info[0:1])

# 3) Add table-vertical.
# how to use: var.table_by_json(json)
word.table_by_json(event_info[0])

# 4) Add text.
# how to use: var.add_text(string)
word.add_text('It\'s my report')

# 5) Add image.
# how to use: var.add_img(img path)
word.add_img(r'.\img.png')

# 6) Save file.
# how to use: var.save(report name)
word.save('my_report')
