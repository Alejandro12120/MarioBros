from ..enemigo import Enemigo
import config


class Cangrejo(Enemigo):
    def __init__(self, x: int, y: int, dir: int, bloques: dict):
        """Este método creará un cangrejo
        Características: se mueve como mario, necesita un golpe para darle la vuelta

        @param x: es la posicion x de inicio del cangrejo
        @param y: es la posicion y de inicio del cangrejo
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param bloques: es un diccionario con los bloques del tablero
        """

        # Inicializamos la clase enemigo
        super().__init__(x, y, dir, config.CANGREJO_SPRITE, bloques, 1)

        # Almacenamos el número de golpes que ha recibido
        self.__golpes_recibidos = 0

        # Almacenamos el número máximo de golpes que puede recibir
        self.__golpes_maximo = 2

        # Almacenamos una variable para saber si el cangrejo está enfadado
        self.__enfadado = False

        # Aceleración en el eje x
        self.__aceleracion_x = 1
        self.__velocidad_y = 0

        self.__gravedad = 0.4
        
    def move(self, ancho: int, alto: int):
        # Como cada enemigo se mueve de una forma diferente, cada uno tendrá su propio método para moverse
        
        """Este método mueve al cangrejo
        
        @param ancho: es el ancho del tablero
        @param alto: es el alto del tablero
        """
        
        self.move_x(ancho)
        
        # Implementamos la gravedad
        self.move_y(alto)

    def move_x(self, ancho: int):
        # Si el enemigo está tumbado no se moverá
        # Si el enemigo está cayendo no se moverá
        if self.tumbado or self.__velocidad_y > 0:
            return

        # Las tortugas se mueven como Mario
        # Actualizamos la x del enemigo
        self.x += self.direccion * self.__aceleracion_x

        # Si se sale por la derecha, aparece por la izquierda
        if self.direccion == 1 and self.x >= ancho:
            self.x = 0
        # Si se sale por la izquierda, aparece por la derecha
        elif self.direccion == -1 and self.x <= 0:
            self.x = ancho

        self.animar()

        # El sprite no es necesario actualizarlo, ya que se actualiza en el getter

    def move_y(self, alto: int):
        """Este método mueve al cangrejo verticalmente, como los cangrejos no saltan, se asume que siempre será por gravedad

        @param alto: es el alto del tablero
        """
        
        if not self.toca_suelo(alto):
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
    
    def comprobar_si_ha_sido_tumbado(self):
        """Este método comprueba si el cangrejo ha sido tumbado"""
        if self.__golpes_recibidos >= self.__golpes_maximo:
            self.tumbar()
        else:
            # Si no ha sido tumbada, se enfada
            self.enfadarse()

    def recibir_golpe(self):
        """Este método hace que el cangrejo reciba un golpe"""
        self.__golpes_recibidos += 1
        # Comprobamos si ha sido tumbada
        self.comprobar_si_ha_sido_tumbado()

    def tumbar(self):
        """Este método, tumba al cangrejo, hacemos un override para cambiar el sprite"""
        super().tumbar()

        # Cambiamos los sprites
        self.sprites = config.CANGREJO_TUMBADO_SPRITE

    def levantar(self):
        """Este método levanta al cangrejo, hacemos un override para reiniciar al enemigo"""
        super().levantar()

        # Reiniciamos los golpes recibidos
        self.__golpes_recibidos = 0

        # Cambiamos los sprites
        self.sprites = config.CANGREJO_SPRITE

    def enfadarse(self):
        """Este método hace que el cangrejo se enfade"""
        self.__enfadado = True

        # Cambiamos los sprites
        self.sprites = config.CANGREJO_ENFADADO_SPRITE
