import pygame
import math
from settings import *

class Bullet:
    def __init__(self, x, y, angle, speed, color, damage, weapon_type, lifetime=None):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.damage = damage
        self.weapon_type = weapon_type
        self.lifetime = lifetime
        
        # Tamaño de la bala según el arma
        if weapon_type == "pistol":
            self.width, self.height = 8, 8
        elif weapon_type == "machinegun":
            self.width, self.height = 6, 6
        elif weapon_type == "flamethrower":
            self.width, self.height = 12, 12
            
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        
    def update(self):
        # Mover la bala según su ángulo y velocidad
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Actualizar rectángulo
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
        
        # Reducir vida útil para balas del lanzallamas
        if self.weapon_type == "flamethrower" and self.lifetime is not None:
            self.lifetime -= 1
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Weapon:
    def __init__(self, name, fire_rate, bullet_speed, bullet_damage, bullet_color):
        self.name = name
        self.fire_rate = fire_rate  # Disparos por segundo
        self.bullet_speed = bullet_speed
        self.bullet_damage = bullet_damage
        self.bullet_color = bullet_color
        self.last_fire_time = 0
        
    def fire(self, x, y, angle):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time > 1000 / self.fire_rate:
            self.last_fire_time = current_time
            return self._create_bullets(x, y, angle)
        return []
        
    def _create_bullets(self, x, y, angle):
        # Método a sobrescribir por las clases hijas
        return []


class Pistol(Weapon):
    def __init__(self):
        super().__init__("Pistola", 2, 10, 25, YELLOW)
        
    def _create_bullets(self, x, y, angle):
        return [Bullet(x, y, angle, self.bullet_speed, self.bullet_color, self.bullet_damage, "pistol")]


class MachineGun(Weapon):
    def __init__(self):
        super().__init__("Metralleta", 10, 15, 10, ORANGE)
        
    def _create_bullets(self, x, y, angle):
        # Ligera dispersión
        import random
        spread = 0.1
        new_angle = angle + random.uniform(-spread, spread)
        return [Bullet(x, y, new_angle, self.bullet_speed, self.bullet_color, self.bullet_damage, "machinegun")]


class Flamethrower(Weapon):
    def __init__(self):
        super().__init__("Lanzallamas", 20, 5, 5, RED)
        
    def _create_bullets(self, x, y, angle):
        # Crear varias partículas de fuego con dispersión
        import random
        bullets = []
        for _ in range(3):
            spread = 0.3
            new_angle = angle + random.uniform(-spread, spread)
            bullets.append(Bullet(x, y, new_angle, self.bullet_speed, self.bullet_color, 
                                 self.bullet_damage, "flamethrower", lifetime=20))
        return bullets
