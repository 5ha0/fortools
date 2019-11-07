from fortools import *

file = Lnk.file_open('path')

# show information from shell-link-header
link_attribute = file.file_attribute()
c_time = file.creation_time()
a_time = file.access_time()
w_time = file.write_time()
size = file.file_size()
iconindex = file.iconindex()
showcommand = file.show_command()
# show information from link-info
volume_information = file.volume()
localbasepath_information = file.localbase_path()
# show information from extra-data
netbios = file.netbios()
machineid_information = file.machine_id()