class Periodista(Usuario):
    def __init__(self, area_especializacion, nombre, apellido):
        super().__init__(nombre, apellido)
        self.__area_especializacion = area_especializacion
        self.__ID = random.randint(1, 1000)

    
