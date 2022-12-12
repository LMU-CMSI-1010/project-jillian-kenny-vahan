import pygame, sys
from settings import *
from menus import StartMenu, GameOver, WinScreen, GameFinished
from level import Level
from interface import Interface

'''
    TODO:
    1. Bug: reset levels and lives when game is won or is over (done)
    2. Add enemies (done)
    3. Add more levels (ongoing)
    4. Add coins (done)
    5. Bug: fix winscreen in the end (done)
'''
# The main class of the game
class Game:
    def __init__(self):
        # Basic setup 
        self.start_menu = StartMenu(self.toggle_start_menu, self.set_level)
        self.winscreen = WinScreen(self.toggle_win_screen)
        self.gameover = GameOver(self.change_status, self.set_level)
        self.finished = GameFinished(self.change_status, self.set_level)
        self.status = 'mainmenu'
        self.level = None
        self.lives = 3
        self.coins = 0
        self.interface = Interface(screen)
        self.max_level = 1
        self.end_level = 2
    def run(self):
        # Checking the status of the game to see what screen to render
        if self.status == 'mainmenu':
            self.start_menu.update()
        elif self.status == 'level':   
            if self.level:
                self.level.run()
                self.interface.show_hearts(self.lives)
                self.interface.show_coins(self.coins)
                self.check_game_over()
            else:
                self.create_level(self.max_level)
        elif self.status == 'winscreen':
            if self.max_level >= self.end_level:
                self.level = None
                self.set_level(1)
                self.change_status('finished')
                self.lives = 3         
                self.coins = 0   
                self.finished.setup()
            else:
                self.winscreen.update()
        elif self.status == 'finished':
            self.finished.run()
        else:
            self.gameover.run()


    # Taking one life from the player when the game is lost
    def change_lives(self):
        self.lives -= 1

    # Adding coins to the player when colliding with them
    def change_coins(self,amount):
        self.coins += amount
        if self.coins >= 5:
            self.lives += 1 # Adding one more life to the player when 5 coins collected
            self.coins -= 5

    # This function is called when the start button is triggered in start menu
    def toggle_start_menu(self):
        self.status = 'level'  
    # This function is called when the trophy is collected in the game
    def toggle_win_screen(self):
        self.max_level += 1
        
        self.create_level(self.max_level)
        self.status = 'level'

    # Creating the level
    def create_level(self, current_level):
        self.level = Level(current_level,screen, self.create_level, self.change_lives, self.change_status, self.max_level, self.change_coins)
        self.status = 'level'
    # Checking game over
    def check_game_over(self):
        if self.lives <= 0:
            self.status = 'gameover'
            self.lives = 3
            self.coins = 0
            self.gameover.setup()
    # Function to change the status of the game from different files
    def change_status(self, status):
        self.status = status
    # Function to change the level of the game from different files
    def set_level(self, level):
        self.level = None
        self.max_level = level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Path to Glory')
clock = pygame.time.Clock()
game = Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    game.run()
    pygame.display.update()
    clock.tick(60)

# if __name__ == '__main__':
#     game = Game()
#     game.run()
