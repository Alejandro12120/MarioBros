import config


class Mario:
    def __init__(self, x: int, y: int, dir: int = 1):
        """Este método creará a Mario
        @param x: es la posicion x de inicio de Mario
        @param y: es la posicion y de inicio de Mario
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha, por defecto 1
        """

        self.__x = x
        self.__y = y
        self.__direccion = dir
        self.__animacion = 0

        # Definimos el sprite de Mario
        self.__sprite = config.MARIO_SPRITE[self.__animacion]

        # Definimos el numero de vidas de Mario
        self.__vidas = 3

        # Me creo un modo dios para hacer pruebas
        self.__godmode = False

    def move(self, ancho: int, dir: int = 0):
        """Este método moverá a Mario

        @param ancho: es el ancho del tablero
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha, por defecto 0
        """

        # Si la nueva direccion es 0 (actuará como un valor especial)
        # se moverá en la dirección que tenga guardada
        if dir == 0:
            dir = self.__direccion

        # Actualizamos la x de Mario
        # Multiplicamos por 1.6 para que se mueva más rápido
        self.__x += dir*1.6

        # Si se sale por la derecha, aparece por la izquierda
        if dir == 1 and self.__x >= ancho:
            self.__x = 0
        # Si se sale por la izquierda, aparece por la derecha
        elif dir == -1 and self.__x <= 0:
            self.__x = ancho

        # Guardamos la dirección
        self.__direccion = dir

        # Cambiamos la animación
        self.__animacion += 1
        # Reiniciamos la animación si se ha pasado
        if self.__animacion >= len(config.MARIO_SPRITE):
            self.__animacion = 0

        # Como hemos cambiado la animacion, actualizamos el sprite
        self.__actualizar_sprite()

    def draw(self, pyxel):
        """Dibujamos a Mario
        @param x: es la posicion x de inicio de Mario
        @param y: es la posicion y de inicio de Mario
        @param pyxel: es el objeto de pyxel
        """

        # Dibujamos a Mario
        # TODO: Tener en cuenta animaciones

        # Si se mueve para la izquierda, se invierte el sprite
        if self.__direccion == -1:
            pyxel.blt(self.__x, self.__y, self.__sprite[0], self.__sprite[1],
                      self.__sprite[2], -self.__sprite[3], self.__sprite[4], 8)
        # Si se mueve para la derecha, se dibuja normal
        else:
            pyxel.blt(self.__x, self.__y, self.__sprite[0], self.__sprite[1],
                      self.__sprite[2], self.__sprite[3], self.__sprite[4], 8)

    def __actualizar_sprite(self):
        """Este método actualizará el sprite de Mario"""
        self.__sprite = config.MARIO_SPRITE[self.__animacion]

    @property
    def vidas(self) -> int:
        """Vidas de Mario"""
        return self.__vidas
