import pytsk3
import os
from abc import *
image_file = os.path.join("/mnt/hgfs/#DFC2019/ARTIFACT/ART400/", "ART400.RAW")


class ExtractFsLog(metaclass=ABCMeta):
    def __init__(self, image, volume):
        self._file = image
        self._volume = volume
        self._img = pytsk3.Img_Info(self._volume)
        self._fs = pytsk3.FS_Info(self._img)


    @abstractmethod
    def extract(self, file_name, output_file):
        file = self._fs.open(file_name)
        with open(output_file, "wb") as output:
            offset = 0
            size = file.info.meta.size
            while offset < size:
                available_to_read = min(1024*1024, size-offset)
                buf = file.read_random(0, available_to_read)
                if not buf:
                    break
                output.write(buf)
                offset += len(buf)
