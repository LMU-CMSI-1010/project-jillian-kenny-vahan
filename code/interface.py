import pygame
# Class for rendering User Interface to the screen
class Interface:
    def __init__(self, surface):
        # Basic setup
        self.display_surface = surface
        self.hearts_start_position_y = 19
        self.heart_size = 40
        self.heart = pygame.transform.scale(pygame.image.load('../graphics/interface/heart.png').convert_alpha(), (self.heart_size, self.heart_size))
        self.coin = pygame.image.load('../graphics/interface/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (20,65))
        self.font = pygame.font.Font('../font/FutilePro.ttf',30)
    # Drawing the hearts according to the number of lives in main file
    def show_hearts(self, amount):
        for i in range(amount):
            heart_rect = self.heart.get_rect(topleft = [(self.heart_size * 1.2 * i) + 15, self.hearts_start_position_y])
            self.display_surface.blit(self.heart, heart_rect)

    # Drawing the coins according to the number of coins in main file
    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)