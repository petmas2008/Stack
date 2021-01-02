import pygame
import sys
import time
from pygame.locals import *
pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode([screen_width, screen_height])
score = 0

#~ This is the moving block's attributes
x, y = 20, 150
width, height = 100, 100

#~ This is the stack's attributes
stack_x, stack_y = 200, 150
stack_width, stack_height = 100, 100

def reset_pos(x, y, axis):
    if axis == "x":
        x = 20
        y = stack_y
    if axis == "y":
        x = stack_x
        y = 20
    return x, y

def draw_rect(rect):
    pygame.draw.rect(screen, (0, 0, 255), rect)

def draw_stack(rect):
    pygame.draw.rect(screen, (255, 0, 255), rect)

def adjust_pos(x, y, x_scale, y_scale):
    return x + x_scale, y + y_scale

def adjust_size(width, height):
    return width + scale, height + scale

def find_direction(x, y, direction):
    if direction in ("right", "left"):
        if x == 500 - width:
            direction = "left"
            return direction
        elif x == 0:
            direction = "right"
            return direction
        else:
            return direction
    elif direction in ("up", "down"):
        if y == 500 - height:
            direction = "up"
            return direction
        elif y == 0:
            direction = "down"
            return direction
        else:
            return direction    

direction = "right"
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.set_caption('Stack')
    
    font1 = pygame.font.SysFont(None, 32)
    text1 = font1.render("Score:%s" %(str(score)), True,(255,0,0))
    direction = find_direction(x, y, direction)
    
    if direction == "right":
        x_scale, y_scale = 5, 0
    elif direction == "left":
        x_scale, y_scale = -5, 0
    elif direction == "down":
        x_scale, y_scale = 0, 5
    elif direction == "up":
        x_scale, y_scale = 0, -5

    x, y = adjust_pos(x, y, x_scale, y_scale)
    moving_rect = pygame.Rect(x, y, width, height)
    stack_rect = pygame.Rect(stack_x, stack_y, stack_width, stack_height)
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if direction in ("right", "left"):
                if (x > stack_x) and (x < stack_x + stack_width):
                    width -= (x + width) - (stack_x + stack_width)
                    stack_x, stack_y = x, y
                elif (x < stack_x) and (x + width > stack_x):
                    width -= stack_x - x
                elif x == stack_x:
                    pass
                elif (y < stack_y) and (y + height < stack_y):
                    break
                x, y = reset_pos(x, y, "y")
                stack_width = width
                direction = "down"
                score += 1
                time.sleep(.25)
            elif direction in ("up", "down"):
                if (y > stack_y) and (y < stack_y + stack_height):
                    height -= (y + height) - (stack_y + stack_height)
                    stack_x, stack_y = x, y
                elif (y < stack_y) and (y + height > stack_y):
                    height = (y + height) - stack_y
                elif y == stack_y:
                    pass
                elif (y < stack_y) and (y + height < stack_y):
                    break
                x, y = reset_pos(x, y, "x")
                stack_height = height
                direction = "right"
                score += 1
                time.sleep(.25)
                
                    
    screen.fill((255, 255, 255))
    draw_stack(stack_rect)
    draw_rect(moving_rect)
    time.sleep(.025)
    screen.blit(text1, (20, 20))
    pygame.display.flip()

pygame.quit()