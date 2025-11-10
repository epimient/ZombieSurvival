"""
¡CÓDIGO DE ARMAS ZOMBIE!
Aquí viven todas las armas mortales para sobrevivir al apocalipsis.
¡Cuidado con lo que disparas!
"""
import pygame
import math
from settings import *

class Bullet:
    def __init__(self, x, y, angle, speed, color, damage, weapon_type, lifetime=None):
        """
        ¡La bala voladora zombie!
        Pequeña pero mortal, sale disparada de tu arma para convertir zombies en ex-zombies.
        """
        self.x = x  # Posición X de la bala
        self.y = y  # Posición Y de la bala
        self.angle = angle  # Ángulo de trayectoria (¡como un proyectil zombie!)
        self.speed = speed  # Velocidad de la bala
        self.color = color  # Color de la bala (¡por si quieres distinguir tus armas!)
        self.damage = damage  # Daño que inflige (¡el poder destructivo!)
        self.weapon_type = weapon_type  # Tipo de arma que disparó esta bala
        self.lifetime = lifetime  # Vida útil de la bala (¡algunas se desvanecen!)
        
        # Tamaño de la bala según el arma (¡cada arma tiene su estilo!)
        if weapon_type == "pistol":
            self.width, self.height = 8, 8  # Pistoletazo preciso
        elif weapon_type == "machinegun":
            self.width, self.height = 6, 6  # Bala rápida de ametralladora
        elif weapon_type == "flamethrower":
            self.width, self.height = 12, 12  # Proyectil grande de lanzallamas
        
        # Rectángulo de colisión (¡para saber qué toca!)
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
    def __init__(self, name, fire_rate, bullet_speed, bullet_damage, bullet_color, heat_per_shot=0, cooldown_rate=0):
        """
        ¡La clase madre de todas las armas zombie!
        Define las propiedades básicas y el comportamiento de disparo.
        """
        self.name = name  # Nombre de la arma (¡por si quieres distinguirlas!)
        self.fire_rate = fire_rate  # Disparos por segundo (¡velocidad de fuego!)
        self.bullet_speed = bullet_speed  # Velocidad de las balas (¡qué tan rápido vuelan!)
        self.bullet_damage = bullet_damage  # Daño de cada bala (¡cuánto le dolió al zombie!)
        self.bullet_color = bullet_color  # Color de las balas (¡por estética zombie!)
        self.last_fire_time = 0  # Última vez que se disparó (¡para controlar la cadencia!)

        # Mecánica de sobrecalentamiento (¡arma que se puede quemar como un zombie con fiebre!)
        self.heat = 0  # Nivel actual de calor
        self.heat_per_shot = heat_per_shot  # Cuánto calor se genera por disparo
        self.cooldown_rate = cooldown_rate  # Velocidad de enfriamiento
        self.overheated = False  # ¿Está sobrecalentada la arma?

    def update(self, dt):
        """
        Actualiza el estado de la arma, especialmente el enfriamiento.
        """
        # Enfriar con el tiempo (¡como un zombie zombie que se enfría!)
        if self.heat > 0:
            self.heat -= self.cooldown_rate * dt
            self.heat = max(0, self.heat)  # No permitir calor negativo

        # Verificar si se ha enfriado lo suficiente para usarse de nuevo
        if self.overheated and self.heat < 10: # Debe enfriarse considerablemente
            self.overheated = False

    def fire(self, x, y, angle):
        """
        Dispara la arma si puede (no está sobrecalentada, respetando cadencia, etc.)
        """
        # Verificar cadencia de disparo (¡no puedes disparar infinito como un zombie infinito!)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time < 1000 / self.fire_rate:
            return []  # No puede disparar aún (¡espera un poco!)

        # Verificar sobrecalentamiento (¡arma caliente como un zombie enojado!)
        if self.overheated:
            return []  # No puede disparar (¡está muy caliente!)

        self.last_fire_time = current_time  # Registrar el momento del disparo
        
        # Aumentar calor para armas que tienen esta mecánica
        if self.heat_per_shot > 0:
            self.heat += self.heat_per_shot
            if self.heat >= MAX_WEAPON_HEAT:  # Máximo calor alcanzado
                self.overheated = True  # ¡Sobrecalentada!
                self.heat = MAX_WEAPON_HEAT  # Limitar al valor máximo

        return self._create_bullets(x, y, angle)  # Crear y devolver balas
        
    def _create_bullets(self, x, y, angle):
        """
        Método a sobrescribir por las clases hijas.
        Cada arma crea sus propias balas de forma diferente.
        """
        return []


class Pistol(Weapon):
    def __init__(self):
        stats = WEAPON_STATS['pistol']
        super().__init__("pistol", stats['fire_rate'], stats['speed'], stats['damage'], YELLOW)
        
    def _create_bullets(self, x, y, angle):
        return [Bullet(x, y, angle, self.bullet_speed, self.bullet_color, self.bullet_damage, "pistol")]


class MachineGun(Weapon):
    def __init__(self):
        stats = WEAPON_STATS['machinegun']
        super().__init__("machinegun", stats['fire_rate'], stats['speed'], stats['damage'], ORANGE, 
                         heat_per_shot=stats['heat_per_shot'], cooldown_rate=stats['cooldown_rate'])
        
    def _create_bullets(self, x, y, angle):
        # Ligera dispersión
        import random
        spread = 0.1
        new_angle = angle + random.uniform(-spread, spread)
        return [Bullet(x, y, new_angle, self.bullet_speed, self.bullet_color, self.bullet_damage, "machinegun")]


class Flamethrower(Weapon):
    def __init__(self):
        stats = WEAPON_STATS['flamethrower']
        super().__init__("flamethrower", stats['fire_rate'], stats['speed'], stats['damage'], RED,
                         heat_per_shot=stats['heat_per_shot'], cooldown_rate=stats['cooldown_rate'])
        self.bullet_lifespan = stats['lifespan']
        
    def _create_bullets(self, x, y, angle):
        # Crear varias partículas de fuego con dispersión
        import random
        bullets = []
        for _ in range(3):
            spread = 0.3
            new_angle = angle + random.uniform(-spread, spread)
            bullets.append(Bullet(x, y, new_angle, self.bullet_speed, self.bullet_color, 
                                 self.bullet_damage, "flamethrower", lifetime=self.bullet_lifespan))
        return bullets

class Mine(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.image_orig = pygame.Surface((20, 20))
        self.image_orig.fill(MINE_COLOR)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.stats = WEAPON_STATS['mine']
        self.state = 'planted' # planted, triggered, exploding
        self.trigger_time = 0
        self.explosion_radius = self.stats['explosion_radius']
        self.damage = self.stats['damage']
        self.countdown = self.stats['countdown']
        self.explosion_start_time = 0

    def update(self):
        if self.state == 'triggered':
            if pygame.time.get_ticks() - self.trigger_time > self.countdown:
                self.explode()
        
        elif self.state == 'exploding':
            # Simple explosion animation
            duration = 250 # ms
            progress = (pygame.time.get_ticks() - self.explosion_start_time) / duration
            if progress >= 1:
                self.kill()
            else:
                current_radius = self.explosion_radius * progress
                self.image = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(self.image, ORANGE, (current_radius, current_radius), int(current_radius))
                self.rect = self.image.get_rect(center=self.rect.center)

    def trigger(self):
        if self.state == 'planted':
            self.state = 'triggered'
            self.trigger_time = pygame.time.get_ticks()
            # Change color to show it's triggered
            self.image.fill(YELLOW)

    def explode(self):
        if self.state == 'exploding': return # a zombie can't re-trigger an exploding mine
        self.state = 'exploding'
        self.explosion_start_time = pygame.time.get_ticks()
        # Find zombies in radius and damage them
        for zombie in self.game.zombies:
            if math.hypot(zombie.rect.centerx - self.rect.centerx, zombie.rect.centery - self.rect.centery) < self.explosion_radius:
                zombie.health -= self.damage
        
        # Damage player if in range
        if math.hypot(self.game.player.rect.centerx - self.rect.centerx, 
                     self.game.player.rect.centery - self.rect.centery) < self.explosion_radius:
            self.game.player.health -= self.damage // 2  # Mine damage to player (half the zombie damage)
        
        # TODO: Add explosion sound
        # self.game.sound_manager.play_sound('explosion')

class MineWeapon(Weapon):
    def __init__(self):
        stats = WEAPON_STATS['mine']
        super().__init__("mine", 2, 0, stats['damage'], MINE_COLOR) 

    def fire(self, x, y, angle): # x, y, angle are not used for mine planting
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fire_time < 1000 / self.fire_rate:
            return False # Did not fire (on cooldown)

        if self.overheated: # This will always be False for mines unless explicitly set
            return False

        self.last_fire_time = current_time
        return True # Mine successfully "fired"
