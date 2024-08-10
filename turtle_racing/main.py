import turtle
import time
import random

WIDTH, HEIGHT = 600, 600
COLORS = ['red', 'green', 'blue', 'orange', 'yellow', 'black', 'purple', 'pink', 'brown', 'cyan']


class MyTurtle:
    def __init__(self, color):
        self.turtle = turtle.Turtle()
        self.color = color

    def set_turtle(self, x_pos, y_pos):
        my_turtle = self.turtle
        my_turtle.color(self.color)
        my_turtle.shape('turtle')
        my_turtle.left(90)
        my_turtle.penup()
        my_turtle.setpos(x_pos, y_pos)
        my_turtle.pendown()

    def move(self):
        step = random.randrange(1, 21)
        self.turtle.forward(step)
        return self.turtle.pos()


def init_arena(count):
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title('Turtle Racing!')

    turtles = []
    colors = random.sample(COLORS, count)
    spacing_x = WIDTH // (len(colors) + 1)
    for i, color in enumerate(colors):
        x_pos, y_pos = -WIDTH // 2 + (i + 1) * spacing_x, -HEIGHT // 2 + 20
        racer = MyTurtle(color)
        racer.set_turtle(x_pos, y_pos)
        turtles.append(racer)

    return turtles


def race(turtles):
    winner = None
    while not winner:
        for racer in turtles:
            x, y = racer.move()
            if y >= HEIGHT // 2 - 10:
                winner = racer.color
                break
    print(f"The winner is the {winner} turtle!")


if __name__ == '__main__':
    racer_count = int(input("Enter number of racers (2 - 10): "))
    if racer_count < 2 or racer_count > 10:
        print("Invalid number of racers")
    else:
        racers = init_arena(racer_count)
        race(racers)
        time.sleep(10)
