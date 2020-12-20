import pygame
import time

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode([screen_width, screen_height])

def create_3D_rect(start_x, start_y, s_side, l_side, depth):
    #~ Draws the top of the rectangle
    px, py = start_x, start_y
    x, y = px+l_side, py-s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x, y
    x, y = px+s_side, py+s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = (start_x+l_side)+s_side, (start_y-s_side)+s_side
    x, y = x-l_side, y+s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = px-l_side, py+s_side
    x, y = start_x, start_y
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    #~ Draws the stems going down from the corners
    px, py = x, y
    x, y = px, py+depth
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x, y
    x, y = px+s_side, py+s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x, y
    x, y = px+l_side, py-s_side
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = start_x+s_side+l_side, start_y+depth+s_side-s_side
    x, y = px, py-depth
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    px, py = x-l_side, y+s_side
    x, y = px, py+depth
    pygame.draw.line(screen, (0, 0, 255), (px, py), (x, y))
    
def adjust_pos(x, y, direction):
    if direction == "SE":
        return x+4, y+4
    if direction == "SW":
        return x-4, y+4
    if direction == "NE":
        return x+4, y-4
    if direction == "NW":
        return x-4, y-4
    return x+4, y+4

def draw_moving_rect(x, y, s_side, l_side, depth):
    create_3D_rect(x, y, s_side, l_side, depth)

def draw_stack():
    create_3D_rect(stack_x, stack_y, stack_s_side, stack_l_side, depth)

def change_direction():
    if cur_direction == "SE":
        return directions[3]
    if cur_direction == "SW":
        return directions[2]
    if cur_direction == "NE":
        return directions[1]
    if cur_direction == "NW":
        return directions[0]

def check_if_hit_edge():
    if x + s_side + l_side + depth + 15 >= screen_width:
        return change_direction()
    elif x == 0:
        return change_direction()
    else:
        return cur_direction

#~ Stack's rect attributes
stack_depth = 40
stack_x, stack_y = 200, 300
stack_s_side, stack_l_side = 50, 60
#~ Moving rects attributes
depth = 20
x, y = 200, stack_y - depth
s_side, l_side = 50, 60

count = 4
running = True
directions = ["SE", "SW", "NE", "NW"]
cur_direction = directions[0]

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill([255, 255, 255])
    pygame.display.set_caption("Stack 3D")
    
    cur_direction = check_if_hit_edge()
    draw_moving_rect(x, y, s_side, l_side, depth)
    draw_stack()
    x, y = adjust_pos(x, y, cur_direction)
    time.sleep(.05)
    pygame.display.flip()