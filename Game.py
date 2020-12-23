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


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.Surface((50, 100))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.fall = 5
        self.jump = [False, -25]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 5:
            self.rect.x -= 6
        if keys[pygame.K_d] and self.rect.right < WIDTH - 5:
            self.rect.x += 6
        if not self.jump[0]:
            if keys[pygame.K_SPACE]:
                self.jump[0] = True
        else:
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
        else:
            self.fall = 5

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
    def __init__(self, coords):
        super().__init__()
        self.image = pygame.Surface((210, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect()
        self.rect.center = coords


if __name__ == '__main__':
    character_sprites, platform_sprites = pygame.sprite.Group(), pygame.sprite.Group()
    player = Player(character_sprites)
    platform_sprites.add(Platform((570, 520)), Platform((350, 520)), Platform((950, 400)),
                         Platform((570, 220)))
    game = Game()
