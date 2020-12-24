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


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
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

        self.rect.y += self.fall  # Падение
        y = self.rect.y
        self.collision()
        if self.rect.bottom > HEIGHT - 11:
            self.rect.bottom = HEIGHT - 11
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


class Platform(pygame.sprite.Sprite):
    def __init__(self, coords_cell):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        visual_board.set_values(coords_cell, 1)
        self.rect.center = visual_board.get_coords(coords_cell)


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

    def get_coords(self, coords_cell):
        if self.board[coords_cell[1]][coords_cell[0]] == 1:
            return [100 * coords_cell[0] + 50, 100 * coords_cell[1] + 70]


if __name__ == '__main__':
    visual_board = VisualBoard()
    character_sprites, platform_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    player = Player(character_sprites)
    platform_sprites.add(Platform((5, 5)), Platform((4, 5)), Platform((3, 5)), Platform((8, 4)),
                         Platform((6, 2)))
    game = Game()
