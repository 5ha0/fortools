from fortools import Disk

file = Disk.disk_open(r"..\dataset\disk\cfreds_2015_data_leakage_pc.E01")

# # disk file info
# rel = file.e01_metadata()
#
# # partition info
# rel = file.volume_metadata()

# get_path (find_path - start is ., partition start sector)
# You can find partition start sector in volume_metadata

rel = file.get_path(".", 2048)

## extract filesystemlog
#rel = file.fslog_extract()

for i in range(len(rel)):
    print(rel[i])
