"""
¡PARÁMETROS ZOMBIE DEL APOCALIPSIS!
Aquí vivimos los valores que definen cómo se comporta tu juego zombie.
¡Cuidado al cambiarlos, puedes crear un mundo zombie aún más caótico!
"""

# Configuración de pantalla
WIDTH = 800          # Ancho de la pantalla (¡como un campo de batalla zombie!)
HEIGHT = 600         # Alto de la pantalla (¡todo el espacio que necesitas para sobrevivir!)
FPS = 60             # Cuadros por segundo (¡velocidad de la matanza zombie!)

# Colores (¡la paleta zombie!)
WHITE = (255, 255, 255)      # Blanco (¡como la esperanza en tiempos de zombies!)
BLACK = (0, 0, 0)            # Negro (¡como la noche de los zombies!)
RED = (255, 0, 0)            # Rojo (¡como la sangre zombie!)
GREEN = (0, 255, 0)          # Verde (¡como los zombies verdes!)
BLUE = (0, 0, 255)           # Azul (¡como tu vida cuando se acaba!)
YELLOW = (255, 255, 0)       # Amarillo (¡como la bala precisa!)
ORANGE = (255, 165, 0)       # Naranja (¡como la ametralladora destructora!)
BROWN = (139, 69, 19)        # Marrón (¡como la tienda de supervivencia!)
GREEN_ZOMBIE = (50, 150, 50) # Verde zombie (¡el color oficial de los zombies!)
BACKGROUND_COLOR = (20, 20, 20)  # Color de fondo (¡oscuro como el apocalipsis!)
MINE_COLOR = (128, 128, 128) # Gris (¡como una mina zombie esperando!)

# Parámetros del jugador
PLAYER_HEALTH = 200    # Vida del jugador (¡cuidado que puede terminar como zombie!)
PLAYER_SPEED = 5       # Velocidad del jugador (¡corre o serás comida zombie!)

# Parámetros de la tienda
TENT_HEALTH = 1000     # Vida de la tienda (¡más fuerte que un zombie normal!)

# Parámetros de los zombies
ZOMBIE_HEALTH = 100    # Vida de un zombie normal (¡más que la esperanza!)
ZOMBIE_SPEED = 1.5     # Velocidad de los zombies (¡lentos pero persistentes!)
ZOMBIE_DAMAGE = 10     # Daño que inflige un zombie (¡mordisco zombie!)
ZOMBIE_DETECTION_RADIUS = 250  # Radio en el que detectan al jugador (¡olfato zombie!)

# Estadísticas de armas
MAX_WEAPON_HEAT = 100  # Calor máximo antes de sobrecalentarse (¡arma que se quema!)
WEAPON_STATS = {
    # Armas y sus poderes destructivos zombie...
    'pistol': {'damage': 50, 'fire_rate': 500, 'speed': 20},  # Precisa y letal
    'machinegun': {'damage': 20, 'fire_rate': 7, 'speed': 25, 'heat_per_shot': 15, 'cooldown_rate': 30},  # Mucho fuego
    'flamethrower': {'damage': 5, 'fire_rate': 20, 'speed': 10, 'lifespan': 300, 'heat_per_shot': 5, 'cooldown_rate': 40},  # Quema todo
    'mine': {'damage': 200, 'explosion_radius': 100, 'countdown': 1000} # 1 second countdown  # Explosión poderosa
}

# Recogida de armas
WEAPON_AMMO_GIVEN = {
    # Cuánta munición da cada arma al recogerla
    'pistol': 35,        # Poco pero letal
    'machinegun': 120,   # ¡Mucho plomo!
    'flamethrower': 300, # ¡Mucho combustible!
    'mine': 8           # Unas cuantas minas explosivas
}
WEAPON_PICKUP_LIFESPAN = 20000 # 20 seconds - Tiempo que duran los pickups (¡no te demores!)

# Recogida de salud
HEALTH_PICKUP_VALUE = 0.2  # 20% of max health - Cuánto se recupera (¡un poco de esperanza zombie!)

WEAPON_SPAWN_WEIGHTS = {
    # Probabilidades de aparición de armas (¡como la lotería zombie!)
    'pistol': 40,        # Común (¡como en las películas!)
    'machinegun': 25,    # Menos común (¡arma poderosa!)
    'flamethrower': 10,  # Raro (¡arma de destrucción zombie!)
    'mine': 25         # Moderadamente común (¡arma trampa!)
}

# Parámetros del zombie jefe
BOSS_ZOMBIE_HEALTH = 1500   # ¡Vida del jefe zombie! (¡mucho más que un zombie normal!)
BOSS_ZOMBIE_SPEED = 1       # Velocidad del jefe zombie (¡lento pero poderoso!)
BOSS_ZOMBIE_SIZE = (60, 60) # Tamaño del jefe zombie (¡grande y amenazante!)
BOSS_ZOMBIE_DAMAGE = 30     # Daño del jefe zombie (¡mucho mordisco zombie!)
BOSS_ZOMBIE_COLOR = (80, 0, 80) # Púrpura (¡como un zombie elegante!)