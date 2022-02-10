import string
import pickle
import math
from os import walk as os_walk
from sys import exit  # import exit from sys to completely stop the code after trying to exit

import pygame  # import the pygame module
from pygame.locals import *  # import pygame modules

from assets.data.crypt import Crypt
from assets.data.spritesheet_parser import Parse  # sprite sheet parser which can parse png files with data in json

from assets.data.game_console import Console

import logging
from colorlog import ColoredFormatter

# initiate logging
stream = logging.StreamHandler()
stream.setFormatter(ColoredFormatter("%(log_color)s%(message)s%(reset)s"))

log = logging.getLogger('pythonConfig')
log.setLevel(logging.DEBUG)
log.addHandler(stream)

log.debug("Logging initiated")

log.debug("Initializing pygame")
pygame.init()  # initiate pygame
log.debug("Initializing pygame complete")

pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

log.debug("Defining constants")
clock, WINDOW_SIZE = pygame.time.Clock(), (1200, 800)  # set up the clock and windows_size
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate screen
TILE_SIZE, CHUNK_SIZE = 16, 16  # set up general tiles size, like floor, walls, etc and chunk size
display, ui = pygame.Surface((600, 400)), pygame.Surface((3 * TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
text_surf = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
pygame.display.set_caption('Pygame Window')  # set the window name
log.debug("Defining constants complete")

log.debug("Parsing spritesheet")
spritesheet = Parse('assets/textures/main.png')  # create an instance of the Parse class
images = {
    'character_images': {
        'knight_f': {
            'run': spritesheet.parse_animation('knight_f', 'run'),
            'idle': spritesheet.parse_animation('knight_f', 'idle'),
            'hit': [spritesheet.parse_entity(name='knight_f', mode='hit', frame=0)]
        },
        'knight_m': {
            'run': spritesheet.parse_animation('knight_m', 'run'),
            'idle': spritesheet.parse_animation('knight_m', 'idle'),
            'hit': [spritesheet.parse_entity(name='knight_m', mode='hit', frame=0)]
        },
        'wizzard_f': {
            'run': spritesheet.parse_animation('wizzard_f', 'run'),
            'idle': spritesheet.parse_animation('wizzard_f', 'idle'),
            'hit': [spritesheet.parse_entity(name='wizzard_f', mode='hit', frame=0)]
        },
        'wizzard_m': {
            'run': spritesheet.parse_animation('wizzard_m', 'run'),
            'idle': spritesheet.parse_animation('wizzard_m', 'idle'),
            'hit': [spritesheet.parse_entity(name='wizzard_m', mode='hit', frame=0)]
        },
        'lizard_f': {
            'run': spritesheet.parse_animation('lizard_f', 'run'),
            'idle': spritesheet.parse_animation('lizard_f', 'idle'),
            'hit': [spritesheet.parse_entity(name='lizard_f', mode='hit', frame=0)]
        },
        'lizard_m': {
            'run': spritesheet.parse_animation('lizard_m', 'run'),
            'idle': spritesheet.parse_animation('lizard_m', 'idle'),
            'hit': [spritesheet.parse_entity(name='lizard_m', mode='hit', frame=0)]
        },
        'elf_f': {
            'run': spritesheet.parse_animation('elf_f', 'run'),
            'idle': spritesheet.parse_animation('elf_f', 'idle'),
            'hit': [spritesheet.parse_entity(name='elf_f', mode='hit', frame=0)]
        },
        'elf_m': {
            'run': spritesheet.parse_animation('elf_m', 'run'),
            'idle': spritesheet.parse_animation('elf_m', 'idle'),
            'hit': [spritesheet.parse_entity(name='elf_m', mode='hit', frame=0)]
        },
    },  # creating a dictionary with animations of the main characters
    'enemies': {
        'skelet': {
            'idle': spritesheet.parse_animation('skelet', 'idle'),
            'run': spritesheet.parse_animation('skelet', 'run'),
        },
        'big_zombie': {
            'idle': spritesheet.parse_animation('big_zombie', 'idle'),
            'run': spritesheet.parse_animation('big_zombie', 'run'),
        },
        'zombie': {
            'idle': spritesheet.parse_animation('zombie', 'idle'),
            'run': spritesheet.parse_animation('zombie', 'run'),
        },
        'tiny_zombie': {
            'idle': spritesheet.parse_animation('tiny_zombie', 'idle'),
            'run': spritesheet.parse_animation('tiny_zombie', 'run'),
        },
        'ice_zombie': {
            'idle': spritesheet.parse_animation('ice_zombie', 'idle'),
            'run': spritesheet.parse_animation('ice_zombie', 'run'),
        },
        'big_demon': {
            'idle': spritesheet.parse_animation('big_demon', 'idle'),
            'run': spritesheet.parse_animation('big_demon', 'run'),
        },
        'chort': {
            'idle': spritesheet.parse_animation('chort', 'idle'),
            'run': spritesheet.parse_animation('chort', 'run'),
        },
        'goblin': {
            'idle': spritesheet.parse_animation('goblin', 'idle'),
            'run': spritesheet.parse_animation('goblin', 'run'),
        },
        'imp': {
            'idle': spritesheet.parse_animation('imp', 'idle'),
            'run': spritesheet.parse_animation('imp', 'run'),
        },
        'masked_orc': {
            'idle': spritesheet.parse_animation('masked_orc', 'idle'),
            'run': spritesheet.parse_animation('masked_orc', 'run'),
        },
        'muddy': {
            'idle': spritesheet.parse_animation('muddy', 'idle'),
            'run': spritesheet.parse_animation('muddy', 'run'),
        },
        'necromancer': {
            'idle': spritesheet.parse_animation('necromancer', 'idle'),
            'run': spritesheet.parse_animation('necromancer', 'run'),
        },
        'ogre': {
            'idle': spritesheet.parse_animation('ogre', 'idle'),
            'run': spritesheet.parse_animation('ogre', 'run'),
        },
        'orc_shaman': {
            'idle': spritesheet.parse_animation('orc_shaman', 'idle'),
            'run': spritesheet.parse_animation('orc_shaman', 'run'),
        },
        'orc_warrior': {
            'idle': spritesheet.parse_animation('orc_warrior', 'idle'),
            'run': spritesheet.parse_animation('orc_warrior', 'run'),
        },
        'swampy': {
            'idle': spritesheet.parse_animation('swampy', 'idle'),
            'run': spritesheet.parse_animation('swampy', 'run'),
        },
        'wogol': {
            'idle': spritesheet.parse_animation('wogol', 'idle'),
            'run': spritesheet.parse_animation('wogol', 'run'),
        },
    },  # creating a dictionary with animations of the enemies
    'walls': {
        'banners': spritesheet.parse_by_name('banner'),
        'columns': spritesheet.parse_by_name('column'),
        'corners': {
            'corners': spritesheet.parse_by_name('wall_corner'),
            'inner': spritesheet.parse_by_name('wall_inner_corner')},
        'sides': spritesheet.parse_by_name('wall_side'),
        'top': spritesheet.parse_by_name('wall_top'),
        'fountains': {
            'top': spritesheet.parse_sprite('wall_fountain_top.png'),
            'mid': {
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
                'mid': spritesheet.parse_sprite('wall_mid.png'),
                'right': spritesheet.parse_sprite('wall_right.png'),
                'side': spritesheet.parse_by_name('wall_side'),
                'top': spritesheet.parse_by_name('wall_top')},
            'dark': {
                'left': spritesheet.parse_sprite('wall_left_dark.png'),
                'mid': spritesheet.parse_sprite('wall_mid_dark.png'),
                'right': spritesheet.parse_sprite('wall_right_dark.png'),
            }
        },
        'doors': spritesheet.parse_by_name('doors'),
    },  # creating a dictionary with walls sprites and wall animations
    'floors': {
        str(typeNum): spritesheet.parse_sprite(f'floor_{typeNum}.png') for typeNum in range(1, 9)
    },
    'misc': {
        'crate': spritesheet.parse_sprite('crate.png'),
        'chest': {
            'empty': spritesheet.parse_animation('chest_empty', 'open', anim_end=2),
            'full': spritesheet.parse_animation('chest_full', 'open', anim_end=2),
            'mimic': spritesheet.parse_animation('chest_mimic', 'open', anim_end=2),
        },

    },
    'ui': {
        'hearts': spritesheet.parse_by_name(startswith='ui_heart')
    },
    'effects': {
        'fire': spritesheet.parse_animation(name='player', mode='fire')
    },
    'items': {
        'potions': spritesheet.parse_by_name('flask'),
    },
}  # Create variables with objects and animations for use in code.
# noinspection PyTypeChecker
images['walls']['columns']['wall'] = spritesheet.parse_by_name('wall_column')
# noinspection PyTypeChecker
images['walls']['banners']['wall'] = spritesheet.parse_by_name('wall_banner')
# noinspection PyTypeChecker
images['floors']['ladder'] = spritesheet.parse_sprite('floor_ladder.png')  # add floor_ladder.png to floors dictionary
# noinspection PyTypeChecker
images['floors']['hole'] = spritesheet.parse_sprite('hole.png')  # add hole.png to floors dictionary
# noinspection PyTypeChecker
images['floors']['spikes'] = spritesheet.parse_animation('floor', 'spikes')  # add spikes animation to floors dictionary
# noinspection PyTypeChecker
images['floors']['goo'] = spritesheet.parse_sprite('wall_goo_base.png')  # add floor with goo to floors dictionary
log.debug('Parsing complete')

log.debug('Defining player data')
player_images = images['character_images']['knight_m']
player_image = player_images['idle']

speed = 2  # set up player speed
starting_position = (2 * TILE_SIZE, 12.25 * TILE_SIZE)
true_scroll = [0, 0]

moving = {'left': False, 'right': False}

player_y_momentum, air_timer = 0, 0

player_rect = pygame.Rect(starting_position[0], starting_position[1], player_image[0].get_width(),
                          player_image[0].get_height())
log.debug('Player data defined')

log.debug('Parsing levels')
old_level_name, level_name = -1, 0
# with open(f'assets/data/maps/level {level_name}/map_background.csv') as f1, \
#         open(f'assets/data/maps/level {level_name}/map_mid.csv') as f2, \
#         open(f'assets/data/maps/level {level_name}/map_top.csv') as f3, \
#         open(f'assets/data/maps/level {level_name}/map_interactive_objects_types.csv') as f4, \
#         open(f'assets/data/maps/level {level_name}/map.csv', 'w') as target:
#     target.write(
#         f1.read() + '\\' + '\n' +
#         f2.read() + '\\' + '\n' +
#         f3.read() + '\\' + '\n' +
#         f4.read()[:-1]
#     )
#
# Crypt.map_encrypt(file_path=f'assets/data/maps/level {level_name}/map.csv', save=True,
#                   save_path='assets/data/game_map.dat',
#                   key=b'ECr41LS4MZZ8n0EnCvCeE-Xve-aufGYrgujmnHKJn5o=')
# map_decrypted = Crypt.map_decrypt(key=b'ECr41LS4MZZ8n0EnCvCeE-Xve-aufGYrgujmnHKJn5o=',
#                                   file_path='assets/data/game_map.dat')

# remove this on release

levels_data = []
for folder_path in [x[0] for x in os_walk('assets/data/maps/') if x[0] != 'assets/data/maps/']:
    with open(f'{folder_path}/map_background.csv') as f1, \
            open(f'{folder_path}/map_mid.csv') as f2, \
            open(f'{folder_path}/map_top.csv') as f3, \
            open(f'{folder_path}/map_interactive_objects_types.csv') as f4, \
            open(f'{folder_path}/map.csv', 'w') as target:
        data = (
                f1.read() + '\\' + '\n' +
                f2.read() + '\\' + '\n' +
                f3.read() + '\\' + '\n' +
                f4.read()[:-1]
        )
        levels_data.append(Crypt.map_encrypt(game_map=data,
                                             key=b'ECr41LS4MZZ8n0EnCvCeE-Xve-aufGYrgujmnHKJn5o='))
        target.write(data)

with open('assets/data/game_map.dat', 'wb') as f:
    pickle.dump(levels_data, f)
with open('assets/data/game_map.dat', 'rb') as f:
    levels_data_decrypted = [
        Crypt.map_decrypt(key=b'ECr41LS4MZZ8n0EnCvCeE-Xve-aufGYrgujmnHKJn5o=',
                          game_map=level_data)
        for level_data in pickle.load(f)
    ]
log.debug('Levels parsed')

log.debug('Loading game map')
# map_layers = [row.split(',') for row in [(layer.split('\n')) for layer in map_decrypted.split('\n\\\n')]]
# layers = [layer.split('\n') for layer in map_decrypted.split('\n\\\n')]
# game_map = []
# for layer in layers:
#     rows = []
#     for row in layer:
#         rows.append(row.split(','))
#     game_map.append(rows)
game_map = [
    [row.split(',') for row in layer] for layer in  # layer.split('\n') -> rows | row.split(',') -> ids
    [layer.split('\n') for layer in levels_data_decrypted[level_name].split('\n\\\n')]
    # map_decrypted.split('\n\\\n') -> layers
]  # list with layers (lists) which contain rows which contain ids [layer[ row[id('42'), ...], row[] ], layer[...]]

# type(game_map) == list, type(game_map[0]) == list, type(game_map[0][0]) == list, type(game_map[0][0][0]) == str

map_items = game_map.pop(2)[:-1]
game_interactive_objects = game_map.pop(2)[:-1]
log.debug('Game map loaded')


def print_list(lst: list, level=0, org_list=True):
    if org_list:
        print('    [\n\n')
    for i in lst:
        if isinstance(i, list) and level < 1:
            print_list(i, level + 1, False)
        else:
            print('    ' * level, i)
        if org_list:
            print('\n')
    if org_list:
        print('    ]')


log.debug('Defining functions')


def collision_test(rect: pygame.Rect, tiles: list) -> list:
    return [tile for tile in tiles if rect.colliderect(tile)]


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


log.debug('Functions defined')

log.debug('Defining animations data')
player_flip, is_moving = False, False
true_anim_game_frame = {'player': 0, 'spikes': 0, 'liquid_water': 0, 'liquid_lava': 0, 'fire': 0, 'item': 0}
anim_game_frame = true_anim_game_frame.copy()
log.debug('Animations data defined')

# config
log.debug('Loading configs')
tile_rects = []
interactive_objects_rects = [[], []]
enemies = []
damage_rects = {
    'spikes': [],
    'lava': [],
    'water': [],
}


class GameConsole:
    def __init__(self):
        self.gamemode = 'survival'
        self.speed = 2

    def change_gamemode(self, mode):
        if type(mode) == str:
            self.gamemode = mode
        elif type(mode) == int:
            self.gamemode = ['survival', 'creative'][mode]
        else:
            raise ValueError('Invalid gamemode')

    def change_speed(self, speed):
        if type(speed) == int:
            self.speed = speed
        else:
            raise ValueError('Invalid speed')


console_config = {
    'global': {
        'layout': 'INPUT_BOTTOM',
        'padding': (10, 10, 10, 10),
        'bck_alpha': 150,
        'welcome_msg': 'You found the console!\n***************\n'
                       'Type "exit" to quit the game\nType "help" or "?" for help',
        'welcome_msg_color': (0, 255, 0)
    },
    'input': {
        'font_file': 'assets/data/pygame_console/fonts/JackInput.ttf',
        'bck_alpha': 0
    },
    'output': {
        'font_file': 'assets/data/pygame_console/fonts/JackInput.ttf',
        'bck_alpha': 0,
        'display_lines': 20,
        'display_columns': 100
    },
}
consoleAPI = GameConsole()
console = Console(consoleAPI, WINDOW_SIZE[0], console_config)
log.debug('Configs loaded')

log.debug('Creating Font class')


class Font:
    def __init__(self):
        self.spacing = 1
        self.character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'a', '&', '@', 'B', '`', r'\\',
                               'b', 'C', 'c', ')', ']', ':', ',', '©', 'D', '-', 'd', '$', '.', 'E', 'e', '=', '€',
                               '!', 'F', 'f', 'G', 'g', 'H', '#', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M',
                               'm', '*', 'N', 'n', 'O', 'o', '(', '[', 'P', '%', '+', 'p', 'Q', 'q', '?', '"', 'R',
                               '®', 'r', 'S', "'", '/', 's', 'T', '~', 't', 'U', '_', 'u', 'V', 'v', 'W', 'w', 'X',
                               'x', 'Y', 'y', 'Z', 'z']
        self.characters = {}
        for char in self.character_list:
            if char in string.ascii_lowercase:
                self.characters[char] = spritesheet.parse_sprite(f'characters_lower_{char}.png')
            elif char in string.ascii_uppercase:
                self.characters[char] = spritesheet.parse_sprite(f'characters_upper_{char}.png')
            # ['&', '@', '`', '\\', ')', ']', ':', ',', '©', '-', '$', '.', '=',
            # '€', '!', '#', '*', '(', '[', '%', '+', '?', '"', '®', "'", '/', '~', '_']:
            elif char in r'&@`\)]:,©-$.\'=€!#*([%+?"®/~_':
                symbol = char.replace(
                    '_', 'underscore').replace('@', 'at').replace('&', 'and').replace(':', 'colon').replace(
                    '-', 'dash').replace(',', 'comma').replace('.', 'dot').replace('=', 'equals').replace(
                    '€', 'euro').replace('!', 'exclamation_mark').replace('#', 'hash').replace('*', 'multiply').replace(
                    '(', 'open_parenthesis').replace('[', 'open_square_bracket').replace('"', 'quote').replace(
                    '\'', 'single_quote').replace('/', 'slash').replace('`', 'backquote').replace(
                    '\\', 'backslash').replace(')', 'closed_parenthesis').replace(']', 'closed_square_bracket').replace(
                    '©', 'copyright').replace('$', 'dollar').replace('%', 'percent').replace('+', 'plus').replace(
                    '?', 'question_mark').replace('®', 'registered_sign').replace('~', 'tilde')
                self.characters[char] = spritesheet.parse_sprite(f'characters_symbol_{symbol}.png')
        self.space_width = self.characters["'"].get_width()

    def render(self, surf: pygame.Surface, text: str, loc: (float, float)) -> None:
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing


log.debug('Font class created')

log.debug('initializing fonts')
font = Font()
log.debug('fonts initialized')


def blit_tile(texture: pygame.Surface or list, x: float, y: float,
              physics: float = 0):  # PS or list is only because of pycharm error
    display.blit(texture, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
    if consoleAPI.gamemode == 'creative':
        return

    if physics == 0:
        pass
    elif physics == 1:
        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    elif physics == 0.5:
        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE / 2, TILE_SIZE, TILE_SIZE))
    elif physics == 0.6:
        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE / 2 + 2, TILE_SIZE, TILE_SIZE))
    elif physics == 0.7:
        tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE / 2 + 1, TILE_SIZE, TILE_SIZE))


show_tutorial = True
tutorial_surf = box_text = cords = None


# noinspection PyTypeChecker
def blit_tiles(layer_map: list,
               starting: list = (0, 0),
               ending: list = (round(len(game_map[0][0])), round(len(game_map[0][0]))),
               ) -> None:
    global show_tutorial, tutorial_surf
    starting, ending = list(starting), list(ending)
    if type(starting[0]) is not int or type(starting[1]) is not int:
        raise Exception(f'starting can be only tuple with ints, while got {starting}')
    elif type(ending[0]) is not int or type(ending[1]) is not int:
        raise Exception(f'ending can be only tuple with ints, while got {ending}')
    starting[0] = starting[0] if starting[0] >= 0 else 0
    starting[1] = starting[1] if starting[1] >= 0 else 0
    y = starting[1]
    for row in layer_map:
        if y >= ending[1]:
            break

        x = starting[0]

        for tile in row:
            if x >= ending[0]:
                break
            if tile == '-1':
                pass
            elif tile == '44':
                blit_tile(images['walls']['walls']['normal']['left'], x, y)  # wall_left.png
            elif tile == '45':
                blit_tile(images['walls']['walls']['normal']['mid'], x, y)  # wall_mid.png
            elif tile == '46':
                blit_tile(images['walls']['walls']['normal']['right'], x, y)  # wall_right.png
            elif tile == '47':
                blit_tile(images['walls']['walls']['dark']['left'], x, y, 1)  # wall_left_dark.png
            elif tile == '48':
                blit_tile(images['walls']['walls']['dark']['mid'], x, y, 1)  # wall_mid_dark.png
            elif tile == '49':
                blit_tile(images['walls']['walls']['dark']['right'], x, y, 1)  # wall_right_dark.png
            elif tile == '65':
                blit_tile(images['walls']['holes']['1_0'], x, y)  # wall_hole_1_0.png
            elif tile == '66':
                blit_tile(images['walls']['holes']['1_1'], x, y)  # wall_hole_1_1.png
            elif tile == '67':
                blit_tile(images['walls']['holes']['1_2'], x, y)  # wall_hole_1_2.png
            elif tile == '68':
                blit_tile(images['walls']['holes']['1_3'], x, y)  # wall_hole_1_3.png
            elif tile == '69':
                blit_tile(images['walls']['holes']['1_4'], x, y)  # wall_hole_1_4.png
            elif tile == '70':
                blit_tile(images['walls']['holes']['1_5'], x, y)  # wall_hole_1_5.png
            elif tile == '71':
                blit_tile(images['walls']['holes']['1_6'], x, y)  # wall_hole_1_6.png
            elif tile == '72':
                blit_tile(images['walls']['holes']['2'], x, y)  # wall_hole_2.png
            elif tile == '73':
                blit_tile(images['walls']['goo'], x, y)  # wall_goo.png
            elif tile == '74':
                blit_tile(images['floors']['goo'], x, y, 0.5)  # wall_goo_base.png
            elif tile == '75':
                blit_tile(images['floors']['1'], x, y, 0.5)  # floor_1.png
            elif tile == '76':
                blit_tile(images['floors']['2'], x, y, 0.5)  # floor_2.png
            elif tile == '77':
                blit_tile(images['floors']['3'], x, y, 0.5)  # floor_3.png
            elif tile == '78':
                blit_tile(images['floors']['4'], x, y, 0.5)  # floor_4.png
            elif tile == '79':
                blit_tile(images['floors']['5'], x, y, 0.5)  # floor_5.png
            elif tile == '80':
                blit_tile(images['floors']['6'], x, y, 0.5)  # floor_6.png
            elif tile == '81':
                blit_tile(images['floors']['7'], x, y, 0.5)  # floor_7.png
            elif tile == '82':
                blit_tile(images['floors']['8'], x, y, 0.5)  # floor_8.png
            elif tile == '83':
                blit_tile(images['floors']['ladder'], x, y, 0.5)  # floor_ladder.png
            elif tile == '84':
                damage_rects['spikes'].append(
                    pygame.Rect((x + 0.1) * TILE_SIZE, y * TILE_SIZE, TILE_SIZE * 0.9, TILE_SIZE))
                blit_tile(images['floors']['spikes'][anim_game_frame['spikes']], x, y, 0.5)  # floor_spikes_anim_f0.png
            elif tile == '106':
                blit_tile(images['floors']['hole'], x, y, 0.5)  # hole.png
            elif tile == '107':
                damage_rects['water'].append(
                    pygame.Rect((x + 0.1) * TILE_SIZE, (y - 0.2) * TILE_SIZE, TILE_SIZE * 0.9, TILE_SIZE))
                blit_tile(images['walls']['fountains']['basin']['blue'][anim_game_frame['liquid_water']],
                          x, y, 1)  # wall_fountain_basin_blue_anim_f0.png
            elif tile == '108':
                blit_tile(images['walls']['fountains']['mid']['blue'][anim_game_frame['liquid_water']],
                          x, y)  # wall_fountain_mid_blue_anim_f0.png
            elif tile == '109':
                damage_rects['lava'].append(
                    pygame.Rect((x + 0.1) * TILE_SIZE, (y - 0.2) * TILE_SIZE, TILE_SIZE * 0.9, TILE_SIZE))
                blit_tile(images['walls']['fountains']['basin']['red'][anim_game_frame['liquid_lava']],
                          x, y, 1)  # wall_fountain_basin_red_anim_f0.png
            elif tile == '110':
                blit_tile(images['walls']['fountains']['mid']['red'][anim_game_frame['liquid_lava']],
                          x, y)  # wall_fountain_mid_red_anim_f0.png
            elif tile == '0':
                blit_tile(images['misc']['chest']['empty'][0], x, y, 0.6)  # chest_empty_open_anim_f0.png
            elif tile == '1':
                blit_tile(images['misc']['chest']['full'][0], x, y, 0.6)  # chest_full_open_anim_f0.png
            elif tile == '2':
                blit_tile(images['misc']['chest']['mimic'][0], x, y, 0.6)  # chest_mimic_open_anim_f0.png
            elif tile == '5':
                blit_tile(images['misc']['crate'][0], x, y, 0.7)  # crate.png
            elif tile == '6':
                blit_tile(images['walls']['columns']['base'], x, y)  # column_base.png
            elif tile == '7':
                blit_tile(images['walls']['columns']['mid'], x, y)  # column_mid.png
            elif tile == '8':
                blit_tile(images['walls']['columns']['top'], x, y, 0.5)  # column_top.png
            elif tile == '9':
                blit_tile(images['walls']['doors']['frame_left_down'], x, y)  # doors_frame_left_down.png
            elif tile == '10':
                blit_tile(images['walls']['doors']['frame_left_up'], x, y)  # doors_frame_left_up.png
            elif tile == '11':
                blit_tile(images['walls']['doors']['frame_right_down'], x, y)  # doors_frame_right_down.png
            elif tile == '12':
                blit_tile(images['walls']['doors']['frame_right_up'], x, y)  # doors_frame_right_up.png
            elif tile == '13':
                blit_tile(images['walls']['doors']['frame_top_left'], x, y)  # doors_frame_top_left.png
            elif tile == '14':
                blit_tile(images['walls']['doors']['frame_top_right'], x, y)  # doors_frame_top_right.png
            elif tile == '15':
                blit_tile(images['walls']['doors']['leaf_closed_downleft'], x, y)  # doors_leaf_closed_downleft.png
            elif tile == '16':
                blit_tile(images['walls']['doors']['leaf_closed_downright'], x, y)  # doors_leaf_closed_downright.png
            elif tile == '17':
                blit_tile(images['walls']['doors']['leaf_closed_upleft'], x, y)  # doors_leaf_closed_upleft.png
            elif tile == '18':
                blit_tile(images['walls']['doors']['leaf_closed_upright'], x, y)  # doors_leaf_closed_upright.png
            elif tile == '19':
                blit_tile(images['walls']['doors']['leaf_open_downleft'], x, y)  # doors_leaf_open_downleft.png
            elif tile == '20':
                blit_tile(images['walls']['doors']['leaf_open_downright'], x, y)  # doors_leaf_open_downright.png
            elif tile == '21':
                blit_tile(images['walls']['doors']['leaf_open_upleft'], x, y)  # doors_leaf_open_upleft.png
            elif tile == '22':
                blit_tile(images['walls']['doors']['leaf_open_upright'], x, y)  # doors_leaf_open_upright.png
            elif tile == '23':
                blit_tile(images['walls']['doors']['wall_frame_left_down'], x, y)  # doors_wall_frame_left_down.png
            elif tile == '24':
                blit_tile(images['walls']['doors']['wall_frame_left_up'], x, y)  # doors_wall_frame_left_up.png
            elif tile == '25':
                blit_tile(images['walls']['doors']['wall_frame_right_down'], x, y)  # doors_wall_frame_right_down.png
            elif tile == '26':
                blit_tile(images['walls']['doors']['wall_frame_right_up'], x, y)  # doors_wall_frame_right_up.png
            elif tile == '27':
                blit_tile(images['walls']['banners']['blue'], x, y)  # banner_blue.png
            elif tile == '28':
                blit_tile(images['walls']['banners']['green'], x, y)  # banner_green.png
            elif tile == '29':
                blit_tile(images['walls']['banners']['red'], x, y)  # banner_red.png
            elif tile == '30':
                blit_tile(images['walls']['banners']['yellow'], x, y)  # banner_yellow.png
            elif tile == '31':
                blit_tile(images['walls']['banners']['wall']['blue'], x, y)  # wall_banner_blue.png
            elif tile == '32':
                blit_tile(images['walls']['banners']['wall']['green'], x, y)  # wall_banner_green.png
            elif tile == '33':
                blit_tile(images['walls']['banners']['wall']['red'], x, y)  # wall_banner_red.png
            elif tile == '34':
                blit_tile(images['walls']['banners']['wall']['yellow'], x, y)  # wall_banner_yellow.png
            elif tile == '35':
                blit_tile(images['walls']['columns']['wall']['base'], x, y, 0.5)  # wall_column_base.png
            elif tile == '36':
                blit_tile(images['walls']['columns']['wall']['mid'], x, y)  # wall_column_mid.png
            elif tile == '37':
                blit_tile(images['walls']['columns']['top'], x, y)  # wall_column_top.png
            elif tile == '38':
                blit_tile(images['walls']['corners']['corners']['front_left'], x, y)  # wall_corner_front_left.png
            elif tile == '39':
                blit_tile(images['walls']['corners']['corners']['front_right'], x, y)  # wall_corner_front_right.png
            elif tile == '40':
                blit_tile(images['walls']['corners']['corners']['left'], x, y)  # wall_corner_left.png
            elif tile == '41':
                blit_tile(images['walls']['corners']['corners']['right'], x, y)  # wall_corner_right.png
            elif tile == '42':
                blit_tile(images['walls']['corners']['inner']['mid_left'], x, y)  # wall_inner_corner_mid_left.png
            elif tile == '43':
                blit_tile(images['walls']['corners']['inner']['mid_right'], x, y)  # wall_inner_corner_mid_right.png
            elif tile == '111':
                blit_tile(images['walls']['corners']['corners']['bottom_left'], x, y)  # wall_corner_bottom_left.png
            elif tile == '112':
                blit_tile(images['walls']['corners']['corners']['bottom_right'], x, y)  # wall_corner_bottom_right.png
            elif tile == '113':
                blit_tile(images['walls']['corners']['corners']['top_left'], x, y)  # wall_corner_top_left.png
            elif tile == '114':
                blit_tile(images['walls']['corners']['corners']['top_right'], x, y)  # wall_corner_top_right.png
            elif tile == '115':
                blit_tile(images['walls']['corners']['inner']['l_top_left'], x, y)  # wall_inner_corner_l_top_left.png
            elif tile == '116':
                blit_tile(images['walls']['corners']['inner']['l_top_right'], x, y)  # wall_inner_corner_l_top_right.png
            elif tile == '117':
                blit_tile(images['walls']['corners']['inner']['l_top_left'], x, y)  # wall_inner_corner_t_top_left.png
            elif tile == '118':
                blit_tile(images['walls']['corners']['inner']['t_top_right'], x, y)  # wall_inner_corner_t_top_right.png
            elif tile == '119':
                ...  # wall_side_front_left.png
            elif tile == '120':
                ...  # wall_side_front_right.png
            elif tile == '121':
                ...  # wall_side_mid_left.png
            elif tile == '122':
                ...  # wall_side_mid_right.png
            elif tile == '123':
                ...  # wall_side_top_left.png
            elif tile == '124':
                ...  # wall_side_top_right.png
            elif tile == '125':
                ...  # wall_top_left.png
            elif tile == '126':
                ...  # wall_top_mid.png
            elif tile == '127':
                ...  # wall_top_right.png
            x += 1
        y += 1


log.debug('Defining levels data')
levels = {
    '0': {
        'locations': {
            'main': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE},
                    },
                    'scroll': {
                        'left': 0,
                        'up': 6 * TILE_SIZE,
                        'right': int(44 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
        },
        'starting_pos': (2 * TILE_SIZE, 12.25 * TILE_SIZE),
        'num': 1,
    },
    '1': {
        'locations': {
            'main': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE},
                    },
                    'scroll': {
                        'left': 0,
                        'up': 6 * TILE_SIZE,
                        'right': int(44 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
        },
        'starting_pos': (2 * TILE_SIZE, 12.25 * TILE_SIZE),
        'num': 2,
    },
    '2': {
        'locations': {
            'main': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE},
                    },
                    'scroll': {
                        'left': 0,
                        'up': 6 * TILE_SIZE,
                        'right': int(44 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
        },
        'starting_pos': (2 * TILE_SIZE, 12.25 * TILE_SIZE),
        'num': 3,
    },
    '3': {
        'locations': {
            'main': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE},
                    },
                    'scroll': {
                        'left': 0,
                        'up': 6 * TILE_SIZE,
                        'right': int(47 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
            'basement': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE + player_rect.height},
                    },
                    'scroll': {
                        'left': 48 * TILE_SIZE,  # 47tiles - display size
                        'up': 2 * TILE_SIZE,
                        'right': int(88 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
        },
        'starting_pos': (2 * TILE_SIZE, 12.25 * TILE_SIZE),
        'num': 4,
        'interactive_objects': {
            'to_basement': [66.5 * TILE_SIZE, 18.25 * TILE_SIZE],
            'to_main': [28 * TILE_SIZE, 13.25 * TILE_SIZE],
        },
    },
    '4': {
        'locations': {
            'main': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE},
                    },
                    'scroll': {
                        'left': 0,
                        'up': 6 * TILE_SIZE,
                        'right': int(47 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
            'basement': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE + player_rect.height},
                    },
                    'scroll': {
                        'left': 48 * TILE_SIZE,  # 47tiles - display size
                        'up': 2 * TILE_SIZE,
                        'right': int(88 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # 47tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
        },
        'starting_pos': (2 * TILE_SIZE, 12.25 * TILE_SIZE),
        'num': 5,
        'interactive_objects': {
            'to_basement': [66.5 * TILE_SIZE, 18.25 * TILE_SIZE],
            'to_main': [28 * TILE_SIZE, 13.25 * TILE_SIZE],
        },
    },
    '5': {
        'locations': {
            'main': {
                'limitations': {
                    'cords': {
                        'start': {'x': None, 'y': None},
                        'end': {'x': None, 'y': 31 * TILE_SIZE},
                    },
                    'scroll': {
                        'left': 0,
                        'up': 6 * TILE_SIZE,
                        'right': int(47 * TILE_SIZE - WINDOW_SIZE[0] / 2),  # tiles - display size
                        'down': (31 * TILE_SIZE) - WINDOW_SIZE[1] / 2,
                    },
                },
            },
        },
        'starting_pos': (4.5 * TILE_SIZE, 24.5 * TILE_SIZE),
        'num': 6,
        'interactive_objects': {},
    },
}
log.debug('Levels data defined')

log.debug('loding level')
level = levels[str(level_name)]
limitations = level['locations']['main']['limitations']
log.debug('level loaded')

log.debug('defining more settings')
damage = {
    'spikes': 1,
    'lava': 1,
}
health = {'player': 6}
damaged_cooldown = 0
damaged = False
jump = False
jump_cooldown = 0
show_cords = False
interactive_object = None
enabled_e = False
on_fire = False
dead = False
items_list = []
log.debug('settings defined')


def convert_game_frame() -> None:
    global true_anim_game_frame, anim_game_frame

    if true_anim_game_frame['fire'] >= 4:
        true_anim_game_frame['fire'] = 0
    if true_anim_game_frame['player'] >= 4:
        true_anim_game_frame['player'] = 0
    if true_anim_game_frame['spikes'] >= 4:
        true_anim_game_frame['spikes'] = -3
    if true_anim_game_frame['liquid_lava'] >= 3:
        true_anim_game_frame['liquid_lava'] = 0
    if true_anim_game_frame['liquid_water'] >= 3:
        true_anim_game_frame['liquid_water'] = 0
    if true_anim_game_frame['item'] >= 2:
        true_anim_game_frame['item'] = 0
    anim_game_frame['fire'] = abs(int(true_anim_game_frame['fire']))
    anim_game_frame['player'] = abs(int(true_anim_game_frame['player']))
    anim_game_frame['spikes'] = abs(int(true_anim_game_frame['spikes']))
    anim_game_frame['liquid_lava'] = abs(int(true_anim_game_frame['liquid_lava']))
    anim_game_frame['liquid_water'] = abs(int(true_anim_game_frame['liquid_water']))
    anim_game_frame['item'] = abs(int(true_anim_game_frame['item']))


def blit_map() -> None:
    for layer in game_map:
        blit_tiles(layer,
                   ending=[round((scroll[0] + int(WINDOW_SIZE[0] / 2)) / TILE_SIZE) + 1,
                           round((scroll[1] + int(WINDOW_SIZE[1] / 2)) / TILE_SIZE) + 1])

    y = 0
    for row in map_items:
        x = 0
        for item in row:
            if item == '3':
                if anim_game_frame['item'] == 0:
                    blit_tile(images['items']['potions']['big_red'], x, y - 0.5)
                elif anim_game_frame['item'] == 1:
                    blit_tile(images['items']['potions']['big_red'], x, y - 0.55)
                interactive_objects_rects[0].append(
                    pygame.Rect(x * TILE_SIZE, (y - 0.5) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                interactive_objects_rects[1].append('big_health_potion')
                items_list.append({
                    'type': 'big_health_potion',
                    'cords': (x, y)
                })
            x += 1
        y += 1
    y = 0

    for row in game_interactive_objects:
        x = 0
        for io in row:  # io = interactive objects
            if io == '-1':
                pass
            elif io == '0':
                interactive_objects_rects[0].append(
                    pygame.Rect(x * TILE_SIZE, (y - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                interactive_objects_rects[1].append('to_basement')
            elif io == '1':
                interactive_objects_rects[0].append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                interactive_objects_rects[1].append('to_main')
            elif io == '2':
                interactive_objects_rects[0].append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                interactive_objects_rects[1].append('end')
            elif io == '3':
                interactive_objects_rects[0].append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                interactive_objects_rects[1].append('goblin_0')
            elif io == '4':
                interactive_objects_rects[0].append(
                    pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                interactive_objects_rects[1].append('goblin_1')
            x += 1
        y += 1


def convert_scroll() -> [int, int]:
    global true_scroll, limitations

    true_scroll[0] += (player_rect.x - true_scroll[0] - 300 + player_rect.size[0]) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 200) / 20

    # noinspection PyTypeChecker
    if true_scroll[1] < limitations['scroll']['up']:
        true_scroll[1] = limitations['scroll']['up']
    # noinspection PyTypeChecker
    if true_scroll[1] > limitations['scroll']['down']:
        # noinspection PyTypeChecker
        true_scroll[1] = limitations['scroll']['down']
    # noinspection PyTypeChecker
    if true_scroll[0] > limitations['scroll']['right']:
        true_scroll[0] = limitations['scroll']['right']
    # noinspection PyTypeChecker
    if true_scroll[0] < limitations['scroll']['left']:
        true_scroll[0] = limitations['scroll']['left']

    return [int(true_scroll[0]), int(true_scroll[1])]


def parse_level():
    global level, levels, limitations, level_name, game_map, game_interactive_objects, map_items, starting_position
    try:
        game_map = [
            [row.split(',') for row in layer] for layer in  # layer.split('\n') -> rows | row.split(',') -> ids
            [layer.split('\n') for layer in levels_data_decrypted[level_name].split('\n\\\n')]
            # map_decrypted.split('\n\\\n') -> layers
        ]
        # list with layers (lists) which contain rows which contain ids [layer[ row[id('42'), ...], row[] ], layer[...]]

        map_items = game_map.pop(2)[:-1]
        game_interactive_objects = game_map.pop(2)[:-1]

        level = levels[str(level_name)]
        limitations = level['locations']['main']['limitations']
        starting_position = level['starting_pos']
        enemy_spawn_points = {}
        y = 0
        for row in game_interactive_objects:
            x = 0
            for io in row:  # io = interactive objects
                if io == '-1':
                    pass
                elif io == '3':
                    enemy_spawn_points['zombie'] = [
                        pygame.Rect(x * TILE_SIZE, (y - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)]
                elif io == '4':
                    enemy_spawn_points['zombie'].append(
                        pygame.Rect(x * TILE_SIZE, (y - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                x += 1
            y += 1
        # check is zombie spawn points are in the the dictionary
        if 'zombie' in enemy_spawn_points:
            spawn_enemy('zombie', (enemy_spawn_points['zombie'][0].x, enemy_spawn_points['zombie'][0].y),
                        enemy_spawn_points['zombie'])
    except IndexError:
        log.error('404 Level not found (99% there is no more levels)')
        pygame.quit()
        input('Press Enter to exit')
        exit()


def spawn_enemy(enemy_type: str, cords: [int, int], spawn_points: list[pygame.Rect]):
    global enemies
    enemies.append(Enemy(enemy_type, cords, spawn_points))


# TODO: сделать все классы рабочими :D
class Enemy:
    def __init__(self, enemy_type: str, cords: [int, int], spawn_points: list[pygame.Rect]):
        self.type = enemy_type
        self.moving = {'left': False, 'right': False, 'up': False, 'down': False}
        self.direction = 'right'
        self.convert_type_to_stats(enemy_type)
        self.animation.update()
        self.rect = pygame.Rect(*cords, self.animation.frame.get_width(),
                                self.animation.frame.get_height())
        self.y_momentum = 0
        self.spawn_points = spawn_points
        self.movement = [0, 0]

    def convert_type_to_stats(self, enemy_type: str):
        match enemy_type:
            case 'zombie':
                self.speed = 2
                self.health = 5
                self.attack = Attack('hand', 2, 125)
                self.animation = EntityAnimation(images['enemies']['zombie'], 'idle')
                self.animation.speed = 2
            case 'big_zombie':
                self.speed = 1
                self.health = 10
                self.attack = Attack('hand', 3, 0)
                self.animation = EntityAnimation(images['enemies']['big_zombie'], 'idle')
                self.animation.speed = 1
            case 'tiny_zombie':
                self.speed = 4
                self.health = 1
                self.attack = Attack('hand', 1, 0)
                self.animation = EntityAnimation(images['enemies']['tiny_zombie'], 'idle')
                self.animation.speed = 4
            case 'ice_zombie':
                self.speed = 3
                self.health = 5
                self.attack = Attack('hand', 3, 0)
                self.animation = EntityAnimation(images['enemies']['ice_zombie'], 'idle')
                self.animation.speed = 3
            case 'big_demon':
                self.speed = 1
                self.health = 20
                self.attack = Attack('hand', 5, 0)
                self.animation = EntityAnimation(images['enemies']['big_demon'], 'idle')
                self.animation.speed = 1
            case 'chort':
                self.speed = 2
                self.health = 5
                self.attack = Attack('hand', 3, 0)
                self.animation = EntityAnimation(images['enemies']['chort'], 'idle')
                self.animation.speed = 2
            case 'goblin':
                self.speed = 3
                self.health = 5
                self.attack = Attack('hand', 2, 0)
                self.animation = EntityAnimation(images['enemies']['goblin'], 'idle')
                self.animation.speed = 3
            case 'imp':
                self.speed = 4
                self.health = 5
                self.attack = Attack('hand', 2, 0)
                self.animation = EntityAnimation(images['enemies']['imp'], 'idle')
                self.animation.speed = 4
            case 'masked_orc':
                self.speed = 5
                self.health = 5
                self.attack = Attack('hand', 1, 0)
                self.animation = EntityAnimation(images['enemies']['masked_orc'], 'idle')
                self.animation.speed = 5
            case 'muddy':
                self.speed = 2
                self.health = 5
                self.attack = Attack('hand', 3, 0)
                self.animation = EntityAnimation(images['enemies']['muddy'], 'idle')
                self.animation.speed = 2
            case 'necromancer':
                self.speed = 1
                self.health = 10
                self.attack = Attack('hand', 10, 0)  # TODO add spell attack
                self.animation = EntityAnimation(images['enemies']['necromancer'], 'idle')
                self.animation.speed = 1
            case 'ogre':
                self.speed = 1
                self.health = 10
                self.attack = Attack('hand', 5, 0)
                self.animation = EntityAnimation(images['enemies']['ogre'], 'idle')
                self.animation.speed = 1
            case 'orc_shaman':
                self.speed = 1
                self.health = 10
                self.attack = Attack('hand', 5, 0)  # TODO add spell attack
                self.animation = EntityAnimation(images['enemies']['orc_shaman'], 'idle')
                self.animation.speed = 1
            case 'orc_warrior':
                self.speed = 5
                self.health = 10
                self.attack = Attack('hand', 1, 0)
                self.animation = EntityAnimation(images['enemies']['orc_warrior'], 'idle')
                self.animation.speed = 5
            case 'swampy':
                self.speed = 3
                self.health = 5
                self.attack = Attack('hand', 2, 0)
                self.animation = EntityAnimation(images['enemies']['swampy'], 'idle')
                self.animation.speed = 3
            case 'wogol':
                self.speed = 6
                self.health = 10
                self.attack = Attack('hand', 2, 0)
                self.animation = EntityAnimation(images['enemies']['wogol'], 'idle')
                self.animation.speed = 6
            case 'skelet':
                self.speed = 1
                self.health = 5
                self.attack = Attack('hand', 5, 0)  # TODO add bow attack
                self.animation = EntityAnimation(images['enemies']['skelet'], 'idle')
                self.animation.speed = 1
            case _:
                raise Exception(f'Unknown enemy type: {enemy_type}')

    def update(self):
        global tile_rects

        self.moving = {'left': False, 'right': False, 'up': False, 'down': False}
        # go to left while didn't passed spawn_points[0]
        if self.rect.x > self.spawn_points[0].x and self.direction == 'left':
            self.moving['left'] = True
        elif self.direction == 'left':
            self.direction = 'right'

        # go to right while didn't passed spawn_points[1]
        if self.rect.x < self.spawn_points[1].x and self.direction == 'right':
            self.moving['right'] = True
        elif self.direction == 'right':
            self.direction = 'left'

        # if passed spawn_points[0] or spawn_points[1] - go to them and change direction to opposite
        if self.rect.x > self.spawn_points[1].x:
            self.rect.x = self.spawn_points[1].x
            self.direction = 'left'
        elif self.rect.x < self.spawn_points[0].x:
            self.rect.x = self.spawn_points[0].x
            self.direction = 'right'

        # update animation and flip image if needed
        if self.moving['left'] or self.moving['right']:
            self.animation.set_animation_type('run')
        else:
            self.animation.set_animation_type('idle')

        self.animation.update()
        if self.moving['right'] != self.moving['left']:  # XOR, if moving right or left but not both
            self.animation.flip = self.moving['left']

        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.animation.frame.get_width(),
                                self.animation.frame.get_height())

        collision = self.move(tile_rects)
        if collision['bottom']:
            self.y_momentum = 0

        # reduce cooldown of attack
        if self.attack.cooldown > 0:
            self.attack.cooldown -= 1

    def move(self, tiles):  # TODO fix y movement making the enemy jump and not walking in straight line
        # move right/up with speed if moving right/up and not moving left/down
        # else move left/down with speed if moving left/down and not moving right
        self.movement = [0, 0]
        self.movement[1] += self.y_momentum
        self.y_momentum += 0.2
        if self.y_momentum > 3:
            self.y_momentum = 3
        if self.moving['right'] != self.moving['left']:  # XOR
            self.movement[0] += self.speed if self.moving['right'] else -self.speed
        if self.moving['up'] != self.moving['down']:  # XOR
            self.movement[1] += self.speed if self.moving['up'] else -self.speed

        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.rect.x += self.movement[0]  # move player (players rect) to x position (right / left)
        hit_list = collision_test(self.rect, tiles)  # check collision on x axis
        for tile in hit_list:
            if self.movement[0] > 0:  # if moving right
                self.rect.right = tile.left  # set right side of a player rect to left side of a tile
                collision_types['right'] = True
            elif self.movement[0] < 0:  # if moving left
                self.rect.left = tile.right  # set left side of a player rect to right side of a tile
                collision_types['left'] = True

        self.rect.y += self.movement[1]  # move player (players rect) to y position (up / down)
        hit_list = collision_test(self.rect, tiles)  # check collision on x axis
        for tile in hit_list:
            if self.movement[1] > 0:  # if moving down
                self.rect.bottom = tile.top  # set bottom side of a player rect to top side of a tile
                collision_types['bottom'] = True
            elif self.movement[1] < 0:  # if moving up
                self.rect.top = tile.bottom  # set top side of a player rect to bottom side of a tile
                collision_types['top'] = True
        return collision_types  # return players rect and all collision types


class Attack:
    def __init__(self, attack_type: str, damage: int, cooldown_time: int):
        self.attack_type = attack_type
        self.damage = damage
        self.cooldown_time = cooldown_time
        self.cooldown = 0

    def attack(self, target_hp: int):
        if self.cooldown == 0:
            target_hp -= self.damage
            self.cooldown = self.cooldown_time
        return target_hp


class Animation:
    def __init__(self, sprites: list, speed: int = 1, loop: bool = True):
        self.sprites = sprites
        self.speed = speed
        self.loop = loop
        self.frame = None
        self.__frame_counter = 0
        self.__frame_counter_max = len(self.sprites)
        self.flip = False

    def update(self):
        if self.__frame_counter >= self.__frame_counter_max:
            self.__frame_counter = 0 if self.loop else -self.__frame_counter

        self.__frame_counter += self.speed / 60
        self.frame = self.sprites[math.floor(abs(self.__frame_counter) % self.__frame_counter_max)]


class EntityAnimation(Animation):
    def __init__(self, animations_package: dict[str, list], animation_type: str, speed: int = 1):
        super().__init__(animations_package[animation_type])
        self.speed = speed
        self.loop = False
        self.animations_package = animations_package
        self.animation_type = animation_type

    def set_animation_type(self, animation_type: str):
        self.animation_type = animation_type
        self.sprites = self.animations_package[animation_type]
        self.__frame_counter_max = len(self.sprites)


def calculate_health():
    global damage_rects, damaged_cooldown, damage_rects, damaged, on_fire, health, dead
    spikes_collide = len(collision_test(player_rect, damage_rects['spikes'])) > 0 and anim_game_frame['spikes'] >= 2
    lava_collide = len(collision_test(player_rect, damage_rects['lava'])) > 0
    water_collide = len(collision_test(player_rect, damage_rects['water'])) > 0
    damage_rects = {
        'spikes': [],
        'lava': [],
        'water': [],
    }
    if damaged_cooldown == 0 and consoleAPI.gamemode != 'creative':
        if spikes_collide:
            damaged_cooldown = 50
            damaged = True
            health['player'] -= damage['spikes']
        elif lava_collide:
            on_fire = True
    elif damaged_cooldown > 0:
        damaged_cooldown -= 1

    if damaged_cooldown == 0:
        damaged = False

    if on_fire and water_collide:
        on_fire = False
        damaged_cooldown = 0
        damaged = False

    if on_fire and damaged_cooldown == 0 and consoleAPI.gamemode != 'creative':
        if health['player'] > 1:
            damaged_cooldown = 120
        else:
            damaged_cooldown = 150
        if spikes_collide:
            damaged = True
            damaged_cooldown = 50
        health['player'] -= damage['lava']

    if health['player'] <= 0:
        dead = True


def text_box(x: int, y: int, w: int, h: int, b: int):
    return pygame.Rect(x, y, w, h), pygame.Rect(x + b, y + b, w - b * 2, h - b * 2)


restart = False


def get_text_size(text: str, font: Font = font) -> int:
    text_size = 0
    for char in text:
        if char != ' ':
            text_size += font.characters[char].get_width() + font.spacing
        else:
            text_size += font.space_width + font.spacing
    return text_size


def death_menu(death_message: str = 'You died'):
    global screen
    death_screen_background = pygame.Surface(WINDOW_SIZE)
    death_screen_background.fill((160, 160, 160))
    death_screen_background.set_alpha(2)
    tick_num = 0

    while True:
        if tick_num == 180:
            break

        tick_num += 1
        death_screen = pygame.Surface((WINDOW_SIZE[0] / 4, WINDOW_SIZE[1] / 4), SRCALPHA, 32)

        font.render(
            death_screen,
            death_message,
            (
                (WINDOW_SIZE[0] / 4 - get_text_size(death_message)) / 2,
                WINDOW_SIZE[1] / 20
            )
        )

        for event in pygame.event.get():
            if event.type == QUIT:  # check for window quit
                pygame.quit()  # stop pygame
                exit()  # stop script

        death_screen = pygame.transform.scale(death_screen, WINDOW_SIZE)
        screen.blit(death_screen_background, (0, 0))
        screen.blit(death_screen, (0, 0))

        pygame.display.update()  # update display
        clock.tick(60)  # maintain 60 fps


def black_screen():
    surf = pygame.Surface(WINDOW_SIZE)
    surf.fill((0, 0, 0))
    surf.set_alpha(5)
    tick_num = 0

    while True:
        if tick_num == 60:
            break

        tick_num += 1
        for event in pygame.event.get():
            if event.type == QUIT:  # check for window quit
                pygame.quit()  # stop pygame
                exit()  # stop script

        screen.blit(surf, (0, 0))
        pygame.display.update()  # update display
        clock.tick(60)  # maintain 60 fps

level_save = None
log.debug('Starting the game')
while True:  # game loop
    speed = consoleAPI.speed

    if old_level_name != level_name:
        enemies = []
        parse_level()
        level_save = {
            'player_health': health['player'],
            'on_fire': on_fire,
        }
        restart = True
        old_level_name = level_name

    display.fill((146, 244, 255))
    # noinspection PyUnresolvedReferences
    if limitations['cords']['end']['y'] is not None and player_rect.y >= limitations['cords']['end']['y']:
        dead = True

    if dead:
        death_menu()
        black_screen()
        restart = True
        player_flip = False
        health['player'] = 6 if level_save is None else level_save['player_health']
        damaged_cooldown = 0
        damaged = False
        jump = False
        interactive_object = None
        enabled_e = False
        on_fire = False if level_save is None else level_save['on_fire']
        is_moving = False
        moving['left'] = False
        moving['right'] = False

    if restart:
        player_rect = pygame.Rect(starting_position[0], starting_position[1], player_image[0].get_width(),
                                  player_image[0].get_height())
        dead = False
        restart = False
        limitations = level['locations']['main']['limitations']
        continue

    convert_game_frame()

    scroll = convert_scroll()

    blit_map()
    if level['num'] == 1:
        if player_rect.x < 250:
            box_text = 'Use A and D to move'
            cords = (10, 7)
        elif player_rect.x > 550:
            box_text = 'Press F to interact'
            cords = (34, 7)
        else:
            tutorial_surf = box_text = cords = None
    elif level['num'] == 2:
        if 7 * TILE_SIZE < player_rect.x < 26 * TILE_SIZE:
            box_text = 'Use W or Space to jump'
            cords = (18, 7)
        else:
            tutorial_surf = box_text = cords = None
    elif level['num'] == 3:
        if 10 * TILE_SIZE < player_rect.x < 16 * TILE_SIZE:
            box_text = 'Lava is hot'
            cords = (16.75, 7)
        elif 17 * TILE_SIZE < player_rect.x < 30 * TILE_SIZE:
            box_text = 'While water is cold'
            cords = (25, 7)
        else:
            tutorial_surf = box_text = cords = None
    elif level['num'] == 4:
        if 10 * TILE_SIZE < player_rect.x < 16 * TILE_SIZE:
            box_text = 'Sometimes the answer isn\'t above the surface'
            cords = (13, 7)
        else:
            tutorial_surf = box_text = cords = None
    elif level['num'] == 5:
        if 27 * TILE_SIZE < player_rect.x < 33 * TILE_SIZE:
            box_text = 'I think you know why you shouldn\'t step on thorns'
            cords = (22, 7)
        elif 31 * TILE_SIZE < player_rect.x and 15 * TILE_SIZE < player_rect.y and limitations == \
                level['locations']['main']['limitations']:
            box_text = 'There is monsters in next level, be careful'
            cords = (28, 10)
        else:
            tutorial_surf = box_text = cords = None
    else:
        tutorial_surf = box_text = cords = None
    if cords is not None:
        if box_text is None:
            box_text = ''
        text_size = 0
        for char in box_text:
            if char != ' ':
                text_size += font.characters[char].get_width() + font.spacing
            else:
                text_size += font.space_width + font.spacing
        tutorial_surf = pygame.Surface((text_size + 24, 26), pygame.SRCALPHA, 32)

        box = text_box(x=0, y=0, w=tutorial_surf.get_width(), h=tutorial_surf.get_height(), b=4)
        pygame.draw.rect(tutorial_surf, (12, 12, 12), box[0], 0, 5)
        pygame.draw.rect(tutorial_surf, (16, 29, 66), box[1], 0, 5)

        font.render(tutorial_surf, box_text, (12, 6))
        display.blit(tutorial_surf, (cords[0] * TILE_SIZE - scroll[0], cords[1] * TILE_SIZE - scroll[1]))

    player_movement = [0, 0]
    if moving['right'] != moving['left'] and not damaged:  # XOR
        if moving['right']:
            player_movement[0] += speed
        elif moving['left']:
            player_movement[0] -= speed

    elif damaged and damaged_cooldown == 20:
        player_y_momentum = 0
        player_movement[0] = 0
    elif damaged and damaged_cooldown > 10:
        if air_timer < 6:
            player_y_momentum = -5

    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3

    if consoleAPI.gamemode == 'creative':
        player_y_momentum = 0

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    for enemy in enemies:
        enemy.update()
        enemy.animation.update()
        display.blit(
            pygame.transform.flip(enemy.animation.frame, enemy.animation.flip, False),
            (enemy.rect.x - scroll[0], enemy.rect.y - scroll[1]),
        )
        # check if player rect collides with enemy rect
        if player_rect.colliderect(enemy.rect) and damaged_cooldown == 0:
            damaged_cooldown = 50
            damaged = True
            # TODO fix bug when player dies, after respawn, all tiles are solid and 16*16
            health['player'] = enemy.attack.attack(health['player'])
    tile_rects = []

    calculate_health()
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    elif collisions['top']:
        player_y_momentum -= player_y_momentum
    else:
        air_timer += 1

    try:
        display.blit(
            pygame.transform.flip(player_image[anim_game_frame['player']], player_flip, False),
            (player_rect.x - scroll[0], player_rect.y - scroll[1]),
        )
        if on_fire:
            # noinspection PyTypeChecker
            display.blit(
                pygame.transform.flip(images['effects']['fire'][anim_game_frame['fire']], player_flip, False),
                (
                    player_rect.x - scroll[0],
                    player_rect.y - scroll[1] + player_image[anim_game_frame['player']].get_height() -
                    images['effects']['fire'][anim_game_frame['fire']].get_height()
                ),
            )
    except IndexError:
        display.blit(
            pygame.transform.flip(player_image[0], player_flip, False),
            (player_rect.x - scroll[0], player_rect.y - scroll[1]),
        )
        if on_fire:
            # noinspection PyTypeChecker
            display.blit(
                pygame.transform.flip(images['effects']['fire'][anim_game_frame['fire']], player_flip, False),
                (
                    player_rect.x - scroll[0],
                    player_rect.y - scroll[1] + player_image[0].get_height() -
                    images['effects']['fire'][anim_game_frame['fire']].get_height()
                ),
            )
    if moving['right'] != moving['left'] and not damaged:  # XOR, if moving right or left but not both
        player_flip = moving['left']

    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:  # check for window quit
            log.debug('Game ended')
            pygame.quit()  # stop pygame
            exit()  # stop script
        elif not console.enabled and event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == K_d:
                moving['right'] = True
            elif event.key == K_LEFT or event.key == K_a:
                moving['left'] = True

            elif event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                jump = True
                if consoleAPI.gamemode == 'creative':
                    player_rect.y -= 16
            elif event.key == K_DOWN or event.key == K_s:
                if consoleAPI.gamemode == 'creative':
                    player_rect.y += 16

            elif event.key == K_f:
                if interactive_object is not None:
                    if interactive_object == 'to_basement':
                        player_rect.x, player_rect.y = level['interactive_objects']['to_basement']
                        limitations = level['locations']['basement']['limitations']
                    elif interactive_object == 'to_main':
                        player_rect.x, player_rect.y = level['interactive_objects']['to_main']
                        limitations = level['locations']['main']['limitations']
                    elif interactive_object == 'big_health_potion':
                        health['player'] += 3
                        if health['player'] > 6:
                            health['player'] = 6
                        for item in items_list:
                            if item['type'] == interactive_object and abs(
                                    player_rect.x / TILE_SIZE - item['cords'][0]) <= 1 and abs(
                                    player_rect.y / TILE_SIZE - item['cords'][1]) <= 1:
                                map_items[item['cords'][1]][item['cords'][0]] = '-1'
                    elif interactive_object == 'end':
                        if not enabled_e:
                            enabled_e = True
                        level_name += 1

        elif event.type == pygame.KEYUP:
            # Toggle console on/off the console
            if event.key == pygame.K_F1:
                # Toggle the console - if on then off if off then on
                console.toggle()

            elif event.key == K_F3:
                show_cords = not show_cords
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moving['right'] = False
            elif event.key == K_LEFT or event.key == K_a:
                moving['left'] = False

            elif event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                jump = False
                jump_cooldown = 0

    items_list = []

    if air_timer < 6 and jump and not damaged and jump_cooldown == 0:
        player_y_momentum = -5
        jump_cooldown = 70
    if jump_cooldown > 0:
        jump_cooldown -= 1

    if damaged:
        is_moving = False
        player_image = player_images['hit']

    elif any(moving.values()):  # if one of the values in {moving} is true
        is_moving = True
        player_image = player_images['run']
    else:
        is_moving = False
        player_image = player_images['idle']

    if is_moving:
        true_anim_game_frame['player'] += round(speed / (2 / 0.15), 1)
    else:
        true_anim_game_frame['player'] += 0.08

    if anim_game_frame['spikes'] == 0:
        true_anim_game_frame['spikes'] += 0.05
    elif anim_game_frame['spikes'] >= 3:
        true_anim_game_frame['spikes'] += 0.02
    elif anim_game_frame['spikes'] < 3:
        true_anim_game_frame['spikes'] += 0.2

    true_anim_game_frame['liquid_lava'] += 0.02
    true_anim_game_frame['liquid_water'] += 0.1
    true_anim_game_frame['fire'] += 0.1
    true_anim_game_frame['item'] += 0.02

    if health['player'] == 6:
        fullness = ('full', 'full', 'full')
    elif health['player'] == 5:
        fullness = ('full', 'full', 'half')
    elif health['player'] == 4:
        fullness = ('full', 'full', 'empty')
    elif health['player'] == 3:
        fullness = ('full', 'half', 'empty')
    elif health['player'] == 2:
        fullness = ('full', 'empty', 'empty')
    elif health['player'] == 1:
        fullness = ('half', 'empty', 'empty')
    else:
        fullness = ('empty', 'empty', 'empty')

    for fullness_type, i in zip(fullness, range(3)):
        # noinspection PyTypeChecker
        ui.blit(images['ui']['hearts'][fullness_type], (TILE_SIZE * i, 0))

    if show_cords:
        log.info(
            f'rl:{(player_rect.x, player_rect.y)} | cords:{(player_rect.x // TILE_SIZE, player_rect.y // TILE_SIZE)}')
        console.write(str((player_rect.x, player_rect.y)))

    ui_surf = pygame.transform.scale(ui, (96, 32))
    if consoleAPI.gamemode != 'creative':
        display.blit(ui_surf, (0, 0))

    if enabled_e and interactive_object is not None:  # player is interacting with io:
        e_button = pygame.Surface((30, 30), pygame.SRCALPHA, 32)
        box = text_box(x=0, y=0, w=30, h=30, b=2)
        # noinspection PyUnresolvedReferences,PyTypeChecker
        pygame.draw.rect(e_button, (240, 240, 240), box[0], 0, 15)
        pygame.draw.rect(e_button, (18, 18, 18), box[1], 0, 15)
        font.render(e_button, 'F', (11, 9))
        e_button = pygame.transform.scale(e_button, (16, 16))
        display.blit(e_button, (player_rect.x - scroll[0] + 20, player_rect.y - scroll[1] - 15))

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    if len(collision_test(player_rect, interactive_objects_rects[0])) > 0:
        for collision_rect in collision_test(player_rect, interactive_objects_rects[0]):
            for rect, io_type in zip(interactive_objects_rects[0], interactive_objects_rects[1]):
                if rect == collision_rect:
                    interactive_object = io_type
                    break
    else:
        interactive_object = None
    interactive_objects_rects = [[], []]

    # Read and process events related to the console in case console is enabled
    console.update(events)

    # Display the console if enabled or animation is still in progress
    console.show(screen)

    pygame.display.update()  # update display
    clock.tick(60)  # maintain 60 fps
