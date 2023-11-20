"""
Módulo en el que se configuran
las diferentes constantes
"""

# Tamaño de la pantalla
ANCHO = 208
ALTO = 128

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
"""

# Bloques, los bloques están en el banco 1
TUBERIA_DERECHA = (1, 0, 0, 16, 16)  # ampliable en ancho hasta 32
TUBERIA_IZQUIERDA = (1, 16, 16, 16, 16)  # ampliable en ancho hasta 32

PLATAFORMA = (1, 0, 32, 16, 16)
PLATAFORMA_GOLPEADA = [(1, 16, 32, 16, 16),
                       (1, 32, 32, 16, 16),
                       (1, 48, 32, 16, 16)]

# Mario
INICIAL_MARIO = (0, 240)
# TODO: Animaciones de Mario
MARIO_SPRITE = [(0, 0, 0, 16, 21),
                (0, 16, 0, 16, 21),
                (0, 32, 0, 16, 21),
                (0, 48, 0, 16, 21)]

# Enemigo
CANGREJO_SPRITE = [(0, 0, 72, 12, 16), 
                  (0, 16, 72, 12, 16), 
                  (0, 32, 72, 12, 16)]

TORTUGA_TUMBADA_SPRITE = [(0, 48, 72, 12, 16), 
                          (0, 64, 72, 12, 16)]

CANGREJO_SPRITE = [(0, 0, 136, 16, 16), 
                   (0, 16, 136, 16, 16), 
                   (0, 32, 136, 16, 16)]

CANGREJO_ENFADADO_SPRITE = [(0, 64, 136, 16, 16),
                            (0, 80, 136, 16, 16),
                            (0, 96, 136, 16, 16)]
    

CANGREJO_TUMBADO_SPRITE = [(0, 112, 136, 16, 16), 
                           (0, 128, 136, 16, 16)]
