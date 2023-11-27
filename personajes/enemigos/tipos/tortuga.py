from ..enemigo import Enemigo
import config


class Tortuga(Enemigo):
    def __init__(self, x: int, y: int, dir: int, bloques: dict):
        """Este método creará una tortuga
        Características: se mueve como mario, necesita un golpe para darle la vuelta

        @param x: es la posicion x de inicio de la tortuga
        @param y: es la posicion y de inicio de la tortuga
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param bloques: es un diccionario con los bloques del tablero
        """

        # Inicializamos la clase enemigo
        super().__init__(x, y, dir, config.TORTUGA_SPRITE, bloques)

        # Almacenamos el número de golpes que ha recibido
        self.__golpes_recibidos = 0

        # Almacenamos el número máximo de golpes que puede recibir
        self.__golpes_maximo = 1
        
        # Aceleración en el eje x
        self.__aceleracion_x = 1
        self.__velocidad_y = 0
        
        self.__gravedad = 0.4

    def move_x(self, ancho: int):
        """Este método mueve la tortuga horizontalmente
        
        @param ancho: es el ancho del tablero
        """
        
        #Como cada enemigo se mueve de una forma diferente, cada uno tendrá su propio método para moverse
        # Si el enemigo está tumbado no se moverá
        if not self.tumbado:
            # Las tortugas se mueven como Mario
            # Actualizamos la x del enemigo
            self.x += self.direccion * self.__aceleracion_x

            # Si se sale por la derecha, aparece por la izquierda
            if self.direccion == 1 and self.x >= ancho:
                self.x = 0
            # Si se sale por la izquierda, aparece por la derecha
            elif self.direccion == -1 and self.x <= 0:
                self.x = ancho
            
            # Actualizamos la animación
            self.animacion += 1
            # Reiniciamos la animación si se ha pasado
            if self.animacion >= len(self.sprites):
                self.animacion = 0
            
            # El sprite no es necesario actualizarlo, ya que se actualiza en el getter 
    
    def move_y(self, alto: int):
        """Este método mueve la tortuga verticalmente, como las tortugas no saltan, se asume que siempre será por gravedad
        
        @param alto: es el alto del tablero
        """
        
        

    def comprobar_si_ha_sido_tumbado(self):
        """Este método comprueba si la tortuga ha sido tumbada"""
        if self.__golpes_recibidos >= self.__golpes_maximo:
            self.tumbar()

    def recibir_golpe(self):
        """Este método hace que la tortuga reciba un golpe"""
        self.__golpes_recibidos += 1
        # Comprobamos si ha sido tumbada
        self.comprobar_si_ha_sido_tumbado()

    def tumbar(self):
        """Este método, tumba a la tortuga, hacemos un override para cambiar el sprite"""
        super().tumbar()

        # Cambiamos los sprites
        self.sprites = config.TORTUGA_TUMBADA_SPRITE

    def levantar(self):
        """Este método levanta a la tortuga, hacemos un override para reiniciar al enemigo"""
        super().levantar()  # Llamamos a la clase enemigo para levantarla

        # Reiniciamos los golpes recibidos
        self.__golpes_recibidos = 0
        
        # Cambiamos los sprites
        self.sprites = config.CANGREJO_SPRITE
