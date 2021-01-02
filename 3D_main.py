'''
This is an attempt to re-create the ios game stack. Since pygame, to
my knowledge, doesn't have a builtin module to make 3D objects and dure to the fact
that I cannot be asked to find one on GitHub. I decided to
create a 3D illusion of a cuboid in which the programme is constantly drawing lines
to portray this effect. To do this I needed the help of my brother so we could create
some code which uses trigonometry to find the next coordinate based on the
length of the side, current position and angle representing the side. The programme is far from finished though
'''

import pygame
import time
import math
from pygame.locals import *

pygame.init()

screen_width = 300
screen_height = 500

screen = pygame.display.set_mode([screen_width, screen_height])
outline_coords = None
stack_outline_coords = []


def adjust_pos(x, y, direction):
    if direction == "SE":
        return x + movement_speed, y + movement_speed
    if direction == "SW":
        return x - movement_speed, y + movement_speed
    if direction == "NE":
        return x + movement_speed, y - movement_speed
    if direction == "NW":
        return x - movement_speed, y - movement_speed

def find_coords(root_coord, angle1, angle2, side1, side2, type):
    global bx_change, by_change
    global x_change, y_change
    global outline_coords
    global stack_outline_coords

    #coorda
    coorda = root_coord
    #coordb
    (bx_change, by_change) = (math.sin((angle2 / 180)*math.pi) * side2, math.cos((angle2 / 180)*math.pi) * side2)
    coordb = (root_coord[0] + bx_change, root_coord[1] - by_change)
    #coordc
    (x_change, y_change) = (math.sin((angle1 / 180)*math.pi) * side1, math.cos((angle1 / 180) *math.pi) * side1)
    coordc = (root_coord[0] + bx_change + x_change, (root_coord[1] - by_change) + y_change)
    #coordd
    coordd = (root_coord[0] + x_change, root_coord[1] + y_change)
    #coorda2
    coorda2 = (coorda[0], coorda[1]+s_depth)
    #coordd2
    coordd2 = (coordd[0], coordd[1]+s_depth)
    #coordc2
    coordc2 = (coordc[0], coordc[1]+s_depth)
    if type == "moving":
        outline_coords = (coorda, coordb, coordc, coordd, coordd2, coorda2, coorda, coordd, coordc, coordc2, coordd2)
    else:
        print(len(stack_outline_coords))
        stack_outline_coords.append((coorda, coordb, coordc, coordd, coordd2, coorda2, coorda, coordd, coordc, coordc2, coordd2))
    return [coorda, coordb, coordc, coordc2, coordd2, coorda2, coorda, coordd]

def draw_cuboid(coords, depth):
    pygame.draw.polygon(screen, (255, 255, 255), coords)

def draw_outlines(coords, type):
    pre_count = 0
    cur_count = 0
    if type == "moving":
        while cur_count != len(outline_coords)-1:
            cur_count += 1
            pygame.draw.line(screen, (255, 0, 0), outline_coords[pre_count], outline_coords[cur_count])
            pre_count += 1
        pre_count, cur_count = 0, 0
    else:
        for coords in stack_outline_coords:
            while cur_count != len(coords)-1:
                cur_count += 1
                pygame.draw.line(screen, (255, 0, 0), coords[pre_count], coords[cur_count])
                pre_count += 1    
            pre_count, cur_count = 0, 0

def change_direction(cur_direction, mode):
    if mode == "edge":
        if cur_direction == "SE":
            return directions[3] # => NW
        if cur_direction == "SW":
            return directions[2] # => NE
        if cur_direction == "NE":
            return directions[1] # => SW
        if cur_direction == "NW":
            return directions[0] # => SE
    elif mode == "space":
        if cur_direction == "SE":
            return directions[1] # => SW
        if cur_direction == "SW":
            return directions[0] # => SE
        if cur_direction == "NE":
            return directions[3] # => NW
        if cur_direction == "NW":
            return directions[2] # => NE

def check_if_hit_edge(x, y, cur_direction):
    global can_space

    if x+bx_change+x_change >= screen_width:
        can_space = True
        return change_direction(cur_direction, "edge")
    elif x == 0:
        can_space = True
        return change_direction(cur_direction, "edge")
    elif (x > 0) and (x < screen_width):
        return cur_direction


def check_space_bar(cur_pos, s_pos):
    global s_side1, s_side2
    global side1, side2
    global can_space
    global score
    global cur_direction
    global root_coord

    x, y = cur_pos
    sx, sy = s_pos
    if can_space:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print(cur_direction)
                if cur_direction in  ("SE", "NW"):
                    if (x < sx) and (x+bx_change+x_change > sx):
                        side1 -= (sx - x)
                        score += 1
                    elif (x > sx) and (x < sx+bx_change+x_change):
                        side1 -= ((x+bx_change+x_change) - (sx+bx_change+x_change))
                        score += 1
                    else:
                        score = 0
                if cur_direction in ("SW", "NE"):
                    if (x < sx) and (x+bx_change+x_change > sx):
                        side2 -= (sx - x)
                        score += 1
                    elif (x > sx) and (x < sx+bx_change+x_change):
                        side2 -= ((x+bx_change+x_change) - (sx+bx_change+x_change))
                        score += 1
                    else:
                        score = 0
            cur_direction = change_direction(cur_direction, "space")
            can_space = False
            generate_new_stack(cur_pos, side1, side2)
            return True
    else:
        return False

def find_starting_coord(movement_speed, stack_x, stack_y, stack_depth, required_dir):
    current_stack_pos = stack_x, stack_y-stack_depth
    while True:
        if required_dir == "SE":
            current_stack_pos = adjust_pos(current_stack_pos[0], current_stack_pos[1], "NW")
            if current_stack_pos[0] == 0:
                return current_stack_pos
            elif current_stack_pos[1] == 0:
                return current_stack_pos
        elif required_dir == "SW":
            current_stack_pos = adjust_pos(current_stack_pos[0], current_stack_pos[1], "NE")
            if current_stack_pos[0] == 0:
                return current_stack_pos
            elif current_stack_pos[1] == 0:
                return current_stack_pos

def generate_new_stack(pos, side1, side2):
    global previous_stack_info
    x, y = pos
    temp_info = []
    for info in previous_stack_info:
        sx, sy = info[0]
        temp_info.append(((sx, sy+s_depth), info[1], info[2]))
        temp_info.insert(0, ((sx, sy), side1, side2))
    previous_stack_info = temp_info

def analyse_info():
    global previous_stack_coords
    global stack_outline_coords

    for info in previous_stack_info:
        x, y = info[0]
        if check_space_bar(root_coord, previous_stack_info[0][0]) == True:
            print("spacebar")
            previous_stack_coords.append(find_coords((x, y), s_angle1, s_angle2, info[1], info[2], "stack"))
        else:
            previous_stack_coords.append(find_coords((x, y), s_angle1, s_angle2, info[1], info[2], "stack"))

    for stack_coords in previous_stack_coords:
        draw_cuboid(stack_coords, s_depth)
        draw_outlines(stack_coords, "stack")
    stack_outline_coords.clear()
    previous_stack_coords.clear()

def handle_drawing():
    global root_coord
    global cur_direction

    pygame.display.set_caption("Stack 3D")
    root_coord = adjust_pos(root_coord[0], root_coord[1], cur_direction)
    analyse_info() # Also draws the stack cuboid
    coords = find_coords(root_coord, angle1, angle2, side1, side2, "moving")
    draw_score()
    draw_cuboid(coords, depth)
    draw_outlines(coords, "moving")
    cur_direction = check_if_hit_edge(root_coord[0], root_coord[1], cur_direction)

def calc_stack_start_coord():
    return screen_width/2-(screen_width/10), screen_height/2

def draw_score():
   screen.blit(text, (20, 20))

running = True
directions = ["SE", "SW", "NE", "NW"]
cur_direction = directions[0]
can_space = True
time_speed = 0.05
movement_speed = 5

score = 0
font = pygame.font.SysFont("Rockwell", 32)
text = font.render("Score: " + str(score), True, (255, 255, 255))

#~ Stack's rect attributes
previous_stack_info = [(calc_stack_start_coord(), 50, 60)]
previous_stack_coords = []
s_root_coord = previous_stack_info[0][0]
s_angle1 = 40
s_angle2 = 80
s_side1 = 50
s_side2 = 60
s_depth = 20


#~ Moving rects attributes
#~ root_coord = (15, 40)
root_coord = (find_starting_coord(movement_speed, s_root_coord[0], s_root_coord[1], s_depth, "SE"))
angle1 = 40
angle2 = 80
side1 = 50
side2 = 60
depth = 20

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill([0, 0, 0])
    pygame.display.set_caption("Stack 3D")
    handle_drawing()
    time.sleep(.05)
    pygame.display.flip()