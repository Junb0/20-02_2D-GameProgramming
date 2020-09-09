import turtle
import random

row = []
col = []
turtle.speed(5)
turtle.penup()
while (True):
    if len(row) >= 6 and len(col) >= 6:
        break
    if len(row) < 6 and random.randint(0, 1):
        r = random.randint(0,5)
        while r in row:
            r = random.randint(0,5)
        row.append(r)
        if random.randint(0,1):
            turtle.goto(0, r*100)
            turtle.setheading(0)
            turtle.pendown()
            turtle.forward(500)
        else:
            turtle.goto(500, r*100)
            turtle.setheading(180)
            turtle.pendown()
            turtle.forward(500)
    elif len(col) < 6:
        c = random.randint(0,5)
        while c in col:
            c = random.randint(0,5)
        col.append(c)
        if random.randint(0,1):
            turtle.goto(c*100, 0)
            turtle.setheading(90)
            turtle.pendown()
            turtle.forward(500)
        else:
            turtle.goto(c*100, 500)
            turtle.setheading(-90)
            turtle.pendown()
            turtle.forward(500)
    turtle.penup()
turtle.penup()
turtle.home()
turtle.exitonclick()
