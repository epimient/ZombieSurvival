"""
¡ATENCIÓN! ¡CÓDIGO DEL GUERRERO ZOMBIE!
Aquí vive el jugador, nuestro héroe solitario en el apocalipsis zombie.
¡Cuidado con lo que toca porque puede explotar!
"""
import pygame
import math
from settings import *
from weapon import Pistol, MachineGun, Flamethrower, MineWeapon, Mine # Importamos la mina para plantarla (¡cuidado al pisar!)

class Player:
    def __init__(self, x, y, game):
        # ¡Posición del jugador en el campo de batalla zombie!
        self.x = x  # Posición X (horizontal)
        self.y = y  # Posición Y (vertical)
        # Dimensiones del jugador (¡tan importante como tu contundencia en la vida!)
        self.width = 40  # Ancho del jugador
        self.height = 40  # Alto del jugador
        # Rectángulo de colisión (¡para saber si te tocan o no!)
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        # Color del jugador (¡como tu personalidad, azul resistente!)
        self.color = BLUE  # Color azul como el de un guerrero zombie
        # Velocidad de movimiento (¡cuánto corre para escapar de los zombies!)
        self.speed = PLAYER_SPEED  # Velocidad según configuración
        # Referencia al juego (¡como tu GPS zombie!)
        self.game = game  # Acceso al juego principal
        
        # Vida del jugador (¡cuidado con que no llegue a cero!)
        self.health = PLAYER_HEALTH  # Vida inicial
        self.max_health = PLAYER_HEALTH  # Vida máxima (¡no puedes pasarte de esta!)
        
        # Sistema de armas y municiones (¡el arsenal zombie!)
        self.weapon = Pistol()  # Empieza con una pistola equipada
        # Munición de cada arma (¡como tus provisiones en el apocalipsis!)
        self.ammo = {'pistol': 35, 'machinegun': 0, 'flamethrower': 0, 'mine': 0}  # Munición inicial para la pistola
        # Diccionario de armas disponibles (¡todo un arsenal!)
        self.weapons = {
            'pistol': Pistol(),        # La pistola básica
            'machinegun': MachineGun(), # La ametralladora letal
            'flamethrower': Flamethrower(), # El lanzallamas destructor
            'mine': MineWeapon()       # Las minas explosivas
        }
        # Lista de balas disparadas (¡la lluvia de plomo zombie!)
        self.bullets = []  # ¡Todas las balas que han salido de tu arma!

    def update(self, dt):
        """
        ¡Actualización del guerrero zombie!
        Se encarga del movimiento, actualización de armas y mantener al jugador dentro de los límites.
        """
        # Actualización de enfriamiento/calor de las armas
        for weapon in self.weapons.values():
            weapon.update(dt)

        # Movimiento con teclas (¡como un baile zombie pero con flechas!)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0  # Desplazamiento inicializado a cero

        # Movimiento en Y (arriba y abajo)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed  # Arriba (negativo en Y)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed  # Abajo (positivo en Y)
        # Movimiento en X (izquierda y derecha)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed  # Izquierda (negativo en X)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed  # Derecha (positivo en X)

        # Diagonal: Corrige la velocidad para no ir más rápido en diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 0.7071 ≈ 1/√2 (para mantener la velocidad constante en diagonal)
            dy *= 0.7071  # ¡Trigonometría zombie en acción!

        # Actualiza la posición
        self.x += dx
        self.y += dy

        # Limita al jugador dentro de la pantalla (¡no puedes escapar del apocalipsis!)
        self.x = max(self.width // 2, min(self.x, WIDTH - self.width // 2))  # Límites horizontales
        self.y = max(self.height // 2, min(self.y, HEIGHT - self.height // 2))  # Límites verticales

        # Actualiza el rectángulo de colisión con la nueva posición
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def shoot(self):
        if not self.weapon:
            return

        weapon_name = self.weapon.name
        
        # Check if ammo is available for any weapon
        if self.ammo.get(weapon_name, 0) > 0:
            # Try to fire the weapon (this handles cooldown and overheating internally)
            if weapon_name == 'mine':
                # Check if mine can be planted (not too close to tent)
                # MineWeapon.fire() returns True if planted, False if on cooldown/overheat
                if self.weapon.fire(self.x, self.y, 0): # Angle not relevant for mine
                    # Attempt to plant the mine, and only use ammo if successful
                    mine_planted = self.game.plant_mine(self.x, self.y)
                    if mine_planted:
                        self.ammo[weapon_name] -= 1
                        if hasattr(self.game, 'sound_manager'):
                            self.game.sound_manager.play_sound(weapon_name) # Play mine plant sound
            else: # Pistol, Machinegun, Flamethrower
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - self.y, mouse_x - self.x)
                new_bullets = self.weapon.fire(self.x, self.y, angle)
                if new_bullets: # If new_bullets is not an empty list, it means a shot was fired
                    self.ammo[weapon_name] -= 1
                    self.bullets.extend(new_bullets)
                    if hasattr(self.game, 'sound_manager'):
                        self.game.sound_manager.play_sound(weapon_name)
            
            # If ammo runs out, unequip the weapon
            if self.ammo.get(weapon_name, 0) <= 0:
                self.weapon = None

    def add_ammo(self, weapon_type, amount):
        """Adds ammo for any weapon type and resets heat for heat-based weapons."""
        if weapon_type in self.ammo:
            self.ammo[weapon_type] += amount
        
        # Reset heat for heat-based weapons when picking up ammo
        if weapon_type in ['machinegun', 'flamethrower']:
            self.weapons[weapon_type].heat = 0
            self.weapons[weapon_type].overheated = False

        # If player has no weapon, equip this one
        if not self.weapon:
            self.switch_weapon(weapon_type)

    def switch_weapon(self, weapon_type):
        """Switches the player's current weapon."""
        if weapon_type in self.weapons:
            # Can only switch if ammo is available
            if self.ammo.get(weapon_type, 0) > 0:
                 self.weapon = self.weapons[weapon_type]

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            
            if (bullet.x < 0 or bullet.x > WIDTH or 
                bullet.y < 0 or bullet.y > HEIGHT or
                (bullet.lifetime is not None and bullet.lifetime <= 0)):
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                continue
                
            for zombie in self.game.zombies:
                if bullet.rect.colliderect(zombie.rect):
                    zombie.health -= bullet.damage
                    
                    if bullet.weapon_type != "flamethrower":
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                    break
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def draw_bullets(self, screen):
        for bullet in self.bullets:
            bullet.draw(screen)