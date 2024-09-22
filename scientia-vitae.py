import random
import unicodedata
import os
import sys
import time

idioma = 'es'  # Idioma predeterminado

# Texto del menú en ambos idiomas
menu_text = {
    'es': ['1. Jugar', '2. Instrucciones', '3. Cambiar idioma', '4. Salir'],
    'en': ['1. Play', '2. Instructions', '3. Change Language', '4. Exit']
}

menu_principal_text = {
    'es': "Menú Principal",
    'en': "Main Menu"
}

instrucciones_text = {
    'es': """Instrucciones del juego:

1. Objetivo del Juego:
   - El objetivo es ser el primero en llegar a 10 puntos respondiendo correctamente preguntas de distintas categorías.

2. Cómo jugar:
   - Dos jugadores compiten en un tablero de 20 casilleros, numerados y con letras que representan categorías de preguntas (Historia, Geografía, Arte, Entretenimiento).
   - Cada turno, un jugador lanza el dado y avanza en el tablero el número de casilleros que indique el dado.
   - Dependiendo del casillero en el que caiga, se le hará una pregunta de la categoría correspondiente.
   - Si el jugador responde correctamente, gana 1 punto.
   - Si la respuesta es incorrecta o no responde, no se obtiene ningún punto.

3. Categorías:
   - Historia (H)
   - Geografía (G)
   - Arte (A)
   - Entretenimiento (E)

4. Mecánica del Turno:
   - Antes de responder la pregunta, el jugador tira el dado, cuyo número es elegido aleatoriamente entre 1 y 6.
   - El tablero muestra la posición del jugador después de tirar el dado.
   - El jugador responde la pregunta de la categoría en la que cae.
   - El primer jugador que acumule 10 puntos es el ganador.

5. Finalización del Juego:
   - Cuando un jugador alcanza 10 puntos, el juego termina y ese jugador es declarado ganador.
""",
    'en': """Game Instructions:

1. Objective:
   - The goal is to be the first player to reach 10 points by correctly answering questions from different categories.

2. How to Play:
   - Two players compete on a board with 20 squares, numbered and labeled with letters representing question categories (History, Geography, Art, Entertainment).
   - Each turn, a player rolls the die and moves forward on the board by the number rolled.
   - Depending on the square the player lands on, a question from the corresponding category will be asked.
   - If the player answers correctly, they earn 1 point.
   - If the answer is incorrect or no answer is given, no points are awarded.

3. Categories:
   - History (H)
   - Geography (G)
   - Art (A)
   - Entertainment (E)

4. Turn Mechanics:
   - Before answering the question, the player rolls the die, which randomly selects a number between 1 and 6.
   - The board shows the player's position after rolling the die.
   - The player answers the question from the category where they landed.
   - The first player to reach 10 points wins.

5. End of the Game:
   - When a player reaches 10 points, the game ends and that player is declared the winner.
"""
}


tablero_text = { 
    'es': "Tablero Inicial",
    'en': "Initial Board"
}

turno_text = {
    'es': "Turno del Jugador",
    'en': "Player's Turn"
}

presiona_enter_text = {
    'es': "Presiona Enter para tirar el dado...",
    'en': "Press Enter to roll the dice..."
}

salio_un_text = {
    'es': "¡Salió un",
    'en': "You rolled a"
}

textos_jugador = {
    'es': ['Jugador 1', 'Jugador 2'],
    'en': ['Player 1', 'Player 2']
}

caiste_en_text = {
    'es': "Caíste en la casilla",
    'en': "You landed on space"
}

correcto_text = {
    'es': "¡Correcto! Ganas un punto.",
    'en': "Correct! You earn a point."
}

incorrecto_text = {
    'es': "Incorrecto. La respuesta correcta era:",
    'en': "Incorrect. The correct answer was:"
}

puntos_text = {
    'es': "tiene puntos.",
    'en': "has points."
}

ganador_text = {
    'es': "¡El Jugador ha ganado!",
    'en': "Player has won!"
}

tirando_dado_text = {
    'es': "Tirando el dado...",
    'en': "Rolling the dice..."
}

tiraste_un_text = {
    'es': "Tiraste un",
    'en': "You rolled a"
}

tu_respuesta_text = {
    'es': "Tu respuesta: ",
    'en': "Your answer: "
}

separacion_text = {
    'es': "=" * 40,
    'en': "=" * 40
}

# Función para obtener la ruta correcta de los archivos
def obtener_ruta(relativa):
    """Obtiene la ruta absoluta de un archivo, ya sea en desarrollo o empaquetado."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relativa)

# Función para normalizar texto eliminando tildes y mayúsculas
def normalizar_texto(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.lower()

# Función para cargar preguntas desde un archivo TXT según la categoría
def cargar_preguntas(categoria):
    """Carga las preguntas desde un archivo TXT según la categoría."""
    archivo = f"questions/{categoria}_{idioma}.txt"  # Cambia según el idioma
    ruta = obtener_ruta(archivo)

    if not os.path.exists(ruta):
        print(f"Error: El archivo de preguntas para la categoría '{categoria}' no se encontró.")
        return []

    preguntas = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or '|' not in linea:
                continue  # Saltar líneas vacías o mal formateadas
            pregunta, respuestas = linea.split('|', 1)
            respuestas_validas = [resp.strip() for resp in respuestas.split(',')]
            preguntas.append((pregunta, respuestas_validas))
    return preguntas

# Función para recargar las preguntas cada vez que comience el juego
def recargar_preguntas():
    global historia, geografia, arte, entretenimiento
    historia = cargar_preguntas("historia")
    geografia = cargar_preguntas("geografia")
    arte = cargar_preguntas("arte")
    entretenimiento = cargar_preguntas("entretenimiento")

# Categorías del tablero
tablero = ['H', 'G', 'A', 'E'] * 5  # Ciclo de categorías en un tablero de 20 casillas

# Función para tirar el dado con animación
def tirar_dado():
    numero_final = random.randint(1, 6)
    
    print(tirando_dado_text[idioma])
    for _ in range(5):  # Simulamos 10 segundos (20 * 0.5)
        numero_actual = random.randint(1, 6)
        print(f"\r{tirando_dado_text[idioma]} {numero_actual}", end="")
        time.sleep(0.3)  # Cambiar número cada medio segundo
    print(f"\r{tiraste_un_text[idioma]} {numero_final}!          ")  # Espacios al final para limpiar la línea
    return numero_final

# Función para mostrar el tablero numerado y la posición de los jugadores
def mostrar_tablero(posiciones):
    print("\n" + tablero_text[idioma] + ":")
    for i, casilla in enumerate(tablero):
        jugador1 = "1" if posiciones[0] == i else " "
        jugador2 = "2" if posiciones[1] == i else " "
        # Mostramos el número del casillero junto a la letra de la categoría
        print(f"{i + 1:02d}[{casilla}] ", end="")
        print(f"({jugador1}/{jugador2}) ", end="")
    print("\n")

# Función para manejar las preguntas según la categoría
def obtener_pregunta(categoria):
    if categoria == 'H':
        return random.choice(historia) if historia else (None, [])
    elif categoria == 'G':
        return random.choice(geografia) if geografia else (None, [])
    elif categoria == 'A':
        return random.choice(arte) if arte else (None, [])
    elif categoria == 'E':
        return random.choice(entretenimiento) if entretenimiento else (None, [])
    else:
        return None, []

# Función para comparar si la respuesta del usuario es correcta
def es_respuesta_correcta(respuesta_usuario, respuestas_validas):
    respuesta_usuario_normalizada = normalizar_texto(respuesta_usuario)
    respuestas_validas_normalizadas = [normalizar_texto(resp) for resp in respuestas_validas]
    return respuesta_usuario_normalizada in respuestas_validas_normalizadas

# Lógica de una ronda
def jugar_turno(jugador, posiciones, puntos):
    print(f"{turno_text[idioma]} {jugador + 1}")
    input(presiona_enter_text[idioma])
    
    dado = tirar_dado()

    # Avanza la ficha
    posiciones[jugador] = (posiciones[jugador] + dado) % len(tablero)
    categoria = tablero[posiciones[jugador]]
    print(f"{caiste_en_text[idioma]} {posiciones[jugador] + 1} de {categoria}.")
    mostrar_tablero(posiciones)

    # Obtener la pregunta correspondiente
    pregunta, respuestas_correctas = obtener_pregunta(categoria)

    if not pregunta:
        print("Error al obtener la pregunta. Reintentando...")
        return False

    print(f"{pregunta}")
    respuesta_usuario = input(tu_respuesta_text[idioma]).strip()

    # Verificar si la respuesta es correcta
    if not respuesta_usuario:
        print("No has ingresado ninguna respuesta." if idioma == 'es' else "You have not entered any answer.")
    elif es_respuesta_correcta(respuesta_usuario, respuestas_correctas):
        print(correcto_text[idioma])
        puntos[jugador] += 1
    else:
        # Mostrar todas las respuestas correctas (puede haber más de una)
        print(f"{incorrecto_text[idioma]} {', '.join(respuestas_correctas)}")

    print(f"Jugador {jugador + 1} {puntos_text[idioma]} {puntos[jugador]}.")
    
    # Separación visual entre jugadas
    print(separacion_text[idioma])

    return puntos[jugador] >= 10

# Función para cambiar el idioma
def cambiar_idioma():
    global idioma
    opciones_idioma = ['es', 'en']
    print("\nSelecciona un idioma:" if idioma == 'es' else "\nSelect a language:")
    for i, op in enumerate(opciones_idioma, 1):
        print(f"{i}. {'Español' if op == 'es' else 'English'}")
    
    seleccion = input("Selecciona una opción: " if idioma == 'es' else "Select an option: ").strip()
    if seleccion == '1':
        idioma = 'es'
        print("Idioma cambiado a español." if idioma == 'es' else "Language changed to Spanish.")
    elif seleccion == '2':
        idioma = 'en'
        print("Language changed to English." if idioma == 'en' else "Idioma cambiado a inglés.")
    else:
        print("Selección no válida. Manteniendo el idioma actual." if idioma == 'es' else "Invalid selection. Keeping the current language.")

# Función para mostrar el menú principal
def mostrar_menu():
    print(f"\n=== {menu_principal_text[idioma]} ({'español' if idioma == 'es' else 'English'}) ===")
    for opcion in menu_text[idioma]:
        print(opcion)
    opcion = input("Selecciona una opción: " if idioma == 'es' else "Select an option: ").strip()
    return opcion

# Función para mostrar las instrucciones
def mostrar_instrucciones():
    print("\n=== Instrucciones ===" if idioma == 'es' else "\n=== Instructions ===")
    print(instrucciones_text[idioma])
    input("Presiona Enter para volver al menú principal." if idioma == 'es' else "Press Enter to return to the main menu.")

# Función principal del juego
def jugar():
    # Recargar preguntas en el idioma actual
    recargar_preguntas()

    posiciones = [0, 0]  # Posiciones de los jugadores en el tablero
    puntos = [0, 0]       # Puntos de los jugadores

    # Mostrar el tablero inicial antes de comenzar
    print(f"\n=== {tablero_text[idioma]} ===")
    mostrar_tablero(posiciones)

    while True:
        # Turno del Jugador 1
        if jugar_turno(0, posiciones, puntos):
            mensaje_ganador = ganador_text[idioma].replace('Jugador', 'Player' if idioma == 'en' else 'Jugador')
            print(f"{mensaje_ganador} 1")
            break

        # Turno del Jugador 2
        if jugar_turno(1, posiciones, puntos):
            mensaje_ganador = ganador_text[idioma].replace('Jugador', 'Player' if idioma == 'en' else 'Jugador')
            print(f"{mensaje_ganador} 2")
            break

# Bucle principal del menú
def main():
    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            jugar()
        elif opcion == '2':
            mostrar_instrucciones()
        elif opcion == '3':
            cambiar_idioma()
        elif opcion == '4':
            print("Saliendo del juego..." if idioma == 'es' else "Exiting the game...")
            break
        else:
            mensaje_error = 'Invalid option, intenta de nuevo.' if idioma == 'es' else 'Invalid option, try again.'
            print(mensaje_error)

# Ejecutar el juego
if __name__ == "__main__":
    main()
