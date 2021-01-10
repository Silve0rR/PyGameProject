import pygame
import os

size = width, height = 1270, 750
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Меню')


class Cur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_cur)
        self.image = load_image("cur.png")  # загружает спрайт
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()

    def get_coords(self, coords):
        self.rect.x, self.rect.y = coords


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
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
    else:
        image = image.convert_alpha()

    return image


all_cur = pygame.sprite.Group()  # курсор

image1 = load_image("FON1.jpg")  # загрузка фона
image11 = pygame.transform.scale(image1, (1280, 750))

if __name__ == '__main__':
    cur = Cur()

    running, draw_sprite = True, False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cur.get_coords(event.pos)
                if pygame.mouse.get_focused():
                    draw_sprite = True
                else:
                    draw_sprite = False

        screen.blit(image11, (0, 0))
        pygame.mouse.set_visible(False)  # скрывает курсор

        if draw_sprite:
            all_cur.draw(screen)
        pygame.display.flip()