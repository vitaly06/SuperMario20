import pygame

from funks_to_draw import *
import game_parametrs
from constants import *
from player import Player
from blocks import Platform, BlockDie, Door


def check(name):
    all_players = dict()
    with open("players.txt", "r") as file:
        for i in file:
            i = i.split(":")
            all_players[i[0]] = int(i[1])
    return all_players[name]


class Camera(object):  # камера
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIDTH / 2, -t + HEIGHT / 2

    l = min(0, l)
    l = max(-(camera.width - WIDTH), l)
    t = max(-(camera.height - HEIGHT), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)


def process_game(lvl, x, y):
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Super Mario')
    bg = pygame.image.load("data/fon.png")

    running = True
    clock = pygame.time.Clock()
    player = Player(x, y)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platforms = []  # все блоки и т.д
    entities.add(player)
    level = LEVELS[lvl]  # получаем уровень игрока
    x = y = 0  # координаты
    # отрисовка уровня
    for row in level:
        for col in row:
            if col == "-" and lvl in [1, 2]:
                pf = Platform(x, y, 'data/platform.png')
                entities.add(pf)
                platforms.append(pf)
            elif lvl == 3 and col == '-':
                pf = Platform(x, y, 'data/snow_block.jpg')
                entities.add(pf)
                platforms.append(pf)
            elif lvl == 4 and col == '-':
                pf = Platform(x, y, 'data/block4.png')
                entities.add(pf)
                platforms.append(pf)
            elif lvl == 5 and col == '-':
                pf = Platform(x, y, 'data/block5.png')
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                if lvl in [1, 2, 3]:
                    bd = BlockDie(x, y, "data/dieBlock.png")
                else:
                    if lvl == 4:
                        bd = BlockDie(x, y, 'data/cactus_enemy.png')
                    elif lvl == 5:
                        bd = BlockDie(x, y, 'data/bomb.png')
                entities.add(bd)
                platforms.append(bd)
            if col == 'l':
                bd = BlockDie(x, y, "data/lava.jpg")
                entities.add(bd)
                platforms.append(bd)
            if col == 's':
                bd = BlockDie(x, y, "data/spike.png")
                entities.add(bd)
                platforms.append(bd)
            if col == 'd':
                door = Door(x, y - 32, 'data/door.png')
                entities.add(door)
                platforms.append(door)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # ширина уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высота
    camera = Camera(camera_configure, total_level_width, total_level_height)
    while running:
        print(game_parametrs.game_over)
        # screen.fill(pygame.image.load('data/fon.png'))
        screen.blit(bg, (0, 0))
        while game_parametrs.game_over:
            # print("говно")
            for j in pygame.event.get():
                if j.type == pygame.QUIT:
                    exit()
                # if game_parametrs.game_over == False:
                #     break
                restart = pygame.sprite.Sprite()
                restart.image = pygame.transform.scale(load_image("restart.png"), (400, 120))
                restart.rect = restart.image.get_rect()
                restart.rect.x = 300
                restart.rect.y = 150
                go_to_level_menu = pygame.sprite.Sprite()
                go_to_level_menu.image = pygame.transform.scale(load_image("go_to_level_menu.png"), (400, 120))
                go_to_level_menu.rect = go_to_level_menu.image.get_rect()
                go_to_level_menu.rect.x = 300
                go_to_level_menu.rect.y = 360
                drawing = pygame.sprite.Group()
                drawing.add(restart)
                drawing.add(go_to_level_menu)
                drawing.draw(screen)
                k = 0
                for i in drawing:
                    if j.type == pygame.MOUSEBUTTONDOWN and \
                            i.rect.collidepoint(j.pos) and j.button == 1:
                        if k == 0:
                            game_parametrs.game_over = False
                            player.teleporting(50, 50)
                            return
                        elif k == 1:
                            game_parametrs.game_over = False
                            game_parametrs.what_to_draw = "level_menu"
                            return
                    k += 1
            pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if game_parametrs.end_level:
                game_parametrs.what_to_draw = "level_menu"
                # game_parametrs.level[0] = check(game_parametrs.name)
                game_parametrs.level = (lvl, player.x, player.y)
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                game_parametrs.what_to_draw = "pause"
                print(player.x, player.y)
                game_parametrs.level = (lvl, player.x, player.y)
                return

            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False
        player.update(left, right, up, platforms)
        camera.update(player)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.flip()
        clock.tick(FPS)
        # print(game_parametrs.level[0])

# if __name__ == '__main__':
#     process_game()
