import pygame, sys, time
from settings import *
from sprites import BG, Ground, Helicopter, Obstacle


class Game:
    def __init__(self):

        # установка
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Mountain Peaks')
        self.clock = pygame.time.Clock()
        self.active = True

        # группа спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # масштабный коэффициент
        bg_height = pygame.image.load('../GAMEINPYTHON/graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # установка спрайтов
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.helicopter = Helicopter(self.all_sprites, self.scale_factor / 1.5)

        # таймер
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
        self.start_offset = 0

        # текст
        self.font = pygame.font.Font('../GAMEINPYTHON/graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.bestscore_s = open('bestscore.txt', 'r+')
        self.bestscore = int(self.bestscore_s.read())
        self.bestscore_s.close()

        # меню
        self.menu_surf = pygame.image.load('../GAMEINPYTHON/graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # музыка
        self.music = pygame.mixer.Sound('../GAMEINPYTHON/sounds/8bit.mp3')
        self.music.set_volume(0.09)
        self.music.play(loops = -1)

    def collisions(self):
        if pygame.sprite.spritecollide(self.helicopter, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.helicopter.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.helicopter.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            self.filescore = open('../GAMEINPYTHON/score.txt', 'w')
            self.filescore.write(str(self.score))
            self.filescore.close()

            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 4 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)


    def display_bestscore(self):
        if self.active:
            if self.score > int(self.bestscore):
                self.bestscore = self.score
                self.bestscore_s = open('bestscore.txt', 'r+')
                self.bestscore_s.seek(0)
                self.bestscore_s.write(str(self.bestscore))
                self.bestscore_s.close()

            y = WINDOW_HEIGHT * 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.bestscore), True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            # время перепада
            dt = time.time() - last_time
            last_time = time.time()

            # цикл событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.helicopter.jump()
                    else:
                        self.helicopter = Helicopter(self.all_sprites, self.scale_factor / 1.5)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.2)


            # игровая логика
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            self.display_bestscore()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()

