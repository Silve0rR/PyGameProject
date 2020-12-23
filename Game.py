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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 5:
            self.rect.x -= 5
        if keys[pygame.K_d] and self.rect.right < WIDTH - 5:
            self.rect.x += 5

        self.rect.y += self.fall  # Падение
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5


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
    platform_sprites.add(Platform((100, 600)))
    game = Game()
