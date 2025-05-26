import datetime
import random
from models.ids import NoticiaID

class Noticia:

    def __init__(self, titulo, subtitulo, contenido, periodista, idunique: NoticiaID):
        self.__titulo = titulo
        self.__subtitulo = subtitulo
        self.__contenido = contenido
        self.__ID = idunique.getAndIncrementID()  # Genera un ID único para la noticia
        self.__vistas = 0
        self.__likes = 0
        self.__comentarios = []  # Inicializa la lista de comentarios
        self.__periodista = periodista  # Almacena el periodista que creó la noticia
        self.__fecha = datetime.datetime.now()  # Almacena la fecha de creación de la noticia
        self.__nxt_cmnt_id = 1
    @property
    def titulo(self):
        return self.__titulo
    @property
    def subtitulo(self):
        return self.__subtitulo
    @property
    def contenido(self):
        return self.__contenido

    @property
    def ID(self):
        return self.__ID
    

    @property
    def vistas(self):
        return self.__vistas
    @property
    def likes(self):
        return self.__likes
    @property
    def comentarios(self):
        return self.__comentarios
    @property
    def periodista(self):
        return self.__periodista
    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def fecha_formateada(self):
        return self.__fecha.strftime("%d/%m/%Y %H:%M:%S")  # Formato de fecha y hora
    
    @vistas.setter
    def vistas(self, vistas):
        self.__vistas = vistas

    @likes.setter
    def likes(self, likes):
        self.__likes = likes


    def add_vista(self):
        self.__vistas += 1

    def like(self):
        self.__likes += 1

    def add_comentario(self, comentario):
        self.__comentarios.append(comentario)

    def remove_comentario(self, comentario):
        for i in self.__comentarios:
            if i == comentario:
                self.__comentarios.remove(i)
                return True
        
        return False

    def getnxtcmntid(self):
        return len(self.comentarios)+1
    