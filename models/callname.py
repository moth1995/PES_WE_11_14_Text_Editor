import struct

class Callname:
    FILE_ID_1_SIZE = 4
    FILE_ID_2_SIZE = 4

    def __init__(self, idx:int, callname_bytes:bytearray, name_size:int, encoding:str):
        self.idx = idx
        self.callname_bytes = callname_bytes
        self.NAME_SIZE = name_size
        self.NAME_ENCODING = encoding
        self.set_name_from_bytes()
        self.set_id_relink_from_bytes()

    def set_name_from_bytes(self):
        """
        Set player name from relevant data bytes.
        """
        name = "???"

        all_name_bytes = self.callname_bytes[
            self.FILE_ID_1_SIZE + self.FILE_ID_2_SIZE
            : 
            self.FILE_ID_1_SIZE + self.FILE_ID_2_SIZE + self.NAME_SIZE
        ]
        name = all_name_bytes.partition(b"\0")[0].decode(self.NAME_ENCODING, 'ignore')

        self.__name = name

    @property
    def name(self):
        """
        Return player name.
        """
        return self.__name

    @name.setter
    def name(self, name:str):
        """
        Update player name with the supplied value.
        """
        new_name = name[: self.NAME_SIZE]

        player_name_bytes = [0] * self.NAME_SIZE
        new_name_bytes = str.encode(new_name, self.NAME_ENCODING)
        player_name_bytes[: len(new_name_bytes)] = new_name_bytes

        for i, byte in enumerate(player_name_bytes):
            self.callname_bytes[self.FILE_ID_1_SIZE + self.FILE_ID_2_SIZE + i] = byte

        self.__name = new_name


    def set_id_relink_from_bytes(self):
        """
        Set player name from relevant data bytes.
        """
        file_1_id = 0
        afs_1_id = 0
        file_2_id = 0
        afs_2_id = 0

        file_1_id, afs_1_id, file_2_id, afs_2_id = struct.unpack("<4H",self.callname_bytes[:8])
        self.__file_1_id = file_1_id
        self.__afs_1_id = afs_1_id
        self.__file_2_id = file_2_id
        self.__afs_2_id = afs_2_id

    @property
    def file_1_id(self):
        """
        Return player name.
        """
        return self.__file_1_id

    @file_1_id.setter
    def file_1_id(self, file_1_id:int):
        """
        Update player name with the supplied value.
        """
        if not 0 <= file_1_id <= 0xFFFF:
            raise ValueError("Number too big to represent with int16")
        
        new_file_1_id_bytes = struct.pack("<H",file_1_id)

        for i, byte in enumerate(new_file_1_id_bytes):
            self.callname_bytes[i] = byte

        self.__file_1_id = file_1_id

    @property
    def afs_1_id(self):
        """
        Return player name.
        """
        return self.__afs_1_id

    @afs_1_id.setter
    def afs_1_id(self, afs_1_id:int):
        """
        Update player name with the supplied value.
        """
        if not 0 <= afs_1_id <= 0xFFFF:
            raise ValueError("Number too big to represent with int16")
        
        new_afs_1_id_bytes = struct.pack("<H",afs_1_id)

        for i, byte in enumerate(new_afs_1_id_bytes):
            self.callname_bytes[i + 2] = byte

        self.__afs_1_id = afs_1_id

    @property
    def file_2_id(self):
        """
        Return player name.
        """
        return self.__file_2_id

    @file_2_id.setter
    def file_2_id(self, file_2_id:int):
        """
        Update player name with the supplied value.
        """
        if not 0 <= file_2_id <= 0xFFFF:
            raise ValueError("Number too big to represent with int16")
        
        new_file_2_id_bytes = struct.pack("<H",file_2_id)

        for i, byte in enumerate(new_file_2_id_bytes):
            self.callname_bytes[i + 4] = byte

        self.__file_2_id = file_2_id

    @property
    def afs_2_id(self):
        """
        Return player name.
        """
        return self.__afs_2_id

    @afs_2_id.setter
    def afs_2_id(self, afs_2_id:int):
        """
        Update player name with the supplied value.
        """
        if not 0 <= afs_2_id <= 0xFFFF:
            raise ValueError("Number too big to represent with int16")
        
        new_afs_2_id_bytes = struct.pack("<H",afs_2_id)

        for i, byte in enumerate(new_afs_2_id_bytes):
            self.callname_bytes[i + 6] = byte

        self.__afs_2_id = afs_2_id
