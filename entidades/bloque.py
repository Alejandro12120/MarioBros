import config


class Bloque:
    def __init__(self, x: int, y: int, tipo: str):
        """Definimos un bloque, que puede ser una tuberia o un bloque normal

        @param x: es la posicion x de inicio de la tortuga
        @param y: es la posicion y de inicio de la tortuga
        @param tipo: es el tipo de bloque, puede ser "TUBERIA_IZQ", "TUBERIA_DER", "PLATAFORMA", "POW"
        """

        self.__id = id(self)

        self.__x = x
        self.__y = y
        self.__animacion = 0
        self.__tuberia = False
        self.__pow = False
        
        self.__golpeable = True

        if tipo == "TUBERIA_IZQ":
            self.__tuberia = True
            self.__sprite = config.TUBERIA_IZQUIERDA
        elif tipo == "TUBERIA_DER":
            self.__tuberia = True
            self.__sprite = config.TUBERIA_DERECHA
        elif tipo == "PLATAFORMA":
            self.__sprite = config.PLATAFORMA[self.__animacion]
        elif tipo == "POW":
            self.__pow = True
            self.__sprite = config.POW[self.__animacion]
        else:
            raise ValueError("Tipo de bloque no válido")

    def golpea(self, x: int, y: int) -> bool:
        """Este método comprueba si un punto golpea al bloque, es decir está dentro del bloque

        @param x: es la posicion x del punto
        @param y: es la posicion y del punto
        @return: True si golpea, False si no
        """

        if self.__tuberia: return False
        
        if self.__pow:
            # Los bloques POW tienen una altura dinámica
            if self.x <= x <= self.x + 16 and self.y <= y <= self.y + self.__sprite[4]:
                return True

            return False
        else:
            if self.x <= x <= self.x + 16 and self.y + 5 <= y <= self.y + 10:
                return True

        return False

    def animar(self, forzar: bool = False):
        """Este método anima el bloque, sólo válido para plataformas

        @param forzar: es un bool para forzar la animación, es decir que empezará a animar a la plataforma
        """
        # Esta función se llamará en dos ocasiones, cuando mario la golpeé que entonces forzaremos la animación
        # Y cuando se dibujen los bloques, de tal forma que si ya está animada volverá a su estado inicial

        if self.__tuberia: return

        # Si es bloque pow, tiene otra animación, ya que no es una animación cíclica, sino que cambia de estado
        if self.__pow and forzar:
            self.__animacion += 1
            
            if self.__animacion >= len(config.POW):
                # Establecemos la animación a -1 para indicarle a tablero que se elimine de los bloques
                self.__animacion = -1
                return
            
            self.__sprite = config.POW[self.__animacion]
            return

        if self.__animacion == 0 and not forzar: return

        self.__animacion += 1

        if self.__animacion >= len(config.PLATAFORMA):
            self.__animacion = 0

        self.__sprite = config.PLATAFORMA[self.__animacion]
    
    def golpear(self):
        """Este método se encarga de golpear el bloque"""
        
        if not self.__golpeable: return
        
        self.animar(True)
        
        self.__golpeable = False
        

    def __str__(self):
        return "(%i, %i, %s)" % (self.x, self.y, self.__pow)

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
    def pow(self) -> bool:
        """Si el bloque es un pow"""
        return self.__pow

    @property
    def sprite(self) -> tuple:
        """Sprite del bloque"""
        return self.__sprite

    @property
    def id(self) -> int:
        """Id del bloque"""
        return self.__id
    
    @property
    def animacion(self) -> int:
        """Animación del bloque"""
        return self.__animacion

    @property
    def golpeable(self) -> bool:
        """Si el bloque es golpeable"""
        return self.__golpeable
    
    @golpeable.setter
    def golpeable(self, golpeable: bool):
        if type(golpeable) != bool:
            raise ValueError("El valor de golpeable debe ser un booleano")
        
        self.__golpeable = golpeable
