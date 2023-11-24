class Enemigo:
    def __init__(self, x: int, y: int, dir: int, sprites: list):
        """Este método creará un enemigo

        @param x: es la posicion x de inicio del enemigo
        @param y: es la posicion y de inicio del enemigo
        @param dir: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param sprite: es una lista con los valores del sprite en forma de tupla (banco, u, v, ancho, alto)
        """

        # Guardamos una variable con el id del enemigo
        # Para poder identificarlo
        self.__id = id(self)

        self.__x = x
        self.__y = y
        self.__direccion = dir
        self.__tumbado = False
        
        self.__sprites = sprites

        # Variable para controlar si el enemigo está tocando el suelo
        # Es necesario para que pueda ser tumbado
        self.__tocando_suelo = False

    def tumbar(self):
        """Este método tumba al enemigo"""
        self.__tumbado = True

    def levantar(self):
        """Este método levanta al enemigo"""
        self.__tumbado = False

    def comprobar_si_toca_suelo(self):
        # TODO: Comprobar si el enemigo está tocando el suelo
        pass
    
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
    
