import random
import sys
import pygame
from src.Road import Road
from src.Dashboard import DashBoard
from src.Player import Player
from src.Obstacle import Obstacle


class Game:

    def __init__(self):
        super().__init__()

        # Game constants
        self.window_width = 600
        self.window_height = 800
        self.fps = 60

        # Game setup
        pygame.init()
        pygame.display.set_caption("Racing Game")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()  # Game start time

        # Create game objects
        self.road = Road(self.screen, self.window_height)
        self.dashboard = DashBoard(self.screen, self.clock, self.start_time, self.window_width)
        self.player = Player()
        # self.obstacle = Obstacle(object_type="car")

        # Create sprites
        self.player_sprite = pygame.sprite.GroupSingle(self.player)
        self.obstacle_group = pygame.sprite.Group()

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

        self.running = True

    def reset_game_values(self):
        self.obstacle_group.empty()
        self.dashboard.game_start_time = pygame.time.get_ticks()
        self.road.increase = False
        self.road.acc = 0
        self.road.speed = 0
        self.dashboard.update(70, 0, 0)
        self.dashboard.reset()

    def game_over(self):
        """Game over condition"""
        if pygame.sprite.spritecollide(self.player_sprite.sprite, self.obstacle_group, False):
            return False
        else:
            return True

    def game_over_screen(self):
        self.screen.fill("blue")
        text = self.dashboard.font.render("GAME OVER", 0, "yellow")
        rect = text.get_rect(center=(self.window_width / 2, self.window_height / 2))
        self.screen.blit(text, rect)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.running:
                    if event.type == self.obstacle_timer:
                        if self.road.increase:
                            timer_value = int(3000 // self.road.acc) if self.road.acc != 0 else 1500
                            pygame.time.set_timer(self.obstacle_timer, timer_value)
                        else:
                            pygame.time.set_timer(self.obstacle_timer, random.randint(1000, 2000))
                        self.obstacle_group.add(Obstacle("car"))

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.running = True
                        self.reset_game_values()

            if self.running:
                self.road.update()
                self.player_sprite.draw(self.screen)
                self.player.update()
                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update(self.road.increase, self.road.acc)
                if len(self.obstacle_group) > 0:
                    self.dashboard.update(self.road.speed, self.road.acc, self.obstacle_group.sprites()[0].rect.midbottom[1])
                else:
                    self.dashboard.update(self.road.speed, self.road.acc, 0)

                self.running = self.game_over()

            else:
                self.game_over_screen()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()
