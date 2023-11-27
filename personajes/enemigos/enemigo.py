from typing import Optional
from entidades.bloque import Bloque


class Enemigo:
    def __init__(self, x: int, y: int, dir: int, sprites: list, bloques: dict):
        """Este método creará un enemigo

        @param x: es la posicion x de inicio del enemigo
        @param y: es la posicion y de inicio del enemigo
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param sprite: es una lista con los valores del sprite en forma de tupla (banco, u, v, ancho, alto)
        @param bloques: es un diccionario con los bloques del tablero
        """

        # Guardamos una variable con el id del enemigo
        # Para poder identificarlo
        self.__id = id(self)

        self.__x = x
        self.__y = y
        self.__direccion = dir
        self.__tumbado = False

        self.__sprites = sprites

        self.__animacion = 0

        # Nos guardamos los bloques para poder comprobar si el enemigo está tocando el suelo
        self.__bloques = bloques

        # Variable para controlar si el enemigo está tocando el suelo
        # Es necesario para que pueda ser tumbado
        self.__tocando_suelo = False

    def tumbar(self):
        """Este método tumba al enemigo"""
        self.__tumbado = True

    def levantar(self):
        """Este método levanta al enemigo"""
        self.__tumbado = False

    def toca_suelo(self, alto: int) -> bool:
        """Este método comprueba si Mario toca el suelo

        @param alto: es el alto del tablero
        @return: True si toca el suelo, False si no
        """

        return (
            self.toca_borde(alto)
            or self.obtener_bloque_golpeado(inferiormente=True) is not None
        )
        
    
    def toca_borde(self, alto: int) -> bool:
        """Este método comprueba si el enemigo está tocando el borde"""
        
        alto_enemigo = self.__sprite[4]

        if self.__y + alto_enemigo >= alto:
            return True

        return False

    def obtener_bloque_golpeado(self, inferiormente=False) -> Optional[Bloque]:
        """Este método obtiene el bloque que golpea el enemigo

        @param inferiormente: es un bool para saber si se comprueba inferiormente, por defecto False
        @return: el bloque que golpea Mario, None si no golpea ningún bloque
        """
        alto_enemigo = self.__sprite[4]
        ancho_enemigo = self.__sprite[3]

        for bloque in self.__bloques.values():
            if bloque.tuberia:
                continue

            # Hacemos el ajuste de +-1 explicado en el método tablero.draw()
            if inferiormente:
                if bloque.golpea(self.__x + 1, self.__y + alto_enemigo):
                    return bloque

                if bloque.golpea(self.__x + ancho_enemigo - 1, self.__y + alto_enemigo):
                    return bloque
            else:
                if bloque.golpea(self.__x + 1, self.__y):
                    return bloque

                if bloque.golpea(self.__x + ancho_enemigo - 1, self.__y):
                    return bloque

        return None

    # Creamos getters de los atributos privados que usaremos en otras clases
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def direccion(self):
        return self.__direccion

    @property
    def sprites(self):
        return self.__sprites

    @property
    def tumbado(self):
        return self.__tumbado

    @property
    def tocando_suelo(self):
        return self.__tocando_suelo

    @property
    def id(self):
        return self.__id

    @property
    def sprite(self):
        return self.__sprites[self.__animacion]

    @property
    def animacion(self):
        return self.__animacion

    # Creamos un setter para los sprites ya que los cambiaremos cuando se tumben a los enemigos
    @sprites.setter
    def sprites(self, sprites: list):
        if type(sprites) != list:
            raise TypeError("El atributo sprites debe ser una lista")

        self.__sprites = sprites

    @direccion.setter
    def direccion(self, dir: int):
        if type(dir) != int:
            raise TypeError("El atributo direccion debe ser un int")

        self.__direccion = dir

    @x.setter
    def x(self, x: int):
        if type(x) != int:
            raise TypeError("El atributo x debe ser un int")

        self.__x = x

    @y.setter
    def y(self, y: int):
        if type(y) != int:
            raise TypeError("El atributo y debe ser un int")

        self.__y = y

    @animacion.setter
    def animacion(self, animacion: int):
        if type(animacion) != int:
            raise TypeError("El atributo animacion debe ser un int")

        self.__animacion = animacion
