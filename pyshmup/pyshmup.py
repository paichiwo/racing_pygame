import random
import sys
import pygame
import pygame._sdl2 as pg_sdl2
from src.player import Player, Fumes
from src.background import Background
from src.enemy import Enemy
from src.explosion import Explosion
from src.dashboard import Dashboard
from src.game_over_screen import GameOverScreen


class Game:

    def __init__(self):

        # Game constants
        self.window_width = 320
        self.window_height = 180
        self.scale = 4
        self.fps = 120
        self.running = True

        # Game setup
        pygame.init()
        pygame.display.set_caption("pyshump")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height),
                                              flags=pygame.RESIZABLE | pygame.HIDDEN | pygame.SCALED,
                                              vsync=1)
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pg_sdl2.Window.from_display_module()
        self.window.size = (self.window_width * self.scale, self.window_height * self.scale)
        self.window.position = pg_sdl2.WINDOWPOS_CENTERED
        self.window.show()

        # Create game objects
        self.game_over_screen = GameOverScreen(self.window_width, self.window_height, self.screen)
        self.dashboard = Dashboard(self.screen)
        self.bg = Background(self.screen, self.window_height)
        self.player = Player(self.bg.bg_1.get_width(), self.window_height)
        self.fumes = Fumes()
        self.player_sprite = pygame.sprite.Group(self.fumes, self.player)
        self.enemy_sprite_group = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # timer_1
        self.enemy_timer_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer_1, 1500)

        self.last_collision_time = 0

        self.god_mode = False
        self.god_timer = None

    def handle_events(self, event):
        """Handle game events"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.running:
            if event.type == self.enemy_timer_1:
                pygame.time.set_timer(self.enemy_timer_1, random.randint(500, 1500))
                width = self.bg.bg_1.get_width()
                height = self.window_height
                choice = random.choice(["sm", "sm", "sm", "sm", "sm", "md", "md", "lg"])
                self.enemy_sprite_group.add(Enemy(self.screen, width, height, choice, self.player.rect))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.running = True

    def update_game(self):
        """Update all game objects"""
        self.screen.fill("black")

        self.bg.update()
        self.player_sprite.draw(self.screen)
        self.player.shots.draw(self.screen)
        self.player.update()
        self.fumes.update((self.player.rect.midbottom[0], self.player.rect.midbottom[1]+8))
        self.enemy_sprite_group.draw(self.screen)
        self.enemy_sprite_group.update()
        self.shot_collide()
        self.player_enemy_collide()
        self.enemy_shot_collide()
        self.explosions.draw(self.screen)
        self.explosions.update()
        self.dashboard.update(self.player.lives, self.player.cur_energy, self.player.max_energy)
        self.check_god_mode()

    def shot_collide(self):
        """When shot collides with the Enemy"""
        for shot in self.player.shots:
            hits = pygame.sprite.spritecollide(shot, self.enemy_sprite_group, False)
            if hits:
                shot.kill()
                for hit_enemy in hits:
                    hit_enemy.energy -= self.player.shot_power
                    self.dashboard.score += hit_enemy.shot_score
                    self.explosions.add(Explosion(hit_enemy.rect.center))
                for enemy in self.enemy_sprite_group:
                    if enemy.energy <= 0:
                        enemy.destroy()
                        self.explosions.add(Explosion(enemy.rect.center))
                        self.dashboard.score += enemy.kill_score

    def player_enemy_collide(self):
        collision_detected = False
        cur_time = pygame.time.get_ticks()

        for enemy in self.enemy_sprite_group:
            if (
                pygame.sprite.collide_mask(self.player, enemy)
                and not collision_detected
                and not self.god_mode
            ):
                if cur_time - self.last_collision_time >= 500:
                    self.player.get_damage(enemy.bump_power)
                    self.explosions.add(Explosion(self.player.rect.center))
                    self.last_collision_time = pygame.time.get_ticks()
                    self.deduct_life()

    def enemy_shot_collide(self):
        """When shot collides with the Enemy"""
        for sprite in self.enemy_sprite_group.sprites():
            for shot in sprite.shots:
                hits = pygame.sprite.collide_mask(shot, self.player)
                if hits:
                    shot.kill()
                    self.player.cur_energy -= sprite.shot_power
                    self.explosions.add(Explosion(shot.rect.center))
                    self.deduct_life()

    def deduct_life(self):
        if self.player.cur_energy <= 0:
            self.player.cur_energy = 100
            if self.player.lives > 0:
                self.player.lives -= 1
                self.god_mode = True
                self.god_timer = pygame.time.get_ticks() + 2000
                self.enemy_sprite_group.empty()

    def check_god_mode(self):
        if self.god_mode and pygame.time.get_ticks() >= self.god_timer:
            self.god_mode = False
        if self.god_mode:
            self.player.god_mode()

    def game_over(self):
        return not self.player.lives <= 0

    def reset_game_values(self):
        self.dashboard.score = 0
        self.player.lives = 4
        self.player.cur_energy = 100
        self.god_mode = False

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                self.handle_events(event)
            if self.running:
                self.update_game()
                self.running = self.game_over()
            else:
                self.game_over_screen.show()
                self.reset_game_values()
                self.enemy_sprite_group.empty()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()
