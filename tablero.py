from fase import Fase
import pyxel
import random
import config


class Tablero:
    """Esta clase será la encargada de gestionar el tablero"""

    def __init__(self, ancho: int, alto: int):
        self.__ancho = ancho
        self.__alto = alto

        self.__fase = Fase(self)
        self.__puntuacion: int = 0

        # Esta lista contendrá dos tuplas con coordenadas x e y de donde saldrán los enemigos
        self.__spawner_enemigos = [(16, 7), (self.ancho - 16 - 12, 7)]

        # Esta lista contendrá dos tuplas con coordenadas x e y de donde desaparecerán los enemigos
        self.__despawn_enemigos = [
            (16, self.alto - 16), (self.ancho - 16 - 12, self.alto - 16)]

        # Nos creamos un booleano para dibujar las hitboxes
        self.__hitboxes = False

        # Nos creamos una variable para saber si el juego ha terminado
        self.__fin_juego = False

        # Nos creamos una variable para controlar si estamos en la pantalla de inicio
        self.__inicio_juego = True
        # Frames inicio juego
        self.__frames_inicio_juego = 0

    def update(self):
        # Controles:
        # Q: Salir del juego
        # A o flecha izquierda: Mover a Mario a la izquierda
        # D o flecha derecha: Mover a Mario a la derecha
        # ESPACIO o flecha arriba: Hacer saltar a Mario
        # E: Mostrar las hitboxes
        # G: Activar godmode
        # M: Spawnear una moneda

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(key=pyxel.KEY_SPACE) and self.__inicio_juego:
            # Iniciamos la fase
            self.__fase.iniciar_fase()

            # Quitamos la pantalla de inicio
            self.__inicio_juego = False
            
            # Nos guardamos el frame en el que se ha pulsado el espacio, para luego hacer calculos de tiempo
            self.__frames_inicio_juego = pyxel.frame_count

        # Si el juego ha terminado solo nos interesa la Q para salir
        # Si el juego aun no ha empezado, solo nos interesa el espacio para empezar
        if self.__fin_juego or self.__inicio_juego:
            return

        # Si estamos en la animación de muerte de Mario, no podemos hacer nada
        if not self.fase.mario.animacion_muerto:
            if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT):
                self.fase.mario.move_x(self.ancho, -1)
            if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
                self.fase.mario.move_x(self.ancho, 1)
            if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.KEY_UP)) and self.fase.mario.toca_suelo(self.alto):
                self.fase.mario.saltar(self.alto, pyxel.frame_count)
            if pyxel.btnp(pyxel.KEY_E):
                self.draw_hitboxes()
            if pyxel.btnp(pyxel.KEY_G):
                self.fase.mario.godmode = not self.fase.mario.godmode
            if pyxel.btnp(pyxel.KEY_M):
                self.fase.spawnear_moneda(
                    random.choice(self.__spawner_enemigos))

        # Implementación de la gravedad
        self.fase.mario.move_y(self.alto, pyxel.frame_count, gravedad=True)

        # Animaciones de la muerte de Mario
        if self.fase.mario.animacion_muerto:
            # Cada 15 segundos cambiamos el sprite
            if pyxel.frame_count % 15 == 0:
                self.fase.mario.animar(True)

            self.fase.mario.y += 3

            # Si Mario sale, del tablero, la animación termina
            if self.fase.mario.y >= self.__alto:
                self.fase.mario.terminar_animacion_muerte()

        a_despawnear = []

        # Animaciones de la muerte de los enemigos
        for enemigo in self.fase.enemigos.values():
            if enemigo.animacion_muerto:
                # Movemos al enemigo hacia los lados en función de la dirección del golpe
                if enemigo.direccion_golpe == 1:
                    enemigo.x += 3
                else:
                    enemigo.x -= 3
                    
                # Si el enemigo sale del borde, finalmente es eliminado
                if enemigo.x < 0 or enemigo.x > self.ancho:
                    a_despawnear.append(enemigo.id)

        for id in a_despawnear:
            # 100 puntos por matar a un enemigo
            self.__puntuacion += 100

            # Eliminamos finalmente al enemigo
            self.fase.despawnear_enemigo(id, False)

        # Cada 4 segundos (30 fps * 4) se generará un enemigo
        # En el segundo 0 no se generará nada
        if (pyxel.frame_count % 120 == 0 and 
            pyxel.frame_count != 0):
            self.fase.spawnear_enemigo(
                self.__spawner_enemigos[random.randint(0, 1)])

        # Movimiento de los enemigos, y animaciones de los enemigos tumbados
        # Despawn de los enemigos
        # Levantamiento automático de los enemigos
        # Colisiones con mario

        a_despawnear = []

        for enemigo in self.fase.enemigos.values():
            # Llamamos al método específico de movimiento de cada enemigo
            enemigo.move(self.ancho, self.alto)
            # Llamamos al método animar de cada enemigo, solo en caso de que esté tumbado
            if enemigo.tumbado:
                # Le metemos un delay de 20 frames para que no se mueva tan rápido
                # 20 frames son 0,6 segundos
                if pyxel.frame_count % 20 == 0:
                    enemigo.animar()

                # Si han pasado 10 segundos desde que se tumbó, se levanta y cambia color
                # 300 frames son 10 segundos (30 fps * 10 segundos)
                if enemigo.frames_tumbado + 300 == pyxel.frame_count:
                    enemigo.levantar()
                    enemigo.cambiar_color()

            # Despawn de los enemigos
            if enemigo.x < self.__despawn_enemigos[0][0] or enemigo.x > self.__despawn_enemigos[1][0]:
                if enemigo.y == self.__despawn_enemigos[0][1] or enemigo.y == self.__despawn_enemigos[1][1]:
                    a_despawnear.append(enemigo.id)

            # Colisiones con mario, en caso de que no esté en godmode
            if not self.fase.mario.godmode:
                # Obtenemos x en función de la dirección y con la corrección de hitbox
                if self.fase.mario.direccion == 1:
                    # La x si vamos para la derecha será igual al ancho menos 1, por la hitbox
                    x_hitbox = self.fase.mario.x + self.fase.mario.sprite[3] - 1
                else:
                    # La x si vamos para la izquierda será igual menos 1 por la hitbox
                    x_hitbox = self.fase.mario.x + 1

                # Comprobamos si golpea con la cabeza o con los pies
                if enemigo.golpea(x_hitbox, self.fase.mario.y) or enemigo.golpea(x_hitbox, self.fase.mario.y + self.fase.mario.sprite[4]):
                    # TODO: Patear enemigos tumbados
                    if enemigo.tumbado:
                        enemigo.matar(self.fase.mario.direccion)
                    else:
                        self.fase.mario.matar()

        for id in a_despawnear:
            self.fase.despawnear_enemigo(id, True)

        # Todo lo relacionado con los bloques
        a_eliminar = []

        for bloque in self.fase.bloques.values():
            if bloque.pow and bloque.animacion == -1:
                # Si el bloque pow ha terminado su animación, lo eliminamos de los bloques
                a_eliminar.append(bloque.id)
                continue

            if not bloque.tuberia and not bloque.pow:
                # Animamos las plataformas para devolveras a su estado inicial ya que no la forzamos
                bloque.animar()

            # Actualizamos los bloques no golpeables cada 0.5 segundos (30 fps * 0.5)
            if pyxel.frame_count % 15 == 0:
                if not bloque.golpeable:
                    bloque.golpeable = True

        # Eliminamos los bloques pow
        for id in a_eliminar:
            del self.fase.bloques[id]

        # Monedas

        a_eliminar.clear()

        for moneda in self.fase.monedas.values():
            # Movemos a la moneda
            moneda.move(self.alto, self.ancho)

            # La animamos
            # Y si devuelve true, la eliminamos
            if moneda.animar():
                a_eliminar.append(moneda.id)

            # Colisiones de Mario con las monedas
            if (not self.fase.mario.godmode and 
                not self.fase.mario.animacion_muerto and 
                not moneda.eliminar):
                # Obtenemos x en función de la dirección y con la corrección de hitbox
                if self.fase.mario.direccion == 1:
                    # La x si vamos para la derecha será igual al ancho menos 1, por la hitbox
                    x_hitbox = self.fase.mario.x + self.fase.mario.sprite[3] - 1
                else:
                    # La x si vamos para la izquierda será igual menos 1 por la hitbox
                    x_hitbox = self.fase.mario.x + 1

                # Comprobamos si golpea con la cabeza o con los pies
                if (moneda.golpea(x_hitbox, self.fase.mario.y) or 
                    moneda.golpea(x_hitbox, self.fase.mario.y + self.fase.mario.sprite[4])):
                    # Eliminamos la moneda
                    moneda.obtener()

                    # Sumamos 100 puntos
                    self.__puntuacion += 100

            # Despawn de las monedas
            if moneda.x < self.__despawn_enemigos[0][0] or moneda.x > self.__despawn_enemigos[1][0]:
                # Hacemos un ajuste de +5 porque la moneda es más baja que los enemigos
                if moneda.y - 5 == self.__despawn_enemigos[0][1] or moneda.y - 5 == self.__despawn_enemigos[1][1]:
                    a_eliminar.append(moneda.id)

        # Eliminamos las monedas
        for id in a_eliminar:
            del self.fase.monedas[id]

        # Fin de la fase/nivel
        if len(self.fase.enemigos_de_la_fase) == 0 and len(self.fase.enemigos) == 0:
            # Mil puntos por completar la fase
            self.__puntuacion += 1000

            # Terminamos la fase
            self.__fase.terminar_fase(True)

            # Nos creamos una nueva fase
            self.__fase = Fase(self, self.fase.numero_fase + 1)

            # La iniciamos
            self.__fase.iniciar_fase()
            self.__frames_inicio_juego = pyxel.frame_count

        # Fin del juego
        if self.fase.mario.vidas == 0:
            self.__fin_juego = True

            # Terminamos la fase
            self.__fase.terminar_fase()

    def draw(self):
        # Aqui vamos a controlar las distintas pantallas del juego
        # Pantalla de inicio
        if self.__inicio_juego:
            pyxel.cls(0)

            pyxel.text(70, 16, "SUPER MARIO BROS", 8)

            pyxel.text(85, 36, "CONTROLES", 12)

            pyxel.blt(20, 46, config.TECLAS_AD[0], config.TECLAS_AD[1],
                      config.TECLAS_AD[2], config.TECLAS_AD[3], config.TECLAS_AD[4], 8)

            pyxel.blt(43, 46, config.FLECHAS[0], config.FLECHAS[1], config.FLECHAS[2],
                      config.FLECHAS[3], config.FLECHAS[4], 8)

            pyxel.text(20, 63, "MOVER A MARIO", 7)

            pyxel.blt(140, 50, config.ESPACIO[0], config.ESPACIO[1], config.ESPACIO[2],
                      config.ESPACIO[3], config.ESPACIO[4], 8)
            pyxel.text(140, 63, "SALTAR", 7)

            pyxel.text(60, 100, "PULSA         PARA EMPEZAR", 14)

            pyxel.blt(85, 98, config.ESPACIO_SOLO[0], config.ESPACIO_SOLO[1], config.ESPACIO_SOLO[2],
                      config.ESPACIO_SOLO[3], config.ESPACIO_SOLO[4], 8)

        # Pantalla de fin de juego
        elif self.__fin_juego:
            pyxel.cls(0)
            pyxel.text(70, 26, "FIN DE LA PARTIDA", 8)
            pyxel.text(90, 46, str(self.__puntuacion) + " puntos", 10)
            pyxel.text(5, 120, "Pulsa Q para salir", 14)
        # Pantalla de juego
        else:
            pyxel.cls(0)

            """Dibujamos los bloques"""
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

            """Dibujamos la animación del texto de la fase"""
            pyxel.text(93, 80, "FASE " + str(self.fase.numero_fase), 7)

            if pyxel.frame_count - self.__frames_inicio_juego > 120:  # 4 segundos (30 fps * 4)
                pyxel.text(
                    93, 80, "FASE " + str(self.fase.numero_fase), 0
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

            """Dibujamos los enemigos"""
            for enemigo in self.fase.enemigos.values():
                pyxel.blt(
                    enemigo.x,
                    enemigo.y,
                    enemigo.sprite[0],
                    enemigo.sprite[1],
                    enemigo.sprite[2],
                    enemigo.direccion * enemigo.sprite[3],
                    enemigo.sprite[4],
                    8,
                )

            """Dibujamos las monedas"""
            for moneda in self.fase.monedas.values():
                pyxel.blt(
                    moneda.x,
                    moneda.y,
                    moneda.sprite[0],
                    moneda.sprite[1],
                    moneda.sprite[2],
                    moneda.sprite[3],
                    moneda.sprite[4],
                    8,
                )

            """Dibujamos las hitboxes"""
            if self.__hitboxes:
                """Hitbox de mario"""
                # Tenemos que hacer un ajuste de +-1 para que mario pueda pasar por los huecos
                # Porque como el ancho de mario es 16, y justo los huecos son de 16, era muy dificil que pasase
                # Entonces con un ajuste de +-1 en la x, mario puede pasar por los huecos

                # Si mario está en godmode no tiene hitbox, o si está con la animación de muerte
                if not self.fase.mario.godmode and not self.fase.mario.animacion_muerto:
                    pyxel.rectb(
                        self.fase.mario.x + 1,
                        self.fase.mario.y,
                        self.fase.mario.sprite[3] - 1,
                        self.fase.mario.sprite[4],
                        7,
                    )

                """Hitboxes de los bloques"""
                for bloque in self.fase.bloques.values():
                    if not bloque.tuberia and not bloque.pow:
                        pyxel.rectb(bloque.x, bloque.y + 5, 16, 5, 7)

                    if bloque.pow:
                        pyxel.rectb(bloque.x, bloque.y, 16,
                                    bloque.sprite[4], 7)

                """Hitboxes de los enemigos"""
                # Tenemos que hacer el mismo ajuste que con mario, aunque depende del enemigo
                for enemigo in self.fase.enemigos.values():
                    # Si el enemigo está con la animación de muerte no tiene hitbox
                    if not enemigo.animacion_muerto:
                        pyxel.rectb(enemigo.x + enemigo.hitbox, enemigo.y, enemigo.sprite[3] - enemigo.hitbox,
                                    enemigo.sprite[4], 7)

                """Hitbox de las monedas"""
                for moneda in self.fase.monedas.values():
                    pyxel.rectb(moneda.x, moneda.y,
                                moneda.sprite[3], moneda.sprite[4], 7)

            """Dibujamos el texto de godmode"""
            if self.fase.mario.godmode:
                pyxel.text(90, 34, "GODMODE", 3)

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
