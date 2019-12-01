from fortools import Disk

file = Disk.disk_open(r"D:\새 폴더 (3)\Adam Ferrante - Laptop-Deadbox\Horcrux\Horcrux.E01")
'''
Precautions
1. You should check volume partition information before collecting files.
2. You must enter the partition start sector you want to analyze.
'''

############ File Collect ###############
# 1. Navigate File Locations in Disk Images (get_path (find_path - start is ., partition start sector))
rel = file.get_path("./Windows/System32/config", 1126400)
# # 2. Extract files based on the information you collect
# extract_SOFTWARE = file.file_extract(1126400, "./Windows/System32/config/SOFTWARE", "extrct_SOFTWARE")
# extract_SAM = file.file_extract(1126400, "./Windows/System32/config/SAM", "extract_SAM")
# # 3. File system log extraction
# file.fslog_extract()
# 
# ############ File Analysis ###############
# # 1. Output basic metadata of the DD.
# rel = file.dd_metadata()
# # 2. Output basic metadata of the E01.
# rel = file.e01_metadata()
# # 3. Print volume partition information.
# rel = file.volume_metadata()

for i in range(len(rel)):
    print(rel[i])

