import config
import pyxel
from tablero import Tablero

tablero = Tablero(config.ANCHO, config.ALTO)

# Inicializamos la pantalla del juego
# 30 fps, esto habrá que tenerlo en cuenta para los movimientos, animaciones, etc
pyxel.init(tablero.ancho, tablero.alto, title="Super Mario Bros", fps=30)

# Cargamos los assets
pyxel.load("assets/characters.pyxres") # Personajes banco 0 Bloques banco 1
# pyxel.load("assets/bloques.pyxres") # Bloques

# Iniciamos el juego
pyxel.run(tablero.update, tablero.draw)