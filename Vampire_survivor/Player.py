from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        path = join('images', 'player', 'down', '0.png')
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.lives = 5
        self.mask = pygame.mask.from_surface(self.image)

    def loose_life(self):
        self.lives -= 1

    def gain_score(self):
        self.score += 1

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_a]) - int(
            keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_s]) + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_w]) - int(
            keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.speed * self.direction * dt  # to reduce power difference in computers

        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

