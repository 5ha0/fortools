from forlib.signature import *

class Chatbot():
    def __init__(self):
        print('input your script name')
        name = input()

        file = open(r'.\\' + name+'.py' , 'w', encoding='utf-8')
        file.write('from fortools import *\n\n')

        while True:
            print('\ninput your artifact path. If you want to finish you need to input -1.')
            path = input()
            if path == '-1':
                break
            try:
                artifact_type = sig_check(path)
            except OSError:
                print('Plz check your path one more time')
                continue
            except:
                print('Plz check your path one more time')
                continue
            if artifact_type == -1 or artifact_type == 'data':
                print(artifact_type)
                print('You need to know your artifact')
            else:
                print('Maybe it is '+str(artifact_type))

            print('\nwhat is your atrifact? \n1.Event log 2.JumpList 3.FileSystem Log 4.Registry 5.Thumb&Icon_##\n'
                  '6.Zip 7.Files 8.Browser 9.Recycle 10.IconCache.db \n11.Lnk 12.Prefetch 13.Disk Image')
            answer = input()
            try:
                answer = int(answer)
            except:
                print('Plz check your input.')
                continue
            if answer > 13 or answer == 0 or answer < -1:
                print('Plz check your input.')
                continue

            if answer == 1:
                file.write('\n# Artifact: EventLog(.evtx)\n')
                file.write('event = EventLog.file_open(r\''+path+'\')\n')
                while True:
                    print('\nchoose your analysis\n1.Show All Info\n2.Get Hash value of Artifact\n3.'
                          'Get String of event log xml\n4.Event ID Search\n5.Date Search\n6.Time Search\n7.Day Search\n'
                          '8.Level Search\n9.Favorite\n10.Get xml strings with idx\n11.Get All Info\n-1:finish')
                    print('input num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 11 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue

                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Print EventLog Information. [event id, creation time, timezone, level, source, computer info, sid]\n')
                        print('print info of event log. '
                              '\n[event id, creation time, timezone, level, source, computer info, sid]')
                        file.write('event.show_all_info()\n')
                    elif analysis == 2:
                        file.write('\n# Get hash info of event log. [before/after analysis hash value]\n')
                        print('You can get hash info of event log. [before/after analysis hash value]')
                        file.write('hash_value = event.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Get strings from event log xml.\n')
                        print('You can get strings from event log xml.')
                        file.write('string_info = event.get_string()\nfor i in string_info:\n\tprint(i)\n')
                    elif analysis == 4:
                        print('You can search with event id. Input event ID: ')
                        event_id = input()
                        file.write('\n# Search EventLog with event id '+event_id+'.\n')
                        file.write('event_id_info = event.eventid('+event_id+')\nfor i in event_id_info:\n\tprint(i)\n')
                    elif analysis == 5:
                        print('You can search with Date. Input Start Date: (form: YYYY-MM-DD)')
                        start_date = input()
                        print('Input End Date: (form: YYYY-MM-DD)')
                        end_date = input()
                        file.write('\n# Search EventLog with date from ' + start_date + ' to '+end_date+'.\n')
                        file.write("date_info = event.date('" + start_date+"', '" + end_date +
                                   "')\nfor i in date_info:\n\tprint(i)\n")
                    elif analysis == 6:
                        print('You can search with Time. Input Start Time: (form: HH:MM:SS)')
                        start_time = input()
                        print('Input End Time: (form: HH:MM:SS)')
                        end_time = input()
                        file.write('\n# Search EventLog with time from ' + start_time + ' to ' + end_time + '.\n')
                        file.write("time_info = event.time('" + start_time + "', '" + end_time +
                                   "')\nfor i in time_info:\n\tprint(i)\n")
                    elif analysis == 7:
                        print('You can search with Day. Input Start Day: (form: YYYY-MM-DD HH:MM:SS)')
                        start_day = input()
                        print('Input End Day: (form: YYYY-MM-DD HH:MM:SS)')
                        end_day= input()
                        file.write('\n# Search EventLog with day from ' + start_day + ' to ' + end_day + '.\n')
                        file.write("day_info = event.day('" + start_day + "', '" + end_day +
                                   "')\nfor i in day_info:\n\tprint(i)\n")
                    elif analysis == 8:
                        print('You can search with Level. Input Level: [0: Audit success/Failure 1: Danger 2: Error 3: Warning 4: Information]')
                        level = input()
                        file.write('\n# Search EventLog with Level ' + level + '.\n# 0: Audit success/Failure 1: Danger 2: Error 3: Warning 4: Information\n')
                        file.write("level_info = event.level(" + level + ")\nfor i in level_info:\n\tprint(i)\n")
                    elif analysis == 9:
                        print('You can use Favorite Function. Choose Category.[1: System 2: Account 3: Etc]')
                        category = input()
                        try:
                            category = int(category)
                        except:
                            print('Plz check your input.')
                            continue
                        if category > 3 or category == 0 or analysis < -1:
                            print('Plz check your input.')
                            continue
                        if category == 1:
                            print('Choose Category.[1: System On 2: System Off 3: Dirty Off]')
                            category = input()
                            try:
                                category = int(category)
                            except:
                                print('Plz check your input.')
                                continue
                            if category > 3 or category == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            if category == 1:
                                file.write('\n# Get system on info\n')
                                file.write('sys_on = event.Favorite.System.system_on()\nfor i in sys_on:\n\tprint(i)\n')
                            elif category ==2:
                                file.write('\n# Get system off info\n')
                                file.write('sys_off = event.Favorite.System.system_off()\nfor i in sys_off:\n\tprint(i)\n')
                            elif category == 3:
                                file.write('\n# Get dirty system off info\n')
                                file.write('sys_dirty_off = event.Favorite.System.dirty_shutdown()\nfor i in sys_dirty_off:\n\tprint(i)\n')
                        elif category == 2:
                            print('\nChoose Category.[1: Log On 2: Log Off 3: Login Failed 4: change password 5: Delete Account '
                                  '6: Verify Account 7: Add Privileged Group]')
                            category = input()
                            try:
                                category = int(category)
                            except:
                                print('Plz check your input.')
                                continue
                            if category > 7 or category == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            if category == 1:
                                file.write('\n# Get log on info\n')
                                file.write('logon = event.Favorite.Account.logon()\nfor i in logon:\n\tprint(i)\n')
                            elif category == 2:
                                file.write('\n# Get log off info\n')
                                file.write('logoff = event.Favorite.Account.logoff()\nfor i in logoff:\n\tprint(i)\n')
                            elif category == 3:
                                file.write('\n# Get login filaed info\n')
                                file.write('login_fail = event.Favorite.Account.login_failed()\nfor i in login_fail:\n\tprint(i)\n')
                            elif category == 4:
                                file.write('\n# Get changed password event info\n')
                                file.write('ch_pwd = event.Favorite.Account.change_pwd()\nfor i in ch_pwd:\n\tprint(i)\n')
                            elif category == 5:
                                file.write('\n# Get deleted account event info\n')
                                file.write('del_acc = event.Favorite.Account.delete_account()\nfor i in del_acc:\n\tprint(i)\n')
                            elif category == 6:
                                file.write('\n# Get verified account event info\n')
                                file.write('ver_acc = event.Favorite.Account.verify_account()\nfor i in ver_acc:\n\tprint(i)\n')
                            elif category == 7:
                                file.write('\n# Get add privileged group event info\n')
                                file.write('pri_group = event.Favorite.Account.add_privileged_group()\nfor i in pri_group:\n\tprint(i)\n')
                        elif category == 3:
                            print('Choose Category.[1: remote 2: app_crashes 3: error_report 4: service_fails 5: firewall '
                                  '6: usb 7: wireless]')
                            category = input()
                            try:
                                category = int(category)
                            except:
                                print('Plz check your input.')
                                continue
                            if category > 7 or category == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            if category == 1:
                                file.write('\n# Get event info about remote\n')
                                file.write('remote = event.Favorite.Etc.remote()\nfor i in remote:\n\tprint(i)\n')
                            elif category == 2:
                                file.write('\n# Get event info about app crash\n')
                                file.write('app_crash = event.Favorite.Account.app_crashes()\nfor i in app_crash:\n\tprint(i)\n')
                            elif category == 3:
                                file.write('\n# Get event info about error report\n')
                                file.write('err_report = event.Favorite.Account.error_report()\nfor i in err_report:\n\tprint(i)\n')
                            elif category == 4:
                                file.write('\n# Get event info about service fail\n')
                                file.write('serv_fail = event.Favorite.Account.service_fails()\nfor i in serv_fail:\n\tprint(i)\n')
                            elif category == 5:
                                file.write('\n# Get event info about firewall\n')
                                file.write('firewall = event.Favorite.Account.firewall()\nfor i in firewall:\n\tprint(i)\n')
                            elif category == 6:
                                file.write('\n# Get event info about usb\n')
                                file.write('usb = event.Favorite.Account.usb()\nfor i in usb:\n\tprint(i)\n')
                            elif category == 7:
                                file.write('\n# Get event info about wireless\n')
                                file.write('wireless = event.Favorite.Account.wireless()\nfor i in wireless:\n\tprint(i)\n')
                    elif analysis == 10:
                        print('Put event log idx what you want to see. Input: ')
                        idx = input()
                        file.write('\n# Search with event log idx '+idx+' and you can get xml strings.\n')
                        file.write('xml_info = log_file.xml_with_num('+idx+')\nprint(xml_info)\n')
                    elif analysis == 11:
                        file.write('\n# Get all event log info. [event id, creation time, timezone, level, source, computer info, sid]\n')
                        print('You can get info of event log.\n[event id, creation time, timezone, level, source, computer info, sid]')
                        file.write('event_info = event.get_all_info()\nfor i in event_info:\n\tprint(i)\n')
                    else:
                        print('plz input num. ex)1')
            elif answer == 2:
                file.write('\n# Artifact: Jumplist\n')
                file.write("jumplist = JumpList.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Get summary info from destlist\n2.Get destlist data list\n3.Get information from streams except destlist\n4.Print all info from streams\n5.Get hash\n-1:finish')
                    print('input num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 5 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Get Jumplist Summary Information.\n# You can get total num of JumpList, Total Num of Add/Delete/Open action, Netbios, Last Access Time, Access Count, Data String\n')
                        print('What is your window version? input [7, 10]: ')
                        while True:
                            ver = input()
                            try:
                                ver = int(ver)
                            except:
                                print('Plz check your input.')
                                continue
                            if ver is 7 or ver is 10:
                                break
                            print('Plz check your input.')
                        if ver == 7:
                            file.write('summary = jumplist.get_summary(7)\nfor i in summary:\n\tprint(i)\n')
                        elif ver == 10:
                            file.write('summary = jumplist.get_summary(10)\nfor i in summary:\n\tprint(i)\n')
                    elif analysis == 2:
                        file.write('\n# Get destlist data list.\n# You can get MAC, Netbios, Last Access Time, New Time, Birth Time\n')
                        print('What is your window version? input [7, 10]: ')
                        ver = input()
                        while True:
                            try:
                                ver = int(ver)
                            except:
                                print('Plz check your input.')
                                continue
                            if ver is 7 or ver is 10:
                                break
                            print('Plz check your input.')
                        if ver == 7:
                            file.write('dest_list = jumplist.get_destlist_data(7,\'all\')\nfor i in dest_list:\n\tprint(i)\n')
                        elif ver == 10:
                            file.write('dest_list = jumplist.get_destlist_data(10,\'all\')\nfor i in dest_list:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Get information from streams.\n# You can get MAC time, File size, Target file size, Local path, Drive type, Drive serial number, Volume label\n')
                        file.write('info_list = jumplist.get_all_info()\nfor i in info_list:\n\tprint(i)\n')
                    elif analysis == 4:
                        file.write('\n# Print information from streams.\n# You can get MAC time, File size, Target file size, Local path, Drive type, Drive serial number, Volume label\n')
                        file.write('jumplist.show_all_info()\n')
                    elif analysis == 5:
                        file.write('\n# Get hash\n')
                        file.write('jump_hash = jumplist.get_hash()\nfor i in jump_hash:\n\tprint(i)\n')
                    else:
                        print('plz input num. ex)1')
            elif answer == 3:
                file.write('\n# Artifact: Filesystem Log\n')
                file.write("filesys_log = FileSystemLog.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Get all info\n2.Get hash\n3.Show all info\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 3 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Get information of filesystem log.\n')
                        file.write('file_syslog_info = filesys_log.get_all_info()\nfor i in file_syslog_info:\n\tprint(i)\n')
                    elif analysis == 2:
                        file.write('\n# Get hash\n')
                        file.write('file_syslog_hash = filesys_log.get_hash()\nfor i in file_syslog_hash:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Print information of filesystem log.\n')
                        file.write('filesys_log.show_all_info()\n')
                    else:
                        print('plz input num. ex)1')
            elif answer == 4:
                file.write('\n# Artifact: Registry\n')
                file.write("reg_file = RegistryHive.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis type.\n1.Find key with keyword search\n2.Find value with key path\n3.Get hash\n4.Favorite\ninput num:')
                    types = input()
                    try:
                        types = int(types)
                    except:
                        print('Plz check your input.')
                        continue
                    if types > 4 or types == 0 or types < -1:
                        print('Plz check your input.')
                        continue
                    if types == -1:
                        break
                    elif types == 1:
                        print('Input your key: ')
                        key_input = input()
                        file.write('\n# Find key path with keyword\n')
                        file.write('key_path_info = reg_file.find_key(\''+key_input+'\')\nfor i in key_path_info:\n\tprint(i)\n')
                    elif types == 2:
                        print('Input your key path: ')
                        key_input = input()
                        file.write('\n# Find value with key path\n')
                        file.write('value = reg_file.find_value(\'' + key_input + '\')\nfor i in value:\n\tprint(i)\n')
                    elif types == 3:
                        file.write('\n# Get hash\n')
                        file.write('hash_value = reg_file.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                    elif types == 4:
                        print('\nchoose your analysis type.\n1.NTUSER.DAT\n2.SYSTEM\n3.SOFTWARE\n4.SAM\ninput num:')
                        ana = input()
                        try:
                            ana = int(ana)
                        except:
                            print('Plz check your input.')
                            continue
                        if ana == 1:
                            print('\nchoose your analysis.\n1.Get info about recent run documents\n2.Get recent file cache info\n3.Get IE visit record\n4.Get MS Office file info\n5.Get userassist info.')
                            file.write('\n# Artifact: Registry - NTUSER.DAT\n')
                            analysis = input()
                            try:
                                analysis = int(analysis)
                            except:
                                print('Plz check your input.')
                                continue
                            if analysis > 5 or analysis == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            if analysis == 1:
                                file.write('\n# Get information about recent run documents\n')
                                file.write('recent_docs = reg_file.Favorite.NTAnalysis.get_recent_docs()\nfor i in recent_docs:\n\tprint(i)\n')
                            elif analysis == 2:
                                file.write('\n# Get recent file cache information\n')
                                file.write('recent_mru = reg_file.Favorite.NTAnalysis.get_recent_MRU()\nfor i in recent_mru:\n\tprint(i)\n')
                            elif analysis == 3:
                                file.write('\n# Get IE visit record\n')
                                file.write(
                                    'visit_record = reg_file.Favorite.NTAnalysis.get_IE_visit()\nfor i in visit_record:\n\tprint(i)\n')
                            elif analysis == 4:
                                file.write('\n# Get MS Office file information\n')
                                file.write('ms_office = reg_file.Favorite.NTAnalysis.get_ms_office()\nfor i in ms_office:\n\tprint(i)\n')
                            elif analysis == 5:
                                print('You can get program list, execution count, execution time, ...')
                                file.write('\n# Get userassist information. [program list, execution count, execution time, ...]\n')
                                file.write('userassit_info = reg_file.get_user_assist()\nfor i in userassit_info:\n\tprint(i)\n')
                        elif ana == 2:
                            print('\nchoose your analysis.\n1.Get Computer basic info about OS\n2.Get usb info\n3.Get Timezone info\n4.Get network info')
                            analysis = input()
                            try:
                                analysis = int(analysis)
                            except:
                                print('Plz check your input.')
                                continue
                            if analysis > 4 or analysis == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            if analysis == 1:
                                print('You can get Domain info, Path, Host Name, Server, ...')
                                file.write('\n# Get Computer basic information about OS. [Domain info, Path, Host Name, Server, ...]\n')
                                file.write('computer_info = reg_file.Favorite.SYSAnalysis.get_computer_info()\nfor i in computer_info:\n\tprint(i)\n')
                            elif analysis == 2:
                                file.write('\n# Get usb information\n')
                                file.write('usb_info = reg_file.Favorite.SYSAnalysis.get_USB()\nfor i in usb_info:\n\tprint(i)\n')
                            elif analysis == 3:
                                file.write('\n# Get timezone information\n')
                                file.write('timezone_info = reg_file.Favorite.SYSAnalysis.get_timezone()\nfor i in timezone_info:\n\tprint(i)\n')
                            elif analysis == 4:
                                file.write('\n# Get network basic information\n')
                                file.write('net_info = reg_file.Favorite.SYSAnalysis.get_network_info()\nfor i in net_info:\n\tprint(i)\n')
                        elif ana == 3:
                            print('\nchoose your analysis.\n1.Get OS info\n2.Get network info')
                            analysis = input()
                            try:
                                analysis = int(analysis)
                            except:
                                print('Plz check your input.')
                                continue
                            if analysis > 2 or analysis == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            elif analysis == 1:
                                file.write('\n# Get basic information of computer OS.\n')
                                file.write('basic_info = reg_file.Favorite.SWAnalysis.get_all_info()\nfor i in basic_info:\n\tprint(i)\n')
                            elif analysis == 2:
                                file.write('\n# Get network card information.\n')
                                file.write('net_info = reg_file.Favorite.SWAnalysis.get_network_info()\nfor i in net_info:\n\tprint(i)\n')
                        elif ana == 4:
                            print('\nchoose your analysis.\n1.Get last login info\n2.Get user name\n3.Get user info')
                            analysis = input()
                            try:
                                analysis = int(analysis)
                            except:
                                print('Plz check your input.')
                                continue
                            if analysis > 3 or analysis == 0 or analysis < -1:
                                print('Plz check your input.')
                                continue
                            if analysis == 1:
                                file.write('\n# Get the information of the last logged in user\n')
                                file.write('last_login = reg_file.Favorite.SAM.last_login()\nfor i in last_login:\n\tprint(i)\n')
                            elif analysis == 2:
                                file.write('\n# Get user basic information\n')
                                file.write('user_name = reg_file.Favorite.SAM.user_name()\nfor i in user_name:\n\tprint(i)\n')
                            elif analysis == 3:
                                file.write('\n# Get user details. [time, user, RID, login info, ...]\n')
                                print('You can get time, user, RID, login info, ...')
                                file.write('user_info = reg_file.Favorite.SAM.user_info()\nfor i in user_info:\n\tprint(i)\n')
                    else:
                        print('plz input num. ex)1')
            elif answer == 5:
                file.write('\n# Artifact: Thumnail or iconcache_##\n')
                file.write("thumbnail = Thumbnail_Iconcache.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Get data of thumnail\n2.Show information\n3.Get info filtering by dimension\n4.Get hash\n-1.finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 4 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Get information of artifact.[file name, hash value, size, system version]\n')
                        print('You can get info of artifact.\n[file name, hash value, size, system version]')
                        file.write('thumbinfo = thumbnail.get_all_info()\nfor i in thumbinfo:\n\tprint(i)\n')
                    elif analysis == 2:
                        file.write('\n# Print information of artifact.\n')
                        print('You can check info but it is not saved in variable.')
                        file.write('thumbnail.show_all_info()\n')
                    elif analysis == 3:
                        print('input your dimension(mxn). input m(type int):')
                        m = input()
                        print('input n(type int):')
                        n = input()
                        file.write('\n# It shows specific width, height file data by this library at once.\n')
                        file.write('thumbnail.dimension('+m+','+n+')\n')
                    elif analysis == 4:
                        file.write('\n# Get hash\n')
                        print('You can check info but it is not saved in variable.')
                        file.write('hash_value = thumbnail.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                    else:
                        print('plz input num. ex)1')
            elif answer == 6:
                file.write('\n# Artifact: zip file\n')
                file.write("zip_file = Files.Zip.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Get all info\n2.Show all info\n3.Extract file\n4.Get hash\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 4 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Get information of zip\n')
                        file.write('zip_info = zip_file.get_all_info()\nfor i in zip_info:\n\tprint(i)\n')
                    elif analysis == 2:
                        file.write('\n# Show information of zip\n')
                        file.write('zip_file.show_all_info()\n')
                    elif analysis == 3:
                        file.write('\n# Extract file\n')
                        file.write('zip_file.extract()\n')
                    elif analysis == 4:
                        file.write('\n# Get hash\n')
                        file.write('hash_value = zip_file.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                    else:
                        print('plz input num. ex)1')
            elif answer == 7:
                print('Input your file type. [1:JPEG, 2:PDF, 3:HWP, 4:MSOld, 5:Get file list of folder]:')
                types = input()
                try:
                    types = int(types)
                except:
                    print('Plz check your input.')
                    continue
                if types > 5 or types < 1:
                    print('Plz check your input.')
                    continue
                if types == 1:
                    file.write('\n# Artifact: JPEG\n')
                    file.write('jpeg = Files.JPEG.file_open(r\''+path+'\')\njpeg_info = jpeg.get_all_info()\nfor i in jpeg_info:\n\tprint(i)\n')
                    file.write('\n# Get Hash Value\n')
                    file.write('hash_value = jpeg.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                elif types == 2:
                    file.write('\n# Artifact: PDF\n')
                    file.write('pdf = Files.PDF.file_open(r\''+path+'\')\npdf_info = pdf.get_all_info()\nfor i in pdf_info:\n\tprint(i)\n')
                    file.write('\n# Get Hash Value\n')
                    file.write('hash_value = pdf_info.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                elif types == 3:
                    file.write('\n# Artifact: HWP\n')
                    file.write('hwp = Files.HWP.file_open(r\''+path+'\')\nhwp_info = hwp.get_all_info()\nfor i in hwp_info:\n\tprint(i)\n')
                    file.write('\n# Get Hash Value\n')
                    file.write('hash_value = hwp_info.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                elif types == 4:
                    file.write('\n# Artifact: MS old\n')
                    file.write('ms = Files.MSOld.file_open(r\''+path+'\')\nms_info = ms.get_all_info()\nfor i in ms_info:\n\tprint(i)\n')
                    file.write('\n# Get Hash Value\n')
                    file.write('hash_value = ms_info.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                elif types == 5:
                    file.write('\n# Print file list\n')
                    file.write("files_analysis.file_list('"+path+"')\n")
            elif answer == 8:
                file.write('\n# Artifact: Browser\n')
                print('Input your Browser type. [1:Chrome, 2:Edge or IE, 3:Firefox]')
                types = input()
                try:
                    types = int(types)
                except:
                    print('Plz check your input.')
                    continue
                if types > 3 or types < 1:
                    print('Plz check your input.')
                    continue
                print('Input your analysis file type. [1:Cookie, 2:History, 3:Download, 4:Cache]')
                ana_type = input()
                try:
                    ana_type = int(ana_type)
                except:
                    print('Plz check your input.')
                    continue
                if ana_type <1 or ana_type >4:
                    print('Plz check your input.')
                    continue
                if types == 1:
                    file.write('browser = Browser.Chrome.')
                elif types == 2:
                    file.write('browser = Browser.Ie_Edge.')
                if types == 3:
                    if ana_type == 4:
                        print('We don\'t support firefox cache now. To be continued...')
                        continue
                    elif ana_type == 1 or ana_type == 2 or ana_type ==3:
                        file.write('browser = Browser.Firefox.')
                if ana_type == 1:
                    file.write('Cookie.file_open(r\''+path+'\')\n')
                elif ana_type == 2:
                    file.write('History.file_open(r\''+path+'\')\n')
                elif ana_type == 3:
                    file.write('Download.file_open(r\''+path+'\')\n')
                elif ana_type == 4:
                    file.write('Cache.file_open(r\''+path+'\')\n')
                while True:
                    print('\nchoose your analysis. \n1.Get all info\n2.Get hash value\n3.Show all info\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 3 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('browser_info = browser.get_all_info()\nfor i in browser_info:\n\tprint(i)\n')
                        if ana_type == 1:
                            while True:
                                print('choose aditional function?\n1.Keyword search\n2.Count sorting\n-1.None')
                                add_func = input()
                                try:
                                    add_func = int(add_func)
                                except:
                                    print('Plz check your input.')
                                    continue
                                if add_func > 2 or add_func == 0 or add_func < -1:
                                    print('Plz check your input.')
                                    continue
                                if add_func == 1:
                                    print('input keyword:')
                                    keyword = input()
                                    file.write('\n# Get information searched by '+keyword+'.\n')
                                    file.write('search_info = browser.keyword_search(\''+keyword+'\')\nfor i in search_info:\n\tprint(i)\n')
                                elif add_func == 2:
                                    file.write('\n# Get information cnt sorted\n')
                                    file.write('cnt_sort = browser.cnt_sort()\nfor i in cnt_sort:\n\tprint(i)\n')
                                elif add_func == -1:
                                    break
                    elif analysis == 2:
                        file.write('\n# Get hash value\n')
                        file.write('hash_value = browser.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Show all information\n')
                        file.write('browser.show_all_info()\n')
            elif answer == 9:
                file.write('\n# Artifact: Recycle\n')
                file.write("recycle = Recycle.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Show all info\n2.Get all info\n3.Get hash\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 3 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Show all information\n')
                        file.write('recycle.show_all_info()\n')
                    elif analysis == 2:
                        file.write('\n# Get all information\n')
                        file.write('recycle_info = recycle.get_all_info()\nfor i in recycle_info:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Get hash value\n')
                        file.write('hash_value = recycle.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
            elif answer == 10:
                file.write('\n# Artifact: Iconcache\n')
                file.write("icon_cache = Iconcache.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Show all info\n2.Get all info\n3.Get hash\n4.File extension filtering\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 4 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Show all information\n')
                        file.write('icon_cache.show_all_info()\n')
                    elif analysis == 2:
                        file.write('\n# Get all information\n')
                        file.write('icon_cache_info = icon_cache.get_all_info()\nfor i in icon_cache_info:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Get hash\n')
                        file.write('hash_value = icon_cache.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
                    elif analysis == 4:
                        print('Input extension:')
                        extension = input()
                        file.write('\n# Allows you to find '+extension+' file from all sections.\n')
                        file.write('icon_cache.extension_filter(\''+extension+'\')\n')
            elif answer == 11:
                file.write('\n# Artifact: LNK\n')
                file.write("lnk = Lnk.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis. \n1.Show all info\n2.Get all info\n3.Get one value\n4.Get hash\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 4 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Show all information\n')
                        file.write('lnk.show_all_info()\n')
                    elif analysis == 2:
                        file.write('\n# Get all information\n')
                        file.write('lnk_info = lnk.get_all_info()\nfor i in lnk_info:\n\tprint(i)\n')
                    elif analysis == 3:
                        file.write('\n# Get information of specific value.\n# [1.creation time 2.file attribute 3.access time 4.modification time 5.lnk_access time 6.file size 7.icon_idex 8.show_command 9.volume info\n'
                              '# 10.localbase path 11.netbios 12.machine id 13.lnk creation time 14. lnk modification time]\n')
                        file.write('parse_value = lnk.')
                        print('choose your value: \n1.creation time 2.file attribute 3.access time 4.modification time 5.lnk_access time 6.file size 7.icon_idex 8.show_command 9.volume info\n'
                              '10.localbase path 11.netbios 12.machine id 13.lnk creation time 14. lnk modification time\n input num: ')
                        category = input()
                        try:
                            category = int(category)
                        except:
                            print('Plz check your input.')
                            continue
                        if category > 14 or category == 0 or category < -1:
                            print('Plz check your input.')
                            continue
                        if category == 1:
                            file.write('creation_time()')
                        elif category == 2:
                            file.write('file_atribute()')
                        elif category == 3:
                            file.write('access_time()')
                        elif category == 4:
                            file.write('write_time()')
                        elif category == 5:
                            file.write('lnk_access_tim()')
                        elif category == 6:
                            file.write('file_size()')
                        elif category == 7:
                            file.write('icon_idex()')
                        elif category == 8:
                            file.write('show_command()')
                        elif category == 9:
                            print("You can get Drive Serial Num, Volume Label")
                            file.write('volume()')
                        elif category == 10:
                            file.write('localbase_path()')
                        elif category == 11:
                            file.write('netbios()')
                        elif category == 12:
                            file.write('machine_id()')
                        elif category == 13:
                            file.write('lnk_creation_time()')
                        elif category == 14:
                            file.write('lnk_write_time()')
                        file.write('\nfor i in parse_value:\n\tprint(i)\n')
                    elif analysis ==4:
                        file.write('\n# Get hash\n')
                        file.write('hash_value = lnk.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
            elif answer == 12:
                file.write('\n# Artifact: Prefetch\n')
                file.write("prefetch = Prefetch.file_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis.\n1.Show all info\n2.Get all info\n3.File extension filtering\n4.Get hash\n-1:finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 4 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        file.write('\n# Show all information\n')
                        file.write('prefetch.show_all_info()\n')
                    elif analysis == 2:
                        file.write('\n# Get all information\n')
                        file.write('prefetch_info = prefetch.get_all_info()\nfor i in prefetch_info:\n\tprint(i)\n')
                    elif analysis == 3:
                        print('Input extension:')
                        extension = input()
                        file.write('\n# Allows you to find ' + extension + ' file from all sections.\n')
                        file.write('filter_info = prefetch.extension_filter_pf(\'' + extension + '\')\nfor i in filter_info:\n\tprint(i)\n')
                    elif analysis == 4:
                        file.write('\n# Get hash\n')
                        file.write('hash_value = prefetch.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
            elif answer == 13:
                file.write('\n# Artifact: Disk Image\n')
                file.write("disk_image = Disk.disk_open(r'" + path + "')\n")
                while True:
                    print('\nchoose your analysis.\n1.Analysis\n2.File Collect\n-1.finish\ninput num: ')
                    analysis = input()
                    try:
                        analysis = int(analysis)
                    except:
                        print('Plz check your input.')
                        continue
                    if analysis > 2 or analysis == 0 or analysis < -1:
                        print('Plz check your input.')
                        continue
                    if analysis == -1:
                        break
                    elif analysis == 1:
                        print('choose type of metadata.[1:e01 2:volume\ninput:')
                        types = input()
                        try:
                            types = int(types)
                        except:
                            print('Plz check your input.')
                            continue
                        if types is not 1 and types is not 2:
                            print('Plz check your input.')
                            continue
                        if types == 1:
                            file.write('\n# Get metadata from e01 disk\n')
                            file.write("e01_meta = disk_image.e01_metadata()\nfor i in e01_meta:\n\tprint(i)\n")
                        elif types == 2:
                            file.write('\n# Get metadata from volume\n')
                            file.write("volume = file.volume_metadata()\nfor i in volume:\n\tprint(i)\n")
                    elif analysis == 2:
                        print('1. You should check volume partition information before collecting files.\n2. You must enter the partition start sector you want to analyze.')
                        file.write("start_sector = []\nfor i in disk_image.volume_metadata():\n\tstart_sector.append(i[\"Start Sector\"])\n")
                        file.write("for i in start_sector:\n\tfile_list=file.get_path(\".\",i)")
                        file.write("# you need to input your information in file_extract()")
                        print('you need to put your information in file_extract() yourself.')
                        file.write("extract_files = file.file_extract()")
        file.close()
