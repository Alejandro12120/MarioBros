"""
Módulo en el que se configuran
las diferentes constantes
"""

# Tamaño de la pantalla
ANCHO = 208
ALTO = 128

"""Vamos a utilizar un algoritmo de generación de enemigos
personalizado. Se puede configurar con los siguientes parámetros:
"""
# Este parámetro multiplicado por el numero de ronda actual, dará lugar al
# numero de enemigos que aparecerán durante la ronda.
# Además si ese resultado es mayor o igual que los paramétros
# de a continuación, aparecerá los distintos enemigos
MULTIPLICADOR_ENEMIGOS = 4
# Si el resultado es mayor o igual a este número, durante la ronda
# podrán aparecer tortugas de forma aleatoria
APARICION_TORTUGA = 4
# Si el resultado es mayor o igual a este número, durante la ronda
# podrán aparecer cangrejos de forma aleatoria
APARICION_CANGREJO = 8
# Si el resultado es mayor o igual a este número, durante la ronda
# podrán aparecer moscas de forma aleatoria
APARICION_MOSCAS = 12


"""
Aquí vamos a definir los sprites
Si el sprite es una lista, es que tiene animación
Los sprites se almacenan en tuplas de 5 elementos
    - Banco
    - Posición x
    - Posición y
    - Ancho
    - Alto
Los personajes están en el banco 0
Los bloques están en el banco 1
Los elementos de la pantalla inicial están en el banco 2
"""

# Elementos de la pantalla inicial
TECLAS_AD = (2, 0, 0, 21, 16)
FLECHAS = (2, 0, 16, 21, 16)
ESPACIO = (2, 0, 32, 41, 16)
ESPACIO_SOLO = (2, 0, 32, 24, 16)

# Monedas
MONEDA_SPRITE = [(0, 0, 184, 7, 11), 
                 (0, 8, 184, 8, 11),
                 (0, 16, 184, 8, 11),
                 (0, 24, 184, 7, 11)]

MONEDA_BRILLO_SPRITE = [(0, 32, 184, 16, 16),
                        (0, 48, 184, 16, 16),
                        (0, 128, 0, 16, 16)]

# Bloques, los bloques están en el banco 1
TUBERIA_DERECHA = (1, 0, 0, 16, 16)  # ampliable en ancho hasta 32
TUBERIA_IZQUIERDA = (1, 16, 16, 16, 16)  # ampliable en ancho hasta 32

PLATAFORMA = [(1, 0, 32, 16, 16),
              (1, 16, 32, 16, 16),
              (1, 32, 32, 16, 16),
              (1, 48, 32, 16, 16)]

POW = [(0, 0, 216, 16, 13),
       (0, 16, 216, 16, 9),
       (0, 32, 216, 16, 5)]

# Mario
INICIAL_MARIO = (0, 240)
MARIO_SPRITE = [(0, 0, 0, 16, 21),
                (0, 16, 0, 16, 21),
                (0, 32, 0, 16, 21),
                (0, 48, 0, 16, 21)]
MARIO_MUERTO_SPRITE = [(0, 0, 48, 16, 21),
                       (0, 16, 48, 16, 21),
                       (0, 32, 48, 16, 21),
                       (0, 48, 48, 16, 21)]

# Enemigo
TORTUGA_SPRITE = [(0, 0, 72, 16, 16),
                  (0, 16, 72, 16, 16),
                  (0, 32, 72, 16, 16)]

TORTUGA_TUMBADA_SPRITE = [(0, 48, 72, 16, 16),
                          (0, 64, 72, 16, 16)]

TORTUGA_COLOR_SPRITE = [(0, 80, 72, 16, 16),
                        (0, 96, 72, 16, 16),
                        (0, 112, 72, 16, 16)]

TORTUGA_COLOR_TUMBADA_SPRITE = [(0, 128, 72, 16, 16),
                                (0, 144, 72, 16, 16)]

CANGREJO_SPRITE = [(0, 0, 136, 16, 16),
                   (0, 16, 136, 16, 16),
                   (0, 32, 136, 16, 16)]

CANGREJO_ENFADADO_SPRITE = [(0, 64, 136, 16, 16),
                            (0, 80, 136, 16, 16),
                            (0, 96, 136, 16, 16)]

CANGREJO_TUMBADO_SPRITE = [(0, 112, 136, 16, 16),
                           (0, 128, 136, 16, 16)]

CANGREJO_COLOR_SPRITE = [(0, 0, 152, 16, 16),
                         (0, 16, 152, 16, 16),
                         (0, 32, 152, 16, 16)]

CANGREJO_COLOR_ENFADADO_SPRITE = [(0, 64, 152, 16, 16),
                                  (0, 80, 152, 16, 16),
                                  (0, 96, 152, 16, 16)]

CANGREJO_COLOR_TUMBADO_SPRITE = [(0, 112, 152, 16, 16),
                                 (0, 128, 152, 16, 16)]


MOSCA_SPRITE = [(0, 0, 104, 16, 15),
                (0, 16, 104, 16, 15),
                (0, 32, 104, 16, 15)]

MOSCA_TUMBADA_SPRITE = [(0, 48, 104, 16, 15),
                        (0, 64, 104, 16, 15)]

MOSCA_COLOR_SPRITE = [(0, 0, 120, 16, 15),
                      (0, 16, 120, 16, 15),
                      (0, 32, 120, 16, 15)]

MOSCA_COLOR_TUMBADA_SPRITE = [(0, 48, 120, 16, 15),
                              (0, 64, 120, 16, 15)]
