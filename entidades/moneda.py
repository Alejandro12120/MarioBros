import config
from .bloque import Bloque
from typing import Optional

class Moneda:
    def __init__(self, x: int, y: int, direccion: int, bloques: dict[Bloque]):
        """Este método creará una moneda
        
        @param x: es la posicion x de inicio de la moneda
        @param y: es la posicion y de inicio de la moneda
        @param direccion: es un int para almacenar la dirección, -1 si va a la izquierda, 1 si va a la derecha
        @param bloques: es un diccionario con los bloques del tablero
        """
        
        self.__id = id(self)
        
        self.__x = x
        self.__y = y
        self.__direccion = direccion
        self.__bloques = bloques
        
        self.__animacion = 0
        
        self.__sprites = config.MONEDA_SPRITE
        
        # Atributo para parar la animación, se utiliza cuando se obtiene una moneda
        self.__parar = False
        
        # Aceleración en el eje x
        self.__aceleracion_x = 1.7
        self.__velocidad_y = 0

        self.__gravedad = 0.4
    
    def move(self, alto: int, ancho: int):
        """Este método mueve la moneda
        
        @param ancho: es el ancho del tablero
        @param alto: es el alto del tablero
        """
        
        self.move_x(ancho)
        
        # Implementacion de la gravedad
        self.move_y(alto)
    
    def move_x(self, ancho: int):
        """Este método mueve la moneda horizontalmente
        
        @param ancho: es el ancho del tablero
        """
        
        # Si la moneda está cayendo no se moverá
        if self.__velocidad_y > 0:
            return
        
        # Las monedas se mueven como Mario
        # Actualizamos la x de la moneda
        self.__x += self.__direccion * self.__aceleracion_x

        # Si se sale por la derecha, aparece por la izquierda
        if self.__direccion == 1 and self.__x + self.sprite[3] >= ancho:
            self.__x = 0
        # Si se sale por la izquierda, aparece por la derecha
        elif self.__direccion == -1 and self.__x <= 0:
            self.__x = ancho - self.sprite[3]

        # La animación la controla el tablero
    
    def move_y(self, alto: int):
        """Este método mueve la moneda verticalmente, como la moneda no salta, solo se mueve por la gravedad
        
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
            self.__y = bloque_golpeado_inferior.y + 5 - self.sprite[4]
        
        # No puede salirse ni por arriba ni por abajo
        # Si la velocidad es negativa significa que va hacia arriba
        # Si la velocidad es positiva significa que va hacia abajo
        if self.__velocidad_y < 0 and self.__y <= 0:
            self.__y = 0
        elif self.__velocidad_y > 0 and self.toca_borde(alto):
            self.__velocidad_y = 0  # Reiniciamos la velocidad
            self.__y = alto - self.sprite[4]  # Cambiamos su posición y

        self.__y += self.__velocidad_y
    
    def animar(self) -> bool:
        """Animar la moneda
        
        @return: True si la animación ha terminado y debe eliminarse la moneda, False si no
        """
        
        self.__animacion += 1
        
        if self.__animacion >= len(self.__sprites):
            if self.__parar:
                self.__animacion = len(self.__sprites) - 1
                
                return True
            else:
                self.__animacion = 0
        
        return False
                
    def obtener(self):
        """Ejecuta la animación de obtención de una moneda"""
        
        self.__sprites = config.MONEDA_BRILLO_SPRITE
        
        self.__parar = True
        
    
    def toca_suelo(self, alto: int) -> bool:
        """Este método comprueba si la moneda toca el suelo

        @param alto: es el alto del tablero
        @return: True si toca el suelo, False si no
        """

        return (
                self.toca_borde(alto)
                or self.obtener_bloque_golpeado() is not None
        )

    def toca_borde(self, alto: int) -> bool:
        """Este método comprueba si la moneda está tocando el borde"""

        alto_moneda = self.sprite[4]

        if self.__y + alto_moneda >= alto:
            return True

        return False

    def obtener_bloque_golpeado(self, inferiormente=True) -> Optional[Bloque]:
        """Este método obtiene el bloque que golpea la moneda

        @param inferiormente: es un bool para saber si se comprueba inferiormente, por defecto False
        @return: el bloque que golpea Mario, None si no golpea ningún bloque
        """
        alto_moneda = self.sprite[4]
        ancho_moneda = self.sprite[3]

        for bloque in self.__bloques.values():
            if bloque.tuberia:
                continue

            if inferiormente:
                if bloque.golpea(self.__x, self.__y + alto_moneda):
                    return bloque

                if bloque.golpea(self.__x + ancho_moneda, self.__y + alto_moneda):
                    return bloque
            else:
                if bloque.golpea(self.__x, self.__y):
                    return bloque

                if bloque.golpea(self.__x + ancho_moneda, self.__y):
                    return bloque

        return None
        
    @property
    def x(self):
        """Devuelve la posición x de la moneda"""
        return self.__x
    
    @property
    def y(self):
        """Devuelve la posición y de la moneda"""
        return self.__y    
        
    @property
    def sprite(self):
        """Devuelve el sprite de la moneda"""
        return self.__sprites[self.__animacion]

    @property
    def id(self):
        """Devuelve el id de la moneda"""
        return self.__id
        