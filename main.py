import pygame
import sys
from game import Game

def main():
    # Inicialización de Pygame
    pygame.init()
    pygame.display.set_caption("Zombie Survival")
    
    # Crear e iniciar el juego
    game = Game()
    game.run()
    
    # Limpiar y salir
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
