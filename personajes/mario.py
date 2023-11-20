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

        # Definimos el sprite de Mario
        self.__sprite = config.MARIO_SPRITE

        # Definimos el numero de vidas de Mario
        self.__vidas = 3

        # Me creo un modo dios para hacer pruebas
        self.__godmode = False

    def move(self, ancho: int, dir: int = 0):
        # Si la nueva direccion es 0 (actuará como un valor especial)
        # se moverá en la dirección que tenga guardada
        if dir == 0:
            dir = self.__direccion

        # Obtenemos el tamaño de Mario para no pasarnos del tablero
        mario_size = self.__sprite[3]

        # De esta forma mario no saldría
        # TODO: Tiene que aparecer en el otro lado
        if dir == 1 and self.__x < ancho - mario_size:
            self.__x += dir
        elif dir == -1 and self.__x > 0:
            self.__x += dir

    def draw(self, pyxel):
        """Dibujamos a Mario
        @param x: es la posicion x de inicio de Mario
        @param y: es la posicion y de inicio de Mario
        @param pyxel: es el objeto de pyxel
        """

        # Dibujamos a Mario
        # TODO: Tener en cuenta animaciones
        pyxel.blt(self.__x, self.__y, self.__sprite[0], self.__sprite[1], self.__sprite[2], self.__sprite[3], self.__sprite[4], 8)

    @property
    def vidas(self) -> int:
        """Vidas de Mario"""
        return self.__vidas
