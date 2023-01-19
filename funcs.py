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
