"""
¡CÓDIGO DE CURACIONES ZOMBIE!
Aquí viven las curaciones que puedes encontrar en el campo de batalla.
¡Recógelas para mantener tu salud al máximo!
"""
import pygame
from settings import *

class HealthPickup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        ¡La pócima de la vida zombie!
        Un regalo del universo zombie para recuperar salud.
        ¡Como una ambulancia zombie pero más pequeña y roja!
        """
        super().__init__()
        self.x = x  # Posición X (horizontal)
        self.y = y  # Posición Y (vertical)
        self.width = 30  # Ancho del pickup
        self.height = 30  # Alto del pickup
        self.image = pygame.Surface((self.width, self.height))  # Superficie para dibujar
        self.image.fill((255, 0, 0))  # Rojo para indicar salud (¡como la sangre pero buena!)
        self.rect = self.image.get_rect()  # Rectángulo de colisión
        self.rect.center = (x, y)  # Centro en la posición indicada
        self.spawn_time = pygame.time.get_ticks()  # Momento en que apareció
        
    def update(self):
        """
        Actualiza el estado de la curación, especialmente para eliminarla después de cierto tiempo.
        """
        # Desaparece después de cierto tiempo (¡como si se evaporara la salud!)
        if pygame.time.get_ticks() - self.spawn_time > WEAPON_PICKUP_LIFESPAN:
            self.kill()  # Elimina la curación del juego (¡se fue, como la salud sin zombies!)