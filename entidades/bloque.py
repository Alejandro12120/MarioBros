import config

class Bloque:
    
    def __init__(self, x: int, y: int, tuberia: bool, izquierda: bool):
        """Definimos un bloque, que puede ser una tuberia o un bloque normal
        
        @param x: es la posicion x de inicio de la tortuga
        @param y: es la posicion y de inicio de la tortuga
        @param tuberia: es un bool para saber si es una tuberia o no
        @param izquierda: es un bool para saber si es una tuberia izquierda o derecha
        """
        
        self.__id = id(self)
        
        self.__x = x
        self.__y = y
        self.__tuberia = tuberia
        self.__animacion = 0
        
        if self.tuberia:
            if izquierda:
                self.__sprite = config.TUBERIA_IZQUIERDA
            else:
                self.__sprite = config.TUBERIA_DERECHA
        else:
            self.__sprite = config.PLATAFORMA[self.__animacion]
            
    
    def golpea(self, x: int, y: int) -> bool:
        """Este método comprueba si un punto golpea al bloque, es decir está dentro del bloque
        
        @param x: es la posicion x del punto
        @param y: es la posicion y del punto
        @return: True si golpea, False si no
        """
        
        if self.x <= x <= self.x + 16 and self.y + 5 <= y <= self.y + 10:
            return True
        
        return False
    
    def animate(self, forzar: bool = False):
        """Este método anima el bloque, sólo válido para plataformas
        
        @param forzar: es un bool para forzar la animación, es decir que empezará a animar a la plataforma
        """
        # Esta función se llamará en dos ocasiones, cuando mario la golpeé que entonces forzaremos la animación
        # Y cuando se dibujen los bloques, de tal forma que si ya está animada volverá a su estado inicial
        
        if self.tuberia: return
        
        if self.__animacion == 0 and not forzar: return
        
        self.__animacion += 1
        
        if self.__animacion >= len(config.PLATAFORMA):
            self.__animacion = 0
            
        self.__sprite = config.PLATAFORMA[self.__animacion]
    

    def __str__(self):
        return "(%i, %i)" % (self.x, self.y)
    
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
        
        
        