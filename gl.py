import pygame
import pygame_menu
from math import cos, sin, pi, atan2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (64, 64, 64)
SPRITE_BACKGROUND = (100, 0, 100, 200)

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

enemies = [
    {
        "x": 100,
        "y": 220,
        "texture" : pygame.image.load('assets/enemy1.png')
    },
    {
        "x": 270,
        "y": 220,
        "texture" : pygame.image.load('assets/enemy2.png')
    },
    {
        "x": 470,
        "y": 420,
        "texture" : pygame.image.load('assets/enemy3.png')
    }
]

gemas = {
    0: {
        "x": 100,
        "y": 175,
        "texture" : pygame.image.load('assets/gema.png')
    },
    1: {
        "x": 250,
        "y": 420,
        "texture" : pygame.image.load('assets/gema.png')
    },
    2: {
        "x": 450,
        "y": 420,
        "texture" : pygame.image.load('assets/gema.png')
    }
}


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.current_level = 0
        self.current_gema = None
        self.map = []
        self.zbuffer = [-float('inf') for z in range(int(self.width / 2))]
        self.blocksize = 50
        self.wallHeight = 50
        self.stepSize = 5
        self.player = {
            "x" : 75,
            "y" : 175,
            "angle" : 0,
            "fov" : 60
        }

    def load_map(self, filename):
        self.map = []
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

    def drawSprite(self, sprite, size):
        spriteDist = ((self.player['x'] - sprite['x'])**2 + (self.player['y'] - sprite['y'])**2) ** 0.5
        spriteAngle = atan2(sprite['y'] - self.player['y'], sprite['x'] - self.player['x'])

        aspectRatio = sprite["texture"].get_width() / sprite["texture"].get_height()
        if spriteDist != 0:
            spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        angleRads = self.player['angle'] * pi / 180
        fovRads = self.player['fov'] * pi / 180

        startX, startY = (self.width * 3 / 4) + (spriteAngle - angleRads) * (self.width/2) / fovRads - (spriteWidth/2), (self.height / 2) - (spriteHeight / 2)
        startX, startY = int(startX), int(startY)

        for x in range(startX, int(startX + spriteWidth)):
            for y in range(startY, int(startY + spriteHeight)):
                if (self.width / 2) < x < self.width:
                    if self.zbuffer[ x - int(self.width/2)] >= spriteDist:
                        tx = int((x - startX) * sprite["texture"].get_width() / spriteWidth )
                        ty = int((y - startY) * sprite["texture"].get_height() / spriteHeight )
                        texColor = sprite["texture"].get_at((tx, ty))
                        if texColor[3] > 128 and texColor != SPRITE_BACKGROUND:
                            self.screen.set_at((x, y), texColor)
                            self.zbuffer[x - int(self.width/2)] = spriteDist

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

            self.zbuffer[i] = dist
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
        
        for enemy in enemies:
            self.screen.fill(pygame.Color("black"), (enemy['x'], enemy['y'], 3, 3))
            self.drawSprite(enemy, 15)

        self.current_gema = gemas[self.current_level]
        if (int(self.current_gema['x']) in range(int(self.player['x'] - 5), int(self.player['x'] + 5))) and (int(self.current_gema['y']) in range(int(self.player['y'] - 5), int(self.player['y'] + 5))):
            self.current_level += 1
            self.current_gema = gemas[self.current_level]
            self.load_map('map{}.txt'.format(self.current_level))
            pygame.display.update()

        self.screen.fill(pygame.Color("black"), (self.current_gema['x'], self.current_gema['y'], 3, 3))
        self.drawSprite(self.current_gema, 15)

        for i in range(self.height):
            self.screen.set_at((halfWidth, i), BLACK)
            self.screen.set_at((halfWidth + 1, i), BLACK)
            self.screen.set_at((halfWidth - 1, i), BLACK)
