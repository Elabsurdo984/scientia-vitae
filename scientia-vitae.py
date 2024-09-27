import pygame
import sys
import random
import os
import unicodedata
import re

# Initialize Pygame
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Scientia Vitae")

# Set the icon (Make sure you have 'mi_icono.ico' in the 'icons/' folder)
if os.path.exists('icons/mi_icono.ico'):
    icon = pygame.image.load('icons/mi_icono.ico')
    pygame.display.set_icon(icon)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

# Category colors (H, G, A, E)
CATEGORY_COLORS = {
    'H': DARK_BLUE,  # History
    'G': GREEN,      # Geography
    'A': ORANGE,     # Art
    'E': PURPLE      # Entertainment
}

# Number of rows and columns
ROWS = 5
COLS = 4

# Size of each cell
CELL_WIDTH = SCREEN_WIDTH // COLS
CELL_HEIGHT = SCREEN_HEIGHT // ROWS

# Define positions of cells with categories
categories = ['H', 'G', 'A', 'E']
casillas_posiciones = {}

for row in range(ROWS):
    for col in range(COLS):
        casilla_num = row * COLS + col + 1
        x = col * CELL_WIDTH
        y = row * CELL_HEIGHT
        casillas_posiciones[casilla_num] = (x, y)

# Font for text
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 50)

# Language variable (default to Spanish)
language = 'es'

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)
        self.text_surface = self.font.render(text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Button border
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

# Player class
class Player:
    def __init__(self, color, casilla_inicial, radius=15):
        self.color = color
        self.casilla_actual = casilla_inicial
        self.radius = radius
        self.position = self.obtener_posicion(casilla_inicial)
        self.target_position = self.position
        self.speed = 5  # Movement speed in pixels

    def obtener_posicion(self, casilla_num):
        x, y = casillas_posiciones[casilla_num]
        # Center the token within the cell
        pos_x = x + CELL_WIDTH // 2
        pos_y = y + CELL_HEIGHT // 2
        return (pos_x, pos_y)

    def mover_a(self, nueva_casilla):
        if nueva_casilla > 20:
            nueva_casilla = 20  # Limit to the end of the board
        self.casilla_actual = nueva_casilla
        self.target_position = self.obtener_posicion(nueva_casilla)

    def actualizar(self):
        if self.position != self.target_position:
            x, y = self.position
            target_x, target_y = self.target_position

            # Calculate direction
            dir_x = target_x - x
            dir_y = target_y - y
            distancia = (dir_x**2 + dir_y**2) ** 0.5

            if distancia > self.speed:
                dir_x /= distancia
                dir_y /= distancia

                # Move position
                x += dir_x * self.speed
                y += dir_y * self.speed
            else:
                # If we're very close to the target, just reach it
                x, y = target_x, target_y

            self.position = (x, y)

def normalizar_texto(texto):
    # Convert to lowercase
    texto = texto.lower()
    # Remove accents and other diacritical marks
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    # Remove special characters and punctuation
    texto = re.sub(r'[^\w\s]', '', texto)
    # Remove extra spaces
    texto = ' '.join(texto.split())
    return texto

# Functions to handle questions and answers
def cargar_preguntas(categoria):
    global language
    try:
        filename = f'questions/{categoria}_{language}.txt'
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            preguntas = []
            for line in lines:
                if '|' in line:
                    pregunta, respuestas = line.strip().split('|', 1)
                    respuestas = [normalizar_texto(resp.strip()) for resp in respuestas.split(',')]
                    preguntas.append((pregunta, respuestas))
            return preguntas
    except FileNotFoundError:
        print(f"Question file for category '{categoria}' not found.")
        return []

def recargar_preguntas():
    global historia, geografia, arte, entretenimiento
    historia = cargar_preguntas("historia")
    geografia = cargar_preguntas("geografia")
    arte = cargar_preguntas("arte")
    entretenimiento = cargar_preguntas("entretenimiento")

def obtener_pregunta(categoria):
    if categoria == 'H' and historia:
        return random.choice(historia)
    elif categoria == 'G' and geografia:
        return random.choice(geografia)
    elif categoria == 'A' and arte:
        return random.choice(arte)
    elif categoria == 'E' and entretenimiento:
        return random.choice(entretenimiento)
    else:
        return None
    
def mostrar_resultado(resultado, respuesta_correcta=None, respuesta_color=BLACK):
    resultado_font = pygame.font.SysFont(None, 40)
    if resultado == "Correct!" or resultado == "¡Correcto!":
        resultado_text = resultado_font.render(resultado, True, GREEN)
    else:
        resultado_text = resultado_font.render(resultado, True, respuesta_color)
    screen.blit(resultado_text, (SCREEN_WIDTH // 2 - resultado_text.get_width() // 2, SCREEN_HEIGHT - 100))
    
    if respuesta_correcta:
        correcta_font = pygame.font.SysFont(None, 30)
        correcta_text = correcta_font.render(f"{'Respuesta correcta' if language == 'es' else 'Correct answer'}: {respuesta_correcta}", True, BLACK)
        screen.blit(correcta_text, (SCREEN_WIDTH // 2 - correcta_text.get_width() // 2, SCREEN_HEIGHT - 60))
    
    continuar_font = pygame.font.SysFont(None, 25)
    continuar_text = continuar_font.render("Presiona Enter para continuar" if language == 'es' else "Press Enter to continue", True, BLACK)
    screen.blit(continuar_text, (SCREEN_WIDTH // 2 - continuar_text.get_width() // 2, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Modify the mostrar_pregunta function to use the color
def mostrar_pregunta(pregunta, respuestas_correctas, jugador_actual, puntos, dado):
    global language
    input_active = True
    user_text = ''
    cursor_visible = True
    cursor_timer = 0
    start_time = pygame.time.get_ticks()
    tiempo_limite = 20000  # 20 seconds

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        # Update cursor timer
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Check time limit
        tiempo_transcurrido = pygame.time.get_ticks() - start_time
        if tiempo_transcurrido >= tiempo_limite:
            input_active = False

        # Draw the board and players
        screen.fill(WHITE)
        dibujar_tablero()
        for jugador in jugadores:
            pygame.draw.circle(screen, jugador.color, (int(jugador.position[0]), int(jugador.position[1])), jugador.radius)

        # Draw question area
        pregunta_area = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
        pygame.draw.rect(screen, LIGHT_BLUE, pregunta_area)

        # Show the question
        pregunta_font = pygame.font.SysFont(None, 30)
        pregunta_text = pregunta_font.render(pregunta, True, BLACK)
        screen.blit(pregunta_text, (10, SCREEN_HEIGHT - 100))

        # Show the answer input
        input_box = pygame.Rect(10, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 20, 40)
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        respuesta_font = pygame.font.SysFont(None, 40)
        respuesta_text = respuesta_font.render(user_text, True, BLACK)
        screen.blit(respuesta_text, (input_box.x + 5, input_box.y + 5))

        # Draw the cursor
        if cursor_visible:
            cursor_x = input_box.x + 5 + respuesta_font.size(user_text)[0]
            cursor_height = respuesta_font.get_height()
            pygame.draw.line(screen, BLACK, (cursor_x, input_box.y + 5), (cursor_x, input_box.y + 5 + cursor_height), 2)

        # Show remaining time
        tiempo_restante = max(0, (tiempo_limite - tiempo_transcurrido) // 1000)
        tiempo_text = font.render(f"Time: {tiempo_restante}s", True, BLACK)
        screen.blit(tiempo_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))

        # Show score and current turn
        puntos_text = font.render(f"Player 1: {puntos[0]} points    Player 2: {puntos[1]} points", True, BLACK)
        screen.blit(puntos_text, (SCREEN_WIDTH // 2 - puntos_text.get_width() // 2, 20))

        turno_text = font.render(f"Turn of: Player {jugador_actual + 1}", True, BLACK)
        screen.blit(turno_text, (SCREEN_WIDTH // 2 - turno_text.get_width() // 2, 60))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    normalized_user_text = normalizar_texto(user_text)
    if normalized_user_text in respuestas_correctas:
        mostrar_resultado("Correct!" if language == 'es' else "Correct!")
        respuesta_color = GREEN
        puntos[jugador_actual] += 1  # Increase the score
        return True
    else:
        mostrar_resultado("Incorrect." if language == 'es' else "Incorrect.", respuestas_correctas[0], respuesta_color=RED)
        return False
# Function to show winner screen
def mostrar_ganador(jugador):
    global estado
    estado = "ganador"
    ganador = f"{'Jugador' if language == 'es' else 'Player'} {jugador + 1}"

    while estado == "ganador":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "menu"

        screen.fill(WHITE)
        ganador_font = pygame.font.SysFont(None, 50)
        ganador_text = ganador_font.render(f"{ganador} {'ha ganado' if language == 'es' else 'has won'}!", True, GREEN)
        ganador_rect = ganador_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(ganador_text, ganador_rect)

        # Instrucción para volver al menú
        instruction_font = pygame.font.SysFont(None, 30)
        instruction_text = instruction_font.render("Presiona ESC para volver al menú principal." if language == 'es' else "Press ESC to return to the main menu.", True, BLACK)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()

# Function to show instructions
def mostrar_instrucciones():
    global estado, language
    estado = "instrucciones"

    instrucciones_es = [
        "Instrucciones del juego:",
        "",
        "1. Objetivo del Juego:",
        "   - Ser el primero en llegar a 10 puntos respondiendo correctamente preguntas de distintas categorías.",
        "",
        "2. Cómo jugar:",
        "   - Dos jugadores compiten en un tablero de 20 casilleros, numerados y con letras que representan categorías de preguntas (Historia, Geografía, Arte, Entretenimiento).",
        "   - Cada turno, un jugador lanza el dado y avanza en el tablero el número de casilleros que indique el dado.",
        "   - Dependiendo del casillero en el que caiga, se le hará una pregunta de la categoría correspondiente.",
        "   - Si el jugador responde correctamente, gana 1 punto.",
        "   - Si la respuesta es incorrecta o no responde, no se obtiene ningún punto.",
        "",
        "3. Categorías:",
        "   - Historia (H)",
        "   - Geografía (G)",
        "   - Arte (A)",
        "   - Entretenimiento (E)",
        "",
        "4. Mecánica del Turno:",
        "   - Al iniciar su turno, el jugador tira el dado.",
        "   - La ficha se mueve al número de casillas correspondiente.",
        "   - Se muestra una pregunta de la categoría de la casilla.",
        "   - Responde la pregunta.",
        "   - El primer jugador en llegar a 10 puntos gana.",
        "",
        "Presiona ESC para volver al menú principal."
    ]

    instrucciones_en = [
        "Game Instructions:",
        "",
        "1. Game Objective:",
        "   - Be the first to reach 10 points by correctly answering questions from different categories.",
        "",
        "2. How to Play:",
        "   - Two players compete on a board of 20 squares, numbered and with letters representing question categories (History, Geography, Art, Entertainment).",
        "   - Each turn, a player rolls the die and moves on the board the number of squares indicated by the die.",
        "   - Depending on the square they land on, they will be asked a question from the corresponding category.",
        "   - If the player answers correctly, they gain 1 point.",
        "   - If the answer is incorrect or they don't answer, no points are obtained.",
        "",
        "3. Categories:",
        "   - History (H)",
        "   - Geography (G)",
        "   - Art (A)",
        "   - Entertainment (E)",
        "",
        "4. Turn Mechanics:",
        "   - At the start of their turn, the player rolls the die.",
        "   - The token moves to the corresponding number of squares.",
        "   - A question from the category of the square is shown.",
        "   - Answer the question.",
        "   - The first player to reach 10 points wins.",
        "",
        "Press ESC to return to the main menu."
    ]

    while estado == "instrucciones":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "menu"
        screen.fill(WHITE)

        instrucciones = instrucciones_es if language == 'es' else instrucciones_en

        y_offset = 20
        for line in instrucciones:
            if line == "":
                y_offset += 20
                continue
            text = font.render(line, True, BLACK)
            screen.blit(text, (50, y_offset))
            y_offset += 30

        pygame.display.flip()
        pygame.time.Clock().tick(60)
def mostrar_dado(dado):
    global turno
    # Area to show the die
    dado_area = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
    pygame.draw.rect(screen, LIGHT_BLUE, dado_area)

    # Show "Rolling die..."
    dado_font = pygame.font.SysFont(None, 50)
    tirando_text = dado_font.render("Tirando dado..." if language == 'es' else "Rolling the dice...", True, BLACK)
    screen.blit(tirando_text, (SCREEN_WIDTH // 2 - tirando_text.get_width() // 2, SCREEN_HEIGHT - 150))

    # Show which player is rolling the die
    jugador_text = font.render(f"{'Jugador' if language == 'es' else 'Player'} {turno + 1} {'está tirando el dado' if language == 'es' else 'is rolling the dice'}", True, BLACK)
    screen.blit(jugador_text, (SCREEN_WIDTH // 2 - jugador_text.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.flip()
    pygame.time.delay(1000)  # Wait 1 second

    # Clear the die area
    pygame.draw.rect(screen, LIGHT_BLUE, dado_area)

    # Show the die result
    dado_text = dado_font.render(f"{'Dado' if language == 'es' else 'Dice'}: {dado}", True, BLACK)
    screen.blit(dado_text, (SCREEN_WIDTH // 2 - dado_text.get_width() // 2, SCREEN_HEIGHT - 150))

    # Keep the player text
    screen.blit(jugador_text, (SCREEN_WIDTH // 2 - jugador_text.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.flip()
    pygame.time.delay(1000)  

# Function to draw the board
def dibujar_tablero():
    for casilla_num, (x, y) in casillas_posiciones.items():
        # Determine the category
        categoria = categories[(casilla_num - 1) % len(categories)]
        color = CATEGORY_COLORS[categoria]

        # Draw the square
        pygame.draw.rect(screen, color, (x, y, CELL_WIDTH, CELL_HEIGHT))

        # Draw the square border
        pygame.draw.rect(screen, BLACK, (x, y, CELL_WIDTH, CELL_HEIGHT), 2)

        # Render the square number
        numero_font = pygame.font.SysFont(None, 30)
        numero_text = numero_font.render(str(casilla_num), True, BLACK)
        screen.blit(numero_text, (x + 10, y + 10))

        # Render the category
        categoria_font = pygame.font.SysFont(None, 24)
        categoria_text = categoria_font.render(categoria, True, BLACK)
        screen.blit(categoria_text, (x + CELL_WIDTH - 30, y + CELL_HEIGHT - 30))

def juego():
    global estado, turno, puntos, jugadores

    estado = "juego"
    turno = 0
    puntos = [0, 0]

    jugador1 = Player(color=RED, casilla_inicial=1)
    jugador2 = Player(color=BLUE, casilla_inicial=1)
    jugadores = [jugador1, jugador2]

    pregunta_text = ""
    respuesta_text = ""
    respuesta_color = BLACK

    clock = pygame.time.Clock()

    while estado == "juego":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        dibujar_tablero()

        for jugador in jugadores:
            jugador.actualizar()
            pygame.draw.circle(screen, jugador.color, (int(jugador.position[0]), int(jugador.position[1])), jugador.radius)

        puntos_text = font.render(f"{'Jugador' if language == 'es' else 'Player'} 1: {puntos[0]} {'puntos' if language == 'es' else 'points'}    {'Jugador' if language == 'es' else 'Player'} 2: {puntos[1]} {'puntos' if language == 'es' else 'points'}", True, BLACK)
        screen.blit(puntos_text, (SCREEN_WIDTH//2 - puntos_text.get_width()//2, 20))

        turno_text = font.render(f"{'Turno de' if language == 'es' else 'Turn of'}: {'Jugador' if language == 'es' else 'Player'} {turno + 1}", True, BLACK)
        screen.blit(turno_text, (SCREEN_WIDTH//2 - turno_text.get_width()//2, 60))

        current_player = jugadores[turno]
        
        if current_player.position == current_player.target_position:
            # Roll the die
            dado = random.randint(1, 6)
            mostrar_dado(dado)
            pygame.display.flip()
            pygame.time.delay(1000)  # Wait for 1 second after showing the dice

            # Calculate new position
            nueva_casilla = current_player.casilla_actual + dado
            if nueva_casilla > 20:
                nueva_casilla = nueva_casilla - 20

            current_player.mover_a(nueva_casilla)

            # Move the player
            while current_player.position != current_player.target_position:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                screen.fill(WHITE)
                dibujar_tablero()
                for jugador in jugadores:
                    jugador.actualizar()
                    pygame.draw.circle(screen, jugador.color, (int(jugador.position[0]), int(jugador.position[1])), jugador.radius)
                
                pygame.display.flip()
                clock.tick(60)

            categoria = categories[(nueva_casilla - 1) % len(categories)]

            # Show question
            pregunta_data = obtener_pregunta(categoria)
            
            if pregunta_data:
                pregunta, respuestas_correctas = pregunta_data
                correcto = mostrar_pregunta(pregunta, respuestas_correctas, turno, puntos, dado)

                if puntos[turno] >= 10:
                    mostrar_ganador(turno)
                    break

            turno = 1 - turno

        # Show the last question and answer
        pregunta_area = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
        pygame.draw.rect(screen, LIGHT_BLUE, pregunta_area)
        pregunta_font = pygame.font.SysFont(None, 24)
        respuesta_font = pygame.font.SysFont(None, 30)
        
        pregunta_render = pregunta_font.render(pregunta_text, True, BLACK)
        respuesta_render = respuesta_font.render(respuesta_text, True, respuesta_color)
        
        screen.blit(pregunta_render, (10, SCREEN_HEIGHT - 190))
        screen.blit(respuesta_render, (10, SCREEN_HEIGHT - 160))

        pygame.display.flip()
        clock.tick(60)

# Function to show start screen and handle menu
def pantalla_inicio():
    global estado, language
    estado = "menu"

    # Create buttons
    play_button = Button(
        x=SCREEN_WIDTH//2 - 100,
        y=SCREEN_HEIGHT//2 - 60,
        width=200,
        height=50,
        text="Jugar",
        color=GREEN,
        hover_color=YELLOW
    )

    instructions_button = Button(
        x=SCREEN_WIDTH//2 - 100,
        y=SCREEN_HEIGHT//2 + 10,
        width=200,
        height=50,
        text="Instrucciones",
        color=ORANGE,
        hover_color=YELLOW
    )

    exit_button = Button(
        x=SCREEN_WIDTH//2 - 100,
        y=SCREEN_HEIGHT//2 + 80,
        width=200,
        height=50,
        text="Salir",
        color=RED,
        hover_color=YELLOW
    )

    # New language switch button
    language_button = Button(
        x=SCREEN_WIDTH - 220,
        y=20,
        width=200,
        height=50,
        text="Switch to English",
        color=BLUE,
        hover_color=LIGHT_BLUE
    )

    while estado == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event):
                    juego()
                if instructions_button.is_clicked(event):
                    mostrar_instrucciones()
                if exit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()
                if language_button.is_clicked(event):
                    # Switch language
                    language = 'en' if language == 'es' else 'es'
                    # Update button texts
                    play_button.update_text("Jugar" if language == 'es' else "Play")
                    instructions_button.update_text("Instrucciones" if language == 'es' else "Instructions")
                    exit_button.update_text("Salir" if language == 'es' else "Exit")
                    language_button.update_text("Switch to English" if language == 'es' else "Cambiar a Español")
                    # Reload questions in the new language
                    recargar_preguntas()

        screen.fill(LIGHT_BLUE)
        dibujar_tablero()

        # Draw buttons
        play_button.draw(screen)
        instructions_button.draw(screen)
        exit_button.draw(screen)
        language_button.draw(screen)

        # Game Title
        title_font = pygame.font.SysFont(None, 60)
        title_text = title_font.render("Scientia Vitae", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        screen.blit(title_text, title_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Limit to 60 FPS

# Main function
def main():
    recargar_preguntas()
    pantalla_inicio()
if __name__ == "__main__":
    main()
