import pytsk3
import pyewf
import json
import datetime
import forlib.calc_hash as calc_hash


class E01Analysis:
    def __init__(self, file, path, hash_val):
        self.file = file
        self.ret_list = list()
        self.partition_list = list()
        self.img_info = EWFImgInfo(self.file)
        self.vol = pytsk3.Volume_Info(self.img_info)
        self.__path = path
        self.__hash_val = [hash_val]
        self.__cal_hash()

    def get_path(self, path, length):
        for partition in self.vol:
            self.partition_list.append(partition.start)

        print("please input argument partition start sector : ", self.partition_list)

        fs = self.open_fs(length)

        try:
            f = fs.open_dir(path)
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
                self.ret_list.append(f_path_obj)
            return self.ret_list

        except:
            print("[-] This is Unallocated Area")

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
        mft_list = self.file_extract(length, '/$MFT', '$MFT')
        log_list = self.file_extract(length, '/$LogFile', '$LogFile')
        UsnJrnl = self.__UsnJrnl_extract(length, '/$Extend/$UsnJrnl')

    def open_fs(self, length):
        if self.vol is not None:
            for part in self.vol:
                if part.len > length and "Unallocated" not in part.desc.decode() \
                        and "Extended" not in part.desc.decode() \
                        and "Primary Table" not in part.desc.decode():
                    try:
                        fs = pytsk3.FS_Info(self.img_info, offset=part.start * self.vol.info.block_size)
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
        hashes = self.file.get_hash_values()

        for head in headers:
            if head == "acquiry_date" or head == "system_date":
                timestamp = datetime.datetime.strptime(headers[head], "%a %b %d %H:%M:%S %Y")
                head_obj[head] = str(timestamp)
            else:
                head_obj[head] = headers[head]

        for h in hashes:
            hash_obj[h] = hashes[h]

        e01_obj = {
            "Bytes per Sector": self.file.bytes_per_sector,
            "Number of Sector": self.file.get_number_of_sectors(),
            "Total Size": self.file.get_media_size()
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
                "Size": str((partition.len * 512) / 1024 ** 2) + "MB"
            }
            self.ret_list.append(e01_obj)
        return self.ret_list

    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.__path)
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
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
    def __init__(self, file, hash_val):
        self.file = file
        self.img = pytsk3.Img_Info(self.file)
        self.partition_list = list()
        self.vol = pytsk3.Volume_Info(self.img)
        self.ret_list = list()
        self.__hash_val = [hash_val]
        self.__cal_hash()

    def get_path(self, path, length):
        for partition in self.vol:
            self.partition_list.append(partition.start)

        print("please input argument partition start sector : ", self.partition_list)

        fs = self.open_fs(length)
        try:
            f = fs.open_dir(path)
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
                self.ret_list.append(f_path_obj)
            return self.ret_list

        except:
            print("[-] This is Unallocated Area")

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
        mft_list = self.file_extract(length, '/$MFT', '$MFT')
        log_list = self.file_extract(length, '/$LogFile', '$LogFile')
        UsnJrnl = self.__UsnJrnl_extract(length, '/$Extend/$UsnJrnl')

    def open_fs(self, length):
        if self.vol is not None:
            for part in self.vol:
                if part.len > length and "Unallocated" not in part.desc.decode() \
                        and "Extended" not in part.desc.decode() \
                        and "Primary Table" not in part.desc.decode():
                    try:
                        fs = pytsk3.FS_Info(self.img, offset=part.start * self.vol.info.block_size)
                        return fs
                    except:
                        print("[-] Unable to open FS")
        else:
            pass

    def volume_metadata(self):
        for partition in self.vol:
            dd_obj = {
                "Type": partition.desc.decode(),
                "Num": partition.addr,
                "Start Sector": partition.start,
                "Total Sector": partition.len,
                "Size": str((partition.len * 512) / 1024 ** 2) + "MB"
            }
            self.ret_list.append(dd_obj)
        return self.ret_list

    def __cal_hash(self):
        after_hash = calc_hash.get_hash(self.file)
        self.__hash_val.append(after_hash)

    def get_hash(self):
        return self.__hash_val
