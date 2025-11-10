# PYZOMBIE - Zombie Survival

Un emocionante juego de supervivencia zombie en Python con Pygame donde debes proteger tu tienda de oleadas de zombies. ¡Sobrevive tantas oleadas como puedas y enfrenta jefes poderosos!

## Desarrollado por
Ing. Eduardo Pimienta

## Asistencia de IA
Qwen Coder (para tareas de mejora, comentario y optimización de código)

## Tecnología
- Python 3
- Pygame

## Descripción

En PYZOMBIE, eres un superviviente en medio del bosque que debe proteger su refugio (una tienda de campaña) de oleadas interminables de zombies que no paran de llegar. Los zombies intentarán destruir tu tienda, pero también te atacarán a ti si te acercas demasiado a ellos.

## Características Principales

- **Sistema de menú completo**: Menú principal con opciones de iniciar juego, configuraciones y créditos
- **Juego topdown con controles sencillos**
- **Sistema de oleadas con dificultad progresiva**
- **4 armas diferentes para combatir zombies**:
  - **Pistola**: Disparo preciso con alto daño
  - **Ametralladora**: Disparo rápido con menor daño por bala
  - **Lanzallamas**: Ataque de área con daño sobre tiempo
  - **Minas**: Armas trampa que explotan al contacto
- **IA avanzada para zombies y jefes**:
  - Zombies normales persiguen jugador o tienda dependiendo de la distancia
  - Zombie jefe **siempre persigue al jugador** y **no desaparece al tocar la tienda**
  - Jefe zombie se vuelve más rápido e impredecible con poca vida
  - Jefe zombie puede generar zombies auxiliares periódicamente
- **Sistema de salud para el jugador y la tienda**
- **Interfaz de usuario con barras de vida, municiones y estadísticas**
- **Sistema de pausa con menú completo**: Continuar juego, opciones o volver al menú principal
- **Sistema de configuración**: Ajuste de volumen de música y efectos en tiempo real
- **Sistema de recolección**: Armas y curaciones que aparecen en el mapa
- **Sin armas iniciales en el mapa**: El jugador comienza con una pistola equipada

## Requisitos

- Python 3.x
- Pygame

## Instalación

1. Asegúrate de tener Python instalado en tu sistema
2. Instala Pygame ejecutando:
   ```
   pip install pygame
   ```
3. Descarga o clona este repositorio
4. Navega hasta la carpeta del juego y ejecuta:
   ```
   python main.py
   ```

## Controles

- **Movimiento**: Teclas de flecha o WASD
- **Apuntar**: Mover el mouse
- **Disparar**: Clic izquierdo del mouse (automático para ametralladora y lanzallamas, manual para pistola y minas)
- **Cambiar armas**:
  - Tecla 1: Pistola
  - Tecla 2: Ametralladora
  - Tecla 3: Lanzallamas
  - Tecla 4: Minas
- **Pausar/Reanudar**: Tecla ESC
- **Reiniciar** (tras Game Over): Tecla R

## Navegación en Menús

- **Menú Principal**: Flechas para navegar, Enter para seleccionar
- **Opciones**: Flechas izq/der para ajustar valores, flechas arriba/abajo para cambiar opción
- **Pausa**: Flechas para navegar, Enter para seleccionar, ESC para continuar

## Estructura del Proyecto

- **main.py**: Punto de entrada del juego
- **game.py**: Clase principal que gestiona el estado del juego, menús y pausa
- **player.py**: Implementación del jugador con sistema de armas
- **zombie.py**: Implementación de zombies normales y jefe con IA avanzada
- **tent.py**: Implementación de la tienda que debes defender
- **weapon.py**: Implementación de las armas, proyectiles y minas
- **sound.py**: Sistema de sonido con control de volumen
- **settings.py**: Constantes y configuraciones del juego
- **weapon_pickup.py**: Sistema de recolección de armas
- **health_pickup.py**: Sistema de recolección de curaciones

## Mecánicas de Juego

### El Jugador

El jugador tiene una barra de salud que disminuye cuando los zombies lo tocan. Si la salud llega a cero, el juego termina. Comienza con una pistola equipada y municiones.

### La Tienda

La tienda tiene su propia barra de salud. Si los zombies la destruyen, el juego termina. Solo los zombies normales desaparecen al tocarla, el jefe zombie continúa atacando.

### Los Zombies

Los zombies normales siguen este comportamiento:
1. Si el jugador está cerca (dentro del radio de detección), lo perseguirán
2. Si el jugador está lejos, atacarán la tienda

### Zombies Jefe

Los zombies jefe tienen comportamiento especial:
1. **Siempre** persiguen al jugador, ignorando la tienda
2. Se vuelven más rápidos e impredecibles con poca vida
3. Pueden generar zombies auxiliares periódicamente
4. No desaparecen al tocar la tienda, continúan atacando

### Las Oleadas

Cada oleada trae más zombies y estos aparecen más rápido, aumentando progresivamente la dificultad del juego. Cada 5 oleadas aparece un jefe zombie con habilidades especiales.

### Minas

Las minas son armas trampa que puedes colocar en el mapa:
1. Explota al contacto con zombies o jugador
2. No se pueden colocar cerca de la tienda (80 píxeles de distancia mínima)
3. Causan daño en área

## Personalización

Actualmente, el juego utiliza formas básicas (rectángulos de colores) para representar todos los elementos. Esto facilita la comprensión del código y su funcionamiento antes de añadir gráficos más elaborados.

Para personalizar el juego, puedes:
- Añadir sprites en lugar de rectángulos
- Añadir nuevas armas o tipos de zombies
- Implementar power-ups o mejoras para el jugador
- Añadir diferentes tipos de zombies jefe
- Expandir el sistema de opciones con más configuraciones

## Futuras Mejoras

- Añadir sistema de puntuación avanzado
- Implementar mejoras permanentes para las armas
- Añadir diferentes tipos de zombies jefe con habilidades únicas
- Incorporar obstáculos y elementos interactivos en el mapa
- Añadir efectos visuales para disparos y explosiones
- Implementar un sistema de guardado/carga
- Añadir niveles o mapas diferentes
- Incorporar logros o desafíos diarios
