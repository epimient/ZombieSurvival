"""
¡CÓDIGO DE LA TIENDA ZOMBIE!
Aquí vive la tienda, el refugio sagrado que debes proteger.
¡Cuidado con los zombies que quieran invadirla!
"""
import pygame
from settings import *

class Tent:
    def __init__(self, x, y):
        """
        ¡El refugio sagrado zombie!
        La tienda que debes proteger con tu vida (literalmente).
        Si cae, ¡game over!
        """
        self.x = x  # Posición X de la tienda
        self.y = y  # Posición Y de la tienda
        self.width = 100  # Ancho de la tienda (¡un refugio espacioso!)
        self.height = 100  # Alto de la tienda (¡mucho espacio para esconderse!)
        # Rectángulo de colisión (¡para saber si los zombies la tocan!)
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = BROWN  # Color marrón como una tienda de verdad (¡todo un clásico!)
        self.health = TENT_HEALTH  # Salud actual de la tienda (¡esperemos que no se acabe!)
        self.max_health = TENT_HEALTH  # Salud máxima (¡como el escudo final!)
        
    def draw(self, screen):
        """
        Dibuja la tienda en la pantalla con su barra de vida.
        ¡Para que veas cuánto le queda antes de que los zombies invadan!
        """
        # Dibujar la tienda (¡el refugio!)
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibujar barra de salud (¡para ver cuánto le queda de resistencia!)
        health_width = self.width  # Ancho de la barra de salud (igual al ancho de la tienda)
        health_height = 10  # Alto de la barra de salud (¡bien visible!)
        # Fondo rojo de la barra (¡cuando está en rojo, se acaba!)
        pygame.draw.rect(screen, RED, (self.rect.x, self.rect.y - 20, health_width, health_height))
        # Barra de vida actual (¡verde si todo va bien!)
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y - 20, health_width * (self.health / self.max_health), health_height))
