import pygame
import math
from settings import *

class Player:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.color = BLUE
        self.speed = 5
        self.game = game
        self.weapon = None
        self.bullets = []
        self.health = 100
        self.max_health = 100
        
    def update(self):
        # Movimiento con teclas de flecha
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            
        # Normalizar movimiento diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071
            
        # Actualizar posición
        self.x += dx
        self.y += dy
        
        # Restricciones de pantalla
        self.x = max(self.width // 2, min(self.x, WIDTH - self.width // 2))
        self.y = max(self.height // 2, min(self.y, HEIGHT - self.height // 2))
        
        # Actualizar rectángulo
        self.rect.x = self.x - self.width // 2
        self.rect.y = self.y - self.height // 2
        
    def shoot(self):
        if self.weapon:
            # Obtener posición del mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calcular dirección
            angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
            
            # Crear balas según el tipo de arma
            new_bullets = self.weapon.fire(self.x, self.y, angle)
            
            # Reproducir sonido de disparo según el tipo de arma
            if new_bullets and hasattr(self.game, 'sound_manager'):
                if self.weapon.name == "Pistola":
                    self.game.sound_manager.play_sound('pistol')
                elif self.weapon.name == "Metralleta":
                    self.game.sound_manager.play_sound('machinegun')
                elif self.weapon.name == "Lanzallamas":
                    self.game.sound_manager.play_sound('flamethrower')
            
            self.bullets.extend(new_bullets)
    
    def update_bullets(self):
        # Actualizar posición de balas
        for bullet in self.bullets[:]:
            bullet.update()
            
            # Eliminar balas fuera de pantalla
            if (bullet.x < 0 or bullet.x > WIDTH or 
                bullet.y < 0 or bullet.y > HEIGHT):
                self.bullets.remove(bullet)
                continue
                
            # Comprobar colisiones con zombies
            for zombie in self.game.zombies[:]:
                if bullet.rect.colliderect(zombie.rect):
                    zombie.health -= bullet.damage
                    
                    # La bala de pistola y metralleta desaparecen al impactar
                    if bullet.weapon_type != "flamethrower":
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                    
                    # Las balas del lanzallamas permanecen pero tienen una vida limitada
                    if bullet.weapon_type == "flamethrower":
                        bullet.lifetime -= 1
                        if bullet.lifetime <= 0 and bullet in self.bullets:
                            self.bullets.remove(bullet)
                    
                    break
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)