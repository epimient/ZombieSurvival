import pygame
import sys
from player import Player
from zombie import Zombie
from tent import Tent
from weapon import Pistol, MachineGun, Flamethrower
from settings import *
from sound import SoundManager

class Game:
    def __init__(self):
        # Configuración básica
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Inicializar el gestor de sonidos
        self.sound_manager = SoundManager()
        self.sound_manager.start_background_music()
        
        # Creación de objetos del juego
        self.player = Player(WIDTH // 2, HEIGHT // 2, self)
        self.tent = Tent(WIDTH // 2, HEIGHT // 4)
        self.zombies = []
        
        # Armas disponibles
        self.weapons = [
            Pistol(),
            MachineGun(),
            Flamethrower()
        ]
        self.current_weapon = 0
        self.player.weapon = self.weapons[self.current_weapon]
        
        # Temporizadores y contadores
        self.zombie_spawn_timer = 0
        self.zombie_spawn_delay = 2000  # milisegundos
        self.wave = 1
        self.zombies_in_wave = 5
        self.zombies_spawned = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Cambio de arma con las teclas 1, 2, 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.current_weapon = 0
                    self.player.weapon = self.weapons[self.current_weapon]
                elif event.key == pygame.K_2:
                    self.current_weapon = 1
                    self.player.weapon = self.weapons[self.current_weapon]
                elif event.key == pygame.K_3:
                    self.current_weapon = 2
                    self.player.weapon = self.weapons[self.current_weapon]
                elif event.key == pygame.K_r:
                    if self.game_over:
                        self.__init__()  # Reiniciar el juego
                
            # Disparar al hacer clic
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.player.shoot()
    
    def update(self):
        if not self.game_over:
            # Actualizar jugador
            self.player.update()
            
            # Reproducir sonidos de zombies ambientales basados en cuántos hay
            self.sound_manager.play_zombie_ambient(len(self.zombies))
            
            # Actualizar zombies
            for zombie in self.zombies[:]:
                zombie.update()
                
                # Verificar colisión con el jugador
                if zombie.rect.colliderect(self.player.rect):
                    self.player.health -= 1
                    if self.player.health <= 0:
                        self.game_over = True
                        self.sound_manager.play_sound('game_over')
                    else:
                        # Sonido de daño al jugador (limitado para no reproducir demasiados)
                        if pygame.time.get_ticks() % 30 == 0:
                            self.sound_manager.play_sound('player_hurt')
                
                # Verificar colisión con la tienda
                if zombie.rect.colliderect(self.tent.rect):
                    self.tent.health -= 1
                    self.zombies.remove(zombie)
                    # Sonido de daño a la tienda
                    self.sound_manager.play_sound('tent_damage')
                    if self.tent.health <= 0:
                        self.game_over = True
                        self.sound_manager.play_sound('game_over')
                
                # Verificar si el zombie está muerto
                if zombie.health <= 0:
                    self.zombies.remove(zombie)
            
            # Actualizar balas del jugador
            self.player.update_bullets()
            
            # Generar nuevos zombies
            self.spawn_zombies()
    
    def spawn_zombies(self):
        current_time = pygame.time.get_ticks()
        
        if self.zombies_spawned < self.zombies_in_wave and current_time - self.zombie_spawn_timer > self.zombie_spawn_delay:
            # Generar zombies desde los bordes de la pantalla
            from random import randint, choice
            
            side = randint(1, 4)  # 1: top, 2: right, 3: bottom, 4: left
            
            if side == 1:  # Top
                x = randint(0, WIDTH)
                y = 0
            elif side == 2:  # Right
                x = WIDTH
                y = randint(0, HEIGHT)
            elif side == 3:  # Bottom
                x = randint(0, WIDTH)
                y = HEIGHT
            else:  # Left
                x = 0
                y = randint(0, HEIGHT)
                
            self.zombies.append(Zombie(x, y, self))
            self.zombie_spawn_timer = current_time
            self.zombies_spawned += 1
            
        # Si se han eliminado todos los zombies de la oleada, aumentar la dificultad
        if self.zombies_spawned >= self.zombies_in_wave and len(self.zombies) == 0:
            self.wave += 1
            self.zombies_in_wave = 5 + (self.wave * 2)
            self.zombies_spawned = 0
            self.zombie_spawn_delay = max(500, 2000 - (self.wave * 100))  # Reducir el tiempo de spawn
            
            # Sonido de nueva oleada
            self.sound_manager.play_sound('new_wave')
    
    def draw(self):
        # Dibujar fondo
        self.screen.fill(BACKGROUND_COLOR)
        
        # Dibujar tienda
        self.tent.draw(self.screen)
        
        # Dibujar zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
            
        # Dibujar jugador
        self.player.draw(self.screen)
        
        # Dibujar balas
        self.player.draw_bullets(self.screen)
        
        # Dibujar interfaz
        self.draw_ui()
        
        # Dibujar pantalla de game over si el juego ha terminado
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Dibujar barra de salud del jugador
        health_bar_width = 200
        pygame.draw.rect(self.screen, RED, (10, 10, health_bar_width, 20))
        pygame.draw.rect(self.screen, GREEN, (10, 10, health_bar_width * (self.player.health / self.player.max_health), 20))
        
        # Dibujar barra de salud de la tienda
        tent_health_bar_width = 200
        pygame.draw.rect(self.screen, RED, (WIDTH - tent_health_bar_width - 10, 10, tent_health_bar_width, 20))
        pygame.draw.rect(self.screen, GREEN, (WIDTH - tent_health_bar_width - 10, 10, tent_health_bar_width * (self.tent.health / self.tent.max_health), 20))
        
        # Dibujar información del arma actual
        font = pygame.font.SysFont(None, 30)
        weapon_text = f"Arma: {self.player.weapon.name}"
        text_surface = font.render(weapon_text, True, WHITE)
        self.screen.blit(text_surface, (10, 40))
        
        # Dibujar información de la oleada
        wave_text = f"Oleada: {self.wave}"
        text_surface = font.render(wave_text, True, WHITE)
        self.screen.blit(text_surface, (10, 70))
    
    def draw_game_over(self):
        # Crear superficie semitransparente para oscurecer la pantalla
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Dibujar texto de game over
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Mostrar estadísticas finales
        font = pygame.font.SysFont(None, 36)
        stats_text = font.render(f"Oleada alcanzada: {self.wave}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(stats_text, stats_rect)
        
        # Mostrar instrucciones para reiniciar
        restart_text = font.render("Presiona 'R' para reiniciar", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)