"""
¡¡CÓDIGO ZO9ol0pol0pñol0hjtgj,h,jhjjMBIE ACTIVADO!! 
¡Cuidado, aquí viven los muertos vivientes!
¡No toques nada sin protección!
"""
import pygame
import math
from settings import *
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        """
        ¡El zombie típico zombie! 
        No muy inteligente, pero sí muy hambriento de cerebros.
        """
        super().__init__()
        self.game = game  # Referencia al juego principal
        self.x = x  # Posición X (horizontal)
        self.y = y  # Posición Y (vertical)
        
        # Imagen y rectángulo de colisión
        self.image_orig = pygame.Surface((30, 30))  # Superficie base del zombie
        self.image_orig.fill(GREEN_ZOMBIE)  # Color verde zombie (¡como debe ser!)
        self.image = self.image_orig.copy()  # Copia de la imagen original
        self.rect = self.image.get_rect()  # Rectángulo de colisión
        self.rect.center = (x, y)  # Centro de la imagen en la posición indicada
        
        # Atributos del zombie (¡todo un personaje!)
        self.speed = ZOMBIE_SPEED  # Velocidad de movimiento (¡aunque sea lento, es persistente!)
        self.health = ZOMBIE_HEALTH  # Salud actual (¡aunque no lo parece, también se puede enfermar!)
        self.max_health = ZOMBIE_HEALTH  # Salud máxima
        self.damage = ZOMBIE_DAMAGE  # Daño que inflige (¡cuidado con sus mordiscos!)
        self.detection_radius = ZOMBIE_DETECTION_RADIUS  # Radio de detección (¡tiene olfato para cerebros!)
        
    def update(self):
        """
        ¡La rutina diaria del zombie zombie!
        Busca, persigue y destruye (o intenta) al jugador o a la tienda.
        También actualiza su barra de vida para que sepas cuánto le queda de existencia.
        """
        # Calcular distancia al jugador (¡siempre buscando cerebros!)
        dx_player = self.game.player.x - self.x
        dy_player = self.game.player.y - self.y
        dist_player = math.hypot(dx_player, dy_player)  # Distancia euclidiana (¡matemáticas zombie!)
        
        # Determinar objetivo (jugador o tienda dependiendo de la distancia)
        if dist_player < self.detection_radius:  # Si el jugador está cerca...
            target_x, target_y = self.game.player.x, self.game.player.y  # ...persigue al jugador
        else:  # Si no...
            target_x, target_y = self.game.tent.x, self.game.tent.y  # ...persigue a la tienda (¡el zombie también tiene prioridades!)
        
        # Calcular dirección hacia el objetivo (¡todo un experto en orientación zombie!)
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)  # Distancia al objetivo
        if dist > 0:  # Si la distancia es mayor que 0 (¡para evitar dividir por cero!)
            dx /= dist  # Normalizar vector X
            dy /= dist  # Normalizar vector Y
        
        # Actualizar posición (¡moviéndose como un zombie zombie!)
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Actualizar la posición del rectángulo de colisión
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # Actualizar barra de vida en la imagen
        self.image = self.image_orig.copy()  # Restaurar imagen original

        # Dibujar barra de vida (¡porque aunque zombie, también se enferma!)
        health_width = 30  # Ancho de la barra de vida
        health_height = 5  # Alto de la barra de vida
        # Fondo de la barra de vida (¡cuando está en rojo significa que algo anda mal!)
        pygame.draw.rect(self.image, RED, (0, -10, health_width, health_height))
        # Barra de vida actual (¡cuanta más verde, mejor salud!)
        current_health_width = max(0, int(health_width * (self.health / self.max_health)))
        pygame.draw.rect(self.image, GREEN, (0, -10, current_health_width, health_height))

class BossZombie(Zombie):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        
        # Ensure we have access to the required settings
        try:
            self.image_orig = pygame.Surface(BOSS_ZOMBIE_SIZE)
            self.image_orig.fill(BOSS_ZOMBIE_COLOR)
        except:
            # Fallback in case settings are not available
            self.image_orig = pygame.Surface((60, 60))  # Default boss size
            self.image_orig.fill((80, 0, 80))  # Default boss color
            
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.speed = BOSS_ZOMBIE_SPEED
        self.health = BOSS_ZOMBIE_HEALTH
        self.max_health = BOSS_ZOMBIE_HEALTH
        self.damage = BOSS_ZOMBIE_DAMAGE
        
        # Bosses always know where the player is
        self.detection_radius = WIDTH * 2
        
        # Special ability: spawn regular zombies
        self.spawn_delay = 8000  # 8 seconds between spawns (initial)
        self.last_spawn_time = pygame.time.get_ticks()
        
    def update(self):
        # Boss zombie always targets the player, never the tent
        target_x, target_y = self.game.player.x, self.game.player.y
        
        # Calculate distance to player
        dx = target_x - self.x
        dy = target_y - self.y
        dist_to_player = math.hypot(dx, dy)
        
        # Normalize direction vector
        if dist_to_player > 0:
            dx /= dist_to_player
            dy /= dist_to_player
        
        # Boss zombie speeds up when health is low (rampage mode) and becomes more unpredictable
        current_speed = self.speed
        health_percentage = self.health / self.max_health
        
        if health_percentage < 0.3:  # When below 30% health, move much faster and more erratically
            current_speed = self.speed * 2.0  # Much faster when low on health
            # Add some randomness to movement when desperate
            dx += random.uniform(-0.2, 0.2)
            dy += random.uniform(-0.2, 0.2)
            # Normalize again after adding randomness
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx /= dist
                dy /= dist
        elif health_percentage < 0.6:  # When below 60% health, move faster
            current_speed = self.speed * 1.5  # 50% faster when damaged
        
        # Update position
        self.x += dx * current_speed
        self.y += dy * current_speed
        
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # Update health bar on the image
        self.image = self.image_orig.copy()

        # Draw health bar and effects
        # Calculate health bar dimensions using the image's width
        health_width = self.image.get_width()
        health_height = 8  # Slightly larger health bar for boss

        # Background for health bar
        pygame.draw.rect(self.image, RED, (0, -10, health_width, health_height))
        
        # Current health bar
        current_health_width = max(0, int(health_width * (self.health / self.max_health)))
        pygame.draw.rect(self.image, GREEN, (0, -10, current_health_width, health_height))

        # Optionally, make the boss flash red when it takes damage
        if self.health < self.max_health:
            damage_ratio = 1 - (self.health / self.max_health)
            damage_indicator_width = max(0, int(health_width * damage_ratio))
            pygame.draw.rect(self.image, RED, (0, -5, damage_indicator_width, 3))

        # Visual effect before spawning zombies (flash when 1 second left)
        current_time = pygame.time.get_ticks()
        time_since_last_spawn = current_time - self.last_spawn_time
        time_until_next_spawn = self.spawn_delay - time_since_last_spawn
        
        if 0 < time_until_next_spawn < 1000:
            # Make the boss flash red more intensely as spawning approaches
            flash_intensity = int(255 * (time_until_next_spawn / 1000))
            flash_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            flash_color = (255, 0, 0, flash_intensity)  # Red with varying alpha
            flash_surface.fill(flash_color)
            self.image.blit(flash_surface, (0, 0))

        # Spawn regular zombies periodically
        if current_time - self.last_spawn_time > self.spawn_delay:
            # Determine how many zombies to spawn based on boss health
            health_percentage = self.health / self.max_health
            if health_percentage < 0.3:  # Below 30% health
                num_zombies = random.randint(3, 5)  # Spawn more zombies when desperate
            elif health_percentage < 0.6:  # Below 60% health
                num_zombies = random.randint(2, 3)  # Spawn 2-3 zombies
            else:
                num_zombies = 1  # Spawn 1 zombie normally

            # Determine new spawn delay based on health (more frequent when low health)
            if health_percentage < 0.3:
                new_spawn_delay = 3000  # 3 seconds when desperate
            elif health_percentage < 0.6:
                new_spawn_delay = 5000  # 5 seconds when damaged
            else:
                new_spawn_delay = 7000  # 7 seconds normally

            # Spawn the zombies
            for _ in range(num_zombies):
                self.spawn_zombie()

            self.last_spawn_time = current_time
            self.spawn_delay = new_spawn_delay  # Update the spawn delay after spawning

    def spawn_zombie(self):
        """Spawns a regular zombie near the boss"""
        # Spawn zombie in a random direction around the boss
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(40, 80)  # Random distance from boss
        new_x = self.x + math.cos(angle) * distance
        new_y = self.y + math.sin(angle) * distance
        
        # Create a new zombie and add it to the game's zombie group
        new_zombie = Zombie(new_x, new_y, self.game)
        self.game.zombies.add(new_zombie)
        
        # Play sound effect when spawning zombie
        if hasattr(self.game, 'sound_manager'):
            try:
                self.game.sound_manager.play_sound('boss_spawn')
            except:
                # In case sound file is not available
                pass