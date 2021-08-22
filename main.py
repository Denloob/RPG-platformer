import sys
import pygame
from pygame.locals import *  # import pygame modules

from spritesheetParser import Parse

pygame.init()  # initiate pygame
clock = pygame.time.Clock()  # set up the clock

pygame.display.set_caption('Pygame Window')  # set the window name

WINDOW_SIZE = (600, 400)  # set up window size

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate screen

display = pygame.Surface((300, 200))

spritesheet = Parse('textures/main.png')  # create an instance of the Parse class
character_images = {
    'knight_f': {
        'run': spritesheet.parse_animation('knight_f', 'run'),
        'idle': spritesheet.parse_animation('knight_f', 'idle')},
    'knight_m': {
        'run': spritesheet.parse_animation('knight_m', 'run'),
        'idle': spritesheet.parse_animation('knight_m', 'idle')},
    'wizzard_f': {
        'run': spritesheet.parse_animation('wizzard_f', 'run'),
        'idle': spritesheet.parse_animation('wizzard_f', 'idle')}
}  # creating a dictionary with animations of the main characters

# Create variables with object and animations for use in code.

player_image = list(character_images['wizzard_f']['run'])[1]
floors = {typeNum: spritesheet.parse_sprite(f'floor_{typeNum}.png') for typeNum in range(1, 9)}

floors['ladder'] = spritesheet.parse_sprite('floor_ladder.png')  # add floor_ladder.png to floors dictionary
floors['hole'] = spritesheet.parse_sprite('hole.png')  # add hole.png to floors dictionary
floors['spikes'] = spritesheet.parse_animation('floor', 'spikes')  # add spikes animation to floors dictionary
floors['goo'] = spritesheet.parse_sprite('wall_goo_base.png')  # add floor with goo to floors dictionary
walls = {
    'banners': spritesheet.parse_by_name('wall_banner'),
    'columns': spritesheet.parse_by_name('wall_column'),
    'corners': {
        'corners': spritesheet.parse_by_name('wall_corner'),
        'inner_corners': spritesheet.parse_by_name('wall_inner_corner')},
    'fountains': {
        'top': spritesheet.parse_sprite('wall_fountain_top.png'),
        'middle': {
            'red': spritesheet.parse_animation('wall', 'fountain_mid_red', anim_end=2),
            'blue': spritesheet.parse_animation('wall', 'fountain_mid_blue', anim_end=2)},
        'basin': {
            'red': spritesheet.parse_animation('wall', 'fountain_basin_red', anim_end=2),
            'blue': spritesheet.parse_animation('wall', 'fountain_basin_blue', anim_end=2)}},
    'goo': spritesheet.parse_sprite('wall_goo.png'),
    'holes': spritesheet.parse_by_name('wall_hole'),
    'walls': {
        'normal': {
            'left': spritesheet.parse_sprite('wall_left.png'),
            'middle': spritesheet.parse_sprite('wall_mid.png'),
            'right': spritesheet.parse_sprite('wall_right.png'),
            'side': spritesheet.parse_by_name('wall_side'),
            'top': spritesheet.parse_by_name('wall_top')},
        'dark': {
            'left': spritesheet.parse_sprite('wall_left_dark.png'),
            'middle': spritesheet.parse_sprite('wall_mid_dark.png'),
            'right': spritesheet.parse_sprite('wall_right_dark.png'),
        }
    },
}  # creating a dictionary with walls sprites and wall animations
TILE_SIZE = 16  # set up general tiles size, like floor, walls, etc.

game_map = [
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '4', '2', '2', '2', '2', '2', '4', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['0', '0', '0', '0', '0', '0', '5', '0', '0', '0', '0', '0', '5', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
     '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    ['2', '2', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '2',
     '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
    ['1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '1', '1', '2', '2', '2', '2',
     '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
     '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]  # move player (players rect) to x position (right / left)
    hit_list = collision_test(rect, tiles)  # check collision on x axis
    for tile in hit_list:
        if movement[0] > 0:  # if moving right
            rect.right = tile.left  # set right side of a player rect to left side of a tile
            collision_types['right'] = True
        elif movement[0] < 0:  # if moving left
            rect.left = tile.right  # set left side of a player rect to right side of a tile
            collision_types['left'] = True

    rect.y += movement[1]  # move player (players rect) to y position (up / down)
    hit_list = collision_test(rect, tiles)  # check collision on x axis
    for tile in hit_list:
        if movement[1] > 0:  # if moving down
            rect.bottom = tile.top  # set bottom side of a player rect to top side of a tile
            collision_types['bottom'] = True
        elif movement[1] < 0:  # if moving up
            rect.top = tile.bottom  # set top side of a player rect to bottom side of a tile
            collision_types['top'] = True
    return rect, collision_types  # return players rect and all collision types


moving_right = False
moving_left = False

player_y_momentum = 0
air_timer = 0

player_rect = pygame.Rect(50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)

while True:  # game loop
    display.fill((146, 244, 255))
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '0':
                display.blit(walls['walls']['normal']['middle'], (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == '1':
                display.blit(walls['walls']['dark']['middle'], (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == '2':
                display.blit(floors[1], (x * TILE_SIZE, y * TILE_SIZE))
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE / 2, TILE_SIZE, TILE_SIZE))
            elif tile == '3':
                display.blit(walls['fountains']['top'], (x * TILE_SIZE, y * TILE_SIZE))
            elif tile == '4':
                display.blit(walls['fountains']['middle']['red'][0], (x * TILE_SIZE, y * TILE_SIZE))
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE / 2 + 2, TILE_SIZE, TILE_SIZE))
            elif tile == '5':
                display.blit(walls['fountains']['basin']['red'][0], (x * TILE_SIZE, y * TILE_SIZE))
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]

    if moving_right and not moving_left:
        player_movement[0] += 2
    elif moving_left and not moving_right:
        player_movement[0] -= 2

    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    elif collisions['top']:
        player_y_momentum -= player_y_momentum
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x, player_rect.y))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:  # check for window quit
            pygame.quit()  # stop pygame
            sys.exit()  # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            elif event.key == K_LEFT:
                moving_left = True
            elif event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            elif event.key == K_LEFT:
                moving_left = False
            elif event.key != K_RIGHT and event.key != K_LEFT:


    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps
