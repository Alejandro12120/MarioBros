from enemigo import Enemigo
import config

class Cangrejo(Enemigo):
    def __init__(self, x: int, y: int, dir: int):
        """Este método creará un cangrejo
        Características: se mueve como mario, necesita un golpe para darle la vuelta

        :param x: es la posicion x de inicio del cangrejo
        :param y: es la posicion y de inicio del cangrejo
        :param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        """

        # Inicializamos la clase enemigo
        super().__init__(x, y, dir, config.CANGREJO_SPRITE)
        
        # Almacenamos el número de golpes que ha recibido
        self.__golpes_recibidos = 0

        # Almacenamos el número máximo de golpes que puede recibir
        self.__golpes_maximo = 2
        
        # Almacenamos una variable para saber si el cangrejo está enfadado
        self.__enfadado = False
    
    def move(self):
        """Como cada enemigo se mueve de una forma diferente, cada uno tendrá su propio método para moverse"""
        
        # Si el enemigo está tumbado no se moverá
        if not self.tumbado:
            # Los cangrejos se mueven como Mario
            # TODO: Hay que hacer que si sale del tablero aparezca en el otro lado
            # TODO: si el cangrejo está enfadado se mueve más rápido y cambia el sprite
            self.__x += self.__direccion
    
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
    
            
        
        
        
        
    