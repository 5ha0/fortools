import binascii
import struct

class JumplistAnalysis:
    def __init__(self, file):
        self.file = file
        self.streams = file.listdir(streams=True, storages=False)
        self. destlist = self.__find_destlist()

    def __find_destlist(self):
        for i in range(len(self.streams)-1, -1, -1):
            if self.streams[i][0] == 'DestList':
                file = self.file.openstream(self.streams[i])
                return file
        print('no destlist')
        return -1

    def access_count(self):
        self.destlist.seek(148)
        cnt = self.destlist.read(4)
        self.destlist.seek(0)
        new = struct.unpack('<i', cnt)
        return new[0]

    def path(self):
        self.destlist.seek(162)
        path = self.destlist.read(400)
        self.destlist.seek(0)
        return path.decode('ascii')

    def recent_time(self):
        self.destlist.seek(132)
        time = self.destlist.read(8)
        self.destlist.seek(0)
        return time

    def show_all_record(self):
        print(self.streams)
        new = self.file.openstream(self.streams[1])
        print(new.read())
