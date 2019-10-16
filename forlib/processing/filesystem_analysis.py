import pytsk3 
import json
class DDAnalysis:
    def __init__(self, file):
        self.file = file

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

    def extract(self):
        fs = pytsk3.FS_Info(self.file)
        print(fs)
        f = fs.open("/users/ann/NTUSER.DAT")
        with open('NTUSER.DAT', "w") as file_w:
            buf = f.read_random(0, f.info.meta_size)
            file_w.write(buf)