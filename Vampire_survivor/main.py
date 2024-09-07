from settings import *
from Player import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # Sound setup
        self.game_music = pygame.mixer.Sound(join('audio', 'music.wav'))
        self.game_music.play(loops = -1)
        # sprites groups
        self.all_sprites = pygame.sprite.Group()

        # creating sprites objects
        self.player = Player(self.all_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)
            self.display_surface.fill('#3a2e3f')  # rosybrown1
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()

    def change_sound(self, volume):
        self.game_music.set_volume(volume)




if __name__ == '__main__':
    game = Game()
    game.run()