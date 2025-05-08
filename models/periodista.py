from models.usuario import Usuario

class Periodista(Usuario):
    def __init__(self, area_especializacion, nombre, apellido, email, password):
        super().__init__(email, password)
        self.__nombre = nombre
        self.__apellido = apellido
        self.__area_especializacion = area_especializacion

    @property
    def nombrecompleto(self):
        return self.__nombre + " " + self.__apellido
    
    @property
    def area_especializacion(self):
        return self.__area_especializacion
    

        

    
