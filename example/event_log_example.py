from fortools import *

# example of evtxlog

# event log(evtx) open
#basic path is [C:\Windows\System32\winevt\Logs\]
path = r'your path'
log_file = EventLog.file_open(path)

'''
Uncomment the comment you want to use.
'''
# 
# # ------------------------1. It shows all the parsing provided by this library at once.---------------------------
# # With this function, you can get index, eventID, create Time, level, source, computer Information, SID.
# log_file.show_info()
# 
# # ------------------------2. Get hash value(before open, after analysis)-------------------------------------------
# hash_value = log_file.show_all_record()
# for i in hash_value:
#     print(i)
# 
# # ------------------------------------3. Get string from event log xml----------------------------------------------
# strings = log_file.get_string()
# 
# # print strings
# for i in strings:
#     print(i)
# 
# # make file with strings
# file = open(r'.\text.txt', 'w')
# for i in strings:
#     file.write(str(i)+'\n')
# file.close()
# 
# # -------------------------------------4. Search ID with event ID---------------------------------------------------
# event_id = log_file.eventid(your event_id)
# for i in event_id:
#     print(i)
# 
# # -------------------------------------5. Search ID with Date -------------------------------------------------------
# date_search = log_file.date('%Y-%m-%d', '%Y-%m-%d')
# for i in date_search:
#     print(i)
# 
# # -------------------------------------6. Search ID with Time -------------------------------------------------------
# date_search = log_file.time('%HH:%MM:%SS', '%HH:%MM:%SS')
# for i in date_search:
#     print(i)
# 
# # -------------------------------------7. Search ID with Day --------------------------------------------------------
# day_search = log_file.day('YYYY-MM-DD HH:MM:SS', 'YYYY-MM-DD HH:MM:SS')
# for i in day_search:
#     print(i)
# 
# # -------------------------------------8. Search ID with Level ------------------------------------------------------
# level = log_file.level(your level_num)
# for i in level:
#     print(i)
# 
# # -------------------------------------9. Favorite Function --------------------------------------------------------
# # favorite is function that binds frequently used events.
# # get information about system event log.
# sys_on = log_file.Favorite.System.system_on()
# sys_off = log_file.Favorite.System.system_off()
# dirty_shutdown = log_file.Favorite.System.dirty_shutdown()
# 
# # get information about account event log.
# logon = log_file.Favorite.AccountType.logon()
# login_failed = log_file.Favorite.AccountType.login_failed()
# verify_account = log_file.Favorite.AccountType.verify_account()
# change_pwd = log_file.Favorite.AccountType.change_pwd()
# delete_account = log_file.Favorite.AccountType.delete_account()
# add_privileged_group = log_file.Favorite.AccountType.add_privileged_group()
# 
# # get information about remote event log.
# remote = log_file.Favorite.Etc.remote()
# wireless = log_file.Favorite.Etc.wireless()
# firewall = log_file.Favorite.Etc.firewall()
# err_report = log_file.Favorite.Etc.error_report()
# app_crush = log_file.Favorite.Etc.app_crashes()
# service_fail = log_file.Favorite.Etc.service_fails()
# usb = log_file.Favorite.Etc.usb()
# 
# # -------------------------------------9. Get xml strings --------------------------------------------------------
# # get xml information with number of event log, in this function number is index of event log
# xml_info = log_file.xml_with_num(num)
# for i in xml_info:
#     print(i)
