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


class Main_menu(pygame.sprite.Sprite):

    def __init__(self, name_file, coord_x, coord_y, size_x, size_y):
        super().__init__(all_sprites_main_menu)

        self.image = load_image(name_file)  # загружает спрайт
        self.image = pygame.transform.scale(self.image, (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord_x, coord_y

    def get_cords(self,  last_y):
        if self.rect.y < last_y:
            self.rect.y += 20


class Options_background(pygame.sprite.Sprite):  # настройки

    def __init__(self, name_file, coord_x, coord_y, size_x, size_y):
        super().__init__(all_Background_options)

        self.image = load_image(name_file)  # загружает спрайт
        self.image = pygame.transform.scale(self.image, (size_x, size_y))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord_x, coord_y

    def get_left(self, last_x):
        if self.rect.x > last_x:
            self.rect.x -= 40

    def get_right(self, last_x):
        if self.rect.x < last_x:
            self.rect.x += 40


all_Background_options = pygame.sprite.Group()  # настройки
all_sprites_main_menu = pygame.sprite.Group()  # кнопки: Старт, Настройки, Выход
all_cur = pygame.sprite.Group()  # курсор

image1 = load_image("FON1.jpg")  # загрузка фона
image11 = pygame.transform.scale(image1, (1280, 750))

if __name__ == '__main__':
    cur = Cur()

    # меню
    start = Main_menu("START_RUSSIA.png", width // 2 - 150, -500, 300, 100)  # кнопка Старт(Start)
    options = Main_menu("OPTIONS_RUSSIA.png", width // 2 - 125, -300, 250, 70)  # кнопка Настройки(Options)
    exit = Main_menu("EXIT_RUSSIA.png", width // 2 - 75, -100, 150, 50)  # кнопка Выход(Exit)

    # настройки_фон
    background_fon = Options_background("Прозрачный фон.png", width, 0, 1280, 750)  # прозрачный фон

    running, draw_sprite = True, False

    background_options = False
    while running:
        pygame.mouse.set_visible(False)  # скрывает курсор
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                cur.get_coords(event.pos)
                if pygame.mouse.get_focused():
                    draw_sprite = True
                else:
                    draw_sprite = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if width // 2 - 125 < x < width // 2 + 115 and 320 < y < 390:
                    background_options = True

        start.get_cords(200)
        options.get_cords(320)
        exit.get_cords(400)

        screen.blit(image11, (0, 0))
        all_sprites_main_menu.draw(screen)
        all_Background_options.draw(screen)

        if background_options:
            background_fon.get_left(0)
        else:
            background_fon.get_right(width)

        if draw_sprite:
            all_cur.draw(screen)
        pygame.time.Clock().tick(60)
        pygame.display.flip()