from abc import *
import os
import pytsk3
import sys

image_file = os.path.join("/mnt/hgfs/#DFC2019/ARTIFACT/ART400/", "ART400.RAW")


class FsLogExtractor(metaclass=ABCMeta):
    def __init__(self, image, volume):
        self._file = image
        self._volume = volume
        self._img = pytsk3.Img_Info(self._volume)
        self._fs = pytsk3.FS_Info(self._img)

    @abstractmethod
    def extract(self, file_name, output_file, output_path):
        file = self._fs.open(file_name)
        with open(os.path.join(output_path, output_file), "wb") as output:
            offset = 0
            size = file.info.meta.size
            while offset < size:
                available_to_read = min(1024*1024, size-offset)
                buf = file.read_random(0, available_to_read)
                if not buf:
                    break
                output.write(buf)
                offset += len(buf)


class UsnJrnlExtractor(FsLogExtractor):
    def extract(self, file_name, output_file, output_path):
        file = self._fs.open('/$Extend/$UsnJrnl')
        found = False
        for attr in file:
            if attr.info.name == '$J':
                found = True
                break
            if not found:
                sys.exit(0)
        super().extract("/$Extend/$UsnJrnl", "$UsnJrnl", output_path)


class MFTExtractor(FsLogExtractor):
    def extract(self, file_name, output_file, output_path):
        super().extract("/$MFT", "$MFT", output_path)


class LogfileExtractor(FsLogExtractor):
    def extract(self, file_name, output_file, output_path): 
        super().extract("/$Logfile", "$Logfile", output_path)