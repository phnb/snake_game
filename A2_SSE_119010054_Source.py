from turtle import Turtle, Screen
from random import randint

#Global variable
g_tip = Turtle()
pre_move = True
pre_move1 = False; pre_move2 = False
pre_move3 = False; pre_move4 = False     #Record the previous move
all_pos = []
b = []
coor_snakeBody = []
rest = 0
num = 0
game_over = False
snake_length = 6
num_contact = 0
status = "Paused"
time = 0

# Draw the margin area
def configureMargin():
    g_margin = Turtle()
    g_margin.speed(0)    
    g_margin.pensize(3)
    g_margin.penup()
    g_margin.goto(-250, 290)
    g_margin.pendown()
    g_margin.color('black')
    for i in range(2):
        g_margin.forward(500)
        g_margin.right(90)
        g_margin.forward(80)
        g_margin.right(90)
    g_margin.penup()
    g_margin.goto(-250, 210)
    g_margin.pendown()
    for i in range(2):
        g_margin.forward(500)
        g_margin.right(90)
        g_margin.forward(500)
        g_margin.right(90)  
    g_margin.hideturtle()

# Draw the screen of width: 660 and height: 740
def configureScreen(x = 660, y = 740):
    screen = Screen()
    screen.setup(x, y)
    screen.title('Snake by Jared Dai')
    screen.tracer(0)
    return screen

# Draw the snake,
def configureSnake():
    t = Turtle("square")
    t.up()
    t.color('red', 'red')
    return t
    
# Draw the monster    
def configureMonster():
    mon = Turtle("square")
    mon.up()
    x = randint(-230,230)
    y = randint(-270,-100)
    mon.color("purple")
    mon.goto(x, y)
    return mon, x, y

#Draw the introduction page
def configureText():
    g_intro = Turtle()
    instroduction = [None]*3
    instroduction[0] = "Welcome to Jared's version of snake..."
    instroduction[1] = "You're going to use the 4 arrow keys to move the snake\naround the screen, trying to consume all the food items\nbefore the monster catches you..."
    instroduction[2] = "Click any where on the screen to start the game, have fun!"

    g_intro.penup()
    g_intro.hideturtle()
    g_intro.goto(-180,160)
    g_intro.write(instroduction[0], font = ("Arial", 12))
    g_intro.penup()
    g_intro.hideturtle()
    g_intro.goto(-180,80)
    g_intro.write(instroduction[1], font = ("Arial", 12))
    g_intro.penup()
    g_intro.hideturtle()
    g_intro.goto(-180,40)
    g_intro.write(instroduction[2],font = ("Arial", 12))

    g_intro.hideturtle() 
    g_intro.penup()
    g_intro.goto(-160, 240)
    g_intro.write(("    Contacted: " + str(num_contact) + "     Time: " + str(int(time)) + "     Motion: " + str(status)), False, font=("Arial", 14))
    g_intro.hideturtle()
    return g_intro

#randomly generateFood the food
def generateFood():
    global g_num
    global all_pos
    for i in range(501*501 + 1):
        all_pos.append(0)
    num = 1
    while num <= 9:
        x = randint(-220, 220)
        y = randint(-260, 180)
        i = 500 * x + y + 250 * 501
        all_pos[i] = num
        g_num.goto(x, y)
        g_num.write(num, font = ("Arial", 12))
        num += 1


#pause the motion of the snake
def pause():
    global pre_move1, pre_move2, pre_move3, pre_move4, status
    status = "Paused"
    pre_move1 = not pre_move1
    pre_move2 = not pre_move2
    pre_move3 = not pre_move3
    pre_move4 = not pre_move4
    if not pre_move1 and not pre_move2 and not pre_move3 and pre_move4:
        moveRight()
    elif not pre_move1 and not pre_move2 and pre_move3 and not pre_move4:
        moveLeft()
    elif not pre_move1 and pre_move2 and not pre_move3 and not pre_move4:
        moveDown()
    elif pre_move1 and not pre_move2 and not pre_move3 and not pre_move4:
        moveUp()

#Check whether monster contact with snake
def contact(x, y):
    global num_contact, coor_snakeBody
    for i in range(len(coor_snakeBody)):
        if coor_snakeBody[i] != None:
            if abs(coor_snakeBody[i][0] - x) < 20 and abs(coor_snakeBody[i][1] - y) < 20:
                num_contact += 1
                break    

# Juage whether there is a food in the area
def judge(x, y):
    global g_num, rest, snake_length
    state = True
    for i in range(x-15, x+16):
        for j in range(y-15, y+16):
            k = 500 * i + j + 250 * 501
            if k > 501 * 501:        # If the detection range is too large
                break
            else:
                if all_pos[k] != 0:
                    snake_length += all_pos[k]
                    rest += all_pos[k]
                    all_pos[k] = 0
                    state = False
    if not state:
        g_num.clear()
        for i in range(-250,251):
            for j in range(-250,251):
                k = 500 * i + j + 250 * 501
                if all_pos[k] != 0:
                    g_num.goto(i,j)
                    g_num.write(all_pos[k], font = ("Arial", 12))

# Determine the different status and move the snake
def moveSnake(snake_status): 
    global g_snake, num, rest, snake_length, status
    g_snake.color("blue", "black")
    if snake_status == "Up":
        status = "Up"
        g_snake.setheading(90)
    elif snake_status == "Down":
        status = "Down"
        g_snake.setheading(270)
    elif snake_status == "Left":
        status = "Left"
        g_snake.setheading(180)
    else:
        status = "Right"
        g_snake.setheading(0)
    b.append(g_snake.stamp())
    g_snake.forward(20)
    g_snake.color("red")
    x = int(g_snake.position()[0])
    y = int(g_snake.position()[1])
    judge(x, y)
    coor_snakeBody.append([x, y])
    if len(b) > 5 and rest == 0:
        g_snake.clearstamp(b[num])
        coor_snakeBody[num] = None
        num += 1
    if rest > 0:
        rest -= 1                   

# Move up the snake's head    
def moveUp():
    global g_snake, g_screen, pre_move2, pre_move3, pre_move4, num, rest, game_over,  snake_length, status
    if pre_move2 or pre_move3 or pre_move4 or game_over : 
        return
    y = int(g_snake.position()[1])
    if y <= 180:
        moveSnake("Up")
    g_screen.update()
    g_screen.ontimer(moveUp, 300 + (snake_length - rest)*2)

# Move down snake's head 
def moveDown():
    global g_snake, g_screen, pre_move1, pre_move3, pre_move4, num, rest, game_over ,  snake_length, status
    if pre_move1 or pre_move3 or pre_move4 or game_over : 
        return
    y = int(g_snake.position()[1])
    if y >= -260:
        moveSnake("Down")
    g_screen.update()
    g_screen.ontimer(moveDown, 300 + (snake_length - rest)*2)

# Move left snake's head
def moveLeft():
    global g_snake, g_screen, pre_move1, pre_move2, pre_move4, num, rest, game_over ,  snake_length, status
    if pre_move1 or pre_move2 or pre_move4 or game_over : 
        return
    x = int(g_snake.position()[0])
    if x >= -220:
        moveSnake("Left")
    g_screen.update()
    g_screen.ontimer(moveLeft, 300 + (snake_length - rest)*2)

# Move right snake's head 
def moveRight():
    global g_snake, g_screen, pre_move1, pre_move2, pre_move3, num, rest, game_over ,  snake_length, status
    if pre_move1 or pre_move2 or pre_move3 or game_over : 
        return
    x = int(g_snake.position()[0])
    if x <= 230:
        moveSnake("Right")
    g_screen.update()
    g_screen.ontimer(moveRight, 300 + (snake_length - rest)*2)

# Move the monster
def monsterMove():
    global g_tip, g_monster, g_screen, g_snake, game_over ,  num_contact, time, status
    if game_over : 
        return
    x1 = int(g_monster.position()[0]) - int(g_snake.position()[0])
    y1 = int(g_monster.position()[1]) - int(g_snake.position()[1])
    n1 = int(0.95*(300 + 2*(snake_length - rest)))
    n2 = int(1.40*(300 + 2*(snake_length - rest)))     
    speed = randint(n1, n2)      # monster moves in a random time
    if abs(x1) > abs(y1):
        if x1 > 0:
            g_monster.setheading(180)
            g_monster.forward(20)
            checkOver()
            g_screen.update()
        else:
            g_monster.setheading(0)
            g_monster.forward(20)
            checkOver()
            g_screen.update()
    else:
        if y1 > 0:
            g_monster.setheading(270)
            g_monster.forward(20)
            checkOver()
            g_screen.update()
        else:
            g_monster.setheading(90)
            g_monster.forward(20)
            checkOver()
            g_screen.update()
    if game_over : 
        return
    g_screen.ontimer(monsterMove, speed)   
    x, y = g_monster.position()
    contact(x, y) 
    time = time + speed/1000
    g_tip.clear()
    g_tip.speed(0)
    g_tip.hideturtle() 
    g_tip.penup()
    g_tip.goto(-160,240)
    g_tip.write(("       Contacted: " + str(num_contact) + "     Time: " + str(int(time)) + "     Motion: " + str(status)), False, font=("Arial", 14))
    g_tip.hideturtle()

def up():
    global pre_move1, pre_move2, pre_move3, pre_move4, g_screen, snake_length, rest
    if status == "Paused" or not pre_move1:
        pre_move1 = True
        pre_move2 = False
        pre_move3 = False
        pre_move4 = False
        g_screen.ontimer(moveUp, 300 + (snake_length - rest)*2)
    else:
        return

def down():
    global pre_move1, pre_move2, pre_move3, pre_move4, g_screen, snake_length, rest
    if status == "Paused" or not pre_move2:
        pre_move2 = True
        pre_move1 = False
        pre_move3 = False
        pre_move4 = False
        g_screen.ontimer(moveDown, 300 + (snake_length - rest)*2)
    else:
        return

def left():
    global pre_move1, pre_move2, pre_move3, pre_move4, g_screen, snake_length, rest
    if status == "Paused" or not pre_move3:
        pre_move3 = True
        pre_move1 = False
        pre_move2 = False
        pre_move4 = False
        g_screen.ontimer(moveLeft, 300 + (snake_length - rest)*2)
    else:
        return

def right():
    global pre_move1, pre_move2, pre_move3, pre_move4, g_screen, snake_length, rest
    if status == "Paused" or not pre_move4:
        pre_move4 = True
        pre_move1 = False
        pre_move2 = False
        pre_move3 = False
        g_screen.ontimer(moveRight, 300 + (snake_length - rest)*2)
    else:
        return

#Check whether the game is over
def checkOver():
    global g_snake, g_screen, g_monster, g_num, game_over ,  num_contact, time
    x1 = int(g_snake.position()[0])
    y1 = int(g_snake.position()[1])
    x2 = int(g_monster.position()[0])
    y2 = int(g_monster.position()[1])
    if abs(x1-x2) < 20 and abs(y1-y2) < 20:
        g_num.goto(max(x1-30, -250), min(y1+10, 250))
        g_num.color("green")
        g_num.write("Game_over !!", font = ("Arial", 12))
        game_over = True
        num_contact += 1
        return
    is_win = True
    for i in range(-250, 251):
        for j in range(-290, 211):
            if all_pos[500*i + j + 250*501] != 0:
                is_win = False
                break
    if is_win:
        game_over = True
        g_num.goto(max(x1-30,-250), min(y1+10,250))
        g_num.color("green")
        g_num.write("Winner!!!", font = ("Arial", 12))

# Relate the movement with the keyboard
def configureKey():
    global g_screen
    g_screen.onkey(up, "Up")
    g_screen.onkey(down, "Down")
    g_screen.onkey(left, "Left")
    g_screen.onkey(right, "Right")
    g_screen.onkey(pause, "space")
    g_screen.listen()


def main(x,y):
    global g_screen, pre_move, g_num
    while pre_move:
        g_num.clear()
        generateFood()
        g_screen.update()
        monsterMove()
        g_screen.ontimer(up, 400)
        g_screen.listen()
        g_screen.ontimer(configureKey, 2500)
        pre_move = False

if __name__ == "__main__":
    configureMargin()
    g_screen = configureScreen()
    g_snake = configureSnake()
    g_monster, x, y = configureMonster()
    g_num = configureText()
    g_screen.update()
    g_screen.onclick(main)
    g_screen.mainloop()