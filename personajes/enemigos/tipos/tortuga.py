from ..enemigo import Enemigo
import config


class Tortuga(Enemigo):
    def __init__(self, x: int, y: int, dir: int):
        """Este método creará una tortuga
        Características: se mueve como mario, necesita un golpe para darle la vuelta

        @param x: es la posicion x de inicio de la tortuga
        @param y: es la posicion y de inicio de la tortuga
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        """

        # Inicializamos la clase enemigo
        super().__init__(x, y, dir, config.CANGREJO_SPRITE)

        # Almacenamos el número de golpes que ha recibido
        self.__golpes_recibidos = 0

        # Almacenamos el número máximo de golpes que puede recibir
        self.__golpes_maximo = 1

    def move(self):
        """Como cada enemigo se mueve de una forma diferente, cada uno tendrá su propio método para moverse"""
        # Si el enemigo está tumbado no se moverá
        if not self.__tumbado:
            # Las tortugas se mueven como Mario
            # TODO: Hay que hacer que si sale del tablero aparezca en el otro lado
            self.__x += self.__direccion

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
