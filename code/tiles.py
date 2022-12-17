import pygame
from support import import_folder

# Parent class for all the tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self, shift):
        self.rect.x += shift

# Static tile without any animation
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

# Tile with animation
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.path = path
        self.image = self.frames[self.frame_index]
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        if 'enemy' in self.path:
            self.image = pygame.transform.scale(self.frames[int(self.frame_index)], (64, 64))
        else:
            self.image = self.frames[int(self.frame_index)]
    def update(self, shift):
        self.animate()
        self.rect.x += shift

# Coin tile
class Coin(AnimatedTile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = 1
