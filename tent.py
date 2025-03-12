import pygame
from settings import *

class Tent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = BROWN
        self.health = 1000
        self.max_health = 1000
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibujar barra de salud
        health_width = self.width
        health_height = 10
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 20, health_width * (self.health / self.max_health), health_height))
