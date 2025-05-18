import pygame
from pygame import Vector2

class Molecule:
    def __init__(self, position: Vector2, velocity: Vector2, mol_type: str) -> None:
        self.position: Vector2 = position
        self.velocity: Vector2 = velocity
        self.mol_type: str = mol_type
        self.past_position: Vector2 = position
        self.time = 1.0
        match mol_type:
            case "A":
                self.color: tuple[int, int, int] = (0,255,0)
                self.radius = 10
                self.mass = 10
            case "B":
                self.color: tuple[int, int, int] = (0, 0, 255)
                self.radius = 15
                self.mass = 20
            case "C":
                self.color: tuple[int, int, int] = (255, 0, 0)
                self.radius = 30
                self.mass = 100


    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (self.position.x, self.position.y), self.radius)