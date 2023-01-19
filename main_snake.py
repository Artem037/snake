import pygame
import random
from funcs import limcheck, resupdate, start_screen, game_time_drawing, score_drawing, \
    respawnApples, respawnApple, key_getting, load_image, get_res, terminate
from classes import Apple, Snake, checkCollision

pygame.init()
pygame.display.set_caption("Snake")
pygame.font.init()
sn_sp = 0.36
sn_size = 9
ap_size = 9
sep = 10
h = 600
w = 800
FPS = 25
keys = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}

screen = pygame.display.set_mode((w, h), pygame.HWSURFACE)

score_font = pygame.font.Font(None, 38)
score_numb_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 46)
play_again_font = score_numb_font
score_msg = score_font.render("Score:", 1, pygame.Color("green"))
score_msg_size = score_font.size("Score")

background_color = pygame.Color('Black')
black = pygame.Color('Black')

clock = pygame.time.Clock()


def db_showing(screen, clock, FPS, w, h):
    sp = [str(i[1]) for i in get_res()]
    if len(sp) > 10:
        sp = ', '.join([str(i[1]) for i in get_res()][-10:])
    else:
        sp = ', '.join([str(i[1]) for i in get_res()])
    ending_text = ["Предыдущие игры: ", "", sp]
    fon = pygame.transform.scale(load_image('fon.jpeg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in ending_text:
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                else:
                    main()
                    return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(FPS)


def exitScreen(res, time, screen, clock, FPS, w, h):
    ending_text = ["Игра окончена", "",
                   f'Ваш результат: {res}',
                   f'Ваше время: {time}',
                   "Нажмите любую кнопку,",
                   "чтобы начать игру.",
                   'Если хотите посмотреть предыдущие игры - нажмите q']
    fon = pygame.transform.scale(load_image('fon.jpeg'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in ending_text:
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    db_showing(screen, clock, FPS, w, h)
                    main()
                    return
                else:
                    main()
                    return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def main(startScreen=False):
    if startScreen:
        start_screen(screen, clock, FPS, w, h)
    score = 0
    player = Snake(w / 2, h / 2)
    player.setDirection(keys["UP"])
    player.move(sn_sp, FPS)
    start_segments = 3
    while start_segments > 0:
        player.grow(sn_size)
        player.move(sn_sp, FPS)
        start_segments -= 1
    max_apples = 1
    eaten_apple = False
    apples = [Apple(random.randint(60, w), random.randint(60, h), 1)]
    respawnApples(apples, max_apples, player.x, player.y, w, h, ap_size)
    time_start = pygame.time.get_ticks()
    final = 0
    while final != 1:
        clock.tick(FPS)
        key_pressed = key_getting(keys)
        if key_pressed == "exit":
            final = 1
        limcheck(player, w, h, sn_size)
        if player.checkCrash(sn_size):
            resupdate(score)
            exitScreen(score, int(pygame.time.get_ticks() - time_start) / 1000, screen, clock, FPS, w, h)
        for apple in apples:
            if apple.state == 1:
                if checkCollision(player.getHead(), sn_size, apple, ap_size):
                    player.grow(sn_size)
                    apple.state = 0
                    score += 5
                    eaten_apple = True
        if key_pressed:
            player.setDirection(key_pressed)
        player.move(sn_sp, FPS)
        if eaten_apple:
            eaten_apple = False
            respawnApple(apples, 0, player.getHead().x, player.getHead().y, w, h)
        screen.fill(background_color)
        for apple in apples:
            if apple.state == 1:
                apple.draw(screen, ap_size)
        player.draw(screen, sn_size)
        score_drawing(score, score_numb_font, w, screen, score_msg, score_msg_size)
        time = pygame.time.get_ticks() - time_start
        game_time_drawing(time, score_font, score_numb_font, screen)
        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main(startScreen=True)
