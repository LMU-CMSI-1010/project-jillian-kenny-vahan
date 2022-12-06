import pygame
from support import import_csv_layout, import_cut_graphics
from settings import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from tiles import StaticTile, Tile, Coin
from player import Player
from decoration import Sky, Clouds, Water
from game_data import levels
from enemy import Enemy
from particles import ParticleEffect
class Level:
    def __init__(self, current_level, surface, create_level, change_lives, change_status, max_level, change_coins):
        # Basic Setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        self.create_level = create_level
        self.max_level = max_level
        self.player_on_ground = False
        self.current_level = current_level
        self.change_status = change_status
        self.change_lives = change_lives
        self.change_coins = change_coins
        # Player
        level_data = levels[self.current_level]
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Particles 
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        # Terrain
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # Decorations
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * TILE_SIZE
        self.clouds = Clouds(400, level_width, 30)
        self.water = Water(SCREEN_HEIGHT - 20, level_width)
        self.enemies_exist = True if 'enemies' in level_data else False
        
        # Enemies
        self.explosion_sprites = pygame.sprite.Group()
        if self.enemies_exist:
            enemy_layout = import_csv_layout(level_data['enemies'])
            self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
            constraints_layout = import_csv_layout(level_data['constraint'])
            self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraint')
        
        # Coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')
        self.coin_sound = pygame.mixer.Sound('../audio/coin.wav')


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                    
                    if type == 'coins':
                        sprite = Coin(TILE_SIZE, x, y, '../graphics/coins/animation')
                    if type == 'enemies':
                        sprite = Enemy(TILE_SIZE, x, y-10)
                    if type == 'constraint':
                        sprite = Tile(TILE_SIZE, x, y)
                    sprite_group.add(sprite)
        return sprite_group
    
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    trophy_surface = pygame.image.load('../graphics/character/trophy.png').convert_alpha()
                    sprite = StaticTile(TILE_SIZE, x, y, trophy_surface)
                    self.goal.add(sprite)

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraints_sprites,False):
                enemy.reverse()

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center,'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.change_lives()
                    self.create_level(self.max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
            
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
    
    def check_death(self):
        if self.player.sprite.rect.top > SCREEN_HEIGHT:
            self.change_lives()
            self.create_level(self.max_level)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
            self.dust_sprite.add(fall_dust_particle)


    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.change_status('winscreen')
    
    def run(self):
        #print('Level Running')
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        if self.enemies_exist:
            self.enemy_sprites.update(self.world_shift)
            self.constraints_sprites.update(self.world_shift)
            self.enemy_collision_reverse()
            self.enemy_sprites.draw(self.display_surface)
            self.check_enemy_collisions()
            self.explosion_sprites.update(self.world_shift)
            self.explosion_sprites.draw(self.display_surface)
        self.player.update()
        self.horizontal_movement_collision()
        self.check_coin_collisions()
        self.get_player_on_ground()
        self.create_landing_dust()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.check_death()
        self.check_win()
        self.water.draw(self.display_surface, self.world_shift)