from fortools import *

file = Lnk.file_open(r'path')
# Or you ca use this
# path = 'path'
# file = file_open(path)

# show information from shell-link-header
link_attribute = file.file_attribute()
print(str(link_attribute))
c_time = file.creation_time()
file.lnk_creation_time()
file.lnk_access_time()
file.lnk_write_time()
size = file.file_size()
iconindex = file.iconindex()
showcommand = file.show_command()

# show information from link-info
volume_information = file.volume()
localbasepath_information = file.localbase_path()

# show information from extra-data
netbios = file.netbios()
machineid_information = file.machine_id()

# show information from show_all_info()
result = file.show_all_info()
