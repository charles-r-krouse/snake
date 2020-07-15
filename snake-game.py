# -*- coding: utf-8 -*-
"""
Simple snake game created using pygame to evaluate Syder and Anaconda for 
learning python

@author: Charles Krouse

@notes:
  - https://techwithtim.net/tutorials/game-development-with-python/snake-pygame/tutorial-4/
  - increased FPS speed -> originally 10 FPS which was too slow
  - up and down are reversed, and I do not know why
  - TODO: draw eyes on the snake
  - going off the screen does not work
  - still lots of bugs
  - not using tkinter for the message box
"""

import pygame
import time
import sys
import random
import tkinter as tk
import math

# ----------------------------------------------------------------------------
# Define classes
# ----------------------------------------------------------------------------

class cube(object):
    
    rows = 20
    w = 500
    
    def __init__(self, start, dir_x=1, dir_y=0, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = 1
        self.dir_y = 0
        self.color = color
    
    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0]+self.dir_x, self.pos[1]+self.dir_y)
    
    def draw(self, surface, eyes=False):
        dis = self.w/self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        # draw the eyes
        if eyes:
            pass
    
    
class snake(object):
    
    body = []
    turns = {}
    
    def __init__(self, color=(255, 0, 0), pos=(0, 0)):
        self.color = color
        self.head = cube(pos) # head is the front of the snake
        # create the body by appending a head, which is just a cube object
        self.body.append(self.head) 
        # used to determine the direction that the snake is moving
        self.dir_x = 0 
        self.dir_y = 1
    
    def move(self):
        for event in pygame.event.get():
            # check if the player hit the red X button
            if event.type == pygame.QUIT:
                # quit the python game
                pygame.quit()
                # cleanly exit
                sys.exit()
                
            # see which keys are pressed
            keys = pygame.key.get_pressed()
            
            # loop through all useful keys
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                    
                if keys[pygame.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                if keys[pygame.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                    
                if keys[pygame.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                    
            # loop through every cube in the snake body
            for i, c in enumerate(self.body):
                # get the cube positions on the grid
                p = c.pos[:]
                # check if the cube current position is one where we turned
                if p in self.turns:
                    turn = self.turns[p] # get the direction to turn
                    c.move(turn[0], turn[1]) # turn in desired direction
                    # check if it is the last cube in the body, and if it is,
                    # then remove it from the body
                    if (i==len(self.body)-1):
                        self.turns.pop(p)
                    # if not the last cube, then we need to check if we reached
                    # the edge of the screen
                else:
                    if (c.dir_x==-1 and c.pos[0]<=0):
                        c.pos = (c.rows-1, c.pos[1])
                    elif(c.dir_x==1 and c.pos[0]>=c.rows-1):
                        c.pos = (0, c.pos[1])
                    elif(c.dir_y==1 and c.pos[1]>=c.rows-1):
                        c.pos = (c.pos[0], 0)
                    elif(c.dir_y==-1 and c.pos[1]<=0):
                        c.pos = (c.pos[0], c.rows-1)
                    # if we don't reach the edge of the screen, then
                    # proceed to move as normal
                    else:
                        c.move(c.dir_x, c.dir_y)
    
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1
    
    # add cube to the end of the snake after eating a snack
    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y
        # check which direction the snake is moving to determine which side of
        # the snake to add the new cube to
        if (dx==1 and dy==0):
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        if (dx==-1 and dy==0):
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        if (dx==0 and dy==1):
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        if (dx==0 and dy==-1):
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
            
        # not sure what this does?
        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy
    
    def draw(self, surface):
        # draw each cube in the body
        for i, c in enumerate(self.body):
            # draw eyes on the head
            if (i==0):
                c.draw(surface, True)
            else:
                c.draw(surface)


# -----------------------------------------------------------------------------
# Define functions
# -----------------------------------------------------------------------------
    
def draw_grid(w, rows, surface):
    size_between = w/rows
    
    x = 0 # track the current x
    y = 0 # track the current y
    
    for i in range(rows):
        x += size_between
        y += size_between
        
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redraw_window(surface):
    global width, rows, s, snack
    surface.fill((0, 0, 0)) # fill the screen with black
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface) # draw the grid lines
    pygame.display.update() # update the screen

def random_snack(rows, item):
    positions = item.body
    
    # keep generating random positions, until we get a valid one
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    pass


# -----------------------------------------------------------------------------
# Define main function
# -----------------------------------------------------------------------------

def main():
    # create global variables for screen width (width), number of rows (rows),
    # and the snake (s)
    global width, rows, s, snack
    # screen width
    width = 500
    # screen height
    height = 500
    # number of rows
    rows = 20
    
    # create the screen object
    window = pygame.display.set_mode((width, height))
    
    # create a snake object
    s = snake(color=(255, 0, 0), pos=(10, 10))
    
    # create a clock object
    clock = pygame.time.Clock()
    
    # create a snack for the snake
    snack = cube(random_snack(rows, s), color=(0, 255, 0))
    
    # main loop
    flag = True
    while flag:
        pygame.time.delay(1)
        # ensure that the game runs at 10 FPS
        clock.tick(100)
        # move the snake
        s.move()
        # check if the snake collides with the snack
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = cube(random_snack(rows, s), color=(0, 255, 0))
        # we lose if the snake collides with its body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: {}'.format(len(s.body)))
                print('You lose!')
                # message_box('You lose!')
                s.reset((10, 10))
                break
            
        # refresh the screen
        redraw_window(window)
        


# -----------------------------------------------------------------------------
# Run the game
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()



