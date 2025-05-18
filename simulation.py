from pygame import Vector2
import pygame
import sys
import molecule
import movementhandler
import random
import math
import grid
from config import *


class Simulation:
    def __init__(self, width: int, height: int, delta_t: float= 0.05, headless: bool = False) -> None:
        """
        :param width: Width of the display
        :param height: Height of the display
        :param delta_t: time step
        :param headless: Not fully implemented
        """
        self.width = width
        self.height = height
        self.delta_t = delta_t
        self.headless = headless

    def generate_molecule(self,mol_type: str, temperature: float | int = 273.15) -> molecule.Molecule:
        """
        :param mol_type: type of molecule
        :param temperature: temperature in Kelvins, the speed variable (default: 273.15)
        :return: new Molecule
        """
        mol = molecule.Molecule(Vector2(0,0), Vector2(0,0), mol_type)

        # generating position
        x: float = random.uniform(mol.radius, self.width - mol.radius)
        y: float = random.uniform(mol.radius, self.height - mol.radius)
        mol.position = Vector2(x,y)

        # generating velocity with maxwell-boltzmann distribution
        k_B = 1.380649e-23
        mass_conversion = 1.660539E-27 #scaling weight to Atomic Mass Unit
        converted_mass = mass_conversion * mol.mass
        std_dev = math.sqrt(k_B * temperature/ converted_mass)
        velocity = math.sqrt(-2 * std_dev**2 * math.log(1 - random.random())) # inverse transform of Rayleigh
        angle: float = random.uniform(0, 2*math.pi) # random angle
        vx: float = velocity * math.cos(angle)
        vy: float = velocity * math.sin(angle)
        mol.velocity = Vector2(vx, vy)

        return mol

    def generate_molecules(self, molecule_count: int, mol_type, molecules: dict, temperature: int | float = 273.15,) -> None:
        """
        :param molecule_count: How many molecules to generate
        :param mol_type: Which type of molecules to generate
        :param molecules: dictionary of molecules and its possible collisions, to append the new ones
        :param temperature: In what temperature (varies the velocities) (default: 273.15
        :return: None, it appends molecules to the provided dictionary of molecules
        """
        attempts = 0
        max_attempts = 100_000
        generated = 0

        while generated < molecule_count:
            if attempts >= max_attempts:
                raise Exception("Couldn't spawn all molecules after 100_000 attempts.")

            mol = self.generate_molecule(mol_type, temperature)
            overlap = any(
                mol.position.distance_to(mols.position) < mol.radius + mols.radius
                for mols in molecules.keys()
            )

            if not overlap:
                molecules[mol] = []
                generated += 1
            attempts += 1

    def run(self, molecules) -> None:
        pygame.init()
        screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Molecule simulation")
        if self.headless: #Not fully implemented
            pygame.display.set_mode((self.width, self.height), pygame.NOFRAME | pygame.HIDDEN)
            wait_time: int = 0
        else: wait_time: int = 1000 # default 1000

        grid_size = max(mol.radius for mol in molecules) * 2 * GRID_SCALE


        running: bool = True
        MH: movementhandler.MovementHandler = movementhandler.MovementHandler(self.width, self.height, molecules, self.delta_t) # MovementHandler initialization
        while running:
            screen.fill((255, 255, 255))
            grid.draw_grid(screen, self.width, self.height, grid_size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            grid.get_all_neighbors(molecules, self.width, self.height, grid_size)

            MH.handle_movement() # handles the movement and collisions of all molecules

            for mol in molecules:
                mol.draw(screen)

            pygame.display.flip()
            pygame.time.wait(int(self.delta_t * wait_time))

        pygame.quit()
        sys.exit()