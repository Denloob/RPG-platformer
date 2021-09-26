import pygame
import json


class Parse:
    def __init__(self, filename: str):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def all_filenames(self) -> list:
        return list(self.data['frames'].keys())

    def parse_by_name(self, startswith: str, replacewith: str = None, extension: str = 'png') -> dict:
        if replacewith is None:
            replacewith = f"{startswith}_"

        return {filename.replace(f'{replacewith}', '').replace(f'.{extension}', ''): self.parse_sprite(filename)
                for filename in self.all_filenames() if filename.startswith(startswith)}

    def parse_sprite(self, name: str) -> pygame.Surface:
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)

        return image

    def parse_entity(self, name: str = "zombie", mode: str = "idle",
                     frame: int = 0, extension: str = 'png') -> pygame.Surface:
        return self.parse_sprite(name=f"{name}_{mode}_anim_f{frame}.{extension}")

    def parse_animation(self, name: str = "zombie", mode: str = "idle",
                        anim_start: int = 0, anim_end: int = 3, extension: str = 'png') -> list:
        return [self.parse_sprite(name=f"{name}_{mode}_anim_f{frame}.{extension}")
                for frame in range(anim_start, anim_end + 1)]
