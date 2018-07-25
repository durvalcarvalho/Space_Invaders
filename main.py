import turtle
import math
import random


# Tela do Jogo
tela = turtle.Screen()
tela.bgcolor('black')
tela.title('Space Invaders')
tela.bgpic('space_invaders_background.gif')

turtle.register_shape('invader.gif')
turtle.register_shape('player.gif')

# Bordas do Jogo
bordas = turtle.Turtle()
bordas.speed(0)
bordas.color('white')
bordas.penup() #Levantando a 'caneta' para mudar a posição da turtle sem 'riscar'
bordas.setposition(-300,-300)
bordas.pendown()    #Descendo a 'caneta'
bordas.pensize(3)   #Grossura da ponta da 'caneta'

for side in range(4): #Um retangulo
    bordas.fd(600)  #Foward
    bordas.rt(90)   #Feft
bordas.hideturtle()

# Pontuação durante o jogo
pontos = 0

# Mostrar a pontuação
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290,280)
scorestring = 'Pontuação: %s' %pontos
score_pen.write(scorestring, False, align='left', font=("Arial", 14, "normal"))
score_pen.hideturtle()
 

# Nave do jogador
player = turtle.Turtle()
player.color('blue')
player.shape('player.gif')
player.penup()
player.speed(0)
#player.turtlesize(.5,.5,.5)
#player.setundobuffer
player.setposition(0, -250)
player.setheading(90)
playerspeed = 25


# Quantidade de enemigos no jogo
number_of_enemies = 10
enemies = []
enemyspeed = 5

#lista de inimgos
for i in range(number_of_enemies):
    # Criando os enimigos
    enemies.append(turtle.Turtle())

for enemy in enemies:
    enemy.color(random.choice(['red', 'green', 'yellow']))
    enemy.shape('invader.gif')
    enemy.penup()
    enemy.speed(0)
    #enemy.turtlesize(.5,.5,.5)
    x = random.randint(-200, 200)
    y = random.randint(100, 150)
    enemy.setposition(x, y)


# Criar a bala da Nave do jogador
bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle()
bulletspeed = 50


# Definir o estado da bala
# Ready
# Firing
bulletstate = 'ready'


# Movimentar o jogador

def move_left():
    x = player.xcor()
    x = x - playerspeed
    if (x < -315):x = -315

    player.setx(x)


def move_right():
    x = player.xcor()
    x = x + playerspeed
    if (x > 315): x = 315

    player.setx(x)


def fire_bullet():
    global bulletstate
    if bulletstate == 'ready':
        bulletstate = 'firing'
        # Movimentar a bola
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x,y)
        bullet.showturtle()


def isColision(t1,t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 25:
        return True
    else:
        return False



'''
# Receber os comandos do jogador teclado
turtle.listen()
turtle.onkey(move_left, 'Left')
turtle.onkey(move_right, 'Right')
turtle.onkey(fire_bullet, 'space')
'''

moving = 'left'
closiest_e = 1000
# Main game loop
while True:

    # Movimentar os Inimigos

    for enemy in enemies:
        x = enemy.xcor()
        x = x + enemyspeed
        enemy.setx(x)

        e_dist = enemy.ycor()
        if (e_dist < closiest_e):
            closiest_e = e_dist
            right_e = enemy

        # Mover todos os inimigos para baixo quando acertar as bordas
        if (enemy.xcor() > 280 or enemy.xcor() < -280):
            for e in enemies:
                y = e.ycor()
                y = y - 20
                e.sety(y)
            enemyspeed *= -1


        # Checar se há colisão
        if isColision(bullet, enemy):
            # Resetar a bullet
            bullet.hideturtle()
            bulletstate = 'ready'
            bullet.setposition(0, -400) # Evitar colisões futuras
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

            # Atualizar a Pontuação
            pontos = pontos + 100
            scorestring = "Pontuação: %s" %pontos
            score_pen.clear()
            score_pen.write(scorestring, False, align='left', font=("Arial", 14, "normal"))
        

        if isColision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print ("Game Over")
            break

    # Movimentar a nave

    if (right_e.xcor() > player.xcor()):
        move_right()
    else:
        move_left()
    
    fire_bullet()


    # Movimentar a bala
    if bulletstate == 'firing':
        y = bullet.ycor()
        y = y + bulletspeed
        bullet.sety(y)

    # Checar se a bala já chegou no limite da tela
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = 'ready'
    
