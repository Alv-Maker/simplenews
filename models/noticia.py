import models.periodista as periodista

class Noticia:


    def __init__(self, titulo, subtitulo, contenido, periodista):
        self.__titulo = titulo
        self.__subtitulo = subtitulo
        self.__contenido = contenido
        if not hasattr(Noticia, '_next_id'):
            Noticia._next_id = 1001
        self.__ID = Noticia._next_id
        Noticia._next_id += 1
        self.__vistas = 0
        self.__likes = 0
        self.__comentarios = []  # Inicializa la lista de comentarios
        self.__periodista = periodista  # Almacena el periodista que creó la noticia
    
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
    def perodista(self):
        return self.__periodista
    
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


    