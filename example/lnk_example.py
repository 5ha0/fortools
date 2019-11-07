from fortools import *

file = Lnk.file_open('path')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show information from shell-link-header
link_attribute = file.file_attribute()
print(str(link_attribute))
c_time = file.creation_time()
print(str(c_time))
a_time = file.access_time()
print(str(a_time))
w_time = file.write_time()
size = file.file_size()
iconindex = file.iconindex()
showcommand = file.show_command()
print(str(showcommand))
# show information from link-info
volume_information = file.volume()
print('dd'+str(volume_information))
localbasepath_information = file.localbase_path()
print('ssd'+str(localbasepath_information))
# show information from extra-data
netbios = file.netbios()
print(str(netbios))
machineid_information = file.machine_id()
print(str(machineid_information))

# show information from show_all_info()
result = file.show_all_info()
