import pygame
import json


class Parse:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def all_filenames(self):
        return list(self.data['frames'].keys())

    def parse_by_name(self, startswith, replacewith=None, extension='png'):
        if replacewith is not None:
            return {filename.replace(f'{replacewith}', '').replace(f'.{extension}', ''): self.parse_sprite(filename)
                    for filename in self.all_filenames() if filename.startswith(startswith)}
        else:
            return self.parse_by_name(startswith=startswith, replacewith=f"{startswith}_", extension=extension)

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)

        return image

    def parse_entity(self, name="zombie", mode="idle", frame='0', extension='png'):
        return self.parse_sprite(name=f"{name}_{mode}_anim_f{frame}.{extension}")

    def parse_animation(self, name="zombie", mode="idle", anim_start=0, anim_end=3, extension='png'):
        return [self.parse_sprite(name=f"{name}_{mode}_anim_f{frame}.{extension}")
                for frame in range(anim_start, anim_end + 1)]
