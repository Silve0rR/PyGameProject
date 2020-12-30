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

    def update(self):  # Обнавление
        character_sprites.update()

    def visualization(self):  # Визуализация
        self.screen.fill('black')
        character_sprites.draw(self.screen)
        platform_sprites.draw(self.screen)

        visual_board.render(self.screen)


class VisualBoard:
    def __init__(self):
        self.width, self.height = WIDTH // 100 + 1, HEIGHT // 100
        self.board = [[0] * self.width for _ in range(self.height)]

    def render(self, screen):  # в игре не учавствует(служебная функция)
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white', (x * 100, y * 100, 100, 100), 1)

    def set_values(self, coords_cell, value):
        self.board[coords_cell[1]][coords_cell[0]] = value

    def get_coords_platform(self, coords_cell):
        if self.board[coords_cell[1]][coords_cell[0]] == 1:
            return [100 * coords_cell[0] + 50, 100 * coords_cell[1] + 70]

    def get_coords(self, coords):
        return [coords[0] // 100, coords[1] // 100]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(character_sprites)
        self.image = pygame.Surface((33, 58))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.fall = 5
        self.jump, self.is_flight = [False, -25], False

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
                        if self.jump[1] < 0:
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(character_sprites)
        self.image = pygame.Surface((33, 58))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT - 23
        self.fall, self.speed = 5, random.randrange(3, 8)
        self.jump, self.is_flight = [False, -25], False
        self.path, self.last_player_cell_coord = [], []
        self.run = [0, 1, False]

    def update(self):
        cell_player, cell_self = visual_board.get_coords(player.rect.center), visual_board.get_coords(self.rect.center)
        if cell_player[1] >= cell_self[1]:
            if player.rect.right < self.rect.left and self.rect.left > 5:
                self.rect.x -= self.speed
            if player.rect.left > self.rect.right and self.rect.right < WIDTH - 5:
                self.rect.x += self.speed
        elif self.path:
            print(self.path, '!!!', cell_self)
            if self.path[0][0] > cell_self[0] and self.run[0] == 0:
                self.run = [100, 1, False]
                self.run[2] = self.path[0][2]
            elif self.path[0][0] < cell_self[0] and self.run[0] == 0:
                self.run = [100, -1, False]
                self.run[2] = self.path[0][2]
            elif self.run[0] > 0:
                if self.run[2] and not self.jump[0]:
                    self.jump[0] = True
                self.run[0] -= self.speed
                if self.run[2] and self.run[0] > 80:
                    if self.run[0] < 85:
                        self.run[0] = 100
                        self.run[2] = False
                else:
                    self.rect.x += self.speed * self.run[1]
                if self.run[0] <= 0:
                    self.run[0] = 0
                    del self.path[0]
            elif self.run[0] == 0 and self.path[0][0] == cell_self[0] and self.path[0][1] == cell_self[1]:
                del self.path[0]
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
                        if self.jump[1] < 0:
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
        if self.last_player_cell_coord != cell_player:
            self.last_player_cell_coord = cell_player
            self.finding_path_1(visual_board.board, cell_player, cell_self)

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

    def finding_path_1(self, board, cell_player, cell_self):
        board2 = []
        if not player.is_flight and not player.jump[0]:
            for i in range(visual_board.height):
                board2.append([])
                for j in range(visual_board.width):
                    if board[i][j] == 0:
                        board2[i].append(-1)
                    elif board[i][j] == 1:
                        board2[i].append(0)
            board2[-1] = [0 for _ in range(visual_board.width)]
            board2[cell_self[1]][cell_self[0]] = 1
            sp = self.finding_path_2(board2, cell_player)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', sp[0])
            if sp[0]:
                self.save_path(sp[1], cell_player)

    def finding_path_2(self, board, cell_player):
        wave = 1
        self.path = []
        for _ in range(visual_board.height * visual_board.width):
            wave += 1
            for y in range(visual_board.height):
                for x in range(visual_board.width):
                    if board[y][x] == wave - 1:
                        if x + 1 < visual_board.width:
                            if board[y][x + 1] == 0 or (board[y][x + 1] != -1 and board[y][x + 1] > wave):
                                print('x')
                                board[y][x + 1] = wave
                        if x - 1 >= 0:
                            if board[y][x - 1] == 0 or (board[y][x - 1] != -1 and board[y][x - 1] > wave):
                                print('-x')
                                board[y][x - 1] = wave
                        if x + 1 < visual_board.width and y - 2 >= 0:
                            if (board[y - 1][x + 1] == 0 or (board[y - 1][x + 1] != -1 and  # 1
                                                             board[y - 1][x + 1] > wave)) and\
                                    board[y - 1][x] == board[y - 2][x] == board[y - 2][x + 1] == -1:
                                print(1, [x, y])
                                board[y - 1][x + 1] = wave
                            if (board[y - 2][x + 1] == 0 or (board[y - 2][x + 1] != -1 and  # 3
                                                             board[y - 2][x + 1] > wave)) and y != 6 and \
                                    board[y - 1][x] == board[y - 2][x] == -1:
                                print(3, [x, y])
                                board[y - 2][x + 1] = wave
                        if x + 2 < visual_board.width and y - 2 >= 0:
                            if (board[y - 1][x + 2] == 0 or (board[y - 1][x + 2] != -1 and  # 2
                                                             board[y - 1][x + 2] > wave)) and\
                                    board[y - 1][x] == board[y - 2][x] == -1 and\
                                    board[y - 2][x + 1] == board[y - 2][x + 2] == -1:
                                print(2, [x, y])
                                board[y - 1][x + 2] = wave
                            if (board[y - 2][x + 2] == 0 or (board[y - 2][x + 2] != -1 and
                                                             board[y - 2][x + 2] > wave)) and y != 6 and \
                                    board[y - 1][x] == board[y - 2][x] == board[y - 2][x + 1] == -1:
                                if board[y - 2][x + 1] == -1:
                                    print(4, [x, y])
                                    board[y - 2][x + 2] = wave
                        if x - 1 >= 0 and y - 2 >= 0:
                            if (board[y - 1][x - 1] == 0 or (board[y - 1][x - 1] != -1 and  # 1
                                                             board[y - 1][x - 1] > wave)) and\
                                    board[y - 1][x] == board[y - 2][x] == board[y - 2][x - 1] == -1:
                                print(1, [x, y])
                                board[y - 1][x - 1] = wave
                            if (board[y - 2][x - 1] == 0 or (board[y - 2][x - 1] != -1 and  # 3
                                                             board[y - 2][x - 1] > wave)) and y != 6 and \
                                    board[y - 1][x] == board[y - 2][x] == -1:
                                print(3, [x, y])
                                board[y - 2][x - 1] = wave
                        if x - 2 >= 0 and y - 2 >= 0:
                            if (board[y - 1][x - 2] == 0 or (board[y - 1][x - 2] != -1 and  # 2
                                                             board[y - 1][x - 2] > wave)) and\
                                    board[y - 1][x] == board[y - 2][x] == -1 and\
                                    board[y - 2][x - 1] == board[y - 2][x - 2] == -1:
                                print(2, [x, y])
                                board[y - 1][x - 2] = wave
                            if (board[y - 2][x - 2] == 0 or (board[y - 2][x - 2] != -1 and
                                                             board[y - 2][x - 2] > wave)) and y != 6 and \
                                    board[y - 1][x] == board[y - 2][x] == board[y - 2][x - 1] == -1:
                                if board[y - 2][x - 1] == -1:
                                    print(4, [x, y])
                                    board[y - 2][x - 2] = wave

                        if y == cell_player[1] and x == cell_player[0]:
                            board[cell_player[1]][cell_player[0]] = wave
                            return [True, board]
        return [False, []]

    def save_path(self, board, cell_player):
        y = cell_player[1]
        x = cell_player[0]
        wave = board[y][x]
        print('Player:', [x, y])
        while wave != 0:
            wave -= 1
            if x + 1 < visual_board.width and board[y][x + 1] == wave:
                self.path.append([x + 1, y, False])
                x += 1
            elif x - 1 >= 0 and board[y][x - 1] == wave:
                self.path.append([x - 1, y, False])
                x -= 1
            elif y + 1 < visual_board.height and board[y + 1][x + 1] == wave and\
                    board[y][x + 1] == board[y - 1][x + 1] == board[y - 1][x] == -1:  # 1
                self.path.append([x, y, True])
                self.path.append([x + 1, y + 1, False])
                x, y = x + 1, y + 1
            elif y + 1 < visual_board.height and board[y + 1][x - 1] == wave and\
                    board[y][x - 1] == board[y - 1][x - 1] == board[y - 1][x] == -1:  # 1
                self.path.append([x, y, True])
                self.path.append([x - 1, y + 1, False])
                x, y = x - 1, y + 1
            elif y + 1 < visual_board.height and board[y + 1][x + 2] == wave and\
                    board[y][x + 2] == board[y - 1][x + 2] == board[y - 1][x + 1] == board[y - 1][x] == -1:  # 2
                self.path.append([x, y, True])
                self.path.append([x + 2, y + 1, False])
                x, y = x + 2, y + 1
            elif y + 1 < visual_board.height and board[y + 1][x - 2] == wave and\
                    board[y][x - 2] == board[y - 1][x - 2] == board[y - 1][x - 1] == board[y - 1][x] == -1:  # 2
                self.path.append([x, y, True])
                self.path.append([x - 2, y + 1, False])
                x, y = x - 2, y + 1
            elif y + 2 < visual_board.height and board[y + 2][x + 1] == wave and\
                    board[y + 1][x + 1] == board[y][x + 1] == -1:  # 3
                self.path.append([x, y, True])
                self.path.append([x + 1, y + 2, False])
                x, y = x + 1, y + 2
            elif y + 2 < visual_board.height and board[y + 2][x - 1] == wave and\
                    board[y + 1][x - 1] == board[y][x - 1] == -1:  # 3
                self.path.append([x, y, True])
                self.path.append([x - 1, y + 2, False])
                x, y = x - 1, y + 2
            elif y + 2 < visual_board.height and board[y + 2][x + 2] == wave and\
                    board[y + 1][x + 2] == board[y][x + 2] == board[y][x + 1] == -1:  # 4
                self.path.append([x, y, True])
                self.path.append([x + 2, y + 2, False])
                x, y = x + 2, y + 2
            elif y + 2 < visual_board.height and board[y + 2][x - 2] == wave and\
                    board[y + 1][x - 2] == board[y][x - 2] == board[y][x - 1] == -1:  # 4
                self.path.append([x, y, True])
                self.path.append([x - 2, y + 2, False])
                x, y = x - 2, y + 2
        self.path = self.path[::-1]
        print('!----------------------!')
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == -1:
                    print(board[i][j], end=' ')
                else:
                    print(' ' + str(board[i][j]), end=' ')
            print()
        print('!----------------------!')


class Platform(pygame.sprite.Sprite):
    def __init__(self, coords_cell):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        visual_board.set_values(coords_cell, 1)
        self.rect.center = visual_board.get_coords_platform(coords_cell)


if __name__ == '__main__':
    visual_board = VisualBoard()
    character_sprites, platform_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    player = Player()
    for _ in range(1):
        Enemy()
    platform_sprites.add(Platform((2, 5)), Platform((3, 5)), Platform((4, 5)),
                         Platform((6, 4)), Platform((7, 4)), Platform((8, 2)))
    game = Game()
