import pytsk3
import pyewf
import time
from datetime import datetime, timedelta
from forlib.processing.convert_time import convert_replace_time as r_time
import forlib.calc_hash as calc_hash


class E01Analysis:
    def __init__(self, file, path, hash_val):
        self.__file = file
        self.__partition_list = list()
        self.__img_info = EWFImgInfo(self.__file)
        self.__vol = pytsk3.Volume_Info(self.__img_info)
        self.__path = path
        self.__hash_val = [hash_val]
        self.__cal_hash()

    def __cal_time(self, int_time):
        date = datetime.utcfromtimestamp(int_time)
        # date = date.strftime("%Y-%m-%d %H:%M:%S")
        return date
    
    def get_path(self, path, length):
        ret_list = list()
        partition_list = list()
        for partition in self.__vol:
            partition_list.append(partition.start)

        print("please input argument partition start sector : ", partition_list)

        try:
            fs = self.open_fs(length)
        except:
            print("[-] Plz Check Disk Area")

        try:
            f = fs.open_dir(path)
            for i in f:
                file_type = str(i.info.name.type)
                if file_type == "TSK_FS_NAME_TYPE_REG":
                    file_type = "FILE"
                elif file_type == "TSK_FS_NAME_TYPE_DIR":
                    file_type = "DIR"
                else:
                    file_type = str(i.info.name.type)

                if i.info.meta is None:
                    f_path_obj = {
                        "file_name": i.info.name.name.decode(),
                        "file_type": file_type,
                        "Type": "Delete",
                        "size": "None",
                        "TimeZone" : "None",
                        "ctime": "None",
                        "mtime": "None",
                        "atime": "None",
                        "change time": "None"
                    }
                    ret_list.append(f_path_obj)
                else:
                    f_path_obj = {
                        "file_name": i.info.name.name.decode(),
                        "file_type": file_type,
                        "Type" : "Exist",
                        "size": str(i.info.meta.size),
                        "TimeZone": r_time(self.__cal_time(i.info.meta.crtime)).strftime("%Z"),
                        "ctime": r_time(self.__cal_time(i.info.meta.crtime)).strftime("%Y-%m-%d %H:%M:%S"),
                        "mtime": r_time(self.__cal_time(i.info.meta.mtime)).strftime("%Y-%m-%d %H:%M:%S"),
                        "atime": r_time(self.__cal_time(i.info.meta.atime)).strftime("%Y-%m-%d %H:%M:%S"),
                        "change time": r_time(self.__cal_time(i.info.meta.ctime)).strftime("%Y-%m-%d %H:%M:%S")
                    }
                    ret_list.append(f_path_obj)
            return ret_list

        except:
            print("[-]  This is not included this path or Not data")
            return -1


    def __UsnJrnl_extract(self, length, filename):
        fs = self.open_fs(length)
        f = fs.open(filename)
        found = False

        for attr in f:
            if attr.info.name == b'$J':
                print("[+] Success Extract : $J")
                found = True
                break
        if not found:
            print("[-] $J is not found")

        with open('$J', 'wb') as file_w:
            offset = 0
            size = attr.info.size
            while offset < size:
                available_to_read = min(1024 * 1024, size - offset)
                buf = f.read_random(offset, available_to_read, attr.info.type, attr.info.id)
                if not buf:
                    break
                file_w.write(buf)
                offset += len(buf)

    def file_extract(self, length, filepath, output_name):
        fs = self.open_fs(length)
        f = fs.open(filepath)

        with open(output_name, 'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

    def fslog_extract(self, length):
        mft_list = self.__file_extract(length, '/$MFT', '$MFT')
        log_list = self.__file_extract(length, '/$LogFile', '$LogFile')
        UsnJrnl = self.__UsnJrnl_extract(length, '/$Extend/$UsnJrnl')

    def open_fs(self, length):
        if self.__vol is not None:
            for part in self.__vol:
                if part.len > length and "Unallocated" not in part.desc.decode() \
                        and "Extended" not in part.desc.decode() \
                        and "Primary Table" not in part.desc.decode():
                    try:
                        fs = pytsk3.FS_Info(self.__img_info, offset=part.start * self.__vol.info.block_size)
                        return fs
                    except:
                        print("[-] Unable to open FS")
        else:
            pass

    def e01_metadata(self):
        ret_list = list()
        head_obj = dict()
        hash_obj = dict()

        e01_list = list()

        headers = self.__file.get_header_values()
        hashes = self.__file.get_hash_values()

        for head in headers:
            if head == "acquiry_date" or head == "system_date":
                timestamp = datetime.strptime(headers[head], "%a %b %d %H:%M:%S %Y")
                head_obj[head] = str(timestamp)
            else:
                head_obj[head] = headers[head]

        for h in hashes:
            hash_obj[h] = hashes[h]

        e01_obj = {
            "Bytes per Sector": self.__file.bytes_per_sector,
            "Number of Sector": self.__file.get_number_of_sectors(),
            "Total Size": self.__file.get_media_size()
        }

        head_obj.update(e01_obj)
        head_obj.update(hash_obj)
        e01_list.append(head_obj)

        ret_list = e01_list

        return ret_list

    def volume_metadata(self):
        ret_list = list()
        for partition in self.__vol:
            e01_obj = {
                "Type": partition.desc.decode(),
                "Num": partition.addr,
                "Start Sector": partition.start,
                "Total Sector": partition.len,
                "Size": str((partition.len * 512) / 1024 ** 2) + "MB"
            }
            ret_list.append(e01_obj)
        return ret_list

    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path, 'after')
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
    # def extract_file(self, output_path, file_extension):
    #     self.__open

    # def __open_fs(self.__vol, self.__file, )


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
    def __init__(self, file, hash_val):
        self.__file = file
        self.img = pytsk3.Img_Info(self.__file)
        self.__partition_list = list()
        self.__vol = pytsk3.Volume_Info(self.img)
        self.__hash_val = [hash_val]
        self.__cal_hash()
        
    def __cal_time(self, int_time):
        if int_time == 0:
            date = 'Never'
        else:
            date = datetime.utcfromtimestamp(int_time)
            # date = date.strftime("%Y-%m-%d %H:%M:%S")
        return date           
        
    def get_path(self, path, length):
        ret_list = list()
        for partition in self.__vol:
            self.__partition_list.append(partition.start)

        print("please input argument partition start sector : ", self.__partition_list)
        try:
            fs = self.open_fs(length)
        except:
            print("[-] Plz Check Disk Area")

        try:
            f = fs.open_dir(path)
            for i in f:
                file_type = str(i.info.name.type)
                if file_type == "TSK_FS_NAME_TYPE_REG":
                    file_type = "FILE"
                elif file_type == "TSK_FS_NAME_TYPE_DIR":
                    file_type = "DIR"
                else:
                    file_type = str(i.info.name.type)

                if i.info.meta is None:
                    f_path_obj = {
                        "file_name": i.info.name.name.decode(),
                        "file_type": file_type,
                        "Type": "Delete",
                        "size": "None",
                        "TimeZone" : "None",
                        "ctime": "None",
                        "mtime": "None",
                        "atime": "None",
                        "change time": "None"
                    }
                    ret_list.append(f_path_obj)
                else:
                    f_path_obj = {
                        "file_name": i.info.name.name.decode(),
                        "file_type": file_type,
                        "Type" : "Exist",
                        "size": str(i.info.meta.size),
                        "TimeZone": r_time(self.__cal_time(i.info.meta.crtime)).strftime("%Z"),
                        "ctime": r_time(self.__cal_time(i.info.meta.crtime)).strftime("%Y-%m-%d %H:%M:%S"),
                        "mtime": r_time(self.__cal_time(i.info.meta.mtime)).strftime("%Y-%m-%d %H:%M:%S"),
                        "atime": r_time(self.__cal_time(i.info.meta.atime)).strftime("%Y-%m-%d %H:%M:%S"),
                        "change time": r_time(self.__cal_time(i.info.meta.ctime)).strftime("%Y-%m-%d %H:%M:%S")
                    }
                    ret_list.append(f_path_obj)
            return ret_list

        except:
            print("[-]  This is not included this path or Not data")
            return -1

    def __UsnJrnl_extract(self, length, filename):
        fs = self.open_fs(length)
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

    def file_extract(self, length, filepath, output_name):
        fs = self.open_fs(length)
        f = fs.open(filepath)
        for attr in f:
            print(attr.info.type)
        with open(output_name, 'wb') as file_w:
            buf = f.read_random(0, f.info.meta.size)
            file_w.write(buf)
        print("[+] Success Extract : " + output_name)

    def fslog_extract(self, length):
        mft_list = self.__file_extract(length, '/$MFT', '$MFT')
        log_list = self.__file_extract(length, '/$LogFile', '$LogFile')
        UsnJrnl = self.__UsnJrnl_extract(length, '/$Extend/$UsnJrnl')

    def open_fs(self, length):
        if self.__vol is not None:
            for part in self.__vol:
                if part.len > length and "Unallocated" not in part.desc.decode() \
                        and "Extended" not in part.desc.decode() \
                        and "Primary Table" not in part.desc.decode():
                    try:
                        fs = pytsk3.FS_Info(self.img, offset=part.start * self.__vol.info.block_size)
                        return fs
                    except:
                        print("[-] Unable to open FS")
        else:
            pass

    def volume_metadata(self):
        ret_list = list()
        for partition in self.__vol:
            dd_obj = {
                "Type": partition.desc.decode(),
                "Num": partition.addr,
                "Start Sector": partition.start,
                "Total Sector": partition.len,
                "Size": str((partition.len * 512) / 1024 ** 2) + "MB"
            }
            ret_list.append(dd_obj)
        return ret_list

    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__file, 'after')
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
