import config

class Moneda:
    def __init__(self, x: int, y: int):
        
        self.__x = x
        self.__y = y
        
        self.__animacion = 0
        
        self.__sprites = config.MONEDA_SPRITE
    
    @property
    def sprite(self):
        """Devuelve el sprite de la moneda"""
        return self.__sprites[self.__animacion]
        