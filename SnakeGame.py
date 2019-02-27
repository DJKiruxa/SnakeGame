# -*- coding: utf-8 -*-
import pygame
import sys
import os
import random
import time
from Snake import Snake
from Food import Food

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image

class Camera:
    def __init__(self):
        global size
        self.dx = 2
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self):
        self.dx = 0
        self.dy = 0

class Game():
    def __init__(self):
        global gameover
        gameover = False
        # задаем размеры экрана
        self.screen_width = 720
        self.screen_height = 460
        self.size = self.screen_width, self.screen_height
        # необходимые цвета
        self.color = ['blue', 'red', 'yellow', 'purple', 'black', 'orange']
        self.red = pygame.Color('red')
        self.blue = pygame.Color(random.choice(self.color))
        self.black= pygame.Color('black')        self.green = pygame.Color('green')

        # будет задавать количество кадров в секунду
        self.fps_controller= pygame.time.Clock()

        # Отображение количества очков
        self.score= 0


    def init_and_check_for_errors(self):
        # Начальная функция для инициализации и
        # проверки как запустится pygame
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        # Задаем surface(поверхность поверх которой будет все рисоваться)
        # и устанавливаем загаловок окна
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')

    def event_loop(self, change_to):
        # Функция для отслеживания нажатий клавиш игроком

        # запускаем цикл по ивентам
        for event in pygame.event.get():
            # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def refresh_screen(self):
        # обновляем экран и задаем фпс
        pygame.display.flip()
        game.fps_controller.tick(5 + self.score * 0.75)

    def show_score(self, choice=1):
        # Отображение результата
        s_font = pygame.font.SysFont('monaco', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_overe отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (360, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        global gameover
        gameover = True
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        while True:
            back_screen = pygame.Surface(self.size)
            all_sprites = pygame.sprite.Group()
            sprite = pygame.sprite.Sprite()
            sprite.image = load_image("GameOver.png")
            sprite.rect = sprite.image.get_rect()
            
            all_sprites.add(sprite)
            sprite.rect.x = 0
            sprite.rect.y = 0
            all_sprites.draw(self.play_surface)
            back_screen.blit(self.play_surface, (0, 0))
            camera = Camera()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('y'):
                        main()
                    elif event.key == ord('n'):
                        pygame.quit()
                        sys.exit()
            self.play_surface.blit(
                back_screen, (sprite.rect.x - 0, sprite.rect.y + 0))
            if sprite.rect.x <= 728:
                for sprite in all_sprites:
                    camera.apply(sprite)

            pygame.display.flip()


def start_game():
    pygame.init()
    size = 720, 460
    screen = pygame.display.set_mode(size)
    fps = 100
    back_screen = pygame.Surface(size)
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("StartGame.png")
    sprite.rect = sprite.image.get_rect()

    all_sprites.add(sprite)
    sprite.rect.x = 0
    sprite.rect.y = 0
    all_sprites.draw(screen)
    back_screen.blit(screen, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                main()
        screen.fill(pygame.Color('white'))
        screen.blit(back_screen, (0, 0))


        pygame.display.flip()
        
def main():
    global game, food, snake, ganeover
    game = Game()
    snake = Snake(game.blue)
    food = Food(game.red, game.screen_width, game.screen_height)

    game.init_and_check_for_errors()
    game.set_surface_and_title()

    while gameover == False:
        snake.change_to = game.event_loop(snake.change_to)

        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(
            game.score, food.food_pos, game.screen_width, game.screen_height)
        snake.draw_snake(game.play_surface, game.green)

        food.draw_food(game.play_surface)

        snake.check_for_boundaries(
            game.game_over, game.screen_width, game.screen_height)

        game.show_score()
        game.refresh_screen()

start_game()