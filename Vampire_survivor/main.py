from settings import *
from Player import *
from Sprites import *
from pytmx.util_pygame import load_pygame

from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        # Sound setup
        self.game_music = pygame.mixer.Sound(join('audio', 'music.wav'))
        # self.game_music.play(loops = -1)

        # sprites groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # creating sprites objects
        self.player = Player((400,300), self.all_sprites, self.collision_sprites) #collision_sprites additional arg, player do not belong them


    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)
            self.display_surface.fill('#3a2e3f')

            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()

    def change_sound(self, volume):
        self.game_music.set_volume(volume)

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))


if __name__ == '__main__':
    game = Game()
    game.run()