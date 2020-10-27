import pygame
import pygame_menu
from math import cos, sin, pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (64, 64, 64)

colors = {
    '1' : (0, 110, 144),
    '2' : (241, 228, 232),
    '3' : (20, 13, 79),
    '4' : (129, 166, 132),
    '5' : (242, 67, 51),
}

textures = {
    '1': pygame.image.load('assets/wall1.jpg'),
    '2': pygame.image.load('assets/wall2.jpeg'),
    '3': pygame.image.load('assets/wall3.jpg'),
    '4': pygame.image.load('assets/wall4.jpeg'),
    '5': pygame.image.load('assets/wall5.jpg')
}


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        self.blocksize = 50
        self.wallHeight = 50
        self.stepSize = 5
        self.setColor(WHITE)
        self.player = {
            "x" : 75,
            "y" : 175,
            "angle" : 0,
            "fov" : 60
        }

    def setColor(self, color):
        self.blockColor = color

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def drawRect(self, x, y, tex):
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize))
        rect = tex.get_rect()
        rect = rect.move((x, y))
        self.screen.blit(tex, rect)

    def drawPlayerIcon(self, color):
        rect = (int(self.player['x'] - 2), int(self.player['y'] - 2), 5, 5)
        self.screen.fill(color, rect)

    def castRay(self, a):
        rads, dist = a * pi / 180, 0

        while True:
            x, y = int(self.player['x'] + dist * cos(rads)), int(self.player['y'] + dist * sin(rads))
            i, j = int(x / self.blocksize), int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitX = x - i * self.blocksize
                hitY = y - j * self.blocksize
                maxHit = hitX if 1 < hitX < self.blocksize - 1 else hitY
                tx = maxHit / self.blocksize
                return dist, self.map[j][i], tx

            self.screen.set_at((x, y), WHITE)
            dist += 2

    def render(self):

        halfWidth, halfHeight = int(self.width / 2), int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i, j = int(x / self.blocksize), int(y / self.blocksize)

                if self.map[j][i] != ' ':
                    self.drawRect(x, y, textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, wallType, tx = self.castRay(angle)

            x = halfWidth + i
            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180 )) * self.wallHeight

            start, end = int(halfHeight - h / 2), int(halfHeight + h / 2)
            img = textures[wallType]
            tx = int(tx * img.get_width())

            for y in range(start, end):
                ty = (y - start) / (end - start)
                ty = int(ty * img.get_height())
                texColor = img.get_at((tx, ty))
                self.screen.set_at((x, y), texColor)

        for i in range(self.height):
            self.screen.set_at((halfWidth, i), BLACK)
            self.screen.set_at((halfWidth + 1, i), BLACK)
            self.screen.set_at((halfWidth - 1, i), BLACK)

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
r.load_map('map.txt')

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
