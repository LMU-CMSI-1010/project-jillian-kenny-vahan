import pygame
from settings import *
from timer import Timer
import sys
class StartMenu:
    def __init__(self, toggle_menu):
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/FutilePro.ttf', 30)
        self.bg = pygame.image.load('../graphics/background/background.png').convert_alpha()
        self.width = 400
        self.space = 10
        self.padding = 8
        self.options = ['Start', 'About', 'Quit']
        self.setup()
        self.index = 0
        self.timer = Timer
        
    def setup(self):
        self.text_surfs = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()
            if keys[pygame.K_RETURN]:
                self.timer.activate()
                current_item = self.options[self.index]
                if current_item == "Start":
                    self.toggle_menu()
                else:
                    sys.exit()
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surf, top, selected):
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)

    def update(self):
        self.input()
        self.display_surface.blit(self.bg, (0,0))
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            self.show_entry(text_surf, top, self.index == text_index)

pygame.init()

screen = pygame.display.set_mode((800, 800))
GAME_FONT = pygame.freetype.Font("../font/FutilePro.ttf", 50)
running =  True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,100))
    GAME_FONT.render_to(screen, (40, 350), "WELCOME TO MARIO BROS 1!", (200, 0, 0))
    pygame.display.flip()
pygame.quit
