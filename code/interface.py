import pygame

class Interface:
    def __init__(self, surface):
        self.display_surface = surface
        self.hearts_start_position = [10, 19]
        self.heart_size = 64
        self.heart = pygame.image.load('../graphics/interface/HeatFull.png').convert_alpha()

    def show_hearts(self, amount):
        heart_pos = self.hearts_start_position
        for i in range(amount):
            heart_rect = self.heart.get_rect(topleft = heart_pos)
            self.display_surface.blit(self.heart, heart_rect)
            heart_pos[0] = self.heart_size * i + 15 
