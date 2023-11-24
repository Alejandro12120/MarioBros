from fase import Fase
import pyxel
import config


class Tablero:
    """Esta clase será la encargada de gestionar el tablero"""

    def __init__(self, ancho: int, alto: int):
        self.__ancho = ancho
        self.__alto = alto

        self.__fase = Fase(self)
        self.__puntuacion: int = 0

        # Esta lista contendrá dos tuplas con coordenadas x e y de donde saldrán los enemigos
        self.__spawner_enemigos = [(16, 5), (self.ancho - 16 - 12, 5)]

        # Nos creamos un booleano para dibujar las hitboxes de las plataformas
        self.__hitboxes = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_A):
            self.fase.mario.move(self.ancho, -1)
        if pyxel.btn(pyxel.KEY_D):
            self.fase.mario.move(self.ancho, 1)
        if pyxel.btn(pyxel.KEY_SPACE) and self.fase.mario.toca_suelo(self.alto):
            self.fase.mario.saltar(self.alto)
        if pyxel.btnp(pyxel.KEY_E):
            self.draw_hitboxes()

        # Implementación de la gravedad
        self.fase.mario.move_y(self.alto, gravedad=True)

        # elif pyxel.btn(pyxel.KEY_RIGHT):
        #     self.mario.move('right', self.width)
        # elif pyxel.btn(pyxel.KEY_LEFT):
        #     self.mario.move('left', self.width)

    def draw(self):
        pyxel.cls(0)

        # Dibujamos los bloques
        for bloque in self.fase.bloques.values():
            pyxel.blt(
                bloque.x,
                bloque.y,
                bloque.sprite[0],
                bloque.sprite[1],
                bloque.sprite[2],
                bloque.sprite[3],
                bloque.sprite[4],
                8,
            )
            if not bloque.tuberia:
                # Animamos las plataformas para devolveras a su estado inicial ya que no la forzamos
                bloque.animate()

        """Dibujamos la animación del texto de la fase"""
        pyxel.text(96, 80, "FASE " + str(self.fase.numero_fase), 7)

        if pyxel.frame_count > 120:  # 4 segundos (30 fps * 4)
            pyxel.text(
                96, 80, "FASE " + str(self.fase.numero_fase), 0
            )  # Lo pintamos de negro, para borrarlo

        """Dibujamos el numero de vidas"""
        pyxel.text(97, 0, str(self.fase.mario.vidas) + " HP", 4)

        """Dibujamos la puntuación"""
        pyxel.text(20, 0, str(self.__puntuacion) + " P", 10)

        """Dibujamos a Mario, teniendo en cuenta la dirección"""
        pyxel.blt(
            self.fase.mario.x,
            self.fase.mario.y,
            self.fase.mario.sprite[0],
            self.fase.mario.sprite[1],
            self.fase.mario.sprite[2],
            self.fase.mario.direccion * self.fase.mario.sprite[3],
            self.fase.mario.sprite[4],
            8,
        )
        
        """Dibujamos las hitboxes"""
        if self.__hitboxes:
            """Hitbox de mario"""
            # Tenemos que hacer un ajuste de +-1 para que mario pueda pasar por los huecos
            # Porque como el ancho de mario es 16, y justo los huecos son de 16, era muy dificil que pasase
            # Entonces con un ajuste de +-1 en la x, mario puede pasar por los huecos
            pyxel.rectb(self.fase.mario.x + 1, self.fase.mario.y, self.fase.mario.sprite[3] - 1, self.fase.mario.sprite[4], 7)
            
            """Hitboxes de los bloques"""
            for bloque in self.fase.bloques.values():
                if not bloque.tuberia:
                    pyxel.rectb(bloque.x, bloque.y + 5, 16, 5, 7)
            

    def draw_hitboxes(self):
        self.__hitboxes = not self.__hitboxes

    @property
    def ancho(self):
        return self.__ancho

    @property
    def alto(self):
        return self.__alto

    @property
    def fase(self):
        return self.__fase
