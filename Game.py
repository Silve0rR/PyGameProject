import pygame
import os
import random
from Levels import get_level

keys_sl = {'run': [pygame.K_a, pygame.K_d], 'jump': pygame.K_SPACE, 'attack': pygame.K_k, 'pay': pygame.K_e}
language = {'RUSSIA': ['Счёт', 'Зелье', 'Цена', 'Купить'], 'ENGLISH': ['Account', 'Potion', 'Price', 'Pay']}

WIDTH, HEIGHT = 1270, 720
FPS = 60
pygame.display.set_caption("Test Game")
pygame.init()
pygame.mixer.init()


music_pleer = ['Музыка 1', 'Музыка 2', 'Музыка 3', 'Музыка 4']
MUSICSOUND = 0

pygame.mixer.music.load('{}.mp3'.format(music_pleer[MUSICSOUND]))
ACTUAL_SOUND = music_pleer[MUSICSOUND]
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

SOUND_PAUSE = False

RUSSIA = True
ENGLISH = False

ARROWS = False
WASD = True

HIT_J = True
HIT_K = False
HIT_L = False


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg = load_image('background.jpg')
        self.coins, self.account, self.time = 0, 0, 0
        self.wave, self.timers = 1, [0, 0]
        self.enemy, self.break_game = 5 + self.wave, [False, 0]
        self.running, self.pause, self.options, self.mini_menu = True, False, False, False
        self.mous_click, self.exit_command = False, ''

    def game_run(self):
        while self.running:
            pygame.time.Clock().tick(FPS)
            self.events()
            self.update()
            self.visualization()
            if player.hp >= 0 and not self.pause:
                self.time += 1
            elif player.hp <= 0 or self.exit_command != '':
                if self.timers[1] < 120 and self.exit_command == '':
                    self.timers[1] += 1
                else:
                    self.timers, self.coins, self.time, self.enemy = [0, 0], 0, 0, 6
                    self.break_game, self.account, self.wave = [False, 0], 0, 1
                    player.hp, self.pause = 1000, False
                    for en in character_sprites:
                        if en != player:
                            en.alive = False
                            en.timers = [0, 0, 0, 0, 0]
                            en.rect.center = en.respawn
                    if self.exit_command == 'menu' or self.timers[1] == 120:
                        self.exit_command = ''
                        break
                    elif self.exit_command == 'game':
                        self.exit_command = ''
                        self.running = False
            pygame.display.flip()
            alive = 0
            for en in character_sprites:
                if en != player and en.alive:
                    alive += 1
            if self.enemy == 0 and alive == 0:
                self.break_game = [True, 420]
                ps.invisibility = False
                self.wave += 1
                self.enemy = 5 + self.wave
            if self.break_game[1] != 0:
                self.break_game[1] -= 1
            else:
                self.break_game[0] = False
                ps.invisibility = True
        with open('Рекорд.txt', 'r') as f:
            n = f.read()
            n = n.split()
            time = str((int(n[1]) // 60) // 60) + ':'
            if (self.time // 60) % 60 < 10:
                time += '0' + str((self.time // 60) % 60)
            else:
                time += str((self.time // 60) % 60)
            if self.account > int(n[0]):
                with open('Рекорд.txt', 'w') as file:
                    file.write(str(self.account) + ' ' + time)

    def events(self):  # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.pause:
                    if 3 < event.pos[0] < 53 and 10 < event.pos[1] < 60:
                        self.pause, self.options = True, True
                    if 57 < event.pos[0] < 107 and 10 < event.pos[1] < 60:
                        self.pause, self.mini_menu = True, True
                self.mous_click = True
            else:
                self.mous_click = False

    def update(self):  # Обнавление
        cur.get_coord(pygame.mouse.get_pos())
        if not self.pause:
            character_sprites.update()
            invisible_sprites.update()
            coins_sprites.update()
            if player.hp <= 0:
                game_over_sprite.update()

    def visualization(self):  # Визуализация
        self.screen.blit(self.bg, [0, 0])
        background_sprites.draw(self.screen)
        invisible_sprites.draw(self.screen)
        coins_sprites.draw(self.screen)
        character_sprites.draw(self.screen)
        platform_sprites.draw(self.screen)
        if player.hp > 0:
            pygame.draw.rect(self.screen, 'red', [127, 15, player.hp // 2, 35], 0)
        foreground_sprites.draw(self.screen)
        self.screen.blit(pygame.font.Font(None, 30).render(str(self.coins), True, (255, 255, 255)), (45, 83))
        if RUSSIA:
            lang = language['RUSSIA']
        else:
            lang = language['ENGLISH']
        self.screen.blit(pygame.font.Font(None, 35).render(lang[0] + ': ' + str(self.account), True, (255, 255, 255)),
                         (WIDTH // 2 + 100, 20))
        time = str((self.time // 60) // 60) + ':'
        if (self.time // 60) % 60 < 10:
            time += '0' + str((self.time // 60) % 60)
        else:
            time += str((self.time // 60) % 60)
        self.screen.blit(pygame.font.Font(None, 35).render(time, True, (255, 255, 255)), (WIDTH // 2 + 500, 20))
        if not psw.invisibility:
            self.screen.blit(pygame.font.Font(None, 25).render(lang[1], True,
                                                               (0, 0, 0)), (psw.rect.x + 5, psw.rect.y + 5))
            self.screen.blit(pygame.font.Font(None, 20).render('+' + str(ps.restoration) + 'HP', True,
                                                               (0, 0, 0)), (psw.rect.x + 5, psw.rect.y + 25))
            self.screen.blit(pygame.font.Font(None, 20).render(lang[2] + ': ' + str(ps.prise), True,
                                                               (0, 0, 0)), (psw.rect.x + 5, psw.rect.y + 50))
        if not psw_pay.invisibility:
            self.screen.blit(pygame.font.Font(None, 15).render(lang[3], True, (0, 0, 0)),
                             (psw_pay.rect.center[0] - 9, psw_pay.rect.center[1] - 4))

        # visual_board.render(self.screen)
        global hp_enemy
        for coord in hp_enemy:
            pygame.draw.rect(game.screen, 'red', coord, 0)
        hp_enemy = []
        if player.hp <= 0:
            game_over_sprite.draw(self.screen)
        if self.pause:
            if self.options:
                self.options = options_menu(*pygame.mouse.get_pos(), self.mous_click)
            elif self.mini_menu:
                all_sprites_mini_menu.draw(self.screen)
                self.mini_menu = mini_menu(*pygame.mouse.get_pos(), self.mous_click)
            else:
                self.pause = False
        options_animation(self.options)
        all_Background_options.draw(game.screen)
        if pygame.mouse.get_pos()[0] < 500 and pygame.mouse.get_pos()[1] < 150:
            all_cur.draw(self.screen)
        elif self.pause:
            all_cur.draw(self.screen)

    def save_game(self):
        save_values = [str(self.account), str(self.time), str(self.coins), str(self.wave),
                       str(player.hp), str(self.enemy), str(ps.uses[0])]
        with open('save.txt', 'w') as save_file:
            save_file.write('&'.join(save_values))


class VisualBoard:
    def __init__(self):
        self.width, self.height = WIDTH // 100 + 1, HEIGHT // 100
        self.board = [[0] * self.width for _ in range(self.height)]

    def render(self, screen):  # в игре не учавствует(служебная функция)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white', (x * 100, y * 100, 100, 100), 1)

    def set_values(self, coord_cell, value):
        self.board[coord_cell[1]][coord_cell[0]] = value

    def get_coord_platform(self, coord_cell):
        if self.board[coord_cell[1]][coord_cell[0]] == 1:
            return [100 * coord_cell[0] + 50, 100 * coord_cell[1] + 70]

    def get_coord(self, coord):
        return [coord[0] // 100, coord[1] // 100]


class Character(pygame.sprite.Sprite):
    def __init__(self, im_stand, im_size_run, im_size_attack, im_size_rip):
        super().__init__(character_sprites)
        self.image_stand = load_image(im_stand, (35, 90, 115))
        self.image = self.image_stand
        self.frames_sl, self.cur_frame = load_frames_sl((im_size_run, im_size_attack, im_size_rip))
        self.hp, self.rect = 1, self.image.get_rect()
        self.jump, self.is_flight, self.fall, self.timers = [False, -25], False, 5, [0, 0, 0]
        self.attack, self.alive = [False, False], False

    def update(self):
        self.char_jump()
        y = self.rect.y + self.fall  # Падение
        for j in range(self.fall):
            self.rect.y += 1
            self.collision()
            if self.rect.bottom > HEIGHT - 23:
                self.rect.bottom = HEIGHT - 23
        if y == self.rect.y and not self.jump[0]:
            self.fall += 1
            self.is_flight = True
        else:
            if self.fall > 10:
                self.hp -= self.fall - 10
            self.fall = 5
            self.is_flight = False
        if self.jump[0]:
            self.is_flight = True
        col_char = pygame.sprite.spritecollide(self, character_sprites, False)
        for char in col_char:
            if self != char and self != player and player != char and self.alive:
                if self.rect.center[0] + 5 >= char.rect.center[0] >= self.rect.center[0] and\
                        self.rect.y == char.rect.y:
                    self.rect.x -= 3
                    char.rect.x += 3
                elif self.rect.center[0] - 5 <= char.rect.center[0] <= self.rect.center[0] and\
                        self.rect.y == char.rect.y:
                    self.rect.x -= 3
                    char.rect.x += 3

    def collision(self):
        platforms = pygame.sprite.spritecollide(self, platform_sprites, False)
        for pl in platforms:
            if pl.rect.bottom > self.rect.bottom > pl.rect.top > self.rect.top:
                self.rect.bottom = pl.rect.top
                return False
            elif pl.rect.top < self.rect.top < pl.rect.bottom < self.rect.bottom:
                self.rect.top = pl.rect.bottom
                return False
            elif self.rect.top <= pl.rect.top or self.rect.bottom >= pl.rect.bottom:
                if self.rect.right > pl.rect.left > self.rect.left:
                    self.rect.right = pl.rect.left
                elif self.rect.left < pl.rect.right < self.rect.right:
                    self.rect.left = pl.rect.right
                return True
            else:
                return True
        return True

    def char_jump(self):
        if self.jump[0]:
            if self.jump[1] == 25:
                self.jump = [False, -25]
            else:
                for i in range(abs(self.jump[1])):
                    if self.jump[1] < 0:
                        self.rect.y -= 1
                    else:
                        self.rect.y += 1
                    if not self.collision():
                        self.jump[1] = 24
                        break
                self.jump[1] += 1

    def animation(self, key, click_attack=True):
        if key[:key.index('_')] == 'run':
            if self.timers[0] == 3:
                self.cur_frame[0] = (self.cur_frame[0] + 1) % len(self.frames_sl[key])
                self.image = self.frames_sl[key][self.cur_frame[0]]
                self.set_rect()
            self.timers[0] += 1
            if self.timers[0] == 4:
                self.timers[0] = 0
        elif key[:key.index('_')] == 'attack':
            if self.timers[1] == 4:
                if not click_attack:
                    self.cur_frame[1] = -1
                else:
                    self.cur_frame[1] = (self.cur_frame[1] + 1) % len(self.frames_sl[key])
                self.image = self.frames_sl[key][self.cur_frame[1]]
                self.set_rect()
            self.timers[1] += 1
            if self.timers[1] == 5:
                self.timers[1] = 0
        elif key[:key.index('_')] == 'rip':
            if self.timers[2] == 9:
                if self.cur_frame[2] != 5:
                    self.cur_frame[2] = (self.cur_frame[2] + 1) % len(self.frames_sl[key])
                self.image = self.frames_sl[key][self.cur_frame[2]]
                self.set_rect()
            if self.cur_frame[2] != 5:
                self.timers[2] += 1
                if self.timers[2] == 10:
                    self.timers[2] = 0

    def set_rect(self):
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


class Player(Character):
    def __init__(self):
        super().__init__('Player.png', ('Player_run.png', (6, 1)), ('Player_attack.png', (4, 3)),
                         ('Player_rip.png', (6, 1)))
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.hp, self.direction = 1000, 'right'

    def update(self):
        if self.hp > 0:
            keys = pygame.key.get_pressed()
            if keys[keys_sl['pay']]:
                if visual_board.get_coord(self.rect.center) == ps.coord_cell and\
                        not ps.invisibility and game.coins >= ps.prise and not ps.uses[1]:
                    self.hp += ps.restoration
                    if self.hp > 1000:
                        self.hp = 1000
                    game.coins -= ps.prise
                    ps.uses[0] += 1
                    ps.uses[1] = True
            if not self.jump[0] and not self.is_flight:
                if keys[pygame.K_SPACE]:
                    self.jump[0] = True
            if not self.jump[0] and not self.is_flight:
                if keys[keys_sl['attack']]:
                    self.attack[0] = True
                if self.attack[0]:
                    self.animation('attack_' + self.direction)
                if self.cur_frame[1] in [3, 8] and not self.attack[1]:
                    global hit_enemy
                    hit_enemy = pygame.sprite.spritecollide(self, character_sprites, False)
                    self.attack[1] = True
                elif self.cur_frame[1] not in [3, 8]:
                    self.attack[1] = False
                if self.cur_frame[1] == 11:
                    self.attack = [False, False, False]
                    self.cur_frame[1] = 0
            if self.attack[0] and self.jump[0]:
                self.attack[0] = False
                self.cur_frame[1] = 0
            if keys[keys_sl['run'][0]] and self.rect.left > 5:
                self.rect.x -= 6
                self.animation('run_left')
                self.direction, self.attack[0], self.cur_frame[1] = 'left', False, 0
            elif keys[keys_sl['run'][1]] and self.rect.right < WIDTH - 5:
                self.rect.x += 6
                self.animation('run_right')
                self.direction, self.attack[0], self.cur_frame[1] = 'right', False, 0
            elif not self.attack[0] and not self.jump[0] and not self.is_flight:
                self.image = self.image_stand
                self.set_rect()
            super().update()
            coins = pygame.sprite.spritecollide(self, coins_sprites, False)
            for coin in coins:
                if self.rect.left < coin.rect.center[0] < self.rect.right and\
                        self.rect.top < coin.rect.center[1] < self.rect.bottom and not coin.is_flight:
                    coins_sprites.remove(coin)
                    game.coins += 1
        else:
            self.animation('rip_' + self.direction)


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(game_over_sprite)
        self.image = load_image('GameOver.png', (35, 90, 115))
        self.rect = self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)


class Enemy(Character):
    def __init__(self):
        super().__init__('Guard.png', ('Guard_run.png', (6, 1)), ('Guard_attack.png', (4, 3)),
                         ('Guard_rip.png', (6, 1)))
        self.hp, self.speed = random.randrange(400, 700, 100), random.randrange(4, 6)
        self.path, self.run = [], [0, 1, False]
        self.respawn = random.choice([[-100, HEIGHT - 50], [WIDTH + 100, HEIGHT - 50]])
        self.timers = [0, 0, 0, 0, 0]
        self.rect.center = self.respawn
        self.time_respawn = random.randrange(120, 600)

    def update(self):
        if self.alive:
            global hit_enemy
            for en in hit_enemy:
                if en == self:
                    self.hp -= random.randrange(100, 150)
                    del hit_enemy[hit_enemy.index(en)]
                    break
            cell_player = visual_board.get_coord(player.rect.center)
            cell_self = visual_board.get_coord(self.rect.center)
            if self.timers[3] == 30:
                self.timers[3] = 0
                self.finding_path_1(visual_board.board, cell_player, cell_self)
            self.timers[3] += 1
            if not self.path and not self.jump[0] and not self.attack[0]:
                if player.rect.right < self.rect.left and self.rect.left > 5:
                    self.rect.x -= self.speed
                    self.animation('run_left')
                elif player.rect.left > self.rect.right and self.rect.right < WIDTH - 5:
                    self.rect.x += self.speed
                    self.animation('run_right')
                elif not self.attack[0]:
                    self.image = self.image_stand
                    self.set_rect()
            elif self.path and not self.attack[0]:
                if self.path[0][0] > cell_self[0] and self.run[0] != self.path[0][0] * 100 + 50 and\
                        self.run[0] != self.path[0][0] * 100 + 30 and self.run[0] != self.path[0][0] * 100 + 80:
                    try:
                        if self.path[1][2] and self.path[1][0] > self.path[0][0]:
                            coord = self.path[0][0] * 100 + 30
                        elif self.path[1][2] and self.path[1][0] < self.path[0][0]:
                            coord = self.path[0][0] * 100 + 80
                        else:
                            coord = self.path[0][0] * 100 + 50
                    except IndexError:
                        coord = self.path[0][0] * 100 + 50
                    self.run = [coord, 1, False]
                    self.run[2] = self.path[0][2]
                elif self.path[0][0] < cell_self[0] and self.run[0] != self.path[0][0] * 100 + 50 and\
                        self.run[0] != self.path[0][0] * 100 + 30 and self.run[0] != self.path[0][0] * 100 + 80:
                    try:
                        if self.path[1][2] and self.path[1][0] > self.path[0][0]:
                            coord = self.path[0][0] * 100 + 30
                        elif self.path[1][2] and self.path[1][0] < self.path[0][0]:
                            coord = self.path[0][0] * 100 + 80
                        else:
                            coord = self.path[0][0] * 100 + 50
                    except IndexError:
                        coord = self.path[0][0] * 100 + 50
                    self.run = [coord, -1, False]
                    self.run[2] = self.path[0][2]
                if self.run[0] != 0:
                    if self.run[2] and not self.jump[0] and not self.is_flight:
                        self.jump[0] = True
                    if self.run[2] and self.jump[1] <= -23:
                        if self.jump[1] == -23:
                            self.run[2] = False
                    else:
                        if self.jump[0]:
                            self.rect.x += 5 * self.run[1]
                        else:
                            self.rect.x += self.speed * self.run[1]
                    if (self.run[1] == 1 and self.run[0] <= self.rect.center[0]) or \
                            (self.run[1] == -1 and self.run[0] >= self.rect.center[0]):
                        self.run[0] = 0
                if self.run[0] == 0 and not self.jump[0]:
                    del self.path[0]
                if self.run[0] != 0:
                    if self.run[1] == -1:
                        self.animation('run_left')
                    else:
                        self.animation('run_right')
                else:
                    self.image = self.image_stand
                    self.set_rect()
            if not self.jump[0] and not self.is_flight and player.hp > 0:
                if self.rect.right > player.rect.center[0] > self.rect.left - 30 and cell_player[1] == cell_self[1]:
                    self.attack[0] = True
                    if self.cur_frame[1] == 7:
                        self.animation('attack_left', random.choice([True, False]))
                    else:
                        self.animation('attack_left')
                elif self.rect.left < player.rect.center[0] < self.rect.right + 30 and cell_player[1] == cell_self[1]:
                    self.attack[0] = True
                    if self.cur_frame[1] == 7:
                        self.animation('attack_right', random.choice([True, False]))
                    else:
                        self.animation('attack_right')
                else:
                    self.attack = [False, False]
                    self.timers[1] = 0
                if self.cur_frame[1] in [3, 8] and self.attack[0] and not self.attack[1]:
                    if self.rect.left - 35 < player.rect.right or self.rect.right + 35 > player.rect.left:
                        player.hp -= random.randrange(10, 25)
                        self.attack[1] = True
                elif self.cur_frame[1] not in [3, 8]:
                    self.attack[1] = False
            elif not self.path:
                self.image = self.image_stand
                self.set_rect()
            super().update()
            hp_enemy.append([self.rect.x, self.rect.y - 15, self.hp // 15, 5])
            if self.hp <= 0:
                self.alive = False
                for _ in range(random.randrange(3, 7)):
                    Coin(*self.rect.center)
                self.timers = [0, 0, 0, 0, 0]
                self.hp = random.randrange(400, 700, 100)
                game.account += random.randrange(10, 30)
                self.time_respawn = random.randrange(120, 600)
                game.enemy -= 1

        else:
            alive = 0
            for en in character_sprites:
                if en != player and en.alive:
                    alive += 1
            if self.timers[4] < 60:
                if player.rect.center[0] > self.rect.center[0]:
                    self.animation('rip_right')
                else:
                    self.animation('rip_left')
                super().update()
            if self.timers[4] == self.time_respawn and game.enemy - alive > 0:
                self.cur_frame[2] = 0
                self.rect.center = self.respawn
                if self.respawn[0] > 0:
                    self.path.append([len(visual_board.board[0]) - 1, 6, False])
                else:
                    self.path.append([0, 6, False])
                self.respawn = random.choice([[-100, HEIGHT - 50], [WIDTH + 100, HEIGHT - 50]])
                self.alive = True
            elif not game.break_game[0] and game.enemy - alive > 0:
                self.timers[4] += 1

    def finding_path_1(self, board, cell_player, cell_self):
        if not self.is_flight and not self.jump[0] and not player.is_flight and not player.jump[0]:
            board2 = []
            for i in range(len(board)):
                board2.append([])
                for j in range(len(board[i])):
                    if board[i][j] == 0:
                        board2[i].append([[-1, '']])
                    elif board[i][j] == 1:
                        board2[i].append([[0, '']])
            board2[-1] = [[[0, '']] for _ in range(len(board[0]))]
            board2[cell_self[1]][cell_self[0]].append([1, '1'])
            board = self.finding_path_2(board2, cell_player, cell_self[0], cell_self[1], 2)
            min_wave = [1000, 0]
            for i in range(len(board[cell_player[1]][cell_player[0]])):
                if board[cell_player[1]][cell_player[0]][i][0] != 0 and \
                        board[cell_player[1]][cell_player[0]][i][0] < min_wave[0]:
                    min_wave = [board[cell_player[1]][cell_player[0]][i][0], i]
            self.save_path(board, cell_player, min_wave[1])

    def finding_path_2(self, board, cell_player, x, y, wave):
        option = '1'
        if wave <= 10:
            try:
                if y == cell_player[1] and x == cell_player[0]:
                    board[y][x].append([wave, board[y][x][-1][1] + option])
                    return board
                if x + 1 < 13:
                    if board[y][x + 1][0][0] == 0 and self.past_action(board, x + 1, y, board[y][x][-1][1] + option):
                        board[y][x + 1].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x + 1, y, wave + 1)
                    if y + 1 < 7:
                        if board[y + 1][x + 1][0][0] == 0 and\
                                self.past_action(board, x + 1, y + 1, board[y][x][-1][1] + option) and\
                                board[y][x + 1] == -1:
                            board[y + 1][x + 1].append([wave, board[y][x][-1][1] + option])
                            option = str(int(option) + 1)
                            board = self.finding_path_2(board, cell_player, x + 1, y + 1, wave + 1)
                if x - 1 >= 0:
                    if board[y][x - 1][0][0] == 0 and self.past_action(board, x - 1, y, board[y][x][-1][1] + option):
                        board[y][x - 1].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x - 1, y, wave + 1)
                    if y + 1 < 7:
                        if board[y + 1][x - 1][0][0] == 0 and \
                                self.past_action(board, x - 1, y + 1, board[y][x][-1][1] + option) and\
                                board[y][x - 1] == -1:
                            board[y + 1][x - 1].append([wave, board[y][x][-1][1] + option])
                            option = str(int(option) + 1)
                            board = self.finding_path_2(board, cell_player, x - 1, y + 1, wave + 1)
                if x + 1 < 13 and y - 2 >= 0:
                    if board[y - 1][x + 1][0][0] == 0 and\
                            self.past_action(board, x + 1, y - 1, board[y][x][-1][1] + option) and\
                            board[y - 1][x][0][0] == -1:
                        board[y - 1][x + 1].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x + 1, y - 1, wave + 1)
                    if board[y - 2][x + 1][0][0] == 0 and\
                            self.past_action(board, x + 1, y - 2, board[y][x][-1][1] + option) and\
                            y != 6 and board[y - 1][x][0][0] == board[y - 2][x][0][0] == -1:
                        board[y - 2][x + 1].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x + 1, y - 2, wave + 1)
                if x + 2 < 13 and y - 2 >= 0:
                    if board[y - 1][x + 2][0][0] == 0 and\
                            self.past_action(board, x + 2, y - 1, board[y][x][-1][1] + option) and\
                            board[y - 1][x][0] == board[y - 2][x][0] == -1 and\
                            board[y - 2][x + 1][0][0] == board[y - 2][x + 2][0][0] == -1:
                        board[y - 1][x + 2].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x + 2, y - 1, wave + 1)
                if x - 1 >= 0 and y - 2 >= 0:
                    if board[y - 1][x - 1][0][0] == 0 and\
                            self.past_action(board, x - 1, y - 1, board[y][x][-1][1] + option) and \
                            board[y - 1][x][0][0] == -1:
                        board[y - 1][x - 1].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x - 1, y - 1, wave + 1)
                    if board[y - 2][x - 1][0][0] == 0 and\
                            self.past_action(board, x - 1, y - 2, board[y][x][-1][1] + option) and\
                            y != 6 and board[y - 1][x][0][0] == board[y - 2][x][0][0] == -1:
                        board[y - 2][x - 1].append([wave, board[y][x][-1][1] + option])
                        option = str(int(option) + 1)
                        board = self.finding_path_2(board, cell_player, x - 1, y - 2, wave + 1)
                if x - 2 >= 0 and y - 2 >= 0:
                    if board[y - 1][x - 2][0][0] == 0 and\
                            self.past_action(board, x - 2, y - 1, board[y][x][-1][1] + option) and \
                            board[y - 1][x][0][0] == board[y - 2][x][0][0] == -1 and\
                            board[y - 2][x - 1][0][0] == board[y - 2][x - 2][0][0] == -1:
                        board[y - 1][x - 2].append([wave, board[y][x][-1][1] + option])
                        board = self.finding_path_2(board, cell_player, x - 2, y - 1, wave + 1)
            except TypeError:
                pass
        return board

    def past_action(self, board, x, y, cod):
        for option in board[y][x]:
            if option[0] != 0 and option[1] == cod[:len(option[1])]:
                return False
        return True

    def save_path(self, board, cell_player, ind):
        self.path = []
        wave, cod_cell = board[cell_player[1]][cell_player[0]][ind][0], board[cell_player[1]][cell_player[0]][ind][1]
        self.path.append([*cell_player, False])
        for ind in range(-1, -len(cod_cell), -1):
            wave -= 1
            cod = cod_cell[:ind]
            for y in range(visual_board.height):
                for x in range(visual_board.width):
                    for option in board[y][x]:
                        if option == [wave, cod]:
                            self.path.append([x, y, False])
                            try:
                                if self.path[-2][1] < y:
                                    self.path[-2][2] = True
                            except IndexError:
                                pass
        self.path = self.path[::-1]
        del self.path[0]


class Platform(pygame.sprite.Sprite):
    def __init__(self, coord_cell):
        super().__init__()
        self.image = load_image('platform.png')
        self.rect = self.image.get_rect()
        visual_board.set_values(coord_cell, 1)
        self.rect.center = visual_board.get_coord_platform(coord_cell)


class PotionStand(pygame.sprite.Sprite):
    def __init__(self, coord_cell):
        super().__init__(invisible_sprites)
        self.frames = load_frames(load_image('PotionStand.png', (35, 90, 115)), 2, 2)
        self.image = self.frames[0]
        self.cur_frame, self.timer = 0, 0
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.coord_cell, self.invisibility = coord_cell, False
        self.restoration, self.prise, self.uses = random.randrange(200, 500, 100), 0, [0, False]

    def update(self):
        if self.invisibility and self.rect.center != (-100, -100):
            self.rect.center = (-100, -100)
            self.uses[1] = False
        elif not self.invisibility and self.rect.center == (-100, -100):
            if visual_board.board[self.coord_cell[1]][self.coord_cell[0]] == 1:
                self.rect.center = (self.coord_cell[0] * 100 + 50, self.coord_cell[1] * 100 + 20)
            else:
                self.rect.center = (self.coord_cell[0] * 100 + 50, self.coord_cell[1] * 100 + 47)
            self.restoration = random.randrange(200, 500, 100)
            self.prise = (self.restoration // 100) * 5 + game.wave * 2 + self.uses[0] * 3
        if not self.invisibility:
            if self.timer == 9:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
            self.timer += 1
            if self.timer == 10:
                self.timer = 0
        if visual_board.get_coord(player.rect.center) == self.coord_cell and not self.invisibility and not self.uses[1]:
            psw.invisibility = False
            if game.coins >= self.prise:
                psw_pay.invisibility = False
        else:
            psw.invisibility, psw_pay.invisibility = True, True


class PotionStandWindow(pygame.sprite.Sprite):
    def __init__(self, image, coord_cell=None):
        super().__init__(invisible_sprites)
        self.image = load_image(image, (35, 90, 115))
        self.rect = self.image.get_rect()
        if coord_cell is None:
            self.rect.center = (-150, -50)
        else:
            self.rect.center = (coord_cell[0] * 100 + 50, coord_cell[1] * 100 + 50)
        self.coord_cell = coord_cell
        self.invisibility = True

    def update(self):
        if self.invisibility:
            self.rect.center = (-150, -50)
        else:
            if self.coord_cell is None:
                self.rect.left = player.rect.right
                self.rect.center = (self.rect.center[0], player.rect.center[1])
            else:
                self.rect.center = (self.coord_cell[0] * 100 + 50, self.coord_cell[1] * 100 + 50)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(coins_sprites)
        self.frames_sl, self.cur_frame = load_frames_sl((('Coin.png', (3, 2)), ('Coin_flight.png', (5, 3))), True)
        self.image = self.frames_sl['coin'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timers, self.is_flight = [240, 0], True
        self.fall = random.randrange(-15, -2)
        self.speed = random.randrange(1, 5) * random.choice([-1, 1])

    def update(self):
        if self.is_flight:
            if self.timers[1] == 1:
                self.cur_frame[1] = (self.cur_frame[1] + 1) % len(self.frames_sl['flight'])
                self.image = self.frames_sl['flight'][self.cur_frame[1]]
            self.timers[1] += 1
            if self.timers[1] == 2:
                self.timers[1] = 0
        elif not self.is_flight:
            if self.cur_frame[0] == 0 and self.timers[0] == 240:
                self.cur_frame[0] = (self.cur_frame[0] + 1) % len(self.frames_sl['coin'])
                self.image = self.frames_sl['coin'][self.cur_frame[0]]
            elif 240 > self.cur_frame[0] > 0 and self.timers[0] % 9 == 0:
                self.cur_frame[0] = (self.cur_frame[0] + 1) % len(self.frames_sl['coin'])
                self.image = self.frames_sl['coin'][self.cur_frame[0]]
            self.timers[0] += 1
            if self.timers[1] == 301:
                self.timers[1] = 0
        y, top_col = self.rect.y + self.fall, False
        for j in range(abs(self.fall)):
            if self.fall < 0:
                self.rect.y -= 1
            else:
                self.rect.y += 1
            if self.collision() is not None:
                top_col = True
            if self.rect.bottom > HEIGHT - 23:
                self.rect.bottom = HEIGHT - 23

        if y == self.rect.y or top_col:
            self.fall += 1
            self.is_flight = True
        else:
            self.is_flight = False
        if self.is_flight:
            self.rect.x += self.speed

    def collision(self):
        platforms = pygame.sprite.spritecollide(self, platform_sprites, False)
        for pl in platforms:
            if pl.rect.bottom > self.rect.bottom > pl.rect.top > self.rect.top:
                self.rect.bottom = pl.rect.top
            elif pl.rect.top < self.rect.top < pl.rect.bottom < self.rect.bottom:
                self.rect.top = pl.rect.bottom
                return True
            elif self.rect.top <= pl.rect.top or self.rect.bottom >= pl.rect.bottom:
                if self.rect.right > pl.rect.left > self.rect.left:
                    self.rect.right = pl.rect.left
                elif self.rect.left < pl.rect.right < self.rect.right:
                    self.rect.left = pl.rect.right


class Decor(pygame.sprite.Sprite):
    def __init__(self, name_image, coord):
        super().__init__()
        self.image = load_image(name_image, (35, 90, 115))
        self.rect = self.image.get_rect()
        self.rect.center = coord


class Cur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_cur)
        self.image = load_image_menu("cur.png")  # загружает спрайт
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

    def get_coord(self, coord):
        self.rect.x, self.rect.y = coord


class MainMenu(pygame.sprite.Sprite):
    def __init__(self, name_file, coord_x, coord_y, size_x, size_y):
        super().__init__(all_sprites_main_menu)

        self.image = load_image_menu(name_file)  # загружает спрайт
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord_x, coord_y

    def get_cords(self,  last_y):
        if self.rect.y < last_y:
            self.rect.y += 20

    def rename(self, name):
        self.image = load_image_menu(name)
        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))


class MiniMenu(pygame.sprite.Sprite):
    def __init__(self, name_file, coord_x, coord_y, size_x, size_y):
        super().__init__(all_sprites_mini_menu)
        self.image = load_image(name_file, (35, 90, 115))
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.center = (coord_x, coord_y)
        self.size_x = size_x
        self.size_y = size_y

    def rename(self, name):
        self.image = load_image(name, (35, 90, 115))
        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))


class OptionsBackground(pygame.sprite.Sprite):  # настройки
    def __init__(self, name_file, coord_x, coord_y, size_x, size_y):
        super().__init__(all_Background_options)

        self.image = load_image_menu(name_file)  # загружает спрайт
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord_x, coord_y

    def get_left(self, last_x):
        if self.rect.x > last_x:
            self.rect.x -= 40

    def get_right(self, last_x):
        if self.rect.x < last_x:
            self.rect.x += 40

    def rename(self, name):
        self.image = load_image_menu(name)
        self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))


def load_frames(image, columns, rows):
    rect = pygame.Rect(0, 0, image.get_width() // columns, image.get_height() // rows)
    frames = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frames.append(image.subsurface(pygame.Rect(frame_location, rect.size)))
    return frames


def load_frames_sl(image_names_sizes, coin=False):
    if not coin:
        frames_sl = {}
        for image_name_size in image_names_sizes:
            name, size = image_name_size
            frames_sl[name[name.index('_') + 1:-4] + '_right'] = load_frames(load_image(name, (35, 90, 115)), *size)
            frames_sl[name[name.index('_') + 1:-4] + '_left'] = []
            for im in frames_sl[name[name.index('_') + 1:-4] + '_right']:
                image = pygame.transform.flip(im, True, False)
                image.set_colorkey((35, 90, 115))
                frames_sl[name[name.index('_') + 1:-4] + '_left'].append(image)
        return frames_sl, [0 for _ in range(len(image_names_sizes))]
    else:
        frames_sl = {}
        for image_name_size in image_names_sizes:
            name, size = image_name_size
            if '_' in name:
                frames_sl['flight'] = load_frames(load_image(name, (35, 90, 115)), *size)
            else:
                frames_sl['coin'] = load_frames(load_image(name, (35, 90, 115)), *size)
        return frames_sl, [0 for _ in range(len(image_names_sizes))]


def load_image(name, color_key=None):
    try:
        image = pygame.image.load(os.path.join('image', name)).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        image.set_colorkey(color_key)
    return image


def load_image_menu(name, color_key=None):
    fullname = os.path.join('image', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_color_key(color_key)

    return image


def game_cycle():
    global RUSSIA, ENGLISH, HIT_J, HIT_K, HIT_L, ARROWS, WASD, SOUND_PAUSE, MUSICSOUND, ACTUAL_SOUND, image1, keys_sl
    image11 = pygame.transform.scale(image1, (1280, 750))
    pygame.init()
    running, draw_sprite = True, False

    background_options = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cur.get_coord(event.pos)
                if pygame.mouse.get_focused():
                    draw_sprite = True
                else:
                    draw_sprite = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 130 < x < WIDTH // 2 + 115 and 320 < y < 390:  # открытие настрооек
                    background_options = True

                if background_options:
                    background_options = options_menu(x, y, True)
                else:
                    if WIDTH // 2 - 155 < x < WIDTH // 2 + 145 and 200 < y < 300:  # нажатие на кнопку старт
                        return True
                    if WIDTH // 2 - 80 < x < WIDTH // 2 + 70 and 400 < y < 445:  # нажатие на кнопку выхода
                        running = False
                    if WIDTH - 100 < x < WIDTH - 70 and 20 < y < 45:  # остановки и воспроизведение музыки
                        if not SOUND_PAUSE:
                            SOUND_PAUSE = True
                            music_sound.rename("SOUND_PAUSE_TRUE.png")
                            pygame.mixer.music.pause()
                        else:
                            SOUND_PAUSE = False
                            music_sound.rename("SOUND_PAUSE_FALSE.png")
                            pygame.mixer.music.unpause()
                    if WIDTH - 65 < x < WIDTH - 40 and 20 < y < 45:  # смена музыки вправо
                        MUSICSOUND += 1
                        if MUSICSOUND == 4:
                            MUSICSOUND = 0
                        pygame.mixer.music.load('{}.mp3'.format(music_pleer[MUSICSOUND]))
                        ACTUAL_SOUND = music_pleer[MUSICSOUND]
                        pygame.mixer.music.play(-1)
                        if SOUND_PAUSE:
                            pygame.mixer.music.pause()
                    if WIDTH - 135 < x < WIDTH - 105 and 20 < y < 45:  # смена музыки влево
                        MUSICSOUND -= 1
                        if MUSICSOUND == -1:
                            MUSICSOUND = 3
                        ACTUAL_SOUND = music_pleer[MUSICSOUND]
                        pygame.mixer.music.load('{}.mp3'.format(music_pleer[MUSICSOUND]))
                        pygame.mixer.music.play(-1)
                        if SOUND_PAUSE:
                            pygame.mixer.music.pause()

        start.get_cords(200)
        options.get_cords(320)
        exit_game.get_cords(400)

        music_sound.get_cords(20)
        right_pleer.get_cords(20)
        left_pleer.get_cords(20)
        note.get_cords(20)

        game.screen.blit(image11, (0, 0))
        all_sprites_main_menu.draw(game.screen)
        font = pygame.font.Font(None, 25)
        text = font.render(ACTUAL_SOUND.upper(), True, (255, 255, 255))
        game.screen.blit(text, (1050, 25))

        with open('Рекорд.txt') as f:
            record_number = f.read()

        width_record = WIDTH // 2 - 100

        font_record = pygame.font.Font(None, 40)
        text_record = font_record.render('Рекорд:', True, (255, 255, 255))
        game.screen.blit(text_record, (width_record, 170))

        font_record_number = pygame.font.Font(None, 40)
        text_record_number = font_record_number.render(record_number, True, (255, 255, 255))
        game.screen.blit(text_record_number, (width_record + 120, 170))

        all_Background_options.draw(game.screen)

        options_animation(background_options)

        if draw_sprite:
            all_cur.draw(game.screen)
        pygame.time.Clock().tick(60)
        pygame.display.flip()


def options_menu(x, y, click):
    global RUSSIA, ENGLISH, HIT_J, HIT_K, HIT_L, ARROWS, WASD, SOUND_PAUSE, MUSICSOUND, ACTUAL_SOUND
    if click:
        if 0 < x < 45 and HEIGHT - 55 < y < HEIGHT:  # закрытие настроек
            return False

        if (WIDTH // 4 + WIDTH // 4 + 150 < x < WIDTH // 4 + WIDTH // 4 + 180 and 120 < y < 145) or \
                (WIDTH // 4 + WIDTH // 4 - 15 < x < WIDTH // 4 + WIDTH // 4 + 10 and 120 < y < 145):  # язык
            if not ENGLISH:
                RUSSIA = False
                ENGLISH = True
                start.rename("START_ENGLISH.png", )
                options.rename("OPTIONS_ENGLISH.png")
                exit_game.rename("EXIT_ENGLISH.png")

                optinons_control.rename("CONTROL_ENGLISH.png")

                options_JUMP.rename("JUMP_ENGLISH.png")

                options_hit.rename("HIT_ENGLISH.png")

                option_languages.rename("LANGUAGES_ENGLISH.png")
                languages_sprite.rename("LANG_ENGLISH.png")

                back_main.rename("BACK_ENGLISH.png")

                continue_btn.rename('Continue_english.png')
                exit_menu.rename('exit_menu_english.png')
                exit_game_mm.rename('exit_game_english.png')
            else:
                RUSSIA = True
                ENGLISH = False
                start.rename("START_RUSSIA.png")
                options.rename("OPTIONS_RUSSIA.png")
                exit_game.rename("EXIT_RUSSIA.png")

                optinons_control.rename("CONTROL_RUSSIA.png")

                options_JUMP.rename("JUMP_RUSSIA.png")

                options_hit.rename("HIT_RUSSIA.png")

                option_languages.rename("LANGUAGES_RUSSIA.png")
                languages_sprite.rename("LANG_RUSSIA.png")

                back_main.rename("BACK_RUSSIA.png")

                continue_btn.rename('Continue_russia.png')
                exit_menu.rename('exit_menu_russia.png')
                exit_game_mm.rename('exit_game_russia.png')
        if (WIDTH // 4 + 120 < x < WIDTH // 4 + 155 and 375 < y < 400) or \
                (WIDTH // 4 + 20 < x < WIDTH // 4 + 45 and 375 < y < 400):  # смена кнопки удара
            if HIT_J:
                HIT_J = False
                HIT_K = True
                keys_sl['attack'] = pygame.K_k
                hit_button.rename("HIT_K.png")

            elif HIT_K:
                HIT_K = False
                HIT_L = True
                keys_sl['attack'] = pygame.K_l
                hit_button.rename("HIT_L.png")
            elif HIT_L:
                HIT_L = False
                HIT_J = True
                keys_sl['attack'] = pygame.K_j
                hit_button.rename("HIT_J.png")
        if (WIDTH // 4 + 160 < x < WIDTH // 4 + 190 and 120 < y < 145) or \
                (WIDTH // 4 - 25 < x < WIDTH // 4 + 5 and 120 < y < 145):  # смена управления
            if ARROWS:
                ARROWS = False
                WASD = True
                keys_sl['run'] = [pygame.K_a, pygame.K_d]
                options_control_arrows.rename("WASD.png")
            elif WASD:
                ARROWS = True
                WASD = False
                keys_sl['run'] = [pygame.K_LEFT, pygame.K_RIGHT]
                options_control_arrows.rename("ARROWS.png")
    return True


def options_animation(tf):

    if tf:  # открытие настроек
        background_fon.get_left(0)

        optinons_control.get_left(WIDTH // 4 + 20)
        options_control_arrows.get_left(WIDTH // 4 + 20)
        control_right.get_left(WIDTH // 4 + 180)
        control_left.get_left(WIDTH // 4)

        options_JUMP.get_left(WIDTH // 4 + 20)
        options_Jump_space.get_left(WIDTH // 4 + 20)

        options_hit.get_left(WIDTH // 4 + 20)
        hit_button.get_left(WIDTH // 4 + 20)
        hit_right.get_left(WIDTH // 4 + 160)
        hit_left.get_left(WIDTH // 4 + 60)

        option_languages.get_left(WIDTH // 4 + WIDTH // 4)
        languages_sprite.get_left(WIDTH // 4 + WIDTH // 4 + 60)
        language_right.get_left(WIDTH // 4 + WIDTH // 4 + 160)
        language_left.get_left(WIDTH // 4 + WIDTH // 4)
        back_main.get_left(0)
    else:  # закрытие настроек
        background_fon.get_right(WIDTH)

        optinons_control.get_right(WIDTH + WIDTH // 4)
        options_control_arrows.get_right(WIDTH + WIDTH // 4)
        control_right.get_right(WIDTH + WIDTH // 4 + 170)
        control_left.get_right(WIDTH + WIDTH // 4 - 30)

        options_JUMP.get_right(WIDTH + WIDTH // 4)
        options_Jump_space.get_right(WIDTH + WIDTH // 4)

        options_hit.get_right(WIDTH + WIDTH // 4)
        hit_button.get_right(WIDTH + WIDTH // 4)
        hit_right.get_right(WIDTH + WIDTH // 4 + 170)
        hit_left.get_right(WIDTH + WIDTH // 4 - 30)

        option_languages.get_right(WIDTH + WIDTH // 4 + WIDTH // 4)
        languages_sprite.get_right(WIDTH + WIDTH // 4 + WIDTH // 4 + 100)
        language_right.get_right(WIDTH + WIDTH // 4 + WIDTH // 4 + 50)
        language_left.get_right(WIDTH + WIDTH // 4)
        back_main.get_right(WIDTH)


def mini_menu(x, y, click):
    if continue_btn.rect.left < x < continue_btn.rect.right and\
            continue_btn.rect.top < y < continue_btn.rect.bottom and click:
        return False
    if exit_menu.rect.left < x < exit_menu.rect.right and \
            exit_menu.rect.top < y < exit_menu.rect.bottom and click:
        game.exit_command = 'menu'
        game.save_game()
        return False
    if exit_game_mm.rect.left < x < exit_game_mm.rect.right and\
            exit_game_mm.rect.top < y < exit_game_mm.rect.bottom and click:
        game.exit_command = 'game'
        game.save_game()
        return False
    return True


if __name__ == '__main__':
    game = Game()
    visual_board = VisualBoard()
    character_sprites, platform_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    foreground_sprites, background_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    coins_sprites, invisible_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    game_over_sprite = pygame.sprite.Group()
    GameOver()
    hp_enemy, hit_enemy = [], []
    player = Player()
    for _ in range(5):
        Enemy()
    level = get_level()
    ps, psw = PotionStand(level[-1]), PotionStandWindow('PotionStand_window.png', [level[-1][0], level[-1][1] - 1])
    psw_pay = PotionStandWindow('pay_window.png')
    del level[-1]
    for coord_pl in level:
        platform_sprites.add(Platform(coord_pl))
    foreground_sprites.add(Decor('foregroundPlant0.png', (639, 683)), Decor('Frame.png', (330, 35)),
                           Decor('Coin_pin.png', (29, 90)))

    image1 = load_image("FON1.jpg")  # загрузка фона
    all_Background_options = pygame.sprite.Group()  # настройки
    all_sprites_main_menu = pygame.sprite.Group()  # кнопки: Старт, Настройки, Выход
    all_sprites_mini_menu = pygame.sprite.Group()  # Кнопки: продолжить, сохранить и выйти(в главное меню)
    all_cur = pygame.sprite.Group()  # курсор
    cur = Cur()

    # меню
    start = MainMenu("START_RUSSIA.png", WIDTH // 2 - 150, -500, 300, 100)  # кнопка Старт(Start)
    options = MainMenu("OPTIONS_RUSSIA.png", WIDTH // 2 - 125, -300, 250, 70)  # кнопка Настройки(Options)
    exit_game = MainMenu("EXIT_RUSSIA.png", WIDTH // 2 - 75, -100, 150, 50)  # кнопка Выход(Exit)

    # музыка в меню
    music_sound = MainMenu("SOUND_PAUSE_FALSE.png", WIDTH - 90, -500, 26, 25)
    right_pleer = MainMenu("RIGHT_PLEER.png", WIDTH - 55, -500, 25, 25)
    left_pleer = MainMenu("LEFT_PLEER.png", WIDTH - 125, -500, 25, 25)
    note = MainMenu("Нота.png", WIDTH - 250, -500, 25, 25)

    # настройки_фон
    background_fon = OptionsBackground("Прозрачный фон.png", WIDTH, 0, 1280, 750)  # прозрачный фон
    all_sprites_mini_menu.add(background_fon)

    # мини меню
    continue_btn = MiniMenu("Continue_russia.png", WIDTH // 2, 210, 350, 125)
    exit_menu = MiniMenu("exit_menu_russia.png", WIDTH // 2, 350, 260, 80)
    exit_game_mm = MiniMenu("exit_game_russia.png", WIDTH // 2, 450, 260, 80)

    # настройки_управление_ персонажем
    optinons_control = OptionsBackground("CONTROL_RUSSIA.png", WIDTH + WIDTH // 4, 50, 200, 50)  # спрайт управления
    options_control_arrows = OptionsBackground("WASD.png", WIDTH + WIDTH // 4 + 25, 115, 150, 40)  # стрелочки
    control_right = OptionsBackground("arrow_right.png", WIDTH + WIDTH // 4 + 180, 120, 25, 25)  # смена(вправо)
    control_left = OptionsBackground("arrow_left.png", WIDTH + WIDTH // 4 + 35, 120, 25, 25)  # смена(влево)

    # настройки_прыжок
    options_JUMP = OptionsBackground("JUMP_RUSSIA.png", WIDTH + WIDTH // 4, 180, 200, 50)  # спрайт прыжок
    options_Jump_space = OptionsBackground("SPACE.png", WIDTH + WIDTH // 4 + 25, 240, 150, 40)  # прыжок(пробел)

    # настройки_удар
    options_hit = OptionsBackground("HIT_RUSSIA.png", WIDTH + WIDTH // 4, 310, 200, 50)  # спрайт удара
    hit_button = OptionsBackground("HIT_J.png", WIDTH + WIDTH // 4 + 25, 370, 150, 40)  # кнопка удара
    hit_right = OptionsBackground("arrow_right.png", WIDTH + WIDTH // 4 + 180, 375, 25, 25)  # смена(вправо)
    hit_left = OptionsBackground("arrow_left.png", WIDTH // 4 + 35 + WIDTH, 375, 25, 25)  # смена(влево)

    # настройки_языки
    option_languages = OptionsBackground("LANGUAGES_RUSSIA.png", WIDTH + WIDTH // 4 + WIDTH // 4, 50, 200, 50)
    languages_sprite = OptionsBackground("LANG_RUSSIA.png", WIDTH + WIDTH // 4 + WIDTH // 4 + 20, 120, 80, 20)
    language_right = OptionsBackground("arrow_right.png", WIDTH + WIDTH // 4 + WIDTH // 4 + 50, 120, 25, 25)
    language_left = OptionsBackground("arrow_left.png", WIDTH + WIDTH // 4 + WIDTH // 4, 120, 25, 25)

    # возвращение в главное меню
    back_main = OptionsBackground("BACK_RUSSIA.png", WIDTH + 50, HEIGHT - 55, 50, 25)
    pygame.mouse.set_visible(False)  # скрывает курсор

    while game.running and game_cycle():
        game.game_run()
    pygame.quit()