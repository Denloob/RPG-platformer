from assets.data.spritesheet_parser import Parse  # sprite sheet parser which can parse png files with data in json

spritesheet = Parse('assets/textures/main.png')  # create an instance of the Parse class
images = {
    'character_images': {
        'knight_f': {
            'run': spritesheet.parse_animation('knight_f', 'run'),
            'idle': spritesheet.parse_animation('knight_f', 'idle'),
            'hit': spritesheet.parse_entity(name='knight_f', mode='hit', frame=0)},
        'knight_m': {
            'run': spritesheet.parse_animation('knight_m', 'run'),
            'idle': spritesheet.parse_animation('knight_m', 'idle'),
            'hit': spritesheet.parse_entity(name='knight_m', mode='hit', frame=0)},
        'wizzard_f': {
            'run': spritesheet.parse_animation('wizzard_f', 'run'),
            'idle': spritesheet.parse_animation('wizzard_f', 'idle'),
            'hit': spritesheet.parse_entity(name='wizzard_f', mode='hit', frame=0)},
        'wizzard_m': {
            'run': spritesheet.parse_animation('wizzard_m', 'run'),
            'idle': spritesheet.parse_animation('wizzard_m', 'idle'),
            'hit': spritesheet.parse_entity(name='wizzard_m', mode='hit', frame=0)},
    },  # creating a dictionary with animations of the main characters
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
