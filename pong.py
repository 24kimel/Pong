import turtle


wn = turtle.Screen()
wn.title("Pong by Itai")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1/4
ball.dy = 1/4


def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def paddle_a_up():
    if paddle_a.ycor() <= 230:
        paddle_a.sety(paddle_a.ycor() + 20)


def paddle_a_down():
    if paddle_a.ycor() >= -230:
        paddle_a.sety(paddle_a.ycor() - 20)


def paddle_b_up():
    if paddle_b.ycor() <= 230:
        paddle_b.sety(paddle_b.ycor() + 20)


def paddle_b_down():
    if paddle_b.ycor() >= -230:
        paddle_b.sety(paddle_b.ycor() - 20)


wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

# pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Score
score_a = 0
score_b = 0


# main loop
while True:
    wn.update()

    # ball movement
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # borders
    if abs(ball.ycor()) > 290:
        ball.sety(sgn(ball.ycor())*290)
        ball.dy *= -1

    if abs(ball.xcor()) > 390:
        if ball.xcor() > 0:
            score_a += 1
        else:
            score_b += 1
        pen.clear()
        pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    # collisions
    if abs(ball.xcor()) > 340 and (abs(ball.ycor() - paddle_b.ycor()) < 50 or abs(ball.ycor() - paddle_a.ycor()) < 50):
        ball.setx(sgn(ball.xcor()) * 340)
        ball.dx *= -1
