from typing import Optional, Union
from entidades.bloque import Bloque


class Enemigo:
    def __init__(self, x: int, y: int, dir: int, sprites: list, bloques: dict[Bloque], hitbox: int):
        """Este método creará un enemigo

        @param x: es la posicion x de inicio del enemigo
        @param y: es la posicion y de inicio del enemigo
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param sprite: es una lista con los valores del sprite en forma de tupla (banco, u, v, ancho, alto)
        @param bloques: es un diccionario con los bloques del tablero
        @param hitbox: es un ajuste que tenemos que hacer para que los enemigos entren bien por los huecos
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
        
        # Almacenamos un atributo para saber los frames que había cuando fue tumbada
        # Para así poder hacer cálculos con el tiempo, y que se levante cuando pase x tiempo
        self.__frames_tumbado = 0

        # Nos guardamos los bloques para poder comprobar si el enemigo está tocando el suelo
        self.__bloques = bloques

        self.__hitbox = hitbox
        
        self.__animacion_muerto = False
        self.__direccion_golpe = 0

    def golpea(self, x: int, y: int) -> bool:
        """Este método comprueba si un punto golpea al enemigo, es decir está dentro de la hitbox

        @param x: es la posicion x del punto
        @param y: es la posicion y del punto
        @return: True si golpea, False si no
        """
        if (self.__x + self.__hitbox <= x <= self.__x + self.sprite[3] - self.__hitbox
                and self.__y <= y <= self.__y + self.sprite[4]):
            return True

        return False
    def animar(self):
        """Este método anima al enemigo"""
        # Actualizamos la animación
        self.animacion += 1

        # Reiniciamos la animación si se ha pasado
        if self.animacion >= len(self.sprites):
            self.animacion = 0

    def tumbar(self, frames_actuales: int):
        """Este método tumba al enemigo"""
        self.__tumbado = True
        
        self.__frames_tumbado = frames_actuales
        
    def levantar(self):
        """Este método levanta al enemigo"""
        self.__tumbado = False
        
    def matar(self, direccion: int):
        """Este método mata al enemigo, para ello debe estar tumbado
        
        @param: es la dirección en la que se golpea al enemigo
        """
        
        if not self.__tumbado or self.__animacion_muerto: return
        
        self.__animacion_muerto = True
        self.__direccion_golpe = direccion
        

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

        alto_enemigo = self.sprite[4]

        if self.__y + alto_enemigo >= alto:
            return True

        return False

    def obtener_bloque_golpeado(self, inferiormente=False) -> Optional[Bloque]:
        """Este método obtiene el bloque que golpea el enemigo

        @param inferiormente: es un bool para saber si se comprueba inferiormente, por defecto False
        @return: el bloque que golpea Mario, None si no golpea ningún bloque
        """
        alto_enemigo = self.sprite[4]
        ancho_enemigo = self.sprite[3]

        for bloque in self.__bloques.values():
            if bloque.tuberia:
                continue

            # Hacemos el ajuste de +-1 explicado en el método tablero.draw()
            if inferiormente:
                if bloque.golpea(self.__x + self.__hitbox, self.__y + alto_enemigo):
                    return bloque

                if bloque.golpea(self.__x + ancho_enemigo - self.__hitbox, self.__y + alto_enemigo):
                    return bloque
            else:
                if bloque.golpea(self.__x + self.__hitbox, self.__y):
                    return bloque

                if bloque.golpea(self.__x + ancho_enemigo - self.__hitbox, self.__y):
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
    def id(self):
        return self.__id

    @property
    def sprite(self):
        if self.__animacion >= len(self.__sprites):
            self.__animacion = 0

        return self.__sprites[self.__animacion]

    @property
    def animacion(self):
        return self.__animacion

    @property
    def animacion_muerto(self):
        return self.__animacion_muerto
    
    @property
    def direccion_golpe(self):
        return self.__direccion_golpe

    @property
    def hitbox(self):
        return self.__hitbox
    
    @property
    def frames_tumbado(self):
        return self.__frames_tumbado
    
    @frames_tumbado.setter
    def frames_tumbado(self, frames: int):
        if type(frames) != int:
            raise TypeError("El atributo frames_tumbado debe ser un int")
        
        self.__frames_tumbado = frames

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
    def x(self, x: Union[int, float]):
        if type(x) != int and type(x) != float:
            raise TypeError("El atributo x debe ser un int o un float")

        self.__x = x

    @y.setter
    def y(self, y: Union[int, float]):
        if type(y) != int and type(y) != float:
            raise TypeError("El atributo y debe ser un int o un float")

        self.__y = y

    @animacion.setter
    def animacion(self, animacion: int):
        if type(animacion) != int:
            raise TypeError("El atributo animacion debe ser un int")

        self.__animacion = animacion
