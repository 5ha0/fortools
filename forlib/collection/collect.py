from abc import *
import os
import pytsk3
import sys



class FsLogExtractor:
    def __init__(self, image, volume):
        self._file = image
        self._volume = volume
        self._img = pytsk3.Img_Info(self._volume)
        self._fs = pytsk3.FS_Info(self._img)

    # @abstractmethod
    def extract(self, output_path, file_name, output_file):
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
    def extract(self, output_path=os.path.join(os.curdir, "fslog"), filename='/$Extend/$UsnJrnl', output_file='$UsnJrnl'):
        file = self._fs.open(filename)
        found = False
        for attr in file:
            if attr.info.name == '$J':
                found = True
                break
            if not found:
                raise FileExistsError
        super().extract(output_path, filename, output_file)


class MFTExtractor(FsLogExtractor):
    def extract(self, output_path=os.path.join(os.curdir, "fslog"), file_name="/$MFT", output_file="$MFT"):
        super().extract(output_path, file_name, output_file)


class LogfileExtractor(FsLogExtractor):
    def extract(self, output_path=os.path.join(os.curdir, "fslog"), file_name="/$Logfile", output_file="$Logfile"):
        super().extract(output_path, file_name, output_file)

def main():
    image_file = os.path.join("/mnt/hgfs/#DFC2019/ARTIFACT/ART400/", "ART400.RAW")
    usn = UsnJrnlExtractor(image_file, '\\\\.\\'+str(sys.argv[1]))
    usn.extract()

if __name__ == "__main__":
    main()