import flask_login

class Usuario(flask_login.UsuarioMixin):
    def __init__(self, nombre, apellido):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__ID = random.randint(1, 1000)
        
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def apellido(self):
        return self.__apellido
    
    @property
    def ID(self):
        return self.__ID
    
    def __str__(self):
        return f"{self.__nombre} {self.__apellido}"