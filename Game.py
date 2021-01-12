import pygame
import os
import random

WIDTH, HEIGHT = 1270, 720
FPS = 60
pygame.display.set_caption("Test Game")
pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.bg = load_image('background.jpg')
        self.coins = 0
        self.running = True
        self.game_run()

    def game_run(self):
        while self.running:
            pygame.time.Clock().tick(FPS)
            self.events()
            self.update()
            self.visualization()
            pygame.display.flip()
        pygame.quit()

    def events(self):  # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = event.pos
                for _ in range(random.randrange(1, 10)):
                    Coin(*coord, random.choice([-1, 1]))

    def update(self):  # Обнавление
        character_sprites.update()
        background_decor.update()
        coins_sprites.update()

    def visualization(self):  # Визуализация
        self.screen.blit(self.bg, [0, 0])
        background_decor.draw(self.screen)
        coins_sprites.draw(self.screen)
        character_sprites.draw(self.screen)
        platform_sprites.draw(self.screen)
        pygame.draw.rect(self.screen, 'red', [127, 15, player.hp // 2, 35], 0)
        foreground_decor.draw(self.screen)

        # visual_board.render(self.screen)

        for character in character_sprites:
            if character != player:
                pygame.draw.rect(self.screen, 'red', [character.rect.x, character.rect.y - 15,
                                                      character.hp // 20, 5], 0)


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
    def __init__(self, im_stand, im_size_run, im_size_attack):
        super().__init__(character_sprites)
        self.image_stand = load_image(im_stand, (35, 90, 115))
        self.image = self.image_stand
        self.frames_sl, self.cur_frame = load_frames_sl((im_size_run, im_size_attack))
        self.hp, self.rect = 1, self.image.get_rect()
        self.jump, self.is_flight, self.fall, self.timers = [False, -25], False, 5, [0, 0]
        self.attack = [False, False]

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
            if self != char:
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
            if self.timers[1] == 10:
                if not click_attack:
                    self.cur_frame[1] = -1
                else:
                    self.cur_frame[1] = (self.cur_frame[1] + 1) % len(self.frames_sl[key])
                self.image = self.frames_sl[key][self.cur_frame[1]]
                self.set_rect()
            self.timers[1] += 1
            if self.timers[1] == 11:
                self.timers[1] = 0

    def set_rect(self):
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(character_sprites)
        self.image = load_image('Player.png', (35, 90, 115))
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.fall, self.hp = 5, 1000
        self.jump, self.is_flight = [False, -25], False
        self.attack = [False, False]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 5:
            self.rect.x -= 6
        if keys[pygame.K_d] and self.rect.right < WIDTH - 5:
            self.rect.x += 6
        if not self.jump[0] and not self.is_flight:
            if keys[pygame.K_SPACE]:
                self.jump[0] = True
        elif self.jump[0]:
            if self.jump[1] == 25:
                self.jump = [False, -25]
            else:
                for _ in range(abs(self.jump[1])):
                    if self.jump[1] < 0:
                        self.rect.y -= 1
                    else:
                        self.rect.y += 1
                    if not self.collision():
                        self.jump[1] = 24
                        break
                self.jump[1] += 1

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
            self.fall = 5
            self.is_flight = False
        if self.jump[0]:
            self.is_flight = True

    def collision(self):
        platforms = pygame.sprite.spritecollide(self, platform_sprites, False)
        for pl in platforms:
            if pl.rect.bottom >= self.rect.bottom >= pl.rect.top > self.rect.top:
                self.rect.bottom = pl.rect.top
                return False
            elif pl.rect.top < self.rect.top < pl.rect.bottom < self.rect.bottom:
                self.rect.top = pl.rect.bottom
                return False
            elif self.rect.top < pl.rect.top or self.rect.bottom > pl.rect.bottom:
                if self.rect.right > pl.rect.left > self.rect.left:
                    self.rect.right = pl.rect.left
                elif self.rect.left < pl.rect.right < self.rect.right:
                    self.rect.left = pl.rect.right
                return True
            else:
                return True
        return True


class Enemy(Character):
    def __init__(self):
        super().__init__('Guard.png', ('Guard_run.png', (6, 1)), ('Guard_attack.png', (4, 3)))
        self.rect.center = WIDTH // 2, HEIGHT - 23
        self.hp, self.speed = random.randrange(400, 700, 100), random.randrange(4, 6)
        self.path, self.run = [], [0, 1, False]
        self.timers.append(0)

    def update(self):
        cell_player, cell_self = visual_board.get_coord(player.rect.center), visual_board.get_coord(self.rect.center)
        if self.timers[2] == 30:
            self.timers[2] = 0
            self.finding_path_1(visual_board.board, cell_player, cell_self)
        self.timers[2] += 1
        if cell_player[1] >= cell_self[1] and not self.jump[0] and not self.attack[0]:
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
                if self.run[2] and not self.jump[0]:
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
        if not self.jump[0] and not self.is_flight:
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
                    player.hp -= 40
                    self.attack[1] = True
            elif self.cur_frame[1] not in [3, 8]:
                self.attack[1] = False
        super().update()

    def finding_path_1(self, board, cell_player, cell_self):
        if not player.is_flight and not player.jump[0] and not self.is_flight and not self.jump[0]:
            board2 = []
            for i in range(visual_board.height):
                board2.append([])
                for j in range(visual_board.width):
                    if board[i][j] == 0:
                        board2[i].append([-1, ''])
                    elif board[i][j] == 1:
                        board2[i].append([0, ''])
            board2[-1] = [[0, ''] for _ in range(visual_board.width)]
            board2[cell_self[1]][cell_self[0]] = [1, '1']
            sp = self.finding_path_2(board2, cell_player)
            if sp[0]:
                self.save_path(sp[1], cell_player)

    def finding_path_2(self, board, cell_player):
        wave = 1
        for _ in range(visual_board.height * visual_board.width):
            wave += 1
            for y in range(visual_board.height):
                for x in range(visual_board.width):
                    option = '1'
                    if board[y][x][0] == wave - 1:
                        if x + 1 < visual_board.width:
                            if board[y][x + 1][0] == 0 or (board[y][x + 1][0] != -1 and board[y][x + 1][0] > wave):
                                board[y][x + 1] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                        if x - 1 >= 0:
                            if board[y][x - 1][0] == 0 or (board[y][x - 1][0] != -1 and board[y][x - 1][0] > wave):
                                board[y][x - 1] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                        if x + 1 < visual_board.width and y - 2 >= 0:
                            if (board[y - 1][x + 1][0] == 0 or (board[y - 1][x + 1][0] != -1 and  # 1
                                                                board[y - 1][x + 1][0] > wave)) and\
                                    board[y - 1][x][0] == board[y - 2][x][0] == board[y - 2][x + 1][0] == -1:
                                board[y - 1][x + 1] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                            if (board[y - 2][x + 1][0] == 0 or (board[y - 2][x + 1][0] != -1 and  # 3
                                                                board[y - 2][x + 1][0] > wave)) and y != 6 and \
                                    board[y - 1][x][0] == board[y - 2][x][0] == -1:
                                board[y - 2][x + 1] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                        if x + 2 < visual_board.width and y - 2 >= 0:
                            if (board[y - 1][x + 2][0] == 0 or (board[y - 1][x + 2][0] != -1 and  # 2
                                                                board[y - 1][x + 2][0] > wave)) and\
                                    board[y - 1][x][0] == board[y - 2][x][0] == -1 and\
                                    board[y - 2][x + 1][0] == board[y - 2][x + 2][0] == -1:
                                board[y - 1][x + 2] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                        if x - 1 >= 0 and y - 2 >= 0:
                            if (board[y - 1][x - 1][0] == 0 or (board[y - 1][x - 1][0] != -1 and  # 1
                                                                board[y - 1][x - 1][0] > wave)) and\
                                    board[y - 1][x][0] == board[y - 2][x][0] == board[y - 2][x - 1][0] == -1:
                                board[y - 1][x - 1] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                            if (board[y - 2][x - 1][0] == 0 or (board[y - 2][x - 1][0] != -1 and  # 3
                                                                board[y - 2][x - 1][0] > wave)) and y != 6 and \
                                    board[y - 1][x][0] == board[y - 2][x][0] == -1:
                                board[y - 2][x - 1] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)
                        if x - 2 >= 0 and y - 2 >= 0:
                            if (board[y - 1][x - 2][0] == 0 or (board[y - 1][x - 2][0] != -1 and  # 2
                                                                board[y - 1][x - 2][0] > wave)) and\
                                    board[y - 1][x][0] == board[y - 2][x][0] == -1 and\
                                    board[y - 2][x - 1][0] == board[y - 2][x - 2][0] == -1:
                                board[y - 1][x - 2] = [wave, board[y][x][1] + option]
                                option = str(int(option) + 1)

                        if y == cell_player[1] and x == cell_player[0]:
                            board[y][x] = [wave, board[y][x][1] + option]
                            return [True, board]

        return [False, []]

    def save_path(self, board, cell_player):
        wave, cod_cell = board[cell_player[1]][cell_player[0]][0], board[cell_player[1]][cell_player[0]][1]
        self.path = []
        self.path.append([*cell_player, False])
        for ind in range(-1, -len(cod_cell), -1):
            wave -= 1
            cod = cod_cell[:ind]
            for y in range(visual_board.height):
                for x in range(visual_board.width):
                    if board[y][x] == [wave, cod]:
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
        super().__init__()
        self.frames = load_frames(load_image('PotionStand.png', (35, 90, 115)), 2, 2)
        self.image = self.frames[0]
        self.cur_frame, self.timer = 0, 0
        self.rect = self.image.get_rect()
        self.rect.center = [coord_cell[0] * 100 + 50, coord_cell[1] * 100 + 47]
        self.coord_cell = coord_cell

    def update(self):
        if self.timer == 9:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.timer += 1
        if self.timer == 10:
            self.timer = 0
        if visual_board.get_coord(player.rect.center) == self.coord_cell:
            pass


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__(coins_sprites)
        self.frames_sl, self.cur_frame = load_frames_sl((('Coin.png', (3, 2)), ('Coin_flight.png', (5, 3))), True)
        self.image = self.frames_sl['coin'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timers, self.is_flight = [240, 0], True
        self.fall = random.randrange(-15, -2)
        self.speed = random.randrange(1, 5) * direction

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
        y = self.rect.y + self.fall
        for j in range(abs(self.fall)):
            if self.fall < 0:
                self.rect.y -= 1
            else:
                self.rect.y += 1
            self.collision()
            if self.rect.bottom > HEIGHT - 23:
                self.rect.bottom = HEIGHT - 23

        if y == self.rect.y:
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
        image = pygame.image.load(os.path.join('image', name))
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        image.set_colorkey(color_key)
    return image


if __name__ == '__main__':
    visual_board = VisualBoard()
    character_sprites, platform_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    foreground_decor, background_decor = pygame.sprite.Group(), pygame.sprite.Group()
    coins_sprites = pygame.sprite.Group()
    player = Player()
    for _ in range(1):
        Enemy()
    platform_sprites.add(Platform((2, 5)), Platform((3, 5)), Platform((4, 5)), Platform((6, 4)), Platform((7, 4)),
                         Platform((8, 2)), Platform((0, 1)), Platform((1, 1)), Platform((2, 2)), Platform((3, 3)),
                         Platform((4, 3)), Platform((9, 5)), Platform((10, 5)), Platform((4, 1)), Platform((5, 1)),
                         Platform((6, 1)), Platform((7, 1)))
    foreground_decor.add(Decor('foregroundPlant0.png', (639, 683)), Decor('Frame.png', (330, 35)))
    background_decor.add(PotionStand((6, 6)))
    game = Game()
