from random import randrange, choice
from turtle import *
from freegames import square, vector

# Preguntas de Gabriela Mistral
PREGUNTAS_GABRIELA_MISTRAL = [
    {
        "pregunta": "¿Cuál era el verdadero nombre de Gabriela Mistral?",
        "opciones": ["Lucila Godoy Alcayaga", "María González", "Ana López"],
        "correcta": 0
    },
    {
        "pregunta": "¿En qué país nació Gabriela Mistral?",
        "opciones": ["Chile", "Argentina", "Perú"],
        "correcta": 0
    },
    {
        "pregunta": "¿Qué premio importante ganó Gabriela Mistral?",
        "opciones": ["Premio Nobel de literatura", "Premio Oscar", "Premio Grammy"],
        "correcta": 0
    }
]

# Variables globales
food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
score = 0
game_over = False
trivia_activa = False
pregunta_actual = None

# Tortugas
score_display = Turtle()
restart_button = Turtle()
wall_drawer = Turtle()
trivia_display = Turtle()
option_buttons = [Turtle() for _ in range(3)]

# Ocultar todas las tortugas
for t in [score_display, restart_button, wall_drawer, trivia_display] + option_buttons:
    t.hideturtle()


def update_score():
    """Actualiza la puntuación en la pantalla"""
    score_display.clear()
    score_display.penup()
    score_display.goto(120, 160)
    score_display.write(
        f"Score: {score}", align="center", font=("Courier", 24, "normal"))


def draw_restart_button():
    """Dibuja el botón de reinicio"""
    restart_button.clear()
    restart_button.penup()
    restart_button.goto(0, -50)
    restart_button.color('black')
    restart_button.write("Click to Restart", align="center",
                         font=("Courier", 24, "normal"))


def inside(head):
    """Verifica si la cabeza de la serpiente está dentro de los límites"""
    return -200 < head.x < 190 and -200 < head.y < 190


def change(x, y):
    """Cambia la dirección de la serpiente"""
    aim.x = x
    aim.y = y


def mostrar_trivia():
    """Muestra una pregunta aleatoria sobre Gabriela Mistral"""
    global trivia_activa, pregunta_actual
    trivia_activa = True
    pregunta_actual = choice(PREGUNTAS_GABRIELA_MISTRAL)

    # Mostrar pregunta
    trivia_display.clear()
    trivia_display.penup()
    trivia_display.goto(0, 50)
    trivia_display.color('black')
    trivia_display.write(
        pregunta_actual["pregunta"], align="center", font=("Arial", 16, "normal"))

    # Mostrar opciones
    for i, (opcion, button) in enumerate(zip(pregunta_actual["opciones"], option_buttons)):
        button.clear()
        button.penup()
        button.goto(-100, 0 - i*40)
        button.write(f"{i+1}. {opcion}", font=("Arial", 14, "normal"))


def verificar_respuesta(opcion):
    """Verifica si la respuesta seleccionada es correcta"""
    global trivia_activa
    if not trivia_activa:
        return

    if opcion == pregunta_actual["correcta"]:
        trivia_display.clear()
        for button in option_buttons:
            button.clear()
        trivia_activa = False
        move()  # Continuar el juego
    else:
        # Mostrar mensaje de error (opcional)
        pass


def move():
    """Move snake forward one segment."""
    global score, game_over, trivia_activa

    if trivia_activa:
        ontimer(move, 150)
        return

    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        game_over = True
        square(head.x, head.y, 9, 'red')
        update()
        draw_restart_button()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        mostrar_trivia()
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
        score += 1
        update_score()
    else:
        snake.pop(0)

    clear()
    draw_walls()

    for body in snake:
        square(body.x, body.y, 9, 'green')

    square(food.x, food.y, 9, 'brown')
    update()
    ontimer(move, 150)


def draw_walls():
    """Dibuja los límites del área de juego"""
    wall_drawer.clear()
    wall_drawer.penup()
    wall_drawer.goto(-200, -200)  # Esquina inferior izquierda
    wall_drawer.pendown()
    wall_drawer.color('blue')  # Color de las paredes
    wall_drawer.pensize(3)  # Grosor de las paredes

    # Dibujar rectángulo 390x390 (límites del juego)
    for _ in range(4):
        wall_drawer.forward(390)
        wall_drawer.left(90)

    wall_drawer.penup()


def restart_game(x, y):
    """Reinicia el juego cuando se hace clic en el botón de reinicio"""
    global snake, score, game_over, trivia_activa
    if game_over and -100 < x < 100 and -70 < y < -30:
        # Reiniciar variables
        snake = [vector(10, 0)]
        score = 0
        game_over = False
        trivia_activa = False

        # Reiniciar comida
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10

        # Limpiar pantalla
        clear()
        restart_button.clear()
        trivia_display.clear()
        for button in option_buttons:
            button.clear()

        # Redibujar elementos
        draw_walls()
        update_score()
        move()


# Asignar teclas 1, 2 y 3 para seleccionar opciones de trivia
onkey(lambda: verificar_respuesta(0), '1')
onkey(lambda: verificar_respuesta(1), '2')
onkey(lambda: verificar_respuesta(2), '3')

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
draw_walls()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
onscreenclick(restart_game)
update_score()
move()
done()
