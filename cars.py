import pygame
import os
import random


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.carImg = None

    def get_height(self):
        return self.carImg.get_height()

    def get_width(self):
        return self.carImg.get_width()


class Player(Car):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.carImg = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "player.png")), (128, 80)
            ),
            -90,
        )
        self.mask = pygame.mask.from_surface(self.carImg)


class Enemy(Car):
    posMap = {1: [513, 53], 2: [404, 53], 3: [293, 53], 4: [189, 53]}
    colorMap = {
        "yellow": pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "yellow.png")), (128, 80)
            ),
            -90,
        ),
        "blue": pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "blue.png")), (140, 90)
            ),
            90,
        ),
        "red": pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "red.png")), (150, 80)
            ),
            -90,
        ),
        "white": pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "white.png")), (128, 80)
            ),
            90,
        ),
    }

    def __init__(self):
        self.x = self.posMap[random.randint(1, 4)][0] - 40
        self.y = self.posMap[random.randint(1, 4)][1] - random.randint(200, 1500)
        self.pos = (self.x, self.y)
        self.carImg = self.colorMap[random.choice(["yellow", "blue", "red", "white"])]
        self.mask = pygame.mask.from_surface(self.carImg)
        self.securityRangeX = self.carImg.get_width() + 50
        self.securityRangeY = self.carImg.get_height() + 50

    def move(self, vel):
        self.y += vel

    def check_spawn(self):
        pass
