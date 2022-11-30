from settings import VERTICAL_TILE_NUMBER, TILE_SIZE, SCREEN_WIDTH
import pygame
from tiles import StaticTile, AnimatedTile
from support import import_folder
from random import choice, randint

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top_2.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom_2.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle_2.png').convert()
        self.horizon = horizon

        self.top = pygame.transform.scale(self.top, (SCREEN_WIDTH, TILE_SIZE))
        self.bottom = pygame.transform.scale(self.bottom, (SCREEN_WIDTH, TILE_SIZE))
        self.middle = pygame.transform.scale(self.middle, (SCREEN_WIDTH, TILE_SIZE))
    
    def draw(self, surface):
        for row in range(VERTICAL_TILE_NUMBER):
            y = row * TILE_SIZE
            if row < self.horizon:
                surface.blit(self.top, (0,y))
            elif row == self.horizon:
                surface.blit(self.middle, (0,y))
            else:
                surface.blit(self.bottom, (0,y))

class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surf_list = import_folder('../graphics/decoration/clouds')
        min_x = -SCREEN_WIDTH
        max_x = level_width + SCREEN_WIDTH
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)
        
    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)

class Lava:
    def __init__(self, top, level_width):
        lava_start = -SCREEN_WIDTH
        lava_tile_width = 192
        tile_x_amount = int((level_width + SCREEN_WIDTH * 2) / lava_tile_width)
        self.lava_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * lava_tile_width + lava_start
            y = top
            sprite = AnimatedTile(192, x, y, '../graphics/decoration/lava')
            self.lava_sprites.add(sprite)
    def draw(self, surface, shift):
        self.lava_sprites.update(shift)
        self.lava_sprites.draw(surface)