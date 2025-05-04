class Comentario:
    def __init__(self, contenido, autor):
        self.__contenido = contenido
        self.__autor = autor
        self.__ID = random.randint(1, 1000)
    
    @property
    def contenido(self):
        return self.__contenido
    @property
    def autor(self):
        return self.__autor
    @property
    def ID(self):
        return self.__ID
    
    def editar(self, nuevo_contenido):
        self.__contenido = nuevo_contenido