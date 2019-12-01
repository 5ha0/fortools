from fortools import *

reg_file = RegistryHive.file_open(r"..\dataset\cfreds_reg\NTUSER.DAT")

# ##################### NTUSER.DAT ###########################
# # 1. Find the key information you want
# info = reg_file.find_key("Microsoft")
# # 2. Bring up a list of recently run documents.
# info = reg_file.get_recent_docs()
# # 3. Check the MRU cache information.
# info = reg_file.get_recent_MRU()
# # 4. Check the MS document and outlook information you ran.
# info = reg_file.get_ms_office()
# # 5. Get information such as the number of times and time of recently executed files.
# info = reg_file.get_userassist()

reg_file = RegistryHive.file_open(r"..\dataset\cfreds_reg\SYSTEM")

# ##################### SYSTEM ###########################
# # 1. Find the key information you want
# info = reg_file.find_key("Microsoft")
# # 2. Get computer basic information.
# info = reg_file.get_computer_info()
# # 3. Get the USB trace and show it.
# info = reg_file.get_USB()
# # 4. Get the set time zone value.
# info = reg_file.get_timezone()
# # 5. Recall network basic information.
# info = reg_file.get_network_info()

reg_file = RegistryHive.file_open(r"..\dataset\cfreds_reg\SOFTWARE")
# ##################### SOFTWARE ###########################
# # 1. Find the key information you want
# info = reg_file.find_key("Microsoft")
# # 2. Get basic information of computer OS.
# info = reg_file.get_info()
# # 3. Get network card information.
# info = reg_file.get_network_info()

reg_file = RegistryHive.file_open(r"..\dataset\cfreds_reg\SAM")
# ##################### SAM ###########################
# # 1. Find the key information you want
# info = reg_file.find_key("Microsoft")
# # 2. Get the information of the last logged in user.
# info = reg_file.last_login()
# # 3. Get user basic information.
# info = reg_file.user_info()
# # 4. Get user details.
# info = reg_file.user_info()

for i in range(len(info)):
    print(info[i])
