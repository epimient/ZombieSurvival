"""
╔════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                        ║
║  ███████╗██████╗  ██████╗ ██████╗                                                                      ║
║  ██╔════╝██╔══██╗██╔═══██╗██╔══██╗                                                                     ║
║  █████╗  ██████╔╝██║   ██║██████╔╝                                                                     ║
║  ██╔══╝  ██╔══██╗██║   ██║██╔══██╗                                                                     ║
║  ███████╗██║  ██║╚██████╔╝██║  ██║                                                                     ║
║  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝                                                                     ║
║                                                                                                        ║
║                            E R O R — Engineered Reality Operating Realm                                 ║
║                                                                                                        ║
║   Failure isn’t the end — it’s the beginning of control.                                                ║
║   System: ACTIVE  |  Core: ONLINE  |  Integrity: 99.98%                                                 ║
║                                                                                                        ║
║  DESARROLLADO POR: Ing. Eduardo Pimienta                                                               ║
║  FECHA: Noviembre 2025                                                                                 ║
║  TECNOLOGÍA: Python 3 + Pygame (Herramientas poderosas para desarrollo de videojuegos)                 ║
║  GÉNERO: Juego de Supervivencia con Zombies                                                            ║
║  DESCRIPCIÓN: El juego más épico de matar zombies y proteger tu tienda                                 ║
║               (¡No dejes que coman tu cerebro ni tu refugio!)                                          ║
║                                                                                                        ║
║  A.I. ASSIST: Qwen Coder (code improvement & optimization tasks)                                       ║
║                                                                                                        ║
║  ⚠ WARNING / ADVERTENCIA: This code may cause severe addiction, sleep loss, and                       ║
║               extreme anxiety when you can’t survive Wave 10.                                          ║
║                                                                                                        ║
║  ¡DIVIÉRTETE... SI ES QUE SOBREVIVES!                                                                  ║
║                                                                                                        ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

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
