import pygame
from gl import *
import math

def updateFPS():
    fps = str(int(clock.get_fps()))
    return font.render(fps, 1, pygame.Color("white"))

pygame.init()
screen = pygame.display.set_mode(
    (1000, 500),
    pygame.DOUBLEBUF | pygame.HWACCEL
)

screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

r = Raycaster(screen)
r.load_map('maps/map{}.txt'.format(r.current_level))

pygame.mixer.init()
pygame.mixer.music.load('assets/soundtrack.mp3')
pygame.mixer.music.play()

def game_loop():
    isRunning = True
    while isRunning:

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            newX = r.player['x']
            newY = r.player['y']

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    newX += cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY += sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    newX -= cos(r.player['angle'] * pi / 180) * r.stepSize
                    newY -= sin(r.player['angle'] * pi / 180) * r.stepSize
                elif ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    newX -= cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY -= sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    newX += cos((r.player['angle'] + 90) * pi / 180) * r.stepSize
                    newY += sin((r.player['angle'] + 90) * pi / 180) * r.stepSize
                elif ev.key == pygame.K_q or ev.key == pygame.K_z:
                    r.player['angle'] -= 5
                elif ev.key == pygame.K_e or ev.key == pygame.K_x:
                    r.player['angle'] += 5

                i, j = int(newX / r.blocksize), int(newY / r.blocksize)

                if r.map[j][i] == ' ':
                    r.player['x'] = newX
                    r.player['y'] = newY
            elif ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 4:
                    r.player["angle"] -= 5
                elif ev.button == 5:
                    r.player["angle"] += 5

        screen.fill(pygame.Color("gray"))
        screen.fill(pygame.Color("saddlebrown"), (int(r.width / 2), 0, int(r.width / 2), int(r.height / 2)))
        screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2), int(r.height / 2)))

        r.render()

        screen.fill(pygame.Color("black"), (0, 0, 30, 30))
        screen.blit(updateFPS(), (0, 0))
        clock.tick(30)

        pygame.display.update()

my_theme = pygame_menu.themes.THEME_BLUE.copy()

background_image = pygame_menu.baseimage.BaseImage(
    image_path = pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
    drawing_mode = pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)

my_theme.background_color = background_image
my_theme.widget_font = pygame_menu.font.FONT_8BIT

menu = pygame_menu.Menu(300, 400, 'Welcome to Walls', theme=my_theme)
menu.add_button('Play', game_loop)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.add_image('assets/wall5.jpg', scale=(0.5, 0.25))
menu.mainloop(screen)

pygame.quit()
