class Chatbot():
    def __init__(self):
        file = open(r'.\script.py', 'w')
        file.write('from fortools import *\n\n')

        print('input your artifact path')
        path = input()

        print('what is your atrifact? 1.event log 2.JumpList 3.FileSystem Log 4.registry ')
        answer = int(input())

        if answer == 1:
            file.write('event = EventLog.file_open(\''+path+'\')\n')
            print('choose your analysis\n1.Show All Info\n2.Get Hash value of Artifact\n3.'
                  'Get String of event log xml\n4.Event ID Search\n5.Date Search\n6.Time Search\n7.Day Search\n'
                  '8.Level Search\n9. Favorite\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    print('You can get info of event log. '
                          '\n[event id, creation time, timezone, level, source, computer info, sid]')
                    file.write('event.show_all_record()\n')
                elif analysis == 2:
                    print('You can get hash info of event log. [before/after analysis hash value]')
                    file.write('hash_value = event.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                elif analysis == 3:
                    print('You can get strings from event log xml.')
                    file.write('string_info = event.get_string()\nfor i in string_info:\n\tprint(i)\n')
                elif analysis == 4:
                    print('You can search with event id. Input event ID: ')
                    event_id = input()
                    file.write('event_id_info = event.eventid('+event_id+')\nfor i in event_id_info:\n\tprint(i)\n')
                elif analysis == 5:
                    print('You can search with Date. Input Start Date: (form: YYYY-MM-DD)')
                    start_date = input()
                    print('Input End Date: (form: YYYY-MM-DD)')
                    end_date = input()
                    file.write("date_info = event.date('" + start_date+"', '" + end_date +
                               "')\nfor i in date_info:\n\tprint(i)\n")
                elif analysis == 6:
                    print('You can search with Time. Input Start Time: (form: HH:MM:SS)')
                    start_time = input()
                    print('Input End Time: (form: HH:MM:SS)')
                    end_time = input()
                    file.write("time_info = event.time('" + start_time + "', '" + end_time +
                               "')\nfor i in time_info:\n\tprint(i)\n")
                elif analysis == 7:
                    print('You can search with Day. Input Start Day: (form: YYYY-MM-DD HH:MM:SS)')
                    start_day = input()
                    print('Input End Day: (form: YYYY-MM-DD HH:MM:SS)')
                    end_day= input()
                    file.write("day_info = event.day('" + start_day + "', '" + end_day +
                               "')\nfor i in day_info:\n\tprint(i)\n")
                elif analysis == 8:
                    print('You can search with Level. Input Level: [0, 1, 2, 3]')
                    level = input()
                    file.write("level_info = event.level(" + level + ")\nfor i in level_info:\n\tprint(i)\n")
                elif analysis == 9:
                    print('You can use Favorite Function. Choose Category.[1: System 2: Account 3: Etc]')
                    category = int(input())
                    if category == 1:
                        print('Choose Category.[1: System On 2: System Off 3: Dirty Off]')
                        category = int(input())
                        if category == 1:
                            file.write('sys_on = event.Favorite.System.system_on()\nfor i in sys_on:\n\tprint(i)\n')
                        elif category ==2:
                            file.write('sys_off = event.Favorite.System.system_off()\nfor i in sys_off:\n\tprint(i)\n')
                        elif category == 3:
                            file.write('sys_dirty_off = event.Favorite.System.dirty_shutdown()\nfor i in sys_dirty_off:\n\tprint(i)\n')
                    elif category == 2:
                        print('Choose Category.[1: Log On 2: Log Off 3: Login Failed 4: change password 5: Delete Account '
                              '6: Verify Account 7: Add Privileged Group]')
                        category = int(input())
                        if category == 1:
                            file.write('logon = event.Favorite.Account.logon()\nfor i in logon:\n\tprint(i)\n')
                        elif category == 2:
                            file.write('logoff = event.Favorite.Account.logoff()\nfor i in logoff:\n\tprint(i)\n')
                        elif category == 3:
                            file.write('login_fail = event.Favorite.Account.login_failed()\nfor i in login_fail:\n\tprint(i)\n')
                        elif category == 4:
                            file.write('ch_pwd = event.Favorite.Account.change_pwd()\nfor i in ch_pwd:\n\tprint(i)\n')
                        elif category == 5:
                            file.write('del_acc = event.Favorite.Account.delete_account()\nfor i in del_acc:\n\tprint(i)\n')
                        elif category == 6:
                            file.write('ver_acc = event.Favorite.Account.verify_account()\nfor i in ver_acc:\n\tprint(i)\n')
                        elif category == 7:
                            file.write('pri_group = event.Favorite.Account.add_privileged_group()\nfor i in pri_group:\n\tprint(i)\n')
                    elif category == 3:
                        print('Choose Category.[1: remote 2: app_crashes 3: error_report 4: service_fails 5: firewall '
                              '6: usb 7: wireless]')
                        if category == 1:
                            file.write('remote = event.Favorite.Etc.remote()\nfor i in remote:\n\tprint(i)\n')
                        elif category == 2:
                            file.write('app_crash = event.Favorite.Account.app_crashes()\nfor i in app_crash:\n\tprint(i)\n')
                        elif category == 3:
                            file.write('err_report = event.Favorite.Account.error_report()\nfor i in err_report:\n\tprint(i)\n')
                        elif category == 4:
                            file.write('serv_fail = event.Favorite.Account.service_fails()\nfor i in serv_fail:\n\tprint(i)\n')
                        elif category == 5:
                            file.write('firewall = event.Favorite.Account.firewall()\nfor i in firewall:\n\tprint(i)\n')
                        elif category == 6:
                            file.write('usb = event.Favorite.Account.usb()\nfor i in usb:\n\tprint(i)\n')
                        elif category == 7:
                            file.write('wireless = event.Favorite.Account.wireless()\nfor i in wireless:\n\tprint(i)\n')
                else:
                    print('plz input num. ex)1')
        elif answer == 2:
            file.write("jumplist = JumpList.file_open('" + path + "')\n")
            print('choose your analysis. \n1.Get access count\n2.Get recent time\n3.Get netbios\n4.Get all info\n5.Get hash')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('print("access count: "+ str(jumplist.access_count()))\n')
                elif analysis == 2:
                    file.write('print("recent time: "+ str(jumplist.recent_time()))\n')
                elif analysis == 3:
                    file.write('print("netbios: "+ str(jumplist.netbios()))\n')
                elif analysis == 4:
                    file.write('jump_info = jumplist.get_info()\nfor i in jump_info:\n\tprint(i)\n')
                elif analysis == 5:
                    file.write('jump_hash = jumplist.get_hash()\nfor i in jump_hash:\n\tprint(i)\n')
        elif answer == 3:
            file.write("filesys_log = FileSystemLog.file_open('" + path + "')\n")
            print('choose your analysis. \n1.Get all info\n2.Get hash')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('file_syslog_info = jfilesys_log.get_info()\nfor i in file_syslog_info:\n\tprint(i)\n')
                elif analysis == 5:
                    file.write('file_syslog_hash = filesys_log.get_hash()\nfor i in file_syslog_hash:\n\tprint(i)\n')
        file.close()
