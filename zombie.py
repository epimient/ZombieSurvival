import pygame
import math
from settings import *

class Zombie:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = GREEN_ZOMBIE
        self.speed = 1
        self.game = game
        self.health = 100
        self.detection_radius = 200  # Radio de detección del jugador
        
    def update(self):
        # Calcular distancia al jugador
        dx_player = self.game.player.x - self.x
        dy_player = self.game.player.y - self.y
        dist_player = math.sqrt(dx_player ** 2 + dy_player ** 2)
        
        # Calcular distancia a la tienda
        dx_tent = self.game.tent.x - self.x
        dy_tent = self.game.tent.y - self.y
        dist_tent = math.sqrt(dx_tent ** 2 + dy_tent ** 2)
        
        # Determinar objetivo (jugador o tienda)
        target_x, target_y = None, None
        
        # Si el jugador está cerca, perseguirlo
        if dist_player < self.detection_radius:
            target_x, target_y = self.game.player.x, self.game.player.y
        else:
            # Si no, ir a la tienda
            target_x, target_y = self.game.tent.x, self.game.tent.y
        
        # Calcular dirección
        dx = target_x - self.x
        dy = target_y - self.y
        
        # Normalizar vector
        dist = max(1, math.sqrt(dx ** 2 + dy ** 2))
        dx = dx / dist
        dy = dy / dist
        
        # Actualizar posición
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Actualizar rectángulo
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibujar barra de salud
        health_width = 30
        health_height = 5
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 10, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 10, health_width * (self.health / 100), health_height))
