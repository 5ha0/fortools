import pytsk3
import pyewf
import json
import datetime

class E01Analysis:
    def __init__(self, file):
        self.file = file
        self.ret_list = list()
        self.partition_list = list()
        self.img_info = EWFImgInfo(self.file)
        self.vol = pytsk3.Volume_Info(self.img_info)

    def get_path(self, path, length):
        for partition in self.vol:
            self.partition_list.append(partition.start)

        print("please input argument partition start sector : ", self.partition_list)

        fs = self.open_fs(length)
        f = fs.open_dir(path)
        ret_list = list()
        for i in f:
            file_type = str(i.info.name.type)
            if file_type == "TSK_FS_NAME_TYPE_REG":
                file_type = "file"
            elif file_type == "TSK_FS_NAME_TYPE_DIR":
                file_type = "directory"
            else:
                file_type = str(i.info.name.type)
            f_path_obj = {
                "file_name": i.info.name.name.decode(),
                "file_type": file_type
            }
            ret_list.append(f_path_obj)
        return ret_list

    def __UsnJrnl_extract(self, filename):
        fs = self.open_fs()
        f = fs.open(filename)
        found = False

        for attr in f:
            if attr.info.name == b'$J':
                print("[+] Success Extract : $J")
                found = True
                break
        if not found:
            print("[-] $J is not found")

        with open('$J', 'wb') as o:
            offset = 0
            size = attr.info.size
            buf = f.read_random(offset, f.info.meta.size, attr.info.type, attr.info.id)
            o.write(buf)

    def __mft_log_extract(self, filename, output_name):
        fs = self.open_fs()
        f = fs.open(filename)
        # for attr in f:
        #     print(attr.info.type)
        with open(output_name, 'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

    def file_extract(self, length, filepath, output_name):
        fs = self.open_fs(length)
        f = fs.open(filepath)
        for attr in f:
            print(attr.info.type)
        with open(output_name, 'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

    def fslog_extract(self):
        mft_list = self.__mft_log_extract('/$MFT', '$MFT')
        log_list = self.__mft_log_extract('/$LogFile', '$LogFile')
        UsnJrnl = self.__UsnJrnl_extract('/$Extend/$UsnJrnl')

    def open_fs(self, length):
        if self.vol is not None:
            for part in self.vol:
                if part.len > length and "Unallocated" not in part.desc.decode() \
                        and "Extended" not in part.desc.decode() \
                        and "Primary Table" not in part.desc.decode():
                    try:
                        fs = pytsk3.FS_Info(self.img_info, offset=part.start*self.vol.info.block_size)
                        return fs
                    except:
                        print("[-] Unable to open FS")
        else:
            pass

    def e01_metadata(self):
        head_obj = dict()
        hash_obj = dict()

        e01_list = list()

        headers = self.file.get_header_values()
        hashes  = self.file.get_hash_values()

        for head in headers:
            if head == "acquiry_date" or head == "system_date":
                timestamp = datetime.datetime.strptime(headers[head], "%a %b %d %H:%M:%S %Y")
                head_obj[head] = str(timestamp)
            else:
                head_obj[head] = headers[head]

        for h in hashes:
            hash_obj[h] = hashes[h]

        e01_obj = {
            "Bytes per Sector" : self.file.bytes_per_sector,
            "Number of Sector" : self.file.get_number_of_sectors(),
            "Total Size" : self.file.get_media_size()
        }

        head_obj.update(e01_obj)
        head_obj.update(hash_obj)
        e01_list.append(head_obj)

        self.ret_list = e01_list

        return self.ret_list

    def volume_metadata(self):
        for partition in self.vol:
            e01_obj = {
                "Type": partition.desc.decode(),
                "Num": partition.addr,
                "Start Sector": partition.start,
                "Total Sector": partition.len,
                "Size" : str((partition.len*512)/1024**2)+"MB"
            }
            self.ret_list.append(e01_obj)
        return self.ret_list

    # def extract_file(self, output_path, file_extension):
    #     self.__open

    # def __open_fs(self.vol, self.file, )


class EWFImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EWFImgInfo, self).__init__(url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)
        
    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)
    
    def get_size(self):
        return self._ewf_handle.get_media_size()


class DDAnalysis:
    def __init__(self, file):
        self.file = file

    def __mft_log_extract(self, filename, output_name):
        fs = pytsk3.FS_Info(self.file)
        f = fs.open(filename)
        for attr in f:
            print(attr.info.type)
        with open(output_name, 'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

    def __UsnJrnl_extract(self, filename):
        fs = pytsk3.FS_Info(self.file)
        f = fs.open(filename)
        found = False

        for attr in f:
            if attr.info.name == '$J':
                found = True
                break
        if not found:
            print("[-] $J is not found")

        with open('$UsnJrnl', 'wb') as o:
            offset = 0
            size = attr.info.size
            buf = f.read_random(offset, f.info.meta.size, attr.info.type, attr.info.id)
            o.write(buf)

    def dd_metadata(self):
        head_obj = dict()
        hash_obj = dict()
    
        dd_list = list()

        headers = self.file.get_header_values()
        hashes  = self.file.get_hash_values()

        for head in headers:
            if head == "acquiry_date" or head == "system_date":
                timestamp = datetime.datetime.strptime(headers[head], "%a %b %d %H:%M:%S %Y")
                head_obj[head] = str(timestamp)
            else:
                head_obj[head] = headers[head]

        for h in hashes:
            hash_obj[h] = hashes[h]

        dd_obj = {
            "Bytes per Sector" : self.file.bytes_per_sector,
            "Number of Sector" : self.file.get_number_of_sectors(),
            "Total Size" : self.file.get_media_size()
        }

        head_obj.update(dd_obj)
        head_obj.update(hash_obj)
        dd_list.append(head_obj)
        
        self.ret_list = dd_list

        return self.ret_list

    def fslog_extract(self):
        mft_list = self.__mft_log_extract('/$MFT', '$MFT')
        log_list = self.__mft_log_extract('/$LogFile', '$LogFile')
        UsnJrnl = self.__UsnJrnl_extract('/$Extend/$UsnJrnl')

    def file_extract(self, filepath, output_name):
        fs = pytsk3.FS_Info(self.file)
        f = fs.open(filepath)
        for attr in f:
            print(attr.info.type)
        with open(output_name, 'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

    def volume_metadata(self):
        p_table = pytsk3.Volume_Info(self.file)
        dd_list = list()
        count = 0
        for partition in p_table:
            dd_obj = {
                "Type": partition.desc.decode(),
                "Num": partition.addr,
                "Start Sector": partition.start,
                "Sector Count": partition.len
            }
            print(json.dumps(dd_obj))

    def get_path(self, path):
        fs = pytsk3.FS_Info(self.file)
        f = fs.open_dir(path)
        ret_list = list()
        for i in f:
            file_type = str(i.info.name.type)
            if file_type == "TSK_FS_NAME_TYPE_REG":
                file_type = "file"
            elif file_type == "TSK_FS_NAME_TYPE_DIR":
                file_type = "directory"
            else:
                file_type = str(i.info.name.type)
            f_path_obj = {
                "file_name" : i.info.name.name.decode(),
                "file_type" : file_type
            }
            ret_list.append(f_path_obj)
        return ret_list



    

