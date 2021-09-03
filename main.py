from random import *
import turtle
import time

# Constants
# States depicted as color
HEALTHY = "green"
EXSPOSED = "orange"
SYMPTOMATIC = "red"
ASYMPTOMATIC = "purple"
RECOVERED = "blue"
DEAD = "black"
START = time.time()  # start time
PEOPLE_COUNT = 100  # amount of people in the world
LENGTH = 80  # box for turtle to draw
BOARDER = LENGTH * 3  # limit the turtles can spawn
SEC_PER_DAY = 1
COLI = ('Arial', 10, 'normal')
POLI = ('Arial', 20, 'normal')

# var
world_time = -1  # world time
running = True  # game run bool
day = 1  # days passed in simulation
healthy = 0
exsposed = 0
symptomatic = 0
asymptomatic = 0
recovered = 0
dead = 0


# class for people in simulation
class Person:
    def __init__(self):
        self.can_move = True
        self.t = turtle.Turtle()
        self.t.pu()
        self.t.rt(randint(0, 360))

    # random movement for turtles
    def movement(self):

        if self.can_move:
            self.t.fd(10)
            self.t.lt(randint(-30, 30))

            if self.t.xcor() > LENGTH:
                self.t.seth(180)
            if self.t.ycor() > LENGTH:
                self.t.seth(270)
            if self.t.xcor() < -LENGTH:
                self.t.seth(0)
            if self.t.ycor() < -LENGTH:
                self.t.seth(90)

    def position(self, x, y):
        self.t.goto(x, y)


# Class for virus states and state changes
class Virus(Person):
    def __init__(self):
        super().__init__()
        self.state = HEALTHY
        self.t.color(self.state)
        self.contact = False
        self.recovery_time = -1
        self.time_of_exsposure = -1
        self.time_of_infection = -1
        self.fate = -1
        self.choice = -1
        self.contact_time = -1

    # state changer
    def change_state(self, state):
        self.state = state
        self.t.color(state)

    # transition from healthy to exposed

    def check(self, sick_p, current_time):
        if self.t.distance(sick_p.t) < 10 and self.state == HEALTHY:
            if not self.contact:
                self.contact_time = current_time
                self.contact = True
            if current_time - self.contact_time >= .5:
                self.change_state(EXSPOSED)
                self.choice = randint(1, 2)  # randomizer for exsposed
                self.time_of_exsposure = current_time
                return True
        else:
            self.contact = False

    # random transition from exposed to either asymptomatic or symptomatic

    def exsposed(self, current_time):
        if current_time - self.time_of_exsposure >= 10:
            if self.choice == 1:
                self.change_state(ASYMPTOMATIC)
                self.time_of_infection = current_time
            if self.choice == 2:
                self.change_state(SYMPTOMATIC)
                self.time_of_infection = current_time
                self.fate = randint(1, 3)

    # transition to recovered only

    def asymptomatic(self, current_time):
        if current_time - self.time_of_infection >= 15:
            self.change_state(RECOVERED)
            self.recovery_time = current_time

    # random transition to either dead or recovered

    def symptomatic(self, current_time):
        if current_time - self.time_of_infection >= 15:
            if self.fate == 1:
                self.change_state(DEAD)
            elif self.fate == 2 or 3:
                self.change_state(RECOVERED)
                self.recovery_time = current_time


# Writer Class
class Gui:
    def __init__(self):
        self.h = turtle.Turtle()
        self.h.pu()
        self.h.hideturtle()

    def goto(self, x, y):
        self.h.goto(x, y)

    def dot(self, size, color):
        self.h.dot(size, color)

    def write(self, text):
        self.h.write(text, False, font=POLI, align="left")

    def stats(self, text):
        self.h.clear()
        self.h.write(text)


# screen setup
s = turtle.Screen()
s.setup(1200, 600)
s.title("Covid Simulation")
s.tracer(0)

# gui writer
g = turtle.Turtle()
g.pu()
g.goto(180, 87)
g.dot(12, HEALTHY)
g.goto(200, 80)
g.write('HEALTHY', False, font=COLI, align="left")
g.goto(180, 47)
g.dot(12, EXSPOSED)
g.goto(200, 40)
g.write('EXSPOSED', False, font=COLI, align="left")
g.goto(180, 7)
g.dot(12, SYMPTOMATIC)
g.goto(200, 0)
g.write('SYMPTOMATIC', False, font=COLI, align="left")
g.goto(180, -32)
g.dot(12, ASYMPTOMATIC)
g.goto(200, -40)
g.write('ASYMPTOMATIC', False, font=COLI, align="left")
g.goto(180, -72)
g.dot(12, RECOVERED)
g.goto(200, -80)
g.write('RECOVERED', False, font=COLI, align="left")
g.goto(180, -112)
g.dot(12, DEAD)
g.goto(200, -120)
g.write('DEAD', False, font=COLI, align="left")
g.goto(-100, 100)
g.write('Day', False, font=COLI, align="left")
g.hideturtle()

# boarder setup
d = turtle.Turtle()
d.pu()
d.goto(-100, 100)
d.pd()
d.fd(BOARDER)
d.rt(90)
d.fd(BOARDER)
d.rt(90)
d.fd(BOARDER)
d.rt(90)
d.fd(BOARDER)
d.hideturtle()

# sets up the speed delay for the drawings
s.tracer(4, 25)

# list of people created for simulation
people_list = []
people_sick = []
for i in range(PEOPLE_COUNT):
    x_pos, y_pos = randint(-LENGTH, LENGTH), randint(-LENGTH, LENGTH)
    p = Virus()
    p.position(x_pos, y_pos)
    people_list.append(p)
    if i == 0:
        p.change_state(ASYMPTOMATIC)
        people_sick.append(i)

h = Gui()
h.goto(-70, 100)

# game loop
while running:
    world_time = round(time.time() - START)

    if world_time > day * SEC_PER_DAY:
        day += 1
        h.stats(day)

    # Loop for people movement
    for p in people_list:
        p.movement()

    # Loop for state changer after exsposed
    for i, p in enumerate(people_list):
        if p.state == EXSPOSED:
            p.exsposed(world_time)
        if p.state == SYMPTOMATIC:
            p.symptomatic(world_time)
        if p.state == ASYMPTOMATIC:
            p.asymptomatic(world_time)
        if p.state == DEAD:
            # people_sick.remove(i)
            p.can_move = False
        if p.state == RECOVERED:
            if world_time - people_list[i].recovery_time >= 15:
                p.change_state(HEALTHY)
                people_sick.remove(i)

    # Loop for checking the distance of sick and adding sick to sick_list
    for s in people_sick:
        for i, p in enumerate(people_list):
            if p.t.distance(people_list[s].t) < 10:
                if p.check(people_list[s], world_time):  # checks if check equal true
                    people_sick.append(i)

# TODO:
# stats display
# setup variant
# Start with a strain
# person who first gets strain hasn't 100%
# the strain going from person to person lowers in %
# when strain is at a certain % do a check and if its low enough make a new strain
