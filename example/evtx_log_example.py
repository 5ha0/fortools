from fortools import *

# example of evtxlog

# event log(evtx) open
log_file = EvtxLog.file_open('C:\\Windows\\System32\\winevt\\Logs\\Security.evtx')

# get strings from event log with function get_string()
strings = log_file.get_string()

# generate text file with extracted strings content
file = open('.\\text.txt', 'w')
for i in strings:
    file.write(str(i)+'\n')
file.close()

# get information of event log.
# With this function, you can get index, eventID, create Time, level, source, computer Information, SID.
log_file.show_all_record()

# get xml information with number of event log, in this function number is index of event log
log_file.xml_with_num(1)

# search information with eventID.
log_file.eventid()

# search information with date.
log_file.date('%Y-%m-%d', '%Y-%m-%d')

# search information with level.
log_file.level()

# favorite is function that binds frequently used events.
# get information about remote event log.
log_file.Favorite.remote()

# get information about account event log.
log_file.Favorite.AccountType.logon
log_file.Favorite.AccountType.login_failed()
log_file.Favorite.AccountType.verify_account()
log_file.Favorite.AccountType.change_pwd()
log_file.Favorite.AccountType.delete_account()
log_file.Favorite.AccountType.add_privileged_group()
