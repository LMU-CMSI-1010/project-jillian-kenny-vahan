import pygame, sys
from settings import *
from menus import StartMenu, WinMenu
from level import Level
class Game:
    def __init__(self):
        self.start_menu = StartMenu(self.toggle_start_menu)
        self.win_menu = WinMenu()
        self.status = 'mainmenu'
        self.level = None
    def run(self):
        if self.status == 'mainmenu':
            self.start_menu.update()
        elif self.status == 'winmenu':
            self.win_menu.update()
        else:   
            if self.level:
                self.level.run()
            else:
                self.create_level(1)

    def toggle_start_menu(self):
        self.status = 'level'

    def create_level(self, current_level):
        self.level = Level(current_level,screen, self.change_status)
        self.status = 'level'

    def change_status(self, status):
        self.status = status
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Final Project')
clock = pygame.time.Clock()
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('grey')
    game.run()
    pygame.display.update()
    clock.tick(60)

# if __name__ == '__main__':
#     game = Game()
#     game.run()
