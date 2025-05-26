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
    
