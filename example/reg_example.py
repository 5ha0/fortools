from fortools import *

################################ Common Function ##################################
reg_file1 = RegistryHive.file_open("D:\\cfreds_reg\\NTUSER.DAT")
reg_file2 = RegistryHive.file_open("D:\\cfreds_reg\\SYSTEM")
reg_file3 = RegistryHive.file_open("D:\\cfreds_reg\\SOFTWARE")
reg_file4 = RegistryHive.file_open("D:\\cfreds_reg\\SAM")

# # 1. File Path -- if you find key, If you want to find the key, enter the value that goes into the key path.
# # ex) Find Path : Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU --> input : reg_file.find_key("MRU")

info = reg_file1.find_key("MRU")
# info = reg_file2.find_key("Microsoft")
# info = reg_file3.find_key("CurrentVersion")
# info = reg_file4.find_key("User")

# # 2. Key Value
info = reg_file1.find_value("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU")
# info = reg_file2.find_value("ControlSet002\\services\\eventlog\\OAlerts\\Microsoft Office 15 Alerts")
# info = reg_file3.find_value("Microsoft\\Windows NT\\CurrentVersion")
# info = reg_file4.find_value("SAM\\Domains\\Account\\Users\\Names\\informant")
#
# # 3. get
# info = reg_file1.get_hash()
# info = reg_file2.get_hash()
# info = reg_file3.get_hash()
# info = reg_file4.get_hash()

################################ Favorite #####################################

# ------------------- NTUSER.DAT ------------------------------------------
# # 1. Bring up a list of recently run documents.
# info = reg_file1.Favorite.NTUSER.get_recent_docs()
# # 2. Check the MRU cache information.
# info = reg_file1.Favorite.NTUSER.get_recent_MRU()
# # 3. Check the MS document and outlook information you ran.
# info = reg_file1.Favorite.NTUSER.get_ms_office()
# # 4. Get information such as the number of times and time of recently executed files.
# info = reg_file1.Favorite.NTUSER.get_userassist()
# # 5. Get Hwp file information
# info = reg_file1.Favorite.NTUSER.get_HWP()
# # 6. Check url accessed from IE
# info = reg_file1.Favorite.NTUSER.get_IE_visit()

# ---------------------SYSTEM -------------------------------------------
# # 1. Get computer basic information.
# info = reg_file2.Favorite.SYSTEM.get_computer_info()
# # 2. Get the USB trace and show it.
# info = reg_file2.Favorite.SYSTEM.get_USB()
# # 3. Get the set time zone value.
# info = reg_file2.Favorite.SYSTEM.get_timezone()
# # 4. Recall network basic information.
# info = reg_file2.Favorite.SYSTEM.get_network_info()

# --------------------- SOFTWARE ---------------------
# # 1. Get basic information of computer OS.
# info = reg_file3.Favorite.SOFTWARE.get_info()
# # 2. Get network card information.
# info = reg_file3.Favorite.SOFTWARE.get_network_info()

# --------------------- SAM ---------------------
# # 1. Get the information of the last logged in user.
# info = reg_file4.Favorite.SAM.last_login()
# # 2. Get user basic information.
# info = reg_file4.Favorite.SAM.user_name()
# # 3. Get user details.
# info = reg_file4.Favorite.SAM.user_info()

for i in info:
    print(i)
