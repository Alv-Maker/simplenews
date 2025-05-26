import datetime
import random


class Comentario:    

    def __init__(self, contenido, autor, noticia_id=None):
        self.__contenido = contenido
        self.__autor = autor
        self.__ID = random.randint(1, 1000)
        self.__noticia_id = noticia_id
        self.__fecha = datetime.datetime.now()
    
    @property
    def contenido(self):
        return self.__contenido
    @property
    def autor(self):
        return self.__autor
    @property
    def ID(self):
        return self.__ID
    @property
    def fecha(self):
        return self.__fecha
    
    def editar(self, nuevo_contenido):
        self.__contenido = nuevo_contenido

    def fecha_formateada(self):
        return self.__fecha.strftime("%d/%m/%Y %H:%M:%S")