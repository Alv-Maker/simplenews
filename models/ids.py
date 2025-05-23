class NoticiaID:
    def __init__(self):
        self.__ID = 1
    
    @property
    def ID(self):
        return self.__ID
    
    def getAndIncrementID(self):
        ID = self.__ID
        self.__ID += 1
        return ID
    
class ComentarioID:
    def __init__(self, noticiaID):
        self.__ID = 1
        self.__noticiaID = noticiaID
    
    @property
    def ID(self):
        return self.__ID
    
    def getAndIncrementID(self):
        ID = self.__ID
        self.__ID += 1
        return ID

    @property
    def noticiaID(self):
        return self.__noticiaID