import random
import unicodedata
import os
import sys
import time
import keyboard

# Idioma predeterminado
idioma = 'es'

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
   - Entre 2 y 10 jugadores compiten en un tablero de 20 casilleros, numerados y con letras que representan categorías de preguntas (Historia, Geografía, Arte, Entretenimiento).
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
   - Between 2 and 10 players compete on a board with 20 squares, numbered and labeled with letters representing question categories (History, Geography, Art, Entertainment).
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
    'es': "Tablero",
    'en': "Board"
}

turno_text = {
    'es': "Turno de",
    'en': "Player's Turn"
}

presiona_enter_text = {
    'es': "Presiona Enter para tirar el dado...",
    'en': "Press Enter to roll the dice..."
}

textos_jugador = {
    'es': [],
    'en': []
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
    
    #base_path = sys._MEIPASS
    base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relativa)

# Función para normalizar texto eliminando tildes y mayúsculas
def normalizar_texto(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.lower()

# Función para cargar preguntas desde un archivo TXT según la categoría
def cargar_preguntas(categoria):
    archivo = f"questions/{categoria}_{idioma}.txt"
    ruta = obtener_ruta(archivo)

    if not os.path.exists(ruta):
        print(f"Error: El archivo de preguntas para la categoría '{categoria}' en path '{ruta}' No se encontró.")
        return []

    preguntas = []
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea_num, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea or '|' not in linea:
                print(f"Línea {linea_num} en '{archivo}' está vacía o mal formateada. Saltando.")
                continue
            try:
                pregunta, respuestas = linea.split('|', 1)
                respuestas_validas = [resp.strip() for resp in respuestas.split(',')]
                preguntas.append((pregunta, respuestas_validas))
            except ValueError:
                print(f"Error al procesar la línea {linea_num} en '{archivo}'.")
                continue
    print(f"Cargadas {len(preguntas)} preguntas de '{archivo}'.")
    return preguntas

# Función para recargar las preguntas
def recargar_preguntas():
    global historia, geografia, arte, entretenimiento
    historia = cargar_preguntas("historia")
    geografia = cargar_preguntas("geografia")
    arte = cargar_preguntas("arte")
    entretenimiento = cargar_preguntas("entretenimiento")

# Categorías del tablero
tablero = ['H', 'G', 'A', 'E'] * 5  # Ciclo de categorías en un tablero de 20 casillas

# Función para tirar el dado
def tirar_dado_func():
    numero_final = random.randint(1, 6)
    
    print(tirando_dado_text[idioma])
    for _ in range(5):  # Simulamos 5 segundos (10 * 0.5)
        numero_actual = random.randint(1, 6)
        print(f"\r{tirando_dado_text[idioma]} {numero_actual}", end="")
        time.sleep(0.3)  # Cambiar número cada medio segundo
    print(f"\r{tiraste_un_text[idioma]} {numero_final}!          ")
    
    input("Presiona Enter para continuar...")  # Espera a que el jugador presione Enter

    return numero_final

# Función para mostrar el tablero
def mostrar_tablero(posiciones):
    print("\n" + tablero_text[idioma] + ":")
    for i, casilla in enumerate(tablero):
        jugadores_en_casilla = [textos_jugador[idioma][j] for j in range(len(posiciones)) if posiciones[j] == i]
        jugadores_str = '/'.join(jugadores_en_casilla) if jugadores_en_casilla else ' '
        print(f"{i + 1:02d}[{casilla}] ({jugadores_str}) ", end="")  
    print("\n")

# Función para manejar las preguntas
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

# Función para verificar si la respuesta es correcta
def es_respuesta_correcta(respuesta_usuario, respuestas_validas):
    respuesta_usuario_normalizada = normalizar_texto(respuesta_usuario)
    respuestas_validas_normalizadas = [normalizar_texto(r) for r in respuestas_validas]
    return respuesta_usuario_normalizada in respuestas_validas_normalizadas

# Función para mostrar las posiciones actuales de los jugadores
def mostrar_posiciones(posiciones):
    print("Posiciones actuales:")
    for i, pos in enumerate(posiciones):
        print(f"{textos_jugador[idioma][i]} está en la casilla {pos + 1}")

# Lógica de una ronda
def jugar_turno(jugador, posiciones, puntos):
    print(f"{turno_text[idioma]} {textos_jugador[idioma][jugador]}")
    input(presiona_enter_text[idioma])
    
    dado = tirar_dado_func()
    # Mostrar posición antes de mover
    print(f"Posición antes de mover: {posiciones[jugador] + 1}")

    # Avanza la ficha
    posiciones[jugador] = (posiciones[jugador] + dado) % len(tablero)
    
    # Mostrar posición después de mover
    print(f"Posición después de mover: {posiciones[jugador] + 1}")
    
    categoria = tablero[posiciones[jugador]]
    print(f"{caiste_en_text[idioma]} {posiciones[jugador] + 1} de {categoria}.")

    # Obtener la pregunta correspondiente
    pregunta_data = obtener_pregunta(categoria)
    if not pregunta_data or not pregunta_data[0]:
        print("Error al obtener la pregunta. Reintentando..." if idioma == 'es' else "Error obtaining the question. Retrying...")
        return False
    pregunta, respuestas_correctas = pregunta_data
    print(f"{pregunta}")
    respuesta_usuario = input(tu_respuesta_text[idioma]).strip()

    # Verificar si la respuesta es correcta
    if not respuesta_usuario:
        print("No has ingresado ninguna respuesta." if idioma == 'es' else "You have not entered any answer.")
    elif es_respuesta_correcta(respuesta_usuario, respuestas_correctas):
        print(correcto_text[idioma])
        puntos[jugador] += 1
    else:
        print(f"{incorrecto_text[idioma]} {', '.join(respuestas_correctas)}")

    # Mostrar las posiciones actuales de los jugadores
    mostrar_posiciones(posiciones)

    # Separación visual entre jugadas
    print(separacion_text[idioma])

    # Esperar a que se presione Ctrl para limpiar el tablero
    print("Presiona Ctrl para continuar...")
    keyboard.wait('ctrl')  # Espera a que se presione Ctrl
    return puntos[jugador] >= 10


# Función para cambiar el idioma
def cambiar_idioma_func():
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
    time.sleep(2)

# Función para mostrar el menú principal
def mostrar_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n=== {menu_principal_text[idioma]} ({'español' if idioma == 'es' else 'English'}) ===")
        for opcion in menu_text[idioma]:
            print(opcion)
        opcion = input("Selecciona una opción: " if idioma == 'es' else "Select an option: ").strip()

        if opcion == '1':
            jugar()
        elif opcion == '2':
            print(instrucciones_text[idioma])
            input("Presiona Enter para volver al menú principal." if idioma == 'es' else "Press Enter to return to the main menu.")
        elif opcion == '3':
            cambiar_idioma_func()
        elif opcion == '4':
            print("Saliendo del juego..." if idioma == 'es' else "Exiting the game...")
            break
        else:
            mensaje_error = "Opción no válida. Intenta de nuevo." if idioma == 'es' else "Invalid option. Try again."
            print(mensaje_error)
            time.sleep(2)

# Función para el juego
iconos_disponibles = ['!', '#', '$', '%', '&', '=', '?', '¿', '@', '¡', '<', '>']

# Función para el juego
def jugar():
    global textos_jugador
    while True:
        try:
            num_jugadores = int(input("¿Cuántos jugadores? (2-10): "))
            if 2 <= num_jugadores <= 10:
                break
            else:
                print("Número de jugadores inválido. Debe ser entre 2 y 10.")
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número entre 2 y 10.")

    textos_jugador[idioma] = []
    usados = []

    for i in range(num_jugadores):
        while True:
            print(f"\nJugador {i + 1}, elige un símbolo de los siguientes:")
            for j, simbolo in enumerate(iconos_disponibles):
                print(f"{j + 1}. {simbolo}")
            try:
                seleccion = int(input("Número del símbolo: ")) - 1
                if 0 <= seleccion < len(iconos_disponibles) and iconos_disponibles[seleccion] not in usados:
                    textos_jugador[idioma].append(iconos_disponibles[seleccion])
                    usados.append(iconos_disponibles[seleccion])
                    break
                else:
                    print("Selección inválida o símbolo ya utilizado. Intenta de nuevo.")
            except ValueError:
                print("Entrada no válida. Por favor, ingresa un número válido.")

    recargar_preguntas()
    puntos = [0] * num_jugadores
    posiciones = [0] * num_jugadores
    turno = 0  # Indica a qué jugador le toca

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"\n=== {tablero_text[idioma]} ===")
        mostrar_tablero(posiciones)
        print(separacion_text[idioma])

        if jugar_turno(turno, posiciones, puntos):
            # Anunciar la clasificación al final del juego
            clasificacion = sorted(enumerate(puntos), key=lambda x: x[1], reverse=True)
            print("\nClasificación Final:")
            for puesto, (jugador, puntaje) in enumerate(clasificacion, 1):
                print(f"{puesto}. {textos_jugador[idioma][jugador]}: {puntaje} puntos")
            input("Presiona Enter para volver al menú principal." if idioma == 'es' else "Press Enter to return to the main menu.")
            break

        # Cambiar de turno
        turno = (turno + 1) % num_jugadores  # Alterna entre jugadores


# Ejecutar el menú principal al inicio
if __name__ == "__main__":
    mostrar_menu()


