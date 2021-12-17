import pygame
from sys import exit
import os
import math
import time
from cars import Enemy, Player

pygame.init()
pygame.font.init()

# Window
WIDTH, HEIGHT = 700, 1000
icon = pygame.image.load(os.path.join("assets", "icon.png"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("Car Dodging")
# Background
background = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT)
)


def collide(obj1, obj2):
    offsetX = obj2.x - obj1.x
    offsetY = obj2.y - obj1.y
    return obj2.mask.overlap(obj2.mask, (offsetX, offsetY))


def main():
    mainFont = pygame.font.SysFont("sans serif", 50)
    loseFont = pygame.font.SysFont("sans serif", 70)
    player = Player(WIDTH // 2, HEIGHT - 150)
    enemies = [Enemy(), Enemy(), Enemy(), Enemy(), Enemy()]
    begin = time.perf_counter()
    clock = pygame.time.Clock()
    bestScore = 0
    changeWaveLenght = True
    FPS = 60
    run = True
    alive = True
    dead = False
    score = 0.1
    waveLength = 5
    level = 1
    lifes = 5
    playerVelocity = 10

    def redraw_window():
        timer_rounded = format(timer, ".1f")
        # Create Fonts
        scoreFont = mainFont.render(f"Score: {math.floor(score)}", True, (0, 0, 0))
        lifesFont = mainFont.render(f"Lives {lifes}", True, (0, 0, 0))
        levelFont = mainFont.render(f"Level: {level}", True, (0, 0, 0))
        timerFont = mainFont.render(f"Chrono: {timer_rounded}", True, (0, 0, 0))
        # Draw the background and Player
        screen.blit(background, (0, 0))
        screen.blit(player.carImg, (player.x, player.y))
        # Draw the enemies
        for enemy in enemies:
            screen.blit(enemy.carImg, (enemy.x, enemy.y))
        # Draw the fonts
        screen.blit(scoreFont, (10, 10))
        screen.blit(lifesFont, (WIDTH - lifesFont.get_width() - 10, 10))
        screen.blit(levelFont, ((10, HEIGHT - levelFont.get_height() - 10)))
        screen.blit(
            timerFont,
            (
                WIDTH - timerFont.get_width() - 10,
                HEIGHT - timerFont.get_height() - 10,
            ),
        )
        if not alive:
            scoreFontLost = loseFont.render(
                f"Score: {math.floor(score)}", True, (0, 0, 0)
            )
            screen.blit(
                scoreFontLost,
                (
                    (WIDTH // 2 - (scoreFontLost.get_width() // 2)),
                    (HEIGHT // 2 - (scoreFontLost.get_height() // 2) - 60),
                ),
            )
            bestScoreFont = loseFont.render(f"Best Score: {bestScore}", True, (0, 0, 0))
            screen.blit(
                bestScoreFont,
                (
                    (WIDTH // 2 - (bestScoreFont.get_width() // 2)),
                    (HEIGHT // 2 - (bestScoreFont.get_height() // 2)),
                ),
            )
            levelFontLost = loseFont.render(f"Level: {level}", True, (0, 0, 0))
            screen.blit(
                levelFontLost,
                (
                    (WIDTH // 2 - (levelFontLost.get_width() // 2)),
                    (HEIGHT // 2 - (levelFontLost.get_height() // 2) + 60),
                ),
            )
        pygame.display.update()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        if dead:
            alive = False
            enemies = []
            if score > bestScore:
                bestScore = math.floor(score)
        elif alive:
            new_begin = time.perf_counter()
            timer = new_begin - begin
            for enemy in enemies:
                enemy.velocity += math.floor(timer // score)
            score += 0.2
            keysPressed = pygame.key.get_pressed()
            if (
                keysPressed[pygame.K_d]
                and (player.x + player.get_width()) < WIDTH - 100
            ):  # RIGHT
                player.x += playerVelocity
            if keysPressed[pygame.K_q] and (player.x) > 100:  # LEFT
                player.x -= playerVelocity
            if keysPressed[pygame.K_z] and player.y > 0:  # UP
                player.y -= playerVelocity
            if (
                keysPressed[pygame.K_s] and (player.y + player.get_height()) < HEIGHT
            ):  # DOWN
                player.y += playerVelocity
            for enemy in enemies:
                enemy.move(enemy.velocity)
                if enemy.y > HEIGHT:
                    enemies.remove(enemy)
                if collide(player, enemy):
                    lifes -= 1
            if len(enemies) == 0 and alive:
                level += 1
                if changeWaveLenght:
                    waveLength += 2
                for i in range(0, waveLength):
                    enemies.append(Enemy())
            if lifes <= 0:
                dead = True
            if waveLength > 12:
                changeWaveLenght = False
        redraw_window()


main()
