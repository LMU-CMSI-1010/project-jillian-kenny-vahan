import pygame, sys
from settings import *
from menus import StartMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_menu = StartMenu(self.toggle_start_menu)
        self.start_menu_active = True
        self.bg = pygame.image.load('../graphics/background/background.png').convert_alpha()
        pygame.display.set_caption('Final Project')
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000
            if self.start_menu_active:
                pygame.display.get_surface().blit(self.bg, (0, 0))
                self.start_menu.update()
            pygame.display.update()

    def toggle_start_menu(self):
        self.start_menu_active = not self.start_menu_active

if __name__ == '__main__':
    game = Game()
    game.run()
