import config
from entidades.bloque import Bloque
from .enemigos.enemigo import Enemigo
from typing import Optional, Union


class Mario:
    def __init__(self, x: int, y: int, bloques: dict[Bloque], enemigos: dict[Enemigo], dir: int = 1):
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
        self.__sprites = config.MARIO_SPRITE

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

        self.__gravedad = 0.3
        
        # Este atributo cambiará cuando se esté ejecutando la animación de muerte
        self.__animacion_muerto = False

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
        # Le hacemos una corrección de +8 para evitar un bug
        if dir == 1 and self.__x + 16 >= ancho:
            self.__x = 0
        # Si se sale por la izquierda, aparece por la derecha
        elif dir == -1 and self.__x <= 0:
            self.__x = ancho

        # Guardamos la dirección
        self.__direccion = dir

        # Animamos a Mario
        self.animar()

    def move_y(self, alto: int, frames: int, gravedad: bool = True):
        """Este método moverá a Mario verticalmente

        @param alto: es el alto del tablero
        @param frames: es el numero de frames actuales
        @param gravedad: es un bool para saber si se aplica gravedad, por defecto True
        """

        # Si es la animación, la controlamos desde tablero
        if self.animacion_muerto: return
        
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
                self.__y = bloque_golpeado_inferior.y - self.sprite[4]
            else:
                self.__y = bloque_golpeado_inferior.y + 5 - self.sprite[4]

        bloque_golpeado_superior = self.obtener_bloque_golpeado()
        if self.__velocidad_y < 0 and bloque_golpeado_superior is not None:
            self.__velocidad_y = 0
            self.__velocidad_y += self.__gravedad

            if not bloque_golpeado_superior.golpeable:
                return

            bloque_golpeado_superior.golpear()
            
            # Golpeamos los enemigos golpeados por la plataforma
            posibles_enemigos_golpeados = self.obtener_enemigo_golpeado(bloque_golpeado_superior)
            if len(posibles_enemigos_golpeados) != 0:
                for enemigo_golpeado in posibles_enemigos_golpeados:
                    # Lo golpeamos
                    enemigo_golpeado.recibir_golpe(frames)
                    
                    # Pequeña animación de bote debido al golpe
                    enemigo_golpeado.saltar(alto, -1.5)
                    
            # Si el bloque es un pow, volteamos todos los enemigos que toquen suelo
            if bloque_golpeado_superior.pow:
                for enemigo in self.__enemigos.values():
                    if enemigo.toca_suelo(alto):
                        if enemigo.tumbado:
                            enemigo.levantar()
                        else:
                            enemigo.tumbar(frames)

        # No puede salirse ni por arriba ni por abajo
        # Si la velocidad es negativa significa que va hacia arriba
        # Si la velocidad es positiva significa que va hacia abajo
        if self.__velocidad_y < 0 and self.__y <= 0:
            self.__velocidad_y = 0
            self.__y = 0
        elif self.__velocidad_y > 0 and self.toca_borde(alto):
            self.__velocidad_y = 0  # Reiniciamos la velocidad
            self.__y = alto - self.sprite[4]  # Cambiamos su posición y

        self.__y += self.__velocidad_y

    def animar(self, parar=False):
        """Este método animar a mario

        @param parar: debemos para en la última animación
        """
        # Cambiamos la animación
        self.__animacion += 1
        # Reiniciamos la animación si se ha pasado
        if self.__animacion >= len(self.__sprites):
            if parar:
                self.__animacion = len(self.__sprites) - 1
            else:
                self.__animacion = 0

    def saltar(self, alto: int, frames: int):
        """Este método hará saltar a Mario

        @param alto: es el alto del tablero
        """

        self.__velocidad_y = -4.9
        self.move_y(alto, frames, False)

    def matar(self):
        """Este método matará a Mario, le restará una vida y lo pondrá en la posición inicial"""
        # Para evitar matarlo varias veces seguidas
        if self.__animacion_muerto: return
        
        # Reiniciamos velocidad por si salta antes de morir
        self.__velocidad_y = 0
        
        self.__vidas -= 1
        self.__sprites = config.MARIO_MUERTO_SPRITE
        self.__animacion_muerto = True
        
        # Lo subimos un poco para dar una sensación de salto
        self.__y -= 6
    
    def terminar_animacion_muerte(self):
        """Este método termina la animación de muerte de Mario, devolviendolo al spawpoint y cambiando los sprites"""
        
        self.__sprites = config.MARIO_SPRITE
        self.__animacion_muerto = False
        
        # Spawnpoint
        self.__x = 96
        self.__y = 107

    def toca_borde(self, alto: int) -> bool:
        """Este método comprueba si Mario toca el borde del tablero

        @param alto: es el alto del tablero
        @return: True si toca el borde, False si no
        """
        alto_mario = self.sprite[4]

        if self.__y + alto_mario >= alto:
            return True

        return False

    def obtener_bloque_golpeado(self, inferiormente=False) -> Optional[Bloque]:
        """Este método obtiene el bloque que golpea Mario

        @param inferiormente: es un bool para saber si se comprueba inferiormente, por defecto False
        @return: el bloque que golpea Mario, None si no golpea ningún bloque
        """
        alto_mario = self.sprite[4]
        ancho_mario = self.sprite[3]

        for bloque in self.__bloques.values():
            if bloque.tuberia:
                continue

            # Hacemos el ajuste de +-2 explicado en el método tablero.draw()
            if inferiormente:
                if bloque.golpea(self.__x + 2, self.__y + alto_mario):
                    return bloque

                if bloque.golpea(self.__x + ancho_mario - 2, self.__y + alto_mario):
                    return bloque
            else:
                if bloque.golpea(self.__x + 2, self.__y):
                    return bloque

                if bloque.golpea(self.__x + ancho_mario - 2, self.__y):
                    return bloque

        return None

    def obtener_enemigo_golpeado(self, bloque: Bloque) -> list[Enemigo]:
        """Este método obtiene el enemigo que golpea Mario al golpear una plataforma
        
        @param bloque: es el bloque que golpea Mario
        @return: una lista de enemigos que golpea Mario, estará vacía si no golpea ningún enemigo
        """
         
        enemigos_golpeados = []   
        for enemigo in self.__enemigos.values():
            alto_enemigo = enemigo.sprite[4]
            ancho_enemigo = enemigo.sprite[3]
            
            # Vamos a tener que hacer un pequeño ajuste en la y de los enemigos
            # Ya que las moscas son súper díficiles de matar
            
            # Comprobamos el pie izquierdo
            if (bloque.y + 2 <= enemigo.y + alto_enemigo <= bloque.y + 5 and
                bloque.x <= enemigo.x <= bloque.x + 16):

                enemigos_golpeados.append(enemigo)
            
            # Comprobamos el pie derecho    
            elif (bloque.y + 2 <= enemigo.y + alto_enemigo <= bloque.y + 5 and
                bloque.x <= enemigo.x  + ancho_enemigo <= bloque.x + 16):

                enemigos_golpeados.append(enemigo)
            
        return enemigos_golpeados

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
        return self.__sprites[self.__animacion]

    @property
    def direccion(self) -> int:
        """Dirección de Mario"""
        return self.__direccion

    @property
    def animacion_muerto(self) -> bool:
        """Está la animación de muerte de Mario activa"""
        return self.__animacion_muerto

    @property
    def godmode(self) -> bool:
        """Godmode de Mario"""
        return self.__godmode

    @godmode.setter
    def godmode(self, godmode: bool):
        if type(godmode) != bool:
            raise TypeError("El godmode debe ser un booleano")

        self.__godmode = godmode
    
    @y.setter
    def y(self, y: Union[int, float]):
        if type(y) != int and type(y) != float:
            raise TypeError("La posicion y debe ser un int o un float")
        
        self.__y = y