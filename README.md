# ZombieSurvival - Juego Topdown de Defensa

Un juego de supervivencia topdown donde debes defender tu tienda de campaña de hordas interminables de zombies.
## Descripción
En Zombie Survival, eres un superviviente en medio del bosque que debe proteger su refugio (una tienda de campaña) de oleadas de zombies que no paran de llegar. Los zombies intentarán destruir tu tienda, pero también te atacarán a ti si te acercas demasiado a ellos.

## Características

Juego topdown con controles sencillos
Sistema de oleadas con dificultad progresiva
Tres armas diferentes para combatir zombies:

Pistola: Disparo lento pero potente
Metralleta: Disparo rápido con menor daño por bala
Lanzallamas: Ataque de área con daño sobre tiempo

IA básica para los zombies que priorizan entre atacar al jugador o a la tienda
Sistema de salud para el jugador y la tienda
Interfaz de usuario que muestra información relevante del juego

## Requisitos

Python 3.x
Pygame

## Instalación

Asegúrate de tener Python instalado en tu sistema
Instala Pygame ejecutando:

pip install pygame

Descarga o clona este repositorio
Navega hasta la carpeta del juego y ejecuta:

python main.py

## Controles

Movimiento: Teclas de flecha o WASD
Apuntar: Mover el mouse
Disparar: Clic izquierdo del mouse
Cambiar armas:

Tecla 1: Pistola
Tecla 2: Metralleta
Tecla 3: Lanzallamas

Reiniciar (tras Game Over): Tecla R

## Estructura del Proyecto

main.py: Punto de entrada del juego
game.py: Clase principal que gestiona el estado del juego
player.py: Implementación del jugador
zombie.py: Implementación de los enemigos zombies
tent.py: Implementación de la tienda que debes defender
weapon.py: Implementación de las armas y proyectiles
settings.py: Constantes y configuraciones del juego

## Personalización

Actualmente, el juego utiliza formas básicas (rectángulos de colores) para representar todos los elementos. Esto facilita la comprensión del código y su funcionamiento antes de añadir gráficos más elaborados.
Para personalizar el juego, puedes:

Añadir sprites en lugar de rectángulos
Incorporar efectos de sonido y música
Añadir nuevas armas o tipos de zombies
Implementar power-ups o mejoras para el jugador

## Mecánicas de Juego

### El Jugador
El jugador tiene una barra de salud que disminuye cuando los zombies lo tocan. Si la salud llega a cero, el juego termina.

### La Tienda

La tienda tiene su propia barra de salud. Si los zombies la destruyen, el juego termina.

### Los Zombies

Los zombies seguirán este comportamiento:

Si el jugador está cerca (dentro del radio de detección), lo perseguirán
Si el jugador está lejos, atacarán la tienda

### Las Oleadas
Cada oleada trae más zombies y estos aparecen más rápido, aumentando progresivamente la dificultad del juego.

## Futuras Mejoras

Añadir sistema de puntuación
Implementar mejoras para las armas
Añadir diferentes tipos de zombies
Incorporar obstáculos en el mapa
Añadir efectos visuales para disparos y explosiones
Implementar un sistema de guardado/carga
