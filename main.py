import pygame
from sys import exit
import os
import math
import time
from cars import Enemy, Player

pygame.init()
pygame.font.init()

#! Window
WIDTH, HEIGHT = 700, 1000
icon = pygame.image.load(os.path.join("assets", "icon.png"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("Car Dodging")
# * Background
background = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT)
)


def collide(obj1, obj2):
    """
    Check if Objects are colliding
    *@param obj1: Object
    *@param obj2: Object
    """
    offsetX = obj2.x - obj1.x
    offsetY = obj2.y - obj1.y
    return obj2.mask.overlap(obj2.mask, (offsetX, offsetY))


def main():
    #! Create all the games variables
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
    enemyVelocity = 5
    lostCount = 0

    def redraw_window():
        timer_rounded = format(timer, ".1f")
        # * Create Fonts
        scoreFont = mainFont.render(f"Score: {math.floor(score)}", True, (0, 0, 0))
        lifesFont = mainFont.render(f"Lives {lifes}", True, (0, 0, 0))
        levelFont = mainFont.render(f"Level: {level}", True, (0, 0, 0))
        timerFont = mainFont.render(f"Chrono: {timer_rounded}", True, (0, 0, 0))
        #! Draw the background and Player
        screen.blit(background, (0, 0))
        if alive:
            screen.blit(player.carImg, (player.x, player.y))
        #! Draw the enemies
        for enemy in enemies:
            screen.blit(enemy.carImg, (enemy.x, enemy.y))
        #! Draw the Fonts
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
        #! Draw the lost Fonts
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

        #! Update the screen
        pygame.display.update()

    while run:
        clock.tick(FPS)

        #! Check the Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

        #! If the player is dead
        if dead:
            alive = False
            enemies = []
            if score > bestScore:
                bestScore = math.floor(score)
            lostCount += 1
            if lostCount > FPS * 3:
                # * Reset everything
                dead = False
                alive = True
                enemies = [Enemy(), Enemy(), Enemy(), Enemy(), Enemy()]
                score = 0.1
                lifes = 5
                lostCount = 0
                level = 1
                enemyVelocity = 5
                begin = time.perf_counter()
                player.x, player.y = WIDTH // 2, HEIGHT - 150

        #! If the player is alive
        elif alive:
            new_begin = time.perf_counter()
            timer = new_begin - begin
            score += 0.1
            enemyVelocity = level * 2

            #! Key Bindings
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

            #! Move and check collisions
            for enemy in enemies:
                enemy.move(enemyVelocity)
                if enemy.y > HEIGHT:
                    enemies.remove(enemy)
                if collide(player, enemy):
                    lifes -= 1
                    enemies.remove(enemy)

            #! Check the end of the wave
            if len(enemies) == 0 and alive:
                level += 1
                if changeWaveLenght:
                    enemies.append(Enemy())
                    waveLength += 2

            #! Check if the player loses
            if lifes <= 0:
                dead = True
            # ? if waveLength >= 16:
            # ?     changeWaveLenght = False

        #! Draw everything on the screen
        redraw_window()


if __name__ == "__main__":
    main()
