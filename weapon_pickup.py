"""
¡CÓDIGO DE ARMAS RECUPERABLES ZOMBIE!
Aquí viven las armas que puedes encontrar en el campo de batalla.
¡Recógelas para sobrevivir al apocalipsis!
"""
import pygame
from settings import *

class WeaponPickup(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type):
        """
        ¡El regalo zombie perfecto!
        Un arma que puedes recoger para mejorar tu arsenal.
        ¡Pero rápido! Se desvanece con el tiempo como un zombie cansado.
        """
        super().__init__()
        self.weapon_type = weapon_type  # Tipo de arma (¡pistola, ametralladora, etc.!)
        self.image = pygame.Surface((30, 30))  # Superficie para dibujar el arma
        self.rect = self.image.get_rect()  # Rectángulo de colisión
        self.rect.center = (x, y)  # Posición central
        self.spawn_time = pygame.time.get_ticks()  # Momento en que apareció (¡para controlar su vida!)

        # Representación visual simple (¡cada arma con su color!)
        if self.weapon_type == 'pistol':
            self.image.fill(YELLOW)  # Pistola: color amarillo (¡preciso y rápido!)
        elif self.weapon_type == 'machinegun':
            self.image.fill(ORANGE)  # Ametralladora: color naranja (¡mucho fuego!)
        elif self.weapon_type == 'flamethrower':
            self.image.fill(RED)  # Lanzallamas: color rojo (¡quema zombies!)
        elif self.weapon_type == 'mine':
            self.image.fill(MINE_COLOR)  # Mina: color gris (¡zombie, ¡no des actives!)

    def update(self):
        """
        Actualiza el estado del pickup, especialmente para eliminarlo después de cierto tiempo.
        """
        # Desaparece después de cierto tiempo (¡como una oferta zombie limitada!)
        if pygame.time.get_ticks() - self.spawn_time > WEAPON_PICKUP_LIFESPAN:
            self.kill()  # Elimina el pickup del juego (¡se desvaneció en el éter zombie!)
