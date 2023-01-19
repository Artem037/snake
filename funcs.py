import sys
import os
import pygame
import random
import math
import sqlite3
from classes import Apple


def limcheck(obj, w, h, sn_size):
    if obj.x > w:
        obj.x = sn_size
    if obj.x < 0:
        obj.x = w - sn_size
    if obj.y > h:
        obj.y = sn_size
    if obj.y < 0:
        obj.y = h - sn_size


def key_getting(keys):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return keys["UP"]
            elif event.key == pygame.K_DOWN:
                return keys["DOWN"]
            elif event.key == pygame.K_LEFT:
                return keys["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return keys["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            sys.exit()


def respawnApple(apples, index, sx, sy, w, h):
    radius = math.sqrt((w / 2 * w / 2 + h / 2 * h / 2)) / 2
    angle = 999
    while angle > radius:
        angle = random.uniform(0, 800) * math.pi * 2
        x = w / 2 + radius * math.cos(angle)
        y = h / 2 + radius * math.sin(angle)
        if x == sx and y == sy:
            continue
    newApple = Apple(x, y, 1)
    apples[index] = newApple


def respawnApples(apples, quantity, sx, sy, w, h, ap_size):
    counter = 0
    del apples[:]
    radius = math.sqrt((w / 2 * w / 2 + h / 2 * h / 2)) / 2
    angle = 999
    while counter < quantity:
        while angle > radius:
            angle = random.uniform(0, 800) * math.pi * 2
            x = w / 2 + radius * math.cos(angle)
            y = h / 2 + radius * math.sin(angle)
            if ((x - ap_size == sx or x + ap_size == sx) and (
                    y - ap_size == sy or y + ap_size == sy) or radius - angle <= 10):
                continue
        apples.append(Apple(x, y, 1))
        angle = 999
        counter += 1


def score_drawing(score, score_numb_font, w, screen, score_msg, score_msg_size):
    score_numb = score_numb_font.render(str(score), 1, pygame.Color("red"))
    screen.blit(score_msg, (w - score_msg_size[0] - 60, 10))
    screen.blit(score_numb, (w - 45, 14))


def game_time_drawing(gameTime, score_font, score_numb_font, screen):
    game_time = score_font.render("Time:", 1, pygame.Color("green"))
    game_time_numb = score_numb_font.render(str(gameTime / 1000), 1, pygame.Color("red"))
    screen.blit(game_time, (30, 10))
    screen.blit(game_time_numb, (105, 14))

  
def get_res():
    # вывод результатов
    with sqlite3.connect('snake_database.db') as db:
        cursor = db.cursor()

        query2 = '''SELECT * from players'''

        data = cursor.execute(query2).fetchall()

        db.commit()
        cursor.close()
    if data:
        return data


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen, clock, FPS, w, h):
    intro_text = ["ЗМЕЙКА", "",
                  "Нажмите любую кнопку,",
                  "чтобы начать игру."]
    fon = pygame.transform.scale(load_image('fon.jpeg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def resupdate(res):
    # сохранение результатов
    with sqlite3.connect('snake_database.db') as db:
        cursor = db.cursor()

        query = f"""INSERT INTO players(points) VALUES ({res})"""
        cursor.execute(query)

        db.commit()
        cursor.close()
