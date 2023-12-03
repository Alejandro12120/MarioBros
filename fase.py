import random

from personajes.mario import Mario
from entidades.bloque import Bloque
from personajes.enemigos.enemigo import Enemigo
from personajes.enemigos.tipos.cangrejo import Cangrejo
from personajes.enemigos.tipos.tortuga import Tortuga
from personajes.enemigos.tipos.mosca import Mosca

class Fase:
    def __init__(self, tablero):
        """Esta clase será la encargada de gestionar la fase
        @param tablero: es el tablero en el que se dibujará la fase
        """

        # Estos diccionarios actuará como visibilidad, es decir todo lo que estén en los diccionarios se dibujará
        # Además los ids de los objetos serán las claves de los diccionarios
        self.__bloques: dict[int, Bloque]  = {}
        self.__enemigos: dict[int, Enemigo]  = {}
        self.__enemigos_de_la_fase: dict[int, Enemigo] =  {} # Este diccionario contendrá todos los enemigos que saldrán progresivamente

        self.__numero_fase: int = 1
        self.__mario: Mario = Mario(96, 107, self.__bloques, self.__enemigos, 1)

        self.__tablero = tablero

        self.__iniciar_fase()

    def __iniciar_fase(self):
        """Cargamos los bloques"""

        # Tuberías
        tuberia_arriba_izquierda = Bloque(0, 4, "TUBERIA_IZQ")
        self.bloques[tuberia_arriba_izquierda.id] = tuberia_arriba_izquierda

        tuberia_arriba_derecha = Bloque(self.__tablero.ancho - 16, 4, "TUBERIA_DER")
        self.bloques[tuberia_arriba_derecha.id] = tuberia_arriba_derecha

        tuberia_abajo_izquierda = Bloque(0, self.__tablero.alto - 16, "TUBERIA_IZQ")
        self.bloques[tuberia_abajo_izquierda.id] = tuberia_abajo_izquierda

        tuberia_abajo_derecha = Bloque(self.__tablero.ancho - 16, self.__tablero.alto - 16, "TUBERIA_DER")
        self.bloques[tuberia_abajo_derecha.id] = tuberia_abajo_derecha

        # Plataformas

        # Primera linea de plataformas
        for i in range(13):
            if i == 6:
                continue  # Hacemos que no se dibuje las plataformas de en medio

            plataforma = Bloque(i * 16, 18, "PLATAFORMA")
            self.bloques[plataforma.id] = plataforma

        # Las plataformas de en medio dan un poco más de dolor de cabeza
        # Porque no están alineadas, así que vamos a dibujar los extremos
        # que sí están alineados y luego las de en medio las dibujaremos a parte

        for i in range(13):
            if 2 <= i <= 10:
                continue

            plataforma = Bloque(i * 16, 64, "PLATAFORMA")
            self.bloques[plataforma.id] = plataforma

        for i in range(3, 10):
            plataforma = Bloque(i * 16, 56, "PLATAFORMA")
            self.bloques[plataforma.id] = plataforma

        # Ultima linea de plataformas
        for i in range(13):
            if 5 <= i <= 7:
                continue  # Hacemos que no se dibuje las plataformas de en medio

            plataforma = Bloque(i * 16, 96, "PLATAFORMA")
            self.bloques[plataforma.id] = plataforma
        
        # Bloque POW
        pow = Bloque(96, 96, "POW")
        self.bloques[pow.id] = pow

        """Cargamos los enemigos"""

        # Vamos a meter todos los enemigos en self.__enemigos_de_la_fase
        # Se generarán de forma aleatoria
        # Y se irán pasando a self.__enemigos para ser dibujados

        # Generamos 30 enemigos
        for i in range(30):
            # Les metemos una posición especial -1, -1, que indicará que se generen en el spawner
            # Le metemos una dirección 0, ya que dependerá del lado en el que se generen
            # Entonces cuando los generemos, les asignaremos una posición y una dirección
            num = random.randint(0, 2)
            if num == 0:
                enemigo = Cangrejo(-1, -1, 0, self.bloques)
            elif num == 1:
                enemigo = Tortuga(-1, -1, 0, self.bloques)
            else:
                enemigo = Mosca(-1, -1, 0, self.bloques)
            
            self.__enemigos_de_la_fase[enemigo.id] = enemigo

    def spawnear_enemigo(self, spawner: tuple):
        """Este método se encargará de spawnear un enemigo de forma aleatoria"""

        # Si no quedan enemigos, no hacemos nada
        if len(self.__enemigos_de_la_fase) == 0:
            return

        # Obtenemos el primer enemigo del diccionario de enemigos de la fase, y lo metemos en el diccionario de enemigos
        # para que se dibuje

        # Obtenemos el primer enemigo del diccionario
        enemigo = self.__enemigos_de_la_fase.popitem()[1]

        # Si es el spawner de la izquierda, le asignamos la dirección 1
        # Si es el spawner de la derecha, le asignamos la dirección -1
        if spawner[0] == 16:
            enemigo.direccion = 1
        else:
            enemigo.direccion = -1
            
        # Le asignamos la posición del spawner
        enemigo.x = spawner[0]
        enemigo.y = spawner[1]
        
        # Lo metemos en el diccionario de enemigos
        self.__enemigos[enemigo.id] = enemigo
        # Lo eliminamos del diccionario de enemigos de la fase
        del enemigo
    
    def despawnear_enemigo(self, id: int, respawn: bool = False):
        """Este método se encargará de despawnear un enemigo"""
        
        # Si el enemigo no está spawneado, no hacemos nada
        if id not in self.__enemigos:
            return
        
        enemigo = self.__enemigos[id]
        
        if respawn:
            # Si queremos que el enemigo se vuelva a spawnear, lo metemos en el diccionario de enemigos de la fase
            self.__enemigos_de_la_fase[enemigo.id] = enemigo
        
        del self.__enemigos[id] # Lo despawneamos, es decir lo eliminamos del diccionario de enemigos

    @property
    def bloques(self) -> dict[int, Bloque]:
        """Lista de bloques"""
        return self.__bloques

    @property
    def enemigos(self) -> dict[int, Enemigo]:
        """Lista de enemigos"""
        return self.__enemigos

    @property
    def numero_fase(self) -> int:
        """Numero de fase"""
        return self.__numero_fase

    @property
    def mario(self) -> Mario:
        """Mario"""
        return self.__mario
