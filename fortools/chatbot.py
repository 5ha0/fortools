class Chatbot():
    def __init__(self):
        print('input your script name')
        name = input()

        file = open(r'.\\' + name+'.py' , 'w')
        file.write('from fortools import *\n\n')

        print('input your artifact path')
        path = input()

        print('what is your atrifact? \n1.event log 2.JumpList 3.FileSystem Log 4.Registry 5.Thumbnail\n'
              '6.Zip 7.Files 8.Browser 9.Recycle 10.IconCache 11.Lnk 12.Disk Image')
        answer = int(input())

        if answer == 1:
            file.write('event = EventLog.file_open(r\''+path+'\')\n')
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
                 elif analysis == 10:
                    print('Put event log idx what you want to see. Input: ')
                    idx = input()
                    file.write('xml_info = log_file.xml_with_num('+idx+')\nfor i in xml_info:\n\tprint(i)')
                else:
                    print('plz input num. ex)1')
        elif answer == 2:
            file.write("jumplist = JumpList.file_open(r'" + path + "')\n")
            print('choose your analysis. \n1.Get summary info from destlist\n2.Get destlist data list\n3.Get information from streams except destlist\n4.Print info from streams\n5.Get hash\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    print('What is your window version? input [7, 10]: ')
                    ver = int(input())
                    if ver == 7:
                        file.write('summary = jumplist.get_summary(7)\nfor i in summary:\n\tprint(i)\n')
                    elif ver == 10:
                        file.write('summary = jumplist.get_summary(10)\nfor i in summary:\n\tprint(i)\n')
                elif analysis == 2:
                    print('What is your window version? input [7, 10]: ')
                    ver = int(input())
                    if ver == 7:
                        file.write('dest_list = jumplist.get_destlist_data(7)\nfor i in dest_list:\n\tprint(i)\n')
                    elif ver == 10:
                        file.write('dest_list = jumplist.get_destlist_data(10)\nfor i in dest_list:\n\tprint(i)\n')
                elif analysis == 3:
                    file.write('info_list = jumplist.get_info\nfor i in info_list:\n\tprint(i)\n')
                elif analysis == 4:
                    file.write('jumplist.show_info()\n')
                elif analysis == 5:
                    file.write('jump_hash = jumplist.get_hash()\nfor i in jump_hash:\n\tprint(i)\n')
        elif answer == 3:
            file.write("filesys_log = FileSystemLog.file_open(r'" + path + "')\n")
            print('choose your analysis. \n1.Get all info\n2.Get hash\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('file_syslog_info = jfilesys_log.get_info()\nfor i in file_syslog_info:\n\tprint(i)\n')
                elif analysis == 5:
                    file.write('file_syslog_hash = filesys_log.get_hash()\nfor i in file_syslog_hash:\n\tprint(i)\n')
        elif answer == 4:
            file.write("reg_file = RegistryHive.file_open(r'" + path + "')\n")
            print('choose your analysis. \n1.Find Key\n2.Get info about recent run documents\n3.Get recent file cache info\n'
                  '4.Get MS Office file info\n5.Get userassist info\n6.Get Computer basic info about OS\n7.Get usb info\n'
                  '8.Get Timezone info\n9.Get network info\n10.Get computer info about tcpip service\n11.Get last login info\n12.Get user name\n'
                  '13.Get user info\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    print('input your key: ')
                    key_input = input()
                    file.write('key_value = reg_file.find_key(\''+key_input+'\')')
                elif analysis == 2:
                    file.write('recent_docs = reg_file.get_recent_docs()\nfor i in recent_docs:\n\tprint(i)\n')
                elif analysis == 3:
                    file.write('recent_mru = reg_file.get_recent_MRU()\nfor i in recent_mru:\n\tprint(i)\n')
                elif analysis == 4:
                    file.write('ms_office = reg_file.get_ms_office()\nfor i in ms_office:\n\tprint(i)\n')
                elif analysis == 5:
                    print('You can get program list, execution count, execution time, ...')
                    file.write('userassit_info = reg_file.get_user_assist()\nfor i in userassit_info:\n\tprint(i)\n')
                elif analysis == 6:
                    print('You can get Domain info, Path, Host Name, Server, ...')
                    file.write('computer_info = reg_file.get_user_info()\nfor i in computer_info:\n\tprint(i)\n')
                elif analysis == 7:
                    file.write('usb_info = reg_file.get_USB()\nfor i in usb_info:\n\tprint(i)\n')
                elif analysis == 8:
                    file.write('timezone_info = reg_file.get_timezone()\nfor i in timezone_info:\n\tprint(i)\n')
                elif analysis == 9:
                    file.write('net_info = reg_file.get_network_info()\nfor i in net_info:\n\tprint(i)\n')
                elif analysis == 10:
                    file.write('basic_info = reg_file.get_info()\nfor i in basic_info:\n\tprint(i)\n')
                elif analysis == 11:
                    file.write('last_login = reg_file.last_login()\nfor i in last_login:\n\tprint(i)\n')
                elif analysis == 12:
                    file.write('user_name = reg_file.user_name()\nfor i in user_name:\n\tprint(i)\n')
                elif analysis == 13:
                    print('You can get time, user, RID, login info, ...')
                    file.write('user_info = reg_file.user_info()\nfor i in user_info:\n\tprint(i)\n')
        elif answer == 5:
            file.write("thumbnail = Thumbnail_Iconcache.file_open(r'" + path + "')\n")
            print('choose your analysis. \n1.Get data of thumnail\n2.Show information\n3.Get info filtering by dimension')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    print('You can get info of thumbnail.\n[file name, hash value, size, system version]')
                    file.write('thumbinfo = thumbnail.get_data()\nfor i in thumbinfo:\n\tprint(i)\n')
                elif analysis == 2:
                    print('You can check info but it is not saved in variable.')
                    file.write('thumbnail.thumb_print()\n')
                elif analysis == 3:
                    print('input your dimension(mxn). input m(type int):')
                    m = input()
                    print('input n(type int):')
                    n = input()
                    file.write('thumbnail.dimension('+m+','+n+')\n')
        elif answer == 6:
            file.write("zip_file = Files.Zip.file_open(r'" + path + "')\n")
            print(
                'choose your analysis. \n1.Get info\n2.Show info\n3.Get last modification time\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('zip_info = zip_file.get_info()\nfor i in zip_info:\n\tprint(i)\n')
                elif analysis == 2:
                    file.write('zip_file.show_info()\n')
        elif answer == 7:
            print('Input your file type. [1:JPEG, 2:PDF, 3:HWP, 4:MSOld, 5:Get file list of folder]')
            types = int(input())
            if types == 1:
                file.write('jpeg = Files.JPEG.file_open(r\''+path+'\')\njpeg_info = jpeg.get_info\nfor i in jpeg_info:\n\tprint(i)\n')
            elif types == 2:
                file.write('pdf = Files.PDF.file_open(r\''+path+'\')\npdf_info = pdf.get_info\nfor i in pdf_info:\n\tprint(i)\n')
            elif types == 3:
                file.write('hwp = Files.HWP.file_open(r\''+path+'\')\nhwp_info = hwp.get_info\nfor i in hwp_info:\n\tprint(i)\n')
            elif types == 4:
                file.write('ms = Files.MSOld.file_open(r\''+path+'\')\nms_info = ms.get_info\nfor i in ms_info:\n\tprint(i)\n')
            elif types == 5:
                file.write("files_analysis.file_list('"+path+"')\n")
        elif answer == 8:
            print('Input your Browser type. [1:Chrome, 2:Edge or IE]')
            types = int(input())
            print('Input your analysis file type. [1:Cookie, 2:History, 3:Download, 4:Cache]')
            ana_type = int(input())
            if types == 1:
                file.write('browser = Browser.Chrome.')
            elif types == 2:
                file.write('browser = Browser.Ie_Edge.')
            if ana_type == 1:
                file.write('Cookies.file_open(r\''+path+'\')\n')
            elif ana_type == 2:
                file.write('History.file_open(r\''+path+'\')\n')
            elif ana_type == 3:
                file.write('Download.file_open(r\''+path+'\')\n')
            elif ana_type == 4:
                file.write('Cache.file_open(r\''+path+'\')\n')
            print('choose your analysis. \n1.Get info\n2.Get hash value\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('browser_info = browser.get_info()\nfor i in browser_info:\n\tprint(i)\n')
                elif analysis == 2:
                    file.write('hash_value = browser.get_hash()\nfor i in hash_value:\n\tprint(i)\n')
        elif answer == 9:
            file.write("recycle = Recycle.file_open(r'" + path + "')\n")
            print(
                'choose your analysis. \n1.Show all info\n2.Get all info\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('recycle.show_all_info()\n')
                elif analysis == 2:
                    file.write('recycle_info = recycle.get_all_info()\nfor i in recycle_info:\n\tprint(i)\n')
        elif answer == 10:
            file.write("icon_cache = Iconcache.file_open(r'" + path + "')\n")
            print('choose your analysis. \n1.Show all info\n2.Get all\n3.Extension Filtering\n4. info\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('icon_cache.show_all_info()\n')
                elif analysis == 2:
                    file.write('icon_cache_info = icon_cache.get_all_info()\nfor i in icon_cache_info:\n\tprint(i)\n')
        elif answer == 11:
            file.write("lnk = Lnk.file_open(r'" + path + "')\n")
            print(
                'choose your analysis. \n1.Show all info\n2.Get all info\n3.Get one value\n-1:finish')
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    file.write('lnk.show_all_info()\n')
                elif analysis == 2:
                    file.write('lnk_info = lnk.get_all_info()\nfor i in lnk_info:\n\tprint(i)\n')
                elif analysis == 3:
                    file.write('parse_value = lnk.')
                    print('choose your value: \n1.creation time 2.file attribute 3.access time 4.modification time 5.lnk_access time 6.file size 7.icon_idex 8.show_command 9.volume info\n'
                          '10.localbase path 11.netbios 12.machine id 13.lnk creation time 14. lnk modification time\n input num: ')
                    category = int(input())
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
        elif answer == 12:
            file.write("disk_image = Disk.disk_open(r'" + path + "')\n")
            print('1. You should check volume partition information before collecting files.\n2. You must enter the partition start sector you want to analyze.')
            print('choose your analysis. \n1.File Collect\n2.File Analysis\n-1:finish')
            file.write("start_sector = disk_image.volume_metadata()\n")
            while True:
                print('\ninput num: ')
                analysis = int(input())
                if analysis == -1:
                    break
                elif analysis == 1:
                    print('Input your file . If you want to find path -start is .,cpartition start sector')
                    file.write('\n')
                elif analysis == 2:
                    file.write('lnk_info = lnk.get_all_info()\nfor i in lnk_info:\n\tprint(i)\n')
                elif analysis == 3:
                    file.write('parse_value = lnk.')
                    print(
                        'choose your value: \n1.creation time 2.file attribute 3.access time 4.modification time 5.lnk_access time 6.file size 7.icon_idex 8.show_command 9.volume info\n'
                        '10.localbase path 11.netbios 12.machine id 13.lnk creation time 14. lnk modification time\n input num: ')
                    category = int(input())
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
        file.close()
