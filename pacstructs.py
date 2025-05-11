import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class SearchNode():
    def __init__(self, location=None, parent=None):
        self.gridloc = location
        self.f = 0
        self.g = 0
        self.parent = parent

class GridCell():
    def __init__(self):
        self.gridloc = [0, 0]
        self.pixelloc = [0, 0]
        self.traversable = False
        self.coin = False
        self.trap = False
        self.powerup = False
        self.dynamic = False  # For dynamic walls

class PacMan(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pacmanright.png").convert()
        self.rect = self.image.get_rect()
        self.gridloc = [7, 7]
        self.goal_cell = [7, 7]
        self.dir = "n"
        self.coins = 0
        self.powered = False
        self.power_timer = 0
        self.trapped = False
        self.trap_timer = 0

    def update(self):
        if self.dir == 'r':
            self.rect.x += 1
        elif self.dir == 'l':
            self.rect.x -= 1
        elif self.dir == 'u':
            self.rect.y -= 1
        elif self.dir == 'd':
            self.rect.y += 1

        if (self.goal_cell[0] * 40 == self.rect.x) and (self.goal_cell[1] * 40 == self.rect.y):
            self.dir = 'n'
            self.gridloc = self.goal_cell

    def draw(self, screen):
        if self.dir == 'r':
            self.image = pygame.image.load("pacmanright.png").convert()
        elif self.dir == 'l':
            self.image = pygame.image.load("pacmanleft.png").convert()
        elif self.dir == 'd':
            self.image = pygame.image.load("pacmandown.png").convert()
        elif self.dir == 'u':
            self.image = pygame.image.load("pacmanup.png").convert()

        screen.blit(self.image, [self.rect.x, self.rect.y])

class Ghost(pygame.sprite.Sprite):
    def __init__(self, color, start_x=9, start_y=9):
        super().__init__()
        if color == "orange":
            self.image = pygame.image.load("OrangeGhost.png").convert()
            self.image.set_colorkey(WHITE)
        elif color == "red":
            self.image = pygame.image.load("RedGhost.png").convert()
            self.image.set_colorkey(WHITE)
        elif color == "green":
            self.image = pygame.image.load("GreenGhost.png").convert()
            self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = start_x * 40
        self.rect.y = start_y * 40
        self.gridloc = [start_x, start_y]
        self.goal_cell = [start_x, start_y]
        self.dir = "n"

    def update(self):
        if self.dir == 'r':
            self.rect.x += 1
        elif self.dir == 'l':
            self.rect.x -= 1
        elif self.dir == 'u':
            self.rect.y -= 1
        elif self.dir == 'd':
            self.rect.y += 1

        if (self.goal_cell[0] * 40 == self.rect.x) and (self.goal_cell[1] * 40 == self.rect.y):
            self.dir = 'n'
            self.gridloc = self.goal_cell

    def draw(self, screen):
        screen.blit(self.image, [self.rect.x, self.rect.y])
