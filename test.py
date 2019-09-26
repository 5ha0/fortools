from log import *

file = file_open('Application.evtx')

#file = evtx_log
with file as log:
    for x in log.records():
        print(x)
