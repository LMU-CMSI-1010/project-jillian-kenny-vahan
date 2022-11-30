import pygame, sys
from settings import *
from menus import StartMenu
from level import Level
from interface import Interface
class Game:
    def __init__(self):
        self.start_menu = StartMenu(self.toggle_start_menu)
        self.status = 'mainmenu'
        self.level = None
        self.lives = 3
        self.interface = Interface(screen)
        self.max_level = 1
    def run(self):
        if self.status == 'mainmenu':
            self.start_menu.update()
        elif self.status == 'level':   
            if self.level:
                self.level.run()
                self.interface.show_hearts(self.lives)
            else:
                self.create_level(1)
    

    def change_lives(self):
        self.lives -= 1
        if self.lives <= 0:
            self.status = 'mainmenu' 
            print('gameover')

    def toggle_start_menu(self):
        self.status = 'level'

    def create_level(self, current_level):
        self.level = Level(current_level,screen, self.create_level, self.change_lives)
        self.status = 'level'


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
