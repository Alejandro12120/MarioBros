import config

class Bloque:
    
    def __init__(self, x: int, y: int, tuberia: bool, izquierda: bool):
        """Definimos un bloque, que puede ser una tuberia o un bloque normal
        
        :param x: es la posicion x de inicio de la tortuga
        :param y: es la posicion y de inicio de la tortuga
        :param tuberia: es un bool para saber si es una tuberia o no
        :param izquierda: es un bool para saber si es una tuberia izquierda o derecha
        """
        
        self.__id = id(self)
        
        self.__x = x
        self.__y = y
        self.__tuberia = tuberia
        
        if self.tuberia:
            if izquierda:
                self.__sprite = config.TUBERIA_IZQUIERDA
            else:
                self.__sprite = config.TUBERIA_DERECHA
        else:
            self.__sprite = config.PLATAFORMA
            
        
    
    @property
    def x(self) -> int:
        """Posicion en x del bloque"""
        return self.__x
    
    @property
    def y(self) -> int:
        """Posicion en y del bloque"""
        return self.__y
    
    @property
    def tuberia(self) -> bool:
        """Si el bloque es una tuberia"""
        return self.__tuberia
    
    @property
    def sprite(self) -> tuple:
        """Sprite del bloque"""
        return self.__sprite
    
    @property
    def id(self) -> int:
        """Id del bloque"""
        return self.__id
        
        
        