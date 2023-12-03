from typing import Optional
from entidades.bloque import Bloque
from ..enemigo import Enemigo
import config


class Mosca(Enemigo):
    def __init__(self, x: int, y: int, dir: int, bloques: dict):
        """Este método creará una mosca,
        Características: se mueven saltando, para golpearlos tienen que tocar la plataforma

        @param x: es la posicion x de inicio de la mosca
        @param y: es la posicion y de inicio de la mosca
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param bloques: es un diccionario con los bloques del tablero
        """

        # Inicializamos la clase enemigo
        super().__init__(x, y, dir,config.MOSCA_SPRITE, bloques, 2)

        # Almacenamos el numero de golpes que ha recibido
        self.__golpes_recibidos = 0

        # Almacenamos el numero maximo de golpes que puede recibir
        self.__golpes_maximo = 1

        # Almacenamos una variable para saber si la mosca está enfadada
        self.__enfadado = False

        # Aceleracon en el eje x
        self.__aceleracion_x = 1
        self.__velocidad_y = 0

        self.__gravedad = 0.1

    def move(self, ancho: int, alto: int):
        self.move_x(ancho)
        
        if self.toca_suelo(alto):
            self.saltar(alto)
        
        # Implementamos la gravedad
        self.move_y(alto)
        
        pass
    
    def move_x(self, ancho: int):
        # Si el enemigo está tumbado no se moverá
        # Si el enemigo está cayendo no se moverá
        if self.tumbado or self.__velocidad_y > 0:
            return
        
        # Las moscas se mueven como Mario pero además saltan
        # Actualizamos la x del enemigo
        self.x += self.direccion * self.__aceleracion_x
        
        # Si se sale por la derecha, aparece por la izquierda
        if self.direccion == 1 and self.x >= ancho:
            self.x = 0
            
        # Si se sale por la izquierda, aparece por la derecha
        elif self.direccion == -1 and self.x <= 0:
            self.x = ancho
            
        self.animar()
            
        # El sprite no es necesario actualizarlo porque se actualiza en el getter de la animación
    
    def move_y(self, alto: int, gravedad: bool = True):
        """Este método mueve la mosca verticalmente
        
        @param alto: es el alto del tablero
        @param gravedad: es un bool para saber si se aplica la gravedad, por defecto True
        """
        
        if gravedad and not self.toca_suelo(alto):
            self.__velocidad_y += self.__gravedad
            
        # Comprobamos de forma distinta si se golpea un bloque o si golpea un borde
        # Para ajustar la y en función de eso
        
        bloque_golpeado_inferior = self.obtener_bloque_golpeado(True)
        # En caso de golpear un bloque mientras el enemigo cae
        if self.__velocidad_y > 0 and bloque_golpeado_inferior is not None:
            self.__velocidad_y = 0  # Reiniciamos la velocidad

            # Ajustamos su posición y
            self.y = bloque_golpeado_inferior.y + 5 - self.sprite[4]
            
        # No puede salirse ni por arriba ni por abajo
        # Si la velocidad es negativa significa que va hacia arriba
        # Si la velocidad es positiva significa que va hacia abajo
        if self.__velocidad_y < 0 and self.y <= 0:
            self.y = 0
        elif self.__velocidad_y > 0 and self.toca_borde(alto):
            self.__velocidad_y = 0  # Reiniciamos la velocidad
            self.y = alto - self.sprite[4]  # Cambiamos su posición y

        self.y += self.__velocidad_y
    
    def saltar(self, alto: int):
        """Este método hará saltar a la mosca
        
        @param alto: es el alto del tablero
        """
        
        if self.tumbado: return
        
        self.__velocidad_y = -1.25
        self.move_y(alto, False)
    
    def comprobar_si_ha_sido_tumbado(self):
        """Este método comprueba si la mosca ha sido tumbada"""
        if self.__golpes_recibidos >= self.__golpes_maximo:
            self.tumbar()

    def recibir_golpe(self):
        """Este método hace que la mosca reciba un golpe"""
        self.__golpes_recibidos += 1
        # Comprobamos si ha sido tumbada
        self.comprobar_si_ha_sido_tumbado()

    def tumbar(self):
        """Este método, tumba a la mosca, hacemos un override para cambiar el sprite"""
        super().tumbar()

        # Cambiamos los sprites
        self.sprites = config.MOSCA_TUMBADA_SPRITE

    def levantar(self):
        """Este método levanta a la mosca, hacemos un override para reiniciar al enemigo"""
        super().levantar()  # Llamamos a la clase enemigo para levantarla

        # Reiniciamos los golpes recibidos
        self.__golpes_recibidos = 0

        # Cambiamos los sprites
        self.sprites = config.MOSCA_SPRITE
