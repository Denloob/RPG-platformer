# Setup Python ----------------------------------------------- #
import pygame
import string
import sys

from assets.data.spritesheet_parser import Parse  # sprite sheet parser which can parse png files with data in json

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500), 0, 32)
spritesheet = Parse('assets/textures/main.png')  # create an instance of the Parse class


# Funcs/Classes ---------------------------------------------- #

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
        self.space_width = self.characters['A'].get_width()

    def render(self, surf: pygame.Surface, text: str, loc: (int, int)) -> None:
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing


# Init ------------------------------------------------------- #

font = Font()

# ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']

# Loop ------------------------------------------------------- #
while True:

    # Background --------------------------------------------- #
    screen.fill((0, 0, 0))

    font.render(screen, 'HELLO WORD', (20, 20))
    # screen.blit(spritesheet.parse_sprite(''))


    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)
