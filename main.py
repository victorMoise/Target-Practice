import pygame
import os
import random

pygame.init()

CLOCK = pygame.time.Clock()
FPS = 144
SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
WHITE = (255, 255, 255)


BACKGROUND_IMAGE = pygame.image.load(os.path.join("images/background.png"))
CROSSHAIR = pygame.image.load(os.path.join("images/crosshair small.png"))
TARGET = pygame.image.load(os.path.join("images/target.png"))
TARGET = pygame.transform.scale(TARGET, (50, 50))

FONT = pygame.font.SysFont("Times New Roman", 64)


class Player(pygame.sprite.Sprite):
    def __init__(self, source):
        super().__init__()
        self.image = source
        self.rect = self.image.get_rect()
        self.rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
        self.shot = pygame.mixer.Sound("sounds/gunshot.mp3")
        self.hit = pygame.mixer.Sound("sounds/hitmarker.mp3")

    def shoot(self, player, targets, score):
        self.shot.play()
        if pygame.sprite.spritecollide(player, targets, True):
            score += 1
        return score

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):
    def __init__(self, source, pos_y, pos_x):
        super().__init__()
        self.image = source
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]


def draw_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    return screen


def update_score(screen, score):
    height = 50
    display_score = FONT.render("SCORE: ", False, WHITE)
    text_rect = display_score.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2, height)
    show_score = FONT.render(str(score), 0, WHITE)
    screen.blit(display_score, text_rect)
    screen.blit(show_score, (SCREEN_WIDTH / 2 + 125, 15))


def main():
    screen = draw_screen()
    pygame.display.set_caption("Target Practice")

    player = Player(CROSSHAIR)
    crosshair = pygame.sprite.Group()
    crosshair.add(player)

    targets = pygame.sprite.Group()
    number_of_targets = 25

    score = 0

    for i in range(number_of_targets):
        position_x = random.randint(150, SCREEN_HEIGHT - 50)
        position_y = random.randint(50, SCREEN_WIDTH - 50)
        target = Target(TARGET, position_x, position_y)
        targets.add(target)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                score = player.shoot(player, targets, score)
        pygame.display.update()
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        targets.draw(screen)
        crosshair.draw(screen)
        update_score(screen, score)
        crosshair.update()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()
