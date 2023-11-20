from personajes.mario import Mario
from entidades.bloque import Bloque


class Fase:
    def __init__(self, tablero):
        """Esta clase será la encargada de gestionar la fase
        :param tablero: es el tablero en el que se dibujará la fase
        """
        
        # Estos diccionarios actuará como visibilidad, es decir todo lo que estén en los diccionarios se dibujará
        # Además los ids de los objetos serán las claves de los diccionarios
        self.__bloques: dict = {}
        self.__enemigos: dict = {}
        self.__enemigos_de_la_fase: dict = {} # Este diccionario contendrá todos los enemigos que saldrán progresivamente

        self.__numero_fase: int = 1
        self.__mario: Mario = Mario(96, 107, 1)

        self.__tablero = tablero

        self.__iniciar_fase()

    def __iniciar_fase(self):
        """Cargamos los bloques"""

        # Tuberías
        tuberia_arriba_izquierda = Bloque(0, 4, True, True)
        self.bloques[tuberia_arriba_izquierda.id] = tuberia_arriba_izquierda

        tuberia_arriba_derecha = Bloque(self.__tablero.ancho - 16, 4, True, False)
        self.bloques[tuberia_arriba_derecha.id] = tuberia_arriba_derecha
        
        tuberia_abajo_izquierda = Bloque(0, self.__tablero.alto - 16, True, True)
        self.bloques[tuberia_abajo_izquierda.id] = tuberia_abajo_izquierda
        
        tuberia_abajo_derecha = Bloque(self.__tablero.ancho - 16, self.__tablero.alto - 16, True, False)
        self.bloques[tuberia_abajo_derecha.id] = tuberia_abajo_derecha
        
        # Plataformas
        
        # Primera linea de plataformas
        for i in range(13):
            if i == 6: continue # Hacemos que no se dibuje las plataformas de en medio
            
            plataforma = Bloque(i * 16, 16, False, False)
            self.bloques[plataforma.id] = plataforma
        
        # Las plataformas de en medio dan un poco más de dolor de cabeza
        # Porque no están alineadas, así que vamos a dibujar los extremos
        # que sí están alineados y luego las de en medio las dibujaremos a parte
        
        for i in range(13):
            if 2 <= i <= 10: continue
            
            plataforma = Bloque(i * 16, 64, False, False)
            self.bloques[plataforma.id] = plataforma
        
        for i in range(3, 10):
            
            plataforma = Bloque(i * 16, 56, False, False)
            self.bloques[plataforma.id] = plataforma
        
        # Ultima linea de plataformas
        for i in range(13):
            if 5 <= i <= 7: continue # Hacemos que no se dibuje las plataformas de en medio
            
            plataforma = Bloque(i * 16, 96, False, False)
            self.bloques[plataforma.id] = plataforma
        
        
    
    @property
    def bloques(self) -> dict:
        """Lista de bloques"""
        return self.__bloques

    @property
    def enemigos(self) -> dict:
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
