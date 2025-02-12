import pygame
from src.helpers import (circular_path, sine_wave_path, diagonal_path, down_and_oscillate_path,  s_shape_path,
                         diagonal_and_oscillate_path,)
from string import ascii_letters, digits

pygame.init()
FONT10 = pygame.font.Font('assets/font/visitorTT1BRK.ttf', 10)
FONT20 = pygame.font.Font('assets/font/visitor1.ttf', 20)

TITLE = 'Space Resistance'
VERSION = '1.5'

WIDTH, HEIGHT = 216, 250
SCALE = 4

OBJECT_SPEEDS = {
    'player': 120,
    'shot': 200,
    'boss': 40,
    'scroll': 30
}

COLORS = {
    'RED': [248, 0, 0],
    'YELLOW': [247, 201, 34],
    'WHITE': [255, 255, 255],
    'BLACK': [0, 0, 0],
    'GREY': [4, 4, 4],
    'GREEN': [0, 250, 0],
    'INDIGO': [80, 33, 173],
    'GOLD': [235, 147, 23]
}
# Updated ENEMY_WAVES structure to include last_spawn_time
ENEMY_WAVES = {
    0: {
        (100, 210): [
            {'type': 'small_1',
             'count': 8,
             'delay': 350,
             'speed':90,
             'rotate': True,
             'path': circular_path(WIDTH, HEIGHT, 'left')}
        ],
        (400, 460): [
            {'type': 'small_1',
             'count': 4,
             'delay': 500,
             'speed': 90,
             'rotate': True,
             'path': sine_wave_path(WIDTH, HEIGHT)}
        ],
        (550, 660): [
            {'type': 'small_2',
             'count': 6,
             'delay': 500,
             'speed': 90,
             'rotate': True,
             'path': diagonal_path(WIDTH, HEIGHT, 'left')}
            ],

        (700, 810): [
            {'type': 'small_2',
             'count': 6,
             'delay': 500,
             'speed': 90,
             'rotate': True,
             'path': diagonal_path(WIDTH, HEIGHT, 'right')},
        ],

        (700, 810): [
            {'type': 'medium',
             'count': 1,
             'delay': 500,
             'speed': 30,
             'rotate': False,
             'path': down_and_oscillate_path(WIDTH, HEIGHT)},
        ],
    }
}

ENEMY_DATA = {
    'small_1': {
        'frames': 'assets/img/enemy/small_1/',
        'energy': 10,
        'bump_power': 20,
        'shot_score': 6,
        'kill_score': 12,
        'can_shoot': True
    },
    'small_2': {
        'frames': 'assets/img/enemy/small_2/',
        'energy': 10,
        'bump_power': 20,
        'shot_score': 6,
        'kill_score': 12,
        'can_shoot': False    
    },
    'medium': {
        'frames': 'assets/img/enemy/medium/',
        'energy': 20,
        'bump_power': 40,
        'shot_score': 12,
        'kill_score': 24,
        'can_shoot': True
    },
    'large': {
        'frames': 'assets/img/enemy/large/',
        'energy': 30,
        'bump_power': 60,
        'shot_score': 24,
        'kill_score': 48,
        'can_shoot': True
    },
    'boss': {
        'frames': 'assets/img/boss/',
        'energy': 300,
        'bump_power': 60,
        'shot_score': 48,
        'kill_score': 5000,
        'can_shoot': True
    }
}

SOUND_EFFECTS = {
    'player_shot': {
        'channel': 5,
        'sound': pygame.mixer.Sound('assets/msx/fx/player_shot.ogg'),
        'vol': 0.6
    },
    'explosion': {
        'channel': 6,
        'sound': pygame.mixer.Sound('assets/msx/fx/explosion_2.ogg'),
        'vol': 1
    },
    'lost_life': {
        'channel': 7,
        'sound': pygame.mixer.Sound('assets/msx/fx/lost_life.ogg'),
        'vol': 1
    },
    'power_up': {
        'channel': 8,
        'sound': pygame.mixer.Sound('assets/msx/fx/power_up.ogg'),
        'vol': 1
    }
}

MUSIC_TRACKS = {
    'welcome_screen_music': {
        'channel': 0,
        'sound': pygame.mixer.Sound('assets/msx/music/lotus2_modbootup.mod'),
        'vol': 0.5
    },
    'levels_1_3_music': {
        'channel': 1,
        'sound': pygame.mixer.Sound('assets/msx/music/C64_Turrican_2.ogg'),
        'vol': 0.5
    },
    'level_4': {
        'channel': 2,
        'sound': pygame.mixer.Sound('assets/msx/music/C64_Turrican_2_boss.ogg'),
        'vol': 0.5
    },
    'game_over_screen': {
        'channel': 3,
        'sound': pygame.mixer.Sound('assets/msx/music/Congrats.ogg'),
        'vol': 0.7
    },
    'congrats_screen': {
        'channel': 4,
        'sound': pygame.mixer.Sound('assets/msx/music/lotus2_modbootup.mod'),
        'vol': 1
    }
}

ALLOWED_CHARACTERS = list(ascii_letters + digits)
