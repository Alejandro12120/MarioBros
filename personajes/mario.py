import config
from entidades.bloque import Bloque
from typing import Optional


class Mario:
    def __init__(self, x: int, y: int, bloques: dict, enemigos: dict, dir: int = 1):
        """Este método creará a Mario
        @param x: es la posicion x de inicio de Mario
        @param y: es la posicion y de inicio de Mario
        @param bloques: es un diccionario con los bloques del tablero
        @param enemigos: es un diccionario con los enemigos del tablero
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

        # Necesitamos los bloques para saber si Mario está en el suelo
        self.__bloques = bloques
        # Necesitamos los enemigos para controlar casi todo el juego
        self.__enemigos = enemigos

        # Me creo un modo dios para hacer pruebas
        self.__godmode = False

        self.__aceleracion_x = 1.6
        self.__velocidad_y = 0

        self.__gravedad = 0.4

    def move_x(self, ancho: int, dir: int = 0):
        """Este método moverá a Mario horizontalmente

        @param ancho: es el ancho del tablero
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha, por defecto 0
        """

        # Si la nueva direccion es 0 (actuará como un valor especial)
        # se moverá en la dirección que tenga guardada
        if dir == 0:
            dir = self.__direccion

        # Actualizamos la x de Mario
        # Multiplicamos por 1.6 para que se mueva más rápido
        self.__x += dir * self.__aceleracion_x

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

    def move_y(self, alto: int, gravedad: bool = True):
        """Este método moverá a Mario verticalmente

        @param alto: es el alto del tablero
        @param gravedad: es un bool para saber si se aplica gravedad, por defecto True
        """

        if gravedad and not self.toca_suelo(alto):
            self.__velocidad_y += self.__gravedad

        # Comprobamos de forma distinta si se golpea un bloque o si golpea un borde
        # Para ajustar la y en función de eso

        bloque_golpeado_inferior = self.obtener_bloque_golpeado(True)
        # En caso de golpear un bloque mientras mario cae
        if self.__velocidad_y > 0 and bloque_golpeado_inferior is not None:
            self.__velocidad_y = 0  # Reiniciamos la velocidad

            # Ajustamos su posición y
            if bloque_golpeado_inferior.pow:
                self.__y = bloque_golpeado_inferior.y - self.__sprite[4]
            else:
                self.__y = bloque_golpeado_inferior.y + 5 - self.__sprite[4]

        bloque_golpeado_superior = self.obtener_bloque_golpeado()
        if self.__velocidad_y < 0 and bloque_golpeado_superior is not None:
            self.__velocidad_y = 0
            self.__velocidad_y += self.__gravedad
            
            if not bloque_golpeado_superior.golpeable: return
            
            bloque_golpeado_superior.golpear()
            
            if bloque_golpeado_superior.pow:
                # Si el bloque es un pow, volteamos todos los enemigos
                for enemigo in self.__enemigos.values():
                    if enemigo.toca_suelo(alto):
                        if enemigo.tumbado:
                            enemigo.levantar()
                        else:
                            enemigo.tumbar()

        # No puede salirse ni por arriba ni por abajo
        # Si la velocidad es negativa significa que va hacia arriba
        # Si la velocidad es positiva significa que va hacia abajo
        if self.__velocidad_y < 0 and self.__y <= 0:
            self.__y = 0
        elif self.__velocidad_y > 0 and self.toca_borde(alto):
            self.__velocidad_y = 0  # Reiniciamos la velocidad
            self.__y = alto - self.__sprite[4]  # Cambiamos su posición y

        self.__y += self.__velocidad_y

    def saltar(self, alto: int):
        """Este método hará saltar a Mario
        
        @param alto: es el alto del tablero
        """

        self.__velocidad_y = -5
        self.move_y(alto, False) 

    def __actualizar_sprite(self):
        """Este método actualizará el sprite de Mario"""
        self.__sprite = config.MARIO_SPRITE[self.__animacion]

    def toca_borde(self, alto: int) -> bool:
        """Este método comprueba si Mario toca el borde del tablero

        @param alto: es el alto del tablero
        @return: True si toca el borde, False si no
        """
        alto_mario = self.__sprite[4]

        if self.__y + alto_mario >= alto:
            return True

        return False

    def obtener_bloque_golpeado(self, inferiormente=False) -> Optional[Bloque]:
        """Este método obtiene el bloque que golpea Mario

        @param inferiormente: es un bool para saber si se comprueba inferiormente, por defecto False
        @return: el bloque que golpea Mario, None si no golpea ningún bloque
        """
        alto_mario = self.__sprite[4]
        ancho_mario = self.__sprite[3]

        for bloque in self.__bloques.values():
            if bloque.tuberia:
                continue
            
            # Hacemos el ajuste de +-1 explicado en el método tablero.draw()
            if inferiormente:
                if bloque.golpea(self.__x + 1, self.__y + alto_mario):
                    return bloque

                if bloque.golpea(self.__x + ancho_mario - 1, self.__y + alto_mario):
                    return bloque
            else:
                if bloque.golpea(self.__x + 1, self.__y):
                    return bloque

                if bloque.golpea(self.__x + ancho_mario - 1, self.__y):
                    return bloque

        return None

    def toca_suelo(self, alto: int) -> bool:
        """Este método comprueba si Mario toca el suelo

        @param alto: es el alto del tablero
        @return: True si toca el suelo, False si no
        """

        return (
            self.toca_borde(alto)
            or self.obtener_bloque_golpeado(inferiormente=True) is not None
        )

    @property
    def vidas(self) -> int:
        """Vidas de Mario"""
        return self.__vidas
    
    @property
    def x(self) -> int:
        """Posición x de Mario"""
        return self.__x
    
    @property
    def y(self) -> int:
        """Posición y de Mario"""
        return self.__y
    
    @property
    def sprite(self) -> tuple:
        """Sprite de Mario"""
        return self.__sprite
    
    @property
    def direccion(self) -> int:
        """Dirección de Mario"""
        return self.__direccion
