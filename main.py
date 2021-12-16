import random
import pygame
from sys import exit
import os
import math

from pygame import key
from pygame import time
from pygame.draw import rect
from pygame.sprite import collide_mask, collide_rect
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
    player = Player(WIDTH // 2, HEIGHT - 150)
    enemy = Enemy()
    enemies = [Enemy(), Enemy(), Enemy(), Enemy(), Enemy()]
    timer = 0.1
    clock = pygame.time.Clock()
    bestScore = 0
    changeWaveLenght = True
    FPS = 60
    run = True
    score = 0.1
    waveLength = 5
    level = 1
    health = 1000
    playerVelocity = 10
    enemyVelocity = 5

    def redraw_window():
        # Create Fonts
        scoreFont = mainFont.render(f"Score: {math.floor(score)}", True, (0, 0, 0))
        healthFont = mainFont.render(f"Health: {health}", True, (0, 0, 0))
        levelFont = mainFont.render(f"Level: {level}", True, (0, 0, 0))
        enemyNumberFont = mainFont.render(
            f"Number of Enemies: {waveLength}", True, (0, 0, 0)
        )
        # Draw the background and Player
        screen.blit(background, (0, 0))
        screen.blit(player.carImg, (player.x, player.y))
        # Draw the enemies
        for enemy in enemies:
            screen.blit(enemy.carImg, (enemy.x, enemy.y))
        # Draw the fonts
        screen.blit(scoreFont, (10, 10))
        screen.blit(healthFont, (WIDTH - healthFont.get_width() - 10, 10))
        screen.blit(levelFont, ((10, HEIGHT - levelFont.get_height() - 10)))
        screen.blit(
            enemyNumberFont,
            (
                WIDTH - enemyNumberFont.get_width() - 10,
                HEIGHT - enemyNumberFont.get_height() - 10,
            ),
        )
        pygame.display.update()

    while run:
        enemyVelocity = (score ** timer) ** 4
        timer += (timer // FPS) * 80
        score += timer
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        keysPressed = pygame.key.get_pressed()
        if (
            keysPressed[pygame.K_d] and (player.x + player.get_width()) < WIDTH - 100
        ):  # RIGHT
            player.x += playerVelocity
        if keysPressed[pygame.K_q] and (player.x) > 100:  # LEFT
            player.x -= playerVelocity
        if keysPressed[pygame.K_z] and (player.y + player.get_height()) > HEIGHT - (
            HEIGHT // 3
        ):  # UP
            player.y -= playerVelocity
        if (
            keysPressed[pygame.K_s] and (player.y + player.get_height()) < HEIGHT
        ):  # DOWN
            player.y += playerVelocity
        for enemy in enemies:
            enemy.move(enemyVelocity)
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
            if collide(player, enemy):
                health -= 1
        if len(enemies) == 0:
            level += 1
            if changeWaveLenght:
                waveLength += 2
            for i in range(0, waveLength):
                enemies.append(Enemy())
        if health <= 0:
            if score > bestScore:
                bestScore = score
        if waveLength > 12:
            changeWaveLenght = False


main()
