"""
¡CÓDIGO DE SONIDO ZOMBIE!
Aquí viven todos los sonidos del apocalipsis zombie.
¡Activa tu volumen para una experiencia zombie total!
"""
import pygame
import os

class SoundManager:
    def __init__(self):
        """
        ¡El DJ del apocalipsis zombie!
        Se encarga de reproducir todos los sonidos del juego: disparos, gritos zombie, explosiones, etc.
        """
        # Asegurarse que el mixer de pygame está inicializado (¡ajustes de audio como un profesional!)
        pygame.mixer.pre_init(44100, -16, 2, 512)  # Configuración de audio (frecuencia, bits, canales, buffer)
        pygame.mixer.init()  # Inicializar el mezclador de sonido
        
        # Directorio para los sonidos (¡la biblioteca de sonidos zombie!)
        self.sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')  # Carpeta 'sounds' en el juego
        
        # Volumen predeterminado (¡ajustes para que no te sordes!)
        self.sfx_volume = 0.5  # Volumen de efectos de sonido (50%)
        self.music_volume = 0.5  # Volumen de la música (50%)
        
        # Diccionario para almacenar todos los efectos de sonido (¡una discoteca zombie!)
        self.sounds = {}
        
        # Cargar sonidos (¡como un DJ preparando su set de apocalipsis!)
        self.load_sounds()
        
    def load_sounds(self):
        """Carga todos los efectos de sonido y música"""
        # Efectos de armas
        self.sounds['pistol'] = self.load_sound('pistol_shot.wav')
        self.sounds['machinegun'] = self.load_sound('machinegun_shot.wav')
        self.sounds['flamethrower'] = self.load_sound('flamethrower.wav')
        
        # Sonidos de zombies
        self.sounds['zombie_ambient'] = self.load_sound('zombie_ambient.wav')
        self.sounds['zombie_attack'] = self.load_sound('zombie_attack.wav')
        
        # Otros efectos
        self.sounds['player_hurt'] = self.load_sound('player_hurt.wav')
        self.sounds['tent_damage'] = self.load_sound('tent_damage.wav')
        self.sounds['game_over'] = self.load_sound('game_over.wav')
        self.sounds['new_wave'] = self.load_sound('new_wave.wav')
        self.sounds['health_pickup'] = self.load_sound('health_pickup.wav')
        self.sounds['boss_spawn'] = self.load_sound('boss_spawn.wav')
        self.sounds['background_music'] = self.load_sound('background_music.mp3')
        
        # Música de fondo (no se almacena en el diccionario)
        self.background_music = os.path.join(self.sound_dir, 'background_music.mp3')
    
    def load_sound(self, filename):
        """Carga un archivo de sonido individual"""
        try:
            sound_path = os.path.join(self.sound_dir, filename)
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(self.sfx_volume)
            return sound
        except pygame.error as e:
            print(f"No se pudo cargar el sonido {filename}: {e}")
            # Devolver un sonido "silencioso" como alternativa para evitar errores
            dummy = pygame.mixer.Sound(buffer=bytearray(100))
            dummy.set_volume(0)
            return dummy
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido por su nombre"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_zombie_ambient(self, count=1):
        """Reproduce sonidos de zombie basados en cuántos hay"""
        # Limitar el número de sonidos simultáneos para evitar sobrecarga
        if count > 0 and pygame.time.get_ticks() % 60 == 0:
            volume = min(0.2 + (count * 0.02), self.sfx_volume)
            self.sounds['zombie_ambient'].set_volume(volume)
            self.sounds['zombie_ambient'].play()
    
    def start_background_music(self):
        """Inicia la reproducción de la música de fondo en bucle"""
        try:
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 para reproducir en bucle infinito
        except pygame.error as e:
            print(f"No se pudo cargar la música de fondo: {e}")
    
    def stop_background_music(self):
        """Detiene la música de fondo"""
        pygame.mixer.music.stop()
    
    def set_sfx_volume(self, volume):
        """Establece el volumen para efectos de sonido (0.0 a 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """Establece el volumen para la música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)