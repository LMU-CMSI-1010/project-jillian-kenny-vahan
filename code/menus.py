import pygame
from settings import *
from timer import Timer
import sys
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
class StartMenu:
    def __init__(self, toggle_menu, set_level):
        self.toggle_menu = toggle_menu
        self.set_level = set_level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/FutilePro.ttf', 30)
        self.title = pygame.font.Font('../font/FutilePro.ttf', 90)
        self.bg = pygame.image.load('../graphics/background/back.png').convert_alpha()
        self.width = 400
        self.space = 10
        self.padding = 8
        self.options = ['Start', 'About', 'Quit']
        self.setup()
        self.index = 0
        self.timer = Timer(200)

    def setup(self):
        self.set_level(1)
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
                    self.set_level(1)
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
        text = self.title.render("Path to Glory", True, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        self.display_surface.blit(text, text_rect)
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            self.show_entry(text_surf, top, self.index == text_index)

class WinScreen:
    def __init__(self, toggle_menu):
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../font/FutilePro.ttf', 30)
        self.bg = pygame.image.load('../graphics/background/back.png').convert_alpha()
        self.width = 400
        self.space = 10
        self.padding = 8
        self.options = ['Continue', 'Quit']
        self.setup()
        self.index = 0
        self.timer = Timer(200)

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
                if current_item == "Continue":
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
        text = self.font.render("You won!", True, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        self.display_surface.blit(text, text_rect)
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            self.show_entry(text_surf, top, self.index == text_index)


class GameOver:
    def __init__(self, change_status, set_level):
        self.display_surface = pygame.display.get_surface()
        self.change_status = change_status
        self.set_level = set_level
        self.font = pygame.font.Font('../font/FutilePro.ttf', 50)
    
    def setup(self):
        self.timer = Timer(3000, self.back_to_menu)
        self.timer.activate()

    def back_to_menu(self):
        self.set_level(1)
        self.change_status('mainmenu')
    def run(self):
        text = self.font.render("Game over!", True, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.display_surface.blit(text, text_rect)
        self.timer.update()

class GameFinished:
    def __init__(self, change_status, set_level):
        self.display_surface = pygame.display.get_surface()
        self.change_status = change_status
        self.set_level = set_level
        self.bg = pygame.image.load('../graphics/background/back.png').convert_alpha()
        self.font = pygame.font.Font('../font/FutilePro.ttf', 60)
    
    def setup(self):
        self.timer = Timer(3000, self.back_to_menu)
        self.timer.activate()

    def back_to_menu(self):
        self.set_level(1)
        self.change_status('mainmenu')

    def run(self):
        self.display_surface.blit(self.bg, (0,0))
        text = self.font.render("Victory!", True, 'white')
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.display_surface.blit(text, text_rect)
        self.timer.update()

