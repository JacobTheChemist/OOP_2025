import math
from pygame import Vector2
import molecule
import random
from config import *

class MovementHandler:
    def __init__(self, width, height, molecules: dict, delta_t: float) -> None:
        self.width = width
        self.height = height
        self.dt = delta_t
        self.molecules = molecules

    def handle_movement(self):
        self.try_decay("B", "A") # tries decaying all B molecules to A before calculating the next frame
        for mol in self.molecules:
            mol.time = 1.0
            mol.past_position = mol.position.copy()
        time_left = 1.0
        while time_left > 0:
            soonest_time = time_left
            collision_type = None
            collision_data = None

            for mol in self.molecules:
                t_wall, axis = self.time_to_wall_collision(mol)
                if t_wall is not None and 0 <= t_wall < soonest_time:
                    soonest_time = t_wall
                    collision_type = "wall"
                    collision_data = (mol, axis)

            for mol in self.molecules:
                for other in self.molecules[mol]:
                    t_mol = self.time_to_molecule_collision(mol, other)
                    if t_mol is not None and 0 <= t_mol < soonest_time:
                        soonest_time = t_mol
                        collision_type = "mol"
                        collision_data = (mol, other)

            for mol in self.molecules:
                mol.position += mol.velocity * self.dt * soonest_time
                mol.time -= soonest_time

            time_left -= soonest_time

            if collision_type == "wall":
                self.handle_wall_collision(*collision_data)
            elif collision_type == "mol":
                self.handle_molecule_collision(*collision_data)

    def time_to_wall_collision(self, mol):
        times = []
        if mol.velocity.x != 0:
            if mol.velocity.x > 0:
                t = (self.width - mol.radius - mol.position.x) / (mol.velocity.x * self.dt)
            else:
                t = (mol.radius - mol.position.x) / (mol.velocity.x * self.dt)
            if 0 <= t <= mol.time:
                times.append((t, 'x'))

        if mol.velocity.y != 0:
            if mol.velocity.y > 0:
                t = (self.height - mol.radius - mol.position.y) / (mol.velocity.y * self.dt)
            else:
                t = (mol.radius - mol.position.y) / (mol.velocity.y * self.dt)
            if 0 <= t <= mol.time:
                times.append((t, 'y'))

        def get_time(collision):
            return collision[0]

        if times:
            soonest = min(times, key=get_time)
            return soonest
        else:
            return (None, None)

    def time_to_molecule_collision(self, mol1, mol2):
        dp = mol1.position - mol2.position
        dv = mol1.velocity * self.dt - mol2.velocity * self.dt
        r = mol1.radius + mol2.radius

        a = dv.dot(dv)
        if a == 0:
            return None
        b = 2 * dp.dot(dv)
        c = dp.dot(dp) - r * r

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None

        sqrt_d = math.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2 * a)
        if 0 <= t1 <= mol1.time:
            return t1
        return None

    def handle_wall_collision(self, mol, axis):
        if axis == 'x':
            mol.velocity.x *= -1
        elif axis == 'y':
            mol.velocity.y *= -1

    def handle_molecule_collision(self, mol1, mol2):
        delta = mol1.position - mol2.position
        dist = delta.length()
        if dist == 0:
            return
        normal = delta.normalize()
        rel_vel = mol1.velocity - mol2.velocity
        speed = rel_vel.dot(normal)
        if speed >= 0:
            return
        impulse = -(1 + 1) * speed / (1 / mol1.mass + 1 / mol2.mass)
        mol1.velocity += impulse * normal / mol1.mass
        mol2.velocity -= impulse * normal / mol2.mass

        # Fusion
        if mol1.mol_type == "A" and mol2.mol_type == "A":
            if random.random() < CHANCE_COMBINE:

                p_total = mol1.velocity * mol1.mass + mol2.velocity * mol2.mass
                mass_after = mol1.mass + mol2.mass

                v_after = p_total / mass_after
                pos_after = (mol1.position + mol2.position) / 2

                new_after = molecule.Molecule(pos_after, v_after, "B")

                if mol1 in self.molecules:
                    del self.molecules[mol1]
                if mol2 in self.molecules:
                    del self.molecules[mol2]
                self.molecules[new_after] = []

    def try_decay(self, from_type: str, to_type :str):

        for mol in list(self.molecules.keys()):
            if mol.mol_type == from_type:
                if random.random() < CHANCE_DECAY:
                    pos = mol.position
                    angle = random.uniform(0, 2 * math.pi)

                    direction = Vector2(math.cos(angle), math.sin(angle))
                    rel_velocity = mol.velocity.length()

                    v1 = direction * rel_velocity + mol.velocity
                    v2 = -direction * rel_velocity + mol.velocity

                    offset = direction * mol.radius * 0.5

                    mol1 = molecule.Molecule(pos + offset, v1, to_type)
                    mol2 = molecule.Molecule(pos - offset, v2, to_type)

                    self.molecules[mol1] = []
                    self.molecules[mol2] = []
                    del self.molecules[mol]


