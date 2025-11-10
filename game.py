"""
¡¡ATENCIÓN!! ¡¡CÓDIGO CON ZOMBIES Y EXPLOSIONES!! 
¡No te asustes si al compilar suena un gemido de zombie!

Aquí empieza la magia del juego, donde controlamos al jugador, matamos zombies,
protegemos la tienda y nos volvemos adictos a disparar cosas.
"""
import pygame
import sys
import random
import math
from player import Player  # Importamos al héroe que se come cerebros zombie (bueno, los zombies que se comen cerebros...)
from zombie import Zombie, BossZombie  # Los enemigos que vienen a arruinar tu día (y tu cerebro), incluyendo el jefe
from tent import Tent  # La tienda que debes proteger... ¡como si fuera tu casa de soltero!
from weapon import Pistol, MachineGun, Flamethrower, MineWeapon, Mine  # Armas para defenderse (y causar estragos)
from weapon_pickup import WeaponPickup  # Armas que aparecen como regalos en el suelo (¡como navidad pero con balas!)
from health_pickup import HealthPickup  # Curaciones para cuando te dejan sin vida (¡como una ambulancia zombie!)
from settings import *  # Configuraciones que mantienen el juego equilibrado (o no)
from sound import SoundManager  # El DJ del apocalipsis zombie

class Game:
    def __init__(self):
        # Configuración básica - Preparando el terreno para la matanza zombie
        pygame.init() # Inicializamos pygame (¡como un ritual de guerra zombie!)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creamos la pantalla donde morirán los zombies
        pygame.display.set_caption("Zombie Survival")  # Título que atrae a los adictos a la acción
        self.clock = pygame.time.Clock()  # Reloj que marca el ritmo de la matanza
        self.running = True  # ¡El show debe continuar! (o la matanza debe continuar)
        self.game_over = False  # Aún no has perdido... (¡pero lo harás!)
        self.show_menu = True  # Mostrar menú principal al inicio
        self.menu_option = 0  # Opción seleccionada en el menú (0: Start, 1: Options, 2: Credits)
        self.show_credits = False  # Mostrar créditos
        self.show_options = False  # Mostrar opciones
        self.paused = False  # Estado de pausa del juego
        self.pause_option = 0  # Opción seleccionada en el menú de pausa (0: Continuar, 1: Opciones, 2: Menú Principal)

        # Inicializar el gestor de sonidos - El DJ del apocalipsis
        self.sound_manager = SoundManager()  # El disc-jockey zombie
        self.sound_manager.start_background_music()  # Pista de fondo para la matanza

        # Variables para el menú de opciones
        self.option_selected = 0  # Opción actualmente seleccionada en el menú de opciones
        self.difficulty = "NORMAL"  # Nivel de dificultad actual

        # Creamos los objetos del juego pero no los inicializamos completamente hasta que se inicie el juego
        self.initialize_game_objects()
        
    def initialize_game_objects(self):
        """Inicializa los objetos del juego para iniciar una nueva partida"""
        # Creación de objetos del juego
        # ¡El héroe solitario en medio del caos zombie!
        self.player = Player(WIDTH // 2, HEIGHT // 2, self)  # Nuestro guerrero anti-zombie
        # La tienda sagrada que debes proteger como a tu vida (porque es tu vida)
        self.tent = Tent(WIDTH // 2, HEIGHT // 4)  # ¡La base, la fortaleza, el refugio!

        # Grupos de Sprites - Como un ejército organizado (bueno, más o menos)
        self.zombies = pygame.sprite.Group()  # Grupo de zombies hostiles
        self.weapon_pickups = pygame.sprite.Group()  # Armas esperando a ser recogidas como regalos
        self.health_pickups = pygame.sprite.Group()  # Pócimas de curación para cuando te sientas débil
        self.mines = pygame.sprite.Group()  # Explosivos escondidos como trampas mortales

        # Temporizadores y contadores - Todo un experto en controlar el caos zombie
        self.zombie_spawn_timer = 0  # Temporizador para saber cuándo aparece el próximo zombie
        self.zombie_spawn_delay = 2000  # milisegundos - Espera para el próximo zombie (¡como un show de talentos zombie!)
        self.wave = 1  # Número de oleada - Cada vez más zombies, cada vez más caos
        self.zombies_in_wave = 5  # Zombies en la oleada actual
        self.zombies_spawned = 0  # Cuántos zombies han aparecido en esta oleada

        # Contador de bajas y mensajes
        self.kill_count = 0  # Cuántos zombies has convertido en ex-zombies (¡baja tras baja!)
        self.pickup_message = None  # Mensaje que aparece cuando recoges algo útil
        self.pickup_message_timer = 0  # Temporizador para el mensaje de recogida
        self.pickup_message_duration = 2000 # 2 segundos - Duración del mensaje de recogida

        # Spawn initial weapons - Armas iniciales por si te sientes indefenso
        self.spawn_initial_weapons()

    def reset_game(self):
        """Resets the game to its initial state."""
        # Resetear variables del juego
        self.game_over = False
        self.show_menu = False
        self.show_credits = False
        self.show_options = False
        
        # Reiniciar objetos del juego
        self.initialize_game_objects()
        
    def spawn_initial_weapons(self):
        """
        Método vacío - ya no se colocan armas al inicio del juego.
        Las armas ahora aparecen durante el juego para que el jugador no comience con ventaja.
        """
        # Este método ahora está vacío, las armas aparecerán durante el juego
        # en lugar de aparecer al inicio
        pass

    def plant_mine(self, x, y):
        """
        ¡Cuidado! ¡Aquí hay trampas! 
        Coloca una mina explosiva en el mapa, pero no tan cerca de la tienda que es como tu casa...
        porque si no te autodestruirías como un zombie kamikaze.
        """
        # Calculamos la distancia desde la tienda (¡no vaya a ser que te explotes a ti mismo!)
        tent_distance = math.hypot(x - self.tent.x, y - self.tent.y)
        
        # No se planta la mina si está muy cerca de la tienda (¡eso sería como un suicidio zombie!)
        if tent_distance < 80:
            # Opcionalmente se puede reproducir un sonido o mostrar un mensaje de error
            return False  # La mina no fue plantada por estar demasiado cerca de la tienda
        
        # ¡Planta la bomba, pero con responsabilidad!
        mine = Mine(x, y, self)
        self.mines.add(mine)
        return True  # Mina plantada con éxito (¡ahora cuidado con donde pisas!)

    def spawn_weapon(self, x, y, weapon_type):
        """Spawns a weapon pickup on the map."""
        pickup = WeaponPickup(x, y, weapon_type)
        self.weapon_pickups.add(pickup)

    def spawn_health_pickup(self, x, y):
        """Spawns a health pickup on the map."""
        pickup = HealthPickup(x, y)
        self.health_pickups.add(pickup)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Manejar eventos en el menú principal
            if self.show_menu and not self.show_credits and not self.show_options:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.menu_option = (self.menu_option - 1) % 3  # Mover hacia arriba entre las 3 opciones
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.menu_option = (self.menu_option + 1) % 3  # Mover hacia abajo entre las 3 opciones
                    elif event.key == pygame.K_RETURN:  # Enter para seleccionar
                        if self.menu_option == 0:  # Start
                            self.show_menu = False
                        elif self.menu_option == 1:  # Options
                            self.show_options = True
                        elif self.menu_option == 2:  # Credits
                            self.show_credits = True
                continue

            # Si estamos viendo opciones, manejar los controles de ajuste
            if self.show_options:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_credits = False
                        self.show_options = False
                        self.show_menu = True
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        # Cambiar a la opción anterior (máximo 3 opciones: 0-2)
                        self.option_selected = (self.option_selected - 1) % 4
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        # Cambiar a la siguiente opción (máximo 3 opciones: 0-2)
                        self.option_selected = (self.option_selected + 1) % 4
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        # Reducir valor de la opción actual
                        self.adjust_option(-1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        # Aumentar valor de la opción actual
                        self.adjust_option(1)
                continue

            # Si el juego está pausado, manejar los eventos del menú de pausa
            if self.paused:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.pause_option = (self.pause_option - 1) % 3  # Mover hacia arriba entre las 3 opciones
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.pause_option = (self.pause_option + 1) % 3  # Mover hacia abajo entre las 3 opciones
                    elif event.key == pygame.K_RETURN:  # Enter para seleccionar
                        if self.pause_option == 0:  # Continuar juego
                            self.paused = False
                        elif self.pause_option == 1:  # Opciones
                            self.show_options = True
                        elif self.pause_option == 2:  # Menú Principal
                            self.paused = False
                            self.show_menu = True
                            self.reset_game()  # Reiniciar el juego al volver al menú
                    elif event.key == pygame.K_ESCAPE:  # ESC para continuar
                        self.paused = False
                continue

            # Si estamos viendo créditos, manejar esos eventos
            if self.show_credits:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.show_credits = False
                    self.show_options = False
                    self.show_menu = True
                continue

            if self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                continue

            # Manejar pausa del juego (tecla ESC)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not self.show_menu and not self.show_credits and not self.show_options:
                    self.paused = not self.paused  # Alternar entre pausa y juego
                continue

            # Cambio de arma con las teclas 1, 2, 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.switch_weapon('pistol')
                elif event.key == pygame.K_2:
                    self.player.switch_weapon('machinegun')
                elif event.key == pygame.K_3:
                    self.player.switch_weapon('flamethrower')
                elif event.key == pygame.K_4:
                    self.player.switch_weapon('mine')
                
            # Single-shot weapons (pistol, mine)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.player.weapon and self.player.weapon.name in ['pistol', 'mine']:
                    self.player.shoot()

    def adjust_option(self, direction):
        """Ajusta la opción seleccionada en el menú de opciones"""
        # Para simplificar, vamos a implementar ajustes temporales
        # que no guardan valor permanente pero se aplican en el juego
        if direction == -1:  # Reducir
            if self.option_selected == 0:  # Volumen de música
                self.sound_manager.set_music_volume(max(0.0, self.sound_manager.music_volume - 0.1))
            elif self.option_selected == 1:  # Volumen de efectos
                self.sound_manager.set_sfx_volume(max(0.0, self.sound_manager.sfx_volume - 0.1))
        elif direction == 1:  # Aumentar
            if self.option_selected == 0:  # Volumen de música
                self.sound_manager.set_music_volume(min(1.0, self.sound_manager.music_volume + 0.1))
            elif self.option_selected == 1:  # Volumen de efectos
                self.sound_manager.set_sfx_volume(min(1.0, self.sound_manager.sfx_volume + 0.1))

    def get_difficulty_text(self):
        """Devuelve el texto de dificultad actual"""
        return self.difficulty
    
    def update(self, dt):
        """
        ¡La caja negra del caos zombie!
        Aquí se maneja toda la lógica del juego: movimientos, colisiones, disparos, etc.
        Un torbellino de acción zombie constante.
        """
        if not self.game_over:
            # ¿Está disparando con armas automáticas?
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]: # Botón izquierdo del ratón presionado
                if self.player.weapon and self.player.weapon.name not in ['pistol', 'mine']:
                    self.player.shoot()

            # Actualizar estado de jugador y objetos recogibles
            self.player.update(dt)  # Movimiento y estado del jugador
            self.weapon_pickups.update()  # Actualizar armas en el suelo
            self.health_pickups.update()  # Actualizar curaciones
            self.mines.update()  # Actualizar estado de las minas
            
            # ¡Explosiones! Verificar colisiones entre zombies y minas
            zombie_mine_hits = pygame.sprite.groupcollide(self.zombies, self.mines, False, False)
            for zombie, mines_hit in zombie_mine_hits.items():
                for mine in mines_hit:
                    mine.trigger()  # ¡La mina se activa y va a explotar!
            
            # El jugador también puede activar minas al caminar sobre ellas (¡cuidado!)
            player_mine_hits = pygame.sprite.spritecollide(self.player, self.mines, False)
            for mine in player_mine_hits:
                if mine.state == 'planted':  # Solo activar minas que aún están plantadas
                    mine.trigger()  # ¡Ups! El jugador activó una mina...
            
            # ¿El jugador recoge un arma? ¡Alegría!
            collided_pickups = pygame.sprite.spritecollide(self.player, self.weapon_pickups, True, pygame.sprite.collide_rect_ratio(0.75))
            for pickup in collided_pickups:
                ammo_amount = WEAPON_AMMO_GIVEN.get(pickup.weapon_type, 0)
                self.player.add_ammo(pickup.weapon_type, ammo_amount)  # Sumar munición
                self.pickup_message = f"Recogiste {pickup.weapon_type.capitalize()}! (+{ammo_amount} munición)"
                self.pickup_message_timer = pygame.time.get_ticks()  # Para mostrar el mensaje temporalmente

            # ¿El jugador recoge una curación? ¡A recuperar vida!
            health_collided = pygame.sprite.spritecollide(self.player, self.health_pickups, True, pygame.sprite.collide_rect_ratio(0.75))
            for pickup in health_collided:
                # Restaurar un porcentaje de salud máxima
                health_restored = int(self.player.max_health * HEALTH_PICKUP_VALUE)  # Recuperación según configuración
                new_health = min(self.player.max_health, self.player.health + health_restored)
                health_gained = new_health - self.player.health
                self.player.health = new_health
                self.pickup_message = f"¡Salud recuperada! (+{health_gained} HP)"
                self.pickup_message_timer = pygame.time.get_ticks()
                self.sound_manager.play_sound('health_pickup')  # ¡Sonido de salud!

            # Reproducir sonidos de zombies ambientales según cuántos hay (¡más zombies = más tensión!)
            self.sound_manager.play_zombie_ambient(len(self.zombies))
            
            # Actualizar zombies: movimiento, daño, etc.
            self.zombies.update()
            for zombie in self.zombies:
                # ¿Chocó con el jugador? ¡Mala suerte!
                if zombie.rect.colliderect(self.player.rect):
                    self.player.health -= zombie.damage
                    if self.player.health <= 0:
                        self.game_over = True  # ¡Fin del juego!
                        self.sound_manager.play_sound('game_over')
                    else:
                        if pygame.time.get_ticks() % 30 == 0:  # Sonido de daño periódicamente
                            self.sound_manager.play_sound('player_hurt')
                
                # ¿Chocó con la tienda? ¡La tienda está en peligro!
                if zombie.rect.colliderect(self.tent.rect):
                    self.tent.health -= zombie.damage
                    # Solo eliminar zombies normales, no al jefe (el jefe continúa atacando)
                    if not isinstance(zombie, BossZombie):
                        zombie.kill() # Eliminar zombie normal de todos los grupos
                    self.sound_manager.play_sound('tent_damage')  # ¡Sonido de daño a la tienda!
                    if self.tent.health <= 0:
                        self.game_over = True  # ¡Fin del juego si la tienda cae!
                        self.sound_manager.play_sound('game_over')
                
                # ¿El zombie está muerto? ¡Fuera de combate!
                if zombie.health <= 0:
                    zombie.kill()  # Eliminar zombie
                    self.kill_count += 1  # Añadir a contador de muertes
            
            # Actualizar balas del jugador (movimiento, colisiones, etc.)
            self.player.update_bullets()
            
            # Generar nuevos zombies
            self.spawn_zombies()
    
    def spawn_zombies(self):
        current_time = pygame.time.get_ticks()
        
        if self.zombies_spawned < self.zombies_in_wave and current_time - self.zombie_spawn_timer > self.zombie_spawn_delay:
            side = random.randint(1, 4)
            if side == 1: x, y = random.randint(0, WIDTH), 0
            elif side == 2: x, y = WIDTH, random.randint(0, HEIGHT)
            elif side == 3: x, y = random.randint(0, WIDTH), HEIGHT
            else: x, y = 0, random.randint(0, HEIGHT)
                
            zombie = Zombie(x, y, self)
            self.zombies.add(zombie)
            self.zombie_spawn_timer = current_time
            self.zombies_spawned += 1
            
        if self.zombies_spawned >= self.zombies_in_wave and len(self.zombies) == 0:
            self.wave += 1
            self.zombies_in_wave = 5 + (self.wave * 2)
            self.zombies_spawned = 0
            self.zombie_spawn_delay = max(500, 2000 - (self.wave * 100))
            self.sound_manager.play_sound('new_wave')

            # Spawn a boss every 5 waves
            if self.wave % 5 == 0:
                # Spawn boss from a random side like regular zombies
                side = random.randint(1, 4)
                if side == 1: x, y = random.randint(0, WIDTH), 0
                elif side == 2: x, y = WIDTH, random.randint(0, HEIGHT)
                elif side == 3: x, y = random.randint(0, WIDTH), HEIGHT
                else: x, y = 0, random.randint(0, HEIGHT)
                
                boss = BossZombie(x, y, self)
                self.zombies.add(boss)

            # Spawn a new weapon every wave (more frequent)
            weapons = list(WEAPON_SPAWN_WEIGHTS.keys())
            weights = list(WEAPON_SPAWN_WEIGHTS.values())
            chosen_weapon = random.choices(weapons, weights=weights, k=1)[0]
            self.spawn_weapon(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100), chosen_weapon)
            
            # Additionally, spawn another weapon every 3 waves for even more availability
            if self.wave % 3 == 0:
                chosen_weapon = random.choices(weapons, weights=weights, k=1)[0]
                self.spawn_weapon(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100), chosen_weapon)

            # Spawn health pickup every 3 waves
            if self.wave % 3 == 0:
                self.spawn_health_pickup(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100))

    def draw(self):
        if self.show_menu and not self.show_credits and not self.show_options:
            self.draw_menu()
        elif self.show_credits:
            self.draw_credits()
        elif self.show_options:
            self.draw_options()
        elif self.paused:
            # Dibujar el juego de fondo (parcialmente visible) y superponer el menú de pausa
            self.screen.fill(BACKGROUND_COLOR)
            self.tent.draw(self.screen)
            self.zombies.draw(self.screen)
            self.weapon_pickups.draw(self.screen)
            self.health_pickups.draw(self.screen)
            self.mines.draw(self.screen)
            self.player.draw(self.screen)
            self.player.draw_bullets(self.screen)
            self.draw_ui()
            
            # Superponer pantalla de pausa
            self.draw_pause_menu()
        else:
            # Dibuja el juego normal cuando no se está en el menú
            self.screen.fill(BACKGROUND_COLOR)
            self.tent.draw(self.screen)
            self.zombies.draw(self.screen)
            self.weapon_pickups.draw(self.screen)
            self.health_pickups.draw(self.screen)
            self.mines.draw(self.screen)
            self.player.draw(self.screen)
            self.player.draw_bullets(self.screen)
            self.draw_ui()

            if self.game_over:
                self.draw_game_over()

        pygame.display.flip()

    def draw_pause_menu(self):
        """Dibuja el menú de pausa"""
        # Superposición semi-transparente
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 36)
        
        # Título PAUSE
        title = font_large.render("PAUSA", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        # Opciones del menú de pausa
        pause_options = ["CONTINUAR", "OPCIONES", "MENÚ PRINCIPAL"]
        
        for i, option in enumerate(pause_options):
            color = GREEN if i == self.pause_option else WHITE
            text = font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Instrucciones
        instructions = font_small.render("Usa las flechas para navegar, ENTER para seleccionar, ESC para continuar", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)

    def draw_menu(self):
        """Dibuja el menú principal del juego"""
        self.screen.fill(BACKGROUND_COLOR)
        
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 48)
        font_small = pygame.font.SysFont(None, 36)
        
        # Dibujar el título del juego
        title = font_large.render("PYZOMBIE", True, GREEN)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        # Subtítulo zombie
        subtitle = font_small.render("ZOMBIE SURVIVAL", True, RED)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 60))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Opciones del menú
        menu_options = ["INICIAR JUEGO", "OPCIONES", "CRÉDITOS"]
        
        for i, option in enumerate(menu_options):
            color = YELLOW if i == self.menu_option else WHITE
            text = font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Instrucciones
        instructions = font_small.render("Usa las flechas para navegar, ENTER para seleccionar", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)

    def draw_credits(self):
        """Dibuja la pantalla de créditos"""
        self.screen.fill(BACKGROUND_COLOR)
        
        font_large = pygame.font.SysFont(None, 48)
        font_medium = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 28)
        
        # Título
        title = font_large.render("CRÉDITOS", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Créditos
        credits_lines = [
            "DESARROLLADO POR:",
            "Ing. Eduardo Pimienta",
            "",
            "HERRAMIENTAS:",
            "Python 3 + Pygame",
            "",
            "ASISTENCIA DE IA:",
            "Qwen Coder",
            "",
            "PRESIONA ESC PARA VOLVER AL MENÚ"
        ]
        
        for i, line in enumerate(credits_lines):
            color = WHITE
            if "Ing. Eduardo Pimienta" in line:
                color = GREEN
            elif any(x in line for x in ["DESARROLLADO", "HERRAMIENTAS", "ASISTENCIA"]):
                color = YELLOW
            elif "PRESIONA" in line:
                color = RED
                
            text = font_medium.render(line, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 120 + i * 40))
            self.screen.blit(text, text_rect)

    def draw_options(self):
        """Dibuja la pantalla de opciones"""
        self.screen.fill(BACKGROUND_COLOR)
        
        font_large = pygame.font.SysFont(None, 48)
        font_medium = pygame.font.SysFont(None, 36)
        
        # Título
        title = font_large.render("OPCIONES", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Mostrar opciones con valores actuales
        options = [
            f"VOLUMEN DE MÚSICA: {int(self.sound_manager.music_volume * 100)}%",
            f"VOLUMEN DE EFECTOS: {int(self.sound_manager.sfx_volume * 100)}%",
            f"VELOCIDAD DEL JUGADOR: {PLAYER_SPEED}",
            f"DIFICULTAD: {self.get_difficulty_text()}",
        ]
        
        for i, option in enumerate(options):
            # Resaltar la opción seleccionada
            color = YELLOW if i == self.option_selected else WHITE
            text = font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, 180 + i * 50))
            self.screen.blit(text, text_rect)
        
        # Instrucciones
        instructions = [
            "FLECHAS IZQ/DER: Ajustar valores",
            "FLECHAS ARR/ABAJO: Cambiar opción",
            "ESC: Volver al menú"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_medium.render(instruction, True, GREEN)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 100 + i * 30))
            self.screen.blit(text, text_rect)
    
    def draw_ui(self):
        font = pygame.font.SysFont(None, 30)
        
        # Player Health
        health_bar_width = 200
        pygame.draw.rect(self.screen, RED, (10, 10, health_bar_width, 20))
        current_health_width = health_bar_width * (self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, GREEN, (10, 10, current_health_width, 20))
        
        # Tent Health
        tent_health_bar_width = 200
        pygame.draw.rect(self.screen, RED, (WIDTH - tent_health_bar_width - 10, 10, tent_health_bar_width, 20))
        current_tent_health_width = tent_health_bar_width * (self.tent.health / self.tent.max_health)
        pygame.draw.rect(self.screen, GREEN, (WIDTH - tent_health_bar_width - 10, 10, current_tent_health_width, 20))
        
        # Weapon Info
        weapon_name = self.player.weapon.name if self.player.weapon else "None"
        weapon_text = f"Arma: {weapon_name.capitalize()}"
        text_surface = font.render(weapon_text, True, WHITE)
        self.screen.blit(text_surface, (10, 40))

        # Ammo or Heat Info
        if self.player.weapon and self.player.weapon.name in ['pistol', 'mine']:
            ammo_count = self.player.ammo.get(weapon_name, 0)
            ammo_text = f"Munición: {ammo_count}"
            ammo_surface = font.render(ammo_text, True, WHITE)
            self.screen.blit(ammo_surface, (10, 70))
            
            # Shift Wave Info down
            wave_text = f"Oleada: {self.wave}"
            wave_surface = font.render(wave_text, True, WHITE)
            self.screen.blit(wave_surface, (10, 100))

            # Shift Kills Info down
            kill_text = f"Bajas: {self.kill_count}"
            kill_surface = font.render(kill_text, True, WHITE)
            self.screen.blit(kill_surface, (10, 130))

        elif self.player.weapon and self.player.weapon.name in ['machinegun', 'flamethrower']:
            # Draw Heat Bar
            heat_bar_width = 150
            heat_bar_height = 15
            heat_x = 10
            heat_y = 70 # Below weapon name

            # Background for heat bar
            pygame.draw.rect(self.screen, BLACK, (heat_x, heat_y, heat_bar_width, heat_bar_height))
            
            current_heat = self.player.weapon.heat
            max_heat = MAX_WEAPON_HEAT # From settings
            
            heat_percentage = current_heat / max_heat
            
            # Color changes based on heat
            if self.player.weapon.overheated:
                heat_color = RED
            elif heat_percentage > 0.7:
                heat_color = ORANGE
            else:
                heat_color = YELLOW

            pygame.draw.rect(self.screen, heat_color, (heat_x, heat_y, heat_bar_width * heat_percentage, heat_bar_height))
            
            # Text for heat
            heat_text = "SOBRECALENTADO!" if self.player.weapon.overheated else f"Calor: {int(current_heat)}%"
            heat_surface = font.render(heat_text, True, WHITE)
            self.screen.blit(heat_surface, (heat_x + heat_bar_width + 5, heat_y - 2))
            
            # Show ammo count as well
            ammo_count = self.player.ammo.get(weapon_name, 0)
            ammo_text = f"Munición: {ammo_count}"
            ammo_surface = font.render(ammo_text, True, WHITE)
            self.screen.blit(ammo_surface, (10, 90))  # Below heat bar

            # Shift Wave Info down
            wave_text = f"Oleada: {self.wave}"
            wave_surface = font.render(wave_text, True, WHITE)
            self.screen.blit(wave_surface, (10, 120))

            # Shift Kills Info down
            kill_text = f"Bajas: {self.kill_count}"
            kill_surface = font.render(kill_text, True, WHITE)
            self.screen.blit(kill_surface, (10, 150))
        else: # No weapon equipped
            # Shift Wave Info down
            wave_text = f"Oleada: {self.wave}"
            wave_surface = font.render(wave_text, True, WHITE)
            self.screen.blit(wave_surface, (10, 70))

            # Shift Kills Info down
            kill_text = f"Bajas: {self.kill_count}"
            kill_surface = font.render(kill_text, True, WHITE)
            self.screen.blit(kill_surface, (10, 100))
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        stats_text = font_small.render(f"Oleada alcanzada: {self.wave}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(stats_text, stats_rect)
        
        restart_text = font_small.render("Presiona 'R' para reiniciar", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)
    
    def reset_game(self):
        """Resets the game to its initial state."""
        self.__init__()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            
            # Solo actualizar el juego si no estamos en el menú principal y no está pausado
            if not self.show_menu and not self.show_credits and not self.show_options and not self.paused:
                self.update(dt)
            
            self.draw()