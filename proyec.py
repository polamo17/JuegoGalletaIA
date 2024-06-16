
import pygame
import sys
import random
import tkinter as tk
from tkinter import Label, PhotoImage, Button
from PIL import Image, ImageTk

# Inicializar pygame
pygame.init()

# Parámetros cambiables
nBombas = random.randrange(2,4,1)
nHielos = random.randrange(5,8,1)

# Constantes para el tamaño de la ventana y el tablero
ANCHO, ALTO = 700, 700
COLOR_FONDO = (255, 255, 255)  # Blanco
COLOR_LINEA = (0, 0, 0)  # Negro
COLOR_BLOQUEADO = (255, 0, 0)  # Rojo
ESPACIO_CUADRADO = ANCHO // 12
MARGEN = ESPACIO_CUADRADO // 2  # Centrar el tablero en la ventana
COLOR_LINEA_NUEVA = (255, 255, 255, 0.0)

COLOR_PREVISUALIZACION = (192, 192, 192)
COLOR_JUGADOR_1 = (0, 0, 255)  # Azul
COLOR_JUGADOR_2 = (0, 255, 0)  # Verde
TAMANO_INDICADOR = ESPACIO_CUADRADO // 2
FUENTE = pygame.font.SysFont('Arial', 24)

# Modificar las constantes para el tamaño de la ventana y el tablero
ANCHO_VENTANA, ALTO_VENTANA = 1100, 700  # Hacer la ventana más ancha
ESPACIO_CUADRADO1 = ALTO_VENTANA // 12
OFFSET_X = (ANCHO_VENTANA - ANCHO) // 2  # Espacio adicional a los lados
OFFSET_Y = (ALTO_VENTANA - ALTO) // 2

# Crear la ventana con las nuevas dimensiones
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de la Galletota")

# Cargar las imágenes para cada jugador (asegúrate de que las rutas sean correctas)
imagen_jugador1 = pygame.image.load('Imagen/jugador1.jpeg').convert_alpha()
imagen_jugador2 = pygame.image.load('Imagen/jugador2.jpeg').convert_alpha()
imagen_bomba = pygame.image.load('Imagen/Bomba.png').convert_alpha()
imagen_hielo = pygame.image.load('Imagen/Hielo.png').convert_alpha()
imagen_fondo_menu = pygame.image.load('Imagen/fondo_menu.png').convert_alpha()  # Nueva imagen de fondo del menú
# Asegúrate de que las imágenes estén escaladas correctamente
imagen_jugador1 = pygame.transform.scale(imagen_jugador1, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_jugador2 = pygame.transform.scale(imagen_jugador2, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_bomba = pygame.transform.scale(imagen_bomba, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_hielo = pygame.transform.scale(imagen_hielo, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
imagen_fondo_menu = pygame.transform.scale(imagen_fondo_menu, (ANCHO_VENTANA, ALTO_VENTANA))  # Escalar la imagen de fondo al tamaño de la ventana

tamaño = 11  # El tamaño del tablero (número de cuadrados por lado)

# Crear las matrices con 'v' para las posiciones vacías
lineas_horizontales = [['v' for _ in range(tamaño)] for _ in range(tamaño + 1)]
lineas_verticales = [['v' for _ in range(tamaño + 1)] for _ in range(tamaño)]

puntaje_jugador1 = 0
puntaje_jugador2 = 0
turno = 'Jugador 1'

cuadrados_completados = [[False] * tamaño for _ in range(tamaño)]

def reemplazar_valor_aleatorio(matriz, valor_antiguo, nuevo_valor, max_cambios):
    posiciones = [(i, j) for i, fila in enumerate(matriz) for j, valor in enumerate(fila) if valor == valor_antiguo]
    random.shuffle(posiciones)
    posiciones_seleccionadas = posiciones[:max_cambios]
    for i, j in posiciones_seleccionadas:
        matriz[i][j] = nuevo_valor

def tablero_lleno(cuadrados):
    for fila in cuadrados:
        if 'v' in fila:
            return False
    return True

def calcular_puntajes():
    global puntaje_jugador1, puntaje_jugador2
    puntaje_jugador1 = sum(fila.count('1') for fila in cuadrados)
    puntaje_jugador2 = sum(fila.count('2') for fila in cuadrados)

def mostrar_ganador(puntaje_jugador1, puntaje_jugador2):
    root = tk.Tk()
    root.title("Fin del juego")
    imagen_path = 'Imagen/trofeo.png'
    original_img = Image.open(imagen_path)
    resized_img = original_img.resize((150, 150), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(resized_img)
    label_imagen = Label(root, image=img)
    label_imagen.image = img
    label_imagen.pack()

    if puntaje_jugador1 > puntaje_jugador2:
        mensaje = "¡Jugador 1 es el ganador!"
    elif puntaje_jugador2 > puntaje_jugador1:
        mensaje = "¡Jugador 2 es el ganador!"
    else:
        mensaje = "¡Es un empate!"

    label_mensaje = Label(root, text=mensaje, font=("Arial", 14))
    label_mensaje.pack()
    boton_cerrar = Button(root, text="Cerrar", command=root.destroy)
    boton_cerrar.pack()
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.mainloop()

centro = tamaño // 2
for i in range(centro + 1):
    for j in range(centro - i):
        lineas_horizontales[i][j] = 'b'
        lineas_horizontales[i][-j - 1] = 'b'
        lineas_horizontales[-i - 1][j] = 'b'
        lineas_horizontales[-i - 1][-j - 1] = 'b'
        if i != centro:
            lineas_verticales[j][i] = 'b'
            lineas_verticales[j][-i - 1] = 'b'
            lineas_verticales[-j - 1][i] = 'b'
            lineas_verticales[-j - 1][-i - 1] = 'b'
    if i != centro:
        lineas_horizontales[i][centro - i] = '0'
        lineas_horizontales[i][centro + i] = '0'
        lineas_horizontales[-i - 1][centro - i] = '0'
        lineas_horizontales[-i - 1][centro + i] = '0'
    lineas_verticales[centro - i][i] = '0'
    lineas_verticales[centro + i][i] = '0'
    lineas_verticales[centro - i][-i - 1] = '0'
    lineas_verticales[centro + i][-i - 1] = '0'

lineas_horizontales[centro] = ['0'] + ['v'] * (tamaño - 2) + ['0']
lineas_horizontales[centro + 1] = ['0'] + ['v'] * (tamaño - 2) + ['0']

cuadrados = [
    ['b', 'b', 'b', 'b', 'b', 'v', 'b', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'v', 'v', 'v', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'v', 'v', 'v', 'v', 'v', 'b', 'b', 'b'],
    ['b', 'b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b', 'b'],
    ['b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b'],
    ['v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v'],
    ['b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b'],
    ['b', 'b', 'v', 'v', 'v', 'v', 'v', 'v', 'v', 'b', 'b'],
    ['b', 'b', 'b', 'v', 'v', 'v', 'v', 'v', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'v', 'v', 'v', 'b', 'b', 'b', 'b'],
    ['b', 'b', 'b', 'b', 'b', 'v', 'b', 'b', 'b', 'b', 'b'],
]

modo_juego = None

def mover_ia(nivel, lineas_horizontales, lineas_verticales, tamaño):
    if nivel == 'principiante':
        return mover_aleatorio(lineas_horizontales, lineas_verticales, tamaño)
    elif nivel == 'intermedio':
        return mover_goloso(lineas_horizontales, lineas_verticales, tamaño)
    elif nivel == 'experto':
        return mover_diferencia_utilidades(lineas_horizontales, lineas_verticales, tamaño)

def mover_aleatorio(lineas_horizontales, lineas_verticales, tamaño):
    movimientos_posibles = []
    for i in range(tamaño):
        for j in range(tamaño):
            if lineas_horizontales[i][j] == 'v':
                movimientos_posibles.append(('h', i, j))
            if lineas_verticales[i][j] == 'v':
                movimientos_posibles.append(('v', i, j))
    return random.choice(movimientos_posibles) if movimientos_posibles else None

def mover_goloso(lineas_horizontales, lineas_verticales, tamaño):
    for i in range(tamaño):
        for j in range(tamaño):
            if lineas_horizontales[i][j] == 'v':
                if verificar_cuadrado_completo_simulado('h', i, j):
                    return ('h', i, j)
            if lineas_verticales[i][j] == 'v':
                if verificar_cuadrado_completo_simulado('v', i, j):
                    return ('v', i, j)
    return mover_aleatorio(lineas_horizontales, lineas_verticales, tamaño)

def verificar_cuadrado_completo_simulado(tipo, fila, columna):
    if tipo == 'h':
        lineas_horizontales[fila][columna] = 'Jugador 2'
    elif tipo == 'v':
        lineas_verticales[fila][columna] = 'Jugador 2'

    completos = 0
    cuadrados_para_verificar = [(fila, columna)]
    if tipo == 'h':
        if fila > 0:
            cuadrados_para_verificar.append((fila - 1, columna))
    else:
        if columna > 0:
            cuadrados_para_verificar.append((fila, columna - 1))

    for f, c in cuadrados_para_verificar:
        if f < tamaño and c < tamaño:
            if (lineas_horizontales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_horizontales[f + 1][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c + 1] in ['Jugador 1', 'Jugador 2', '0']):
                completos += 1

    if tipo == 'h':
        lineas_horizontales[fila][columna] = 'v'
    elif tipo == 'v':
        lineas_verticales[fila][columna] = 'v'

    return completos > 0

def mover_diferencia_utilidades(lineas_horizontales, lineas_verticales, tamaño):
    mejor_movimiento = None
    mejor_utilidad = -float('inf')

    for i in range(tamaño):
        for j in range(tamaño):
            if lineas_horizontales[i][j] == 'v':
                utilidad = evaluar_utilidad('h', i, j)
                if utilidad > mejor_utilidad:
                    mejor_utilidad = utilidad
                    mejor_movimiento = ('h', i, j)
            if lineas_verticales[i][j] == 'v':
                utilidad = evaluar_utilidad('v', i, j)
                if utilidad > mejor_utilidad:
                    mejor_utilidad = utilidad
                    mejor_movimiento = ('v', i, j)

    return mejor_movimiento

def evaluar_utilidad(tipo, fila, columna):
    puntaje_actual_jugador1 = puntaje_jugador1
    puntaje_actual_jugador2 = puntaje_jugador2

    if tipo == 'h':
        lineas_horizontales[fila][columna] = 'Jugador 2'
    elif tipo == 'v':
        lineas_verticales[fila][columna] = 'Jugador 2'

    for f in range(tamaño):
        for c in range(tamaño):
            if (lineas_horizontales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_horizontales[f + 1][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c + 1] in ['Jugador 1', 'Jugador 2', '0']):
                if cuadrados[f][c] == 'v':
                    puntaje_actual_jugador2 += 1
                elif cuadrados[f][c] == '1':
                    puntaje_actual_jugador1 -= 1

    if tipo == 'h':
        lineas_horizontales[fila][columna] = 'v'
    elif tipo == 'v':
        lineas_verticales[fila][columna] = 'v'

    return puntaje_actual_jugador2 - puntaje_actual_jugador1

def obtener_posicion_matriz(x, y):
    fila = (y - OFFSET_Y) // ESPACIO_CUADRADO
    columna = (x - OFFSET_X) // ESPACIO_CUADRADO
    return fila, columna

def es_posicion_valida(fila, columna, matriz):
    if 0 <= fila < len(matriz) and 0 <= columna < len(matriz[0]):
        return matriz[fila][columna] == 'v'
    return False

def verificar_cuadrado_completo(fila, columna, lineas_horizontales, lineas_verticales):
    global turno, puntaje_jugador1, puntaje_jugador2
    cuadrados_completados_ahora = 0
    turno_cambiado = False
    cuadrados_para_verificar = [
        (fila, columna),
    ]
    if fila > 0:
        cuadrados_para_verificar.append((fila - 1, columna))
    if columna > 0:
        cuadrados_para_verificar.append((fila, columna - 1))

    for f, c in cuadrados_para_verificar:
        if f < tamaño and c < tamaño:
            if (lineas_horizontales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_horizontales[f + 1][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c + 1] in ['Jugador 1', 'Jugador 2', '0']):
                if cuadrados[f][c] == 'pb':
                    limpiar_explosion(f, c)
                elif cuadrados[f][c] == 'ph':
                    turno_cambiado = True
                    if turno == 'Jugador 1':
                        cuadrados[f][c] = '1'
                        turno = 'Jugador 2'
                    else:
                        cuadrados[f][c] = '2'
                        turno = 'Jugador 1'
                elif not cuadrados_completados[f][c]:
                    cuadrados_completados[f][c] = True
                    cuadrados_completados_ahora += 1
                    if turno == 'Jugador 1':
                        cuadrados[f][c] = '1'
                    else:
                        cuadrados[f][c] = '2'
    if cuadrados_completados_ahora == 0 and not turno_cambiado:
        turno = 'Jugador 2' if turno == 'Jugador 1' else 'Jugador 1'
    calcular_puntajes()

def limpiar_explosion(f, c):
    global cuadrados, lineas_horizontales, lineas_verticales, cuadrados_completados
    for i in range(max(0, f - 1), min(tamaño, f + 2)):
        for j in range(max(0, c - 1), min(tamaño, c + 2)):
            if cuadrados[i][j] != 'b':
                cuadrados[i][j] = 'v'
                cuadrados_completados[i][j] = False
                if i < tamaño and j < tamaño:
                    if lineas_horizontales[i][j] != '0' and lineas_horizontales[i][j] != 'b':
                        lineas_horizontales[i][j] = 'v'
                    if lineas_horizontales[i + 1][j] != '0' and lineas_horizontales[i + 1][j] != 'b':
                        lineas_horizontales[i + 1][j] = 'v'
                    if lineas_verticales[i][j] != '0' and lineas_verticales[i][j] != 'b':
                        lineas_verticales[i][j] = 'v'
                    if lineas_verticales[i][j + 1] != '0' and lineas_verticales[i][j + 1] != 'b':
                        lineas_verticales[i][j + 1] = 'v'
    cuadrados[f][c] = 'v'
    actualizar_cuadrados_completados()

def actualizar_cuadrados_completados():
    global cuadrados_completados
    for f in range(tamaño):
        for c in range(tamaño):
            if (lineas_horizontales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_horizontales[f + 1][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c] in ['Jugador 1', 'Jugador 2', '0'] and
                lineas_verticales[f][c + 1] in ['Jugador 1', 'Jugador 2', '0']):
                if not cuadrados_completados[f][c]:
                    cuadrados_completados[f][c] = True
            else:
                cuadrados_completados[f][c] = False
                if cuadrados[f][c] in ['1', '2']:
                    cuadrados[f][c] = 'v'
    calcular_puntajes()

def dibujar_cuadrados_completos():
    for fila in range(tamaño - 1):
        for columna in range(tamaño - 1):
            if cuadrados_completados[fila][columna]:
                x = columna * ESPACIO_CUADRADO + OFFSET_X + ESPACIO_CUADRADO // 2
                y = fila * ESPACIO_CUADRADO + OFFSET_Y + ESPACIO_CUADRADO // 2
                imagen = imagen_jugador1 if cuadrados[fila][columna] == '1' else imagen_jugador2
                imagen = pygame.transform.scale(imagen, (ESPACIO_CUADRADO, ESPACIO_CUADRADO))
                x -= imagen.get_width() // 2
                y -= imagen.get_height() // 2
                pantalla.blit(imagen, (x, y))

def dibujar_indicadores_jugadores():
    ficha_tamaño = TAMANO_INDICADOR * 3
    calcular_puntajes()
    texto_jugador_1 = FUENTE.render('Jugador 1', True, COLOR_JUGADOR_1)
    ficha_jugador_1 = pygame.transform.scale(imagen_jugador1, (ficha_tamaño, ficha_tamaño))
    pantalla.blit(texto_jugador_1, (OFFSET_X - texto_jugador_1.get_width() - 20 - ficha_jugador_1.get_width(), MARGEN))
    pantalla.blit(ficha_jugador_1, (OFFSET_X - texto_jugador_1.get_width() - 110, MARGEN + texto_jugador_1.get_height() + 10))
    texto_puntaje_1 = FUENTE.render(f'Puntaje: {puntaje_jugador1}', True, COLOR_JUGADOR_1)
    pantalla.blit(texto_puntaje_1, (OFFSET_X - texto_puntaje_1.get_width() -110, MARGEN + ficha_jugador_1.get_height() + 50))

    texto_jugador_2 = FUENTE.render('Jugador 2', True, COLOR_JUGADOR_2)
    ficha_jugador_2 = pygame.transform.scale(imagen_jugador2, (ficha_tamaño, ficha_tamaño))
    pantalla.blit(texto_jugador_2, (ANCHO_VENTANA - OFFSET_X + 25, MARGEN))
    pantalla.blit(ficha_jugador_2, (ANCHO_VENTANA - OFFSET_X -70 + texto_jugador_2.get_width() + 10, MARGEN + texto_jugador_2.get_height() + 10))
    texto_puntaje_2 = FUENTE.render(f'Puntaje: {puntaje_jugador2}', True, COLOR_JUGADOR_2)
    pantalla.blit(texto_puntaje_2, (ANCHO_VENTANA - OFFSET_X + 25, MARGEN + ficha_jugador_2.get_height() + 50))

    if turno == 'Jugador 1':
        pygame.draw.circle(pantalla, COLOR_JUGADOR_1, (OFFSET_X - 80, MARGEN + texto_jugador_1.get_height() // 2), TAMANO_INDICADOR // 2)
    else:
        pygame.draw.circle(pantalla, COLOR_JUGADOR_2, (ANCHO_VENTANA - OFFSET_X + texto_jugador_2.get_width() -50 + ficha_jugador_2.get_width(), MARGEN + texto_jugador_2.get_height() // 2), TAMANO_INDICADOR // 2)

ancho_tablero = tamaño * ESPACIO_CUADRADO
alto_tablero = tamaño * ESPACIO_CUADRADO
OFFSET_X = (ANCHO_VENTANA - ancho_tablero) // 2
OFFSET_Y = (ALTO_VENTANA - alto_tablero) // 2

def dibujar_tablero():
    pantalla.fill(COLOR_FONDO)
    max_hor = len(lineas_horizontales[0])
    max_ver = len(lineas_verticales[0])
    max_cua = len(cuadrados[0])
    for fila in range(11):
        for columna in range(11):
            rect = pygame.Rect(columna * ESPACIO_CUADRADO + OFFSET_X, fila * ESPACIO_CUADRADO + OFFSET_Y, ESPACIO_CUADRADO, ESPACIO_CUADRADO)
            pygame.draw.rect(pantalla, COLOR_LINEA_NUEVA, rect, 1)
            if cuadrados[fila][columna] == '1':
                pantalla.blit(imagen_jugador1, (columna * ESPACIO_CUADRADO + OFFSET_X, fila * ESPACIO_CUADRADO + OFFSET_Y))
            elif cuadrados[fila][columna] == '2':
                pantalla.blit(imagen_jugador2, (columna * ESPACIO_CUADRADO + OFFSET_X, fila * ESPACIO_CUADRADO + OFFSET_Y))
            elif cuadrados[fila][columna] == 'pb':
                pantalla.blit(imagen_bomba, (columna * ESPACIO_CUADRADO + OFFSET_X, fila * ESPACIO_CUADRADO + OFFSET_Y))
            elif cuadrados[fila][columna] == 'ph':
                pantalla.blit(imagen_hielo, (columna * ESPACIO_CUADRADO + OFFSET_X, fila * ESPACIO_CUADRADO + OFFSET_Y))
    for i, fila in enumerate(lineas_horizontales):
        for j, valor in enumerate(fila):
            if valor == 'Jugador 1':
                inicio = (j * ESPACIO_CUADRADO + OFFSET_X, (i) * ESPACIO_CUADRADO + OFFSET_Y)
                fin = ((j + 1) * ESPACIO_CUADRADO + OFFSET_X, (i) * ESPACIO_CUADRADO + OFFSET_Y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_1, inicio, fin, 5)
            elif valor == 'Jugador 2':
                inicio = (j * ESPACIO_CUADRADO + OFFSET_X, (i) * ESPACIO_CUADRADO + OFFSET_Y)
                fin = ((j + 1) * ESPACIO_CUADRADO + OFFSET_X, (i) * ESPACIO_CUADRADO + OFFSET_Y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_2, inicio, fin, 5)
            inicio = (j * ESPACIO_CUADRADO + OFFSET_X, i * ESPACIO_CUADRADO + OFFSET_Y)
            fin = ((j + 1) * ESPACIO_CUADRADO + OFFSET_X, i * ESPACIO_CUADRADO + OFFSET_Y)
            if valor == '0':
                pygame.draw.line(pantalla, COLOR_LINEA, inicio, fin, 5)
            elif valor == 'b':
                pygame.draw.line(pantalla, COLOR_BLOQUEADO, inicio, fin, 3)
    for i, fila in enumerate(lineas_verticales):
        for j, valor in enumerate(fila):
            if valor == 'Jugador 1':
                inicio = (j * ESPACIO_CUADRADO + OFFSET_X, i * ESPACIO_CUADRADO + OFFSET_Y)
                fin = (j * ESPACIO_CUADRADO + OFFSET_X, (i + 1) * ESPACIO_CUADRADO + OFFSET_Y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_1, inicio, fin, 5)
            elif valor == 'Jugador 2':
                inicio = (j * ESPACIO_CUADRADO + OFFSET_X, i * ESPACIO_CUADRADO + OFFSET_Y)
                fin = (j * ESPACIO_CUADRADO + OFFSET_X, (i + 1) * ESPACIO_CUADRADO + OFFSET_Y)
                pygame.draw.line(pantalla, COLOR_JUGADOR_2, inicio, fin, 5)
            inicio = (j * ESPACIO_CUADRADO + OFFSET_X, i * ESPACIO_CUADRADO + OFFSET_Y)
            fin = (j * ESPACIO_CUADRADO + OFFSET_X, (i + 1) * ESPACIO_CUADRADO + OFFSET_Y)
            if valor == '0':
                pygame.draw.line(pantalla, COLOR_LINEA, inicio, fin, 5)
            elif valor == 'b':
                pygame.draw.line(pantalla, COLOR_BLOQUEADO, inicio, fin, 3)
    dibujar_indicadores_jugadores()

reemplazar_valor_aleatorio(cuadrados, 'v', 'pb', nBombas)
reemplazar_valor_aleatorio(cuadrados, 'v', 'ph', nHielos)

def mostrar_pantalla_inicio():
    color_rect = (173, 216, 230)  # Color de los rectángulos
    radio_bordes = 10  # Radio de los bordes redondeados
    pantalla.blit(imagen_fondo_menu, (0, 0))
    fuente_titulo = pygame.font.SysFont('Ballon', 100, bold=True)
    fuente_opcion = pygame.font.SysFont('Arial', 36, bold=True)

    titulo = fuente_titulo.render('JUEGO DE LA GALLETA', True, (255, 255, 0))
    
    opcion_1 = fuente_opcion.render('Jugador vs Jugador', True, (0, 0, 0))
    opcion_2 = fuente_opcion.render('Jugador vs Maquina (Facil)', True, (0, 0, 0))
    opcion_3 = fuente_opcion.render('Jugador vs Maquina (Medio)', True, (0, 0, 0))
    opcion_4 = fuente_opcion.render('Jugador vs Maquina (Dificil)', True, (0, 0, 0))

# Crear rectángulos ajustados para asegurar que el texto esté centrado y los bordes sean redondeados
    rect_opcion_1 = pygame.Rect((ANCHO_VENTANA - opcion_1.get_width()) // 2 - 10, 300, opcion_1.get_width() + 6, opcion_1.get_height() + 8)
    rect_opcion_2 = pygame.Rect((ANCHO_VENTANA - opcion_2.get_width()) // 2 - 10, 400, opcion_2.get_width() + 6, opcion_2.get_height() + 8)
    rect_opcion_3 = pygame.Rect((ANCHO_VENTANA - opcion_3.get_width()) // 2 - 10, 500, opcion_3.get_width() + 6, opcion_3.get_height() + 8)
    rect_opcion_4 = pygame.Rect((ANCHO_VENTANA - opcion_4.get_width()) // 2 - 10, 600, opcion_4.get_width() + 6, opcion_4.get_height() + 8)

    # Dibujar rectángulos redondeados en la pantalla
    pygame.draw.rect(pantalla, color_rect, rect_opcion_1, border_radius=radio_bordes)
    pygame.draw.rect(pantalla, color_rect, rect_opcion_2, border_radius=radio_bordes)
    pygame.draw.rect(pantalla, color_rect, rect_opcion_3, border_radius=radio_bordes)
    pygame.draw.rect(pantalla, color_rect, rect_opcion_4, border_radius=radio_bordes)

    pantalla.blit(titulo, ((ANCHO_VENTANA - titulo.get_width()) // 2, 150))
    pantalla.blit(opcion_1, rect_opcion_1.topleft)
    pantalla.blit(opcion_2, rect_opcion_2.topleft)
    pantalla.blit(opcion_3, rect_opcion_3.topleft)
    pantalla.blit(opcion_4, rect_opcion_4.topleft)

    pygame.display.flip()

def seleccionar_modo(x, y):
    global modo_juego
    if 300 < y < 350:
        modo_juego = '1v1'
    elif 400 < y < 450:
        modo_juego = '1vCPU'
    elif 500 < y < 550:
        modo_juego = '1vCPU_medio'
    elif 600 < y < 650:
        modo_juego = '1vCPU_dificil'

mostrar_pantalla_inicio()

while modo_juego is None:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            seleccionar_modo(x, y)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            columna = (x - OFFSET_X) // ESPACIO_CUADRADO
            fila = (y - OFFSET_Y) // ESPACIO_CUADRADO
            pos_x_exacta = (x - OFFSET_X) % ESPACIO_CUADRADO
            pos_y_exacta = (y - OFFSET_Y) % ESPACIO_CUADRADO
            if columna < tamaño and fila < tamaño:
                if pos_x_exacta > pos_y_exacta:
                    if es_posicion_valida(fila, columna, lineas_horizontales):
                        lineas_horizontales[fila][columna] = turno
                        verificar_cuadrado_completo(fila, columna, lineas_horizontales, lineas_verticales)
                        pantalla.fill(COLOR_FONDO)
                        dibujar_cuadrados_completos()
                        dibujar_tablero()
                        pygame.display.flip()
                        if tablero_lleno(cuadrados):
                            calcular_puntajes()
                            mostrar_ganador(puntaje_jugador1, puntaje_jugador2)
                            pygame.quit()
                            sys.exit()
                else:
                    if es_posicion_valida(fila, columna, lineas_verticales):
                        lineas_verticales[fila][columna] = turno
                        verificar_cuadrado_completo(fila, columna, lineas_horizontales, lineas_verticales)
                        pantalla.fill(COLOR_FONDO)
                        dibujar_cuadrados_completos()
                        dibujar_tablero()
                        pygame.display.flip()
                        if tablero_lleno(cuadrados):
                            calcular_puntajes()
                            mostrar_ganador(puntaje_jugador1, puntaje_jugador2)
                            pygame.quit()
                            sys.exit()

    pantalla.fill(COLOR_FONDO)
    dibujar_cuadrados_completos()
    dibujar_tablero()

    if tablero_lleno(cuadrados):
        calcular_puntajes()
        mostrar_ganador(puntaje_jugador1, puntaje_jugador2)
        pygame.quit()
        sys.exit()

    if pygame.mouse.get_focused() and pantalla.get_rect().collidepoint(pygame.mouse.get_pos()):
        x, y = pygame.mouse.get_pos()
        columna = (x - OFFSET_X) // ESPACIO_CUADRADO
        fila = (y - OFFSET_Y) // ESPACIO_CUADRADO
        inicio_x = columna * ESPACIO_CUADRADO + OFFSET_X
        inicio_y = fila * ESPACIO_CUADRADO + OFFSET_Y
        fin_x = columna * ESPACIO_CUADRADO + OFFSET_X
        fin_y = fila * ESPACIO_CUADRADO + OFFSET_Y
        if columna < tamaño and fila < tamaño:
            pos_x_exacta = (x - OFFSET_X) % ESPACIO_CUADRADO
            pos_y_exacta = (y - OFFSET_Y) % ESPACIO_CUADRADO
            if pos_x_exacta > pos_y_exacta:
                fin_x += ESPACIO_CUADRADO
            else:
                fin_y += ESPACIO_CUADRADO
        pygame.draw.line(pantalla, COLOR_PREVISUALIZACION, (inicio_x, inicio_y), (fin_x, fin_y), 3)

    if (modo_juego == '1vCPU' and turno == 'Jugador 2') or (modo_juego == '1vCPU_medio' and turno == 'Jugador 2') or (modo_juego == '1vCPU_dificil' and turno == 'Jugador 2'):
        pygame.time.wait(1000)  # Esperar un segundo antes de hacer la jugada
        nivel = 'principiante' if modo_juego == '1vCPU' else 'intermedio' if modo_juego == '1vCPU_medio' else 'experto'
        movimiento = mover_ia(nivel, lineas_horizontales, lineas_verticales, tamaño)
        if movimiento:
            tipo, fila, columna = movimiento
            if tipo == 'h':
                lineas_horizontales[fila][columna] = 'Jugador 2'
                verificar_cuadrado_completo(fila, columna, lineas_horizontales, lineas_verticales)
                pantalla.fill(COLOR_FONDO)
                dibujar_cuadrados_completos()
                dibujar_tablero()
                pygame.display.flip()
                if tablero_lleno(cuadrados):
                    calcular_puntajes()
                    mostrar_ganador(puntaje_jugador1, puntaje_jugador2)
                    pygame.quit()
                    sys.exit()
            elif tipo == 'v':
                lineas_verticales[fila][columna] = 'Jugador 2'
                verificar_cuadrado_completo(fila, columna, lineas_horizontales, lineas_verticales)
                pantalla.fill(COLOR_FONDO)
                dibujar_cuadrados_completos()
                dibujar_tablero()
                pygame.display.flip()
                if tablero_lleno(cuadrados):
                    calcular_puntajes()
                    mostrar_ganador(puntaje_jugador1, puntaje_jugador2)
                    pygame.quit()
                    sys.exit()

    pygame.display.flip()
    