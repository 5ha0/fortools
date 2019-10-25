import pytsk3 
import json

class DDAnalysis:
    def __init__(self, file):
        self.file = file

    def __mft_log_extract(self, filename, output_name):
        fs = pytsk3.FS_Info(self.file)
        f  = fs.open(filename)
        for attr in f:
            print(attr.info.type)
        with open(output_name,'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

#     def __UsnJrnl_extract(self, filename):
#         fs = pytsk3.FS_Info(self.file)
#         f  = fs.open(filename)
#         found=False

#         for attr in f:
#             if attr.info.name == '$J':
#                 found=True
#                 break
#         if not found:
#             print("[-] $J is not found")

        with open('$UsnJrnl','wb') as o:
            offset=0
            size=attr.info.size
            buf=f.read_random(offset,f.info.meta.size,attr.info.type,attr.info.id)
            o.write(buf)


    def fslog_extract(self):
        mft_list = self.__mft_log_extract('/$MFT','$MFT')
        log_list = self.__mft_log_extract('/$LogFile', '$LogFile')
#         UsnJrnl = self.__UsnJrnl_extract('/$Extend/$UsnJrnl')


    
'''
    def get_info(self):
        p_table = pytsk3.Volume_Info(self.file)
        dd_list = list()
        count = 0
        for partition in p_table:
            dd_obj = {
                "Type" : partition.desc.decode(),
                "Num" : partition.addr,
                "Start Sector" : partition.start,
                "Sector Count" : partition.len
            }
            print(json.dumps(dd_obj))
'''
