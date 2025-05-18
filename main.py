import simulation as sim
from config import *

if __name__ == "__main__":
    simulation = sim.Simulation(WIDTH, HEIGHT)
    molecules = {}
    simulation.generate_molecules(A_MOLECULES, "A", molecules, temperature=TEMPERATURE)
    simulation.generate_molecules(B_MOLECULES, "B", molecules, temperature=TEMPERATURE)
    simulation.generate_molecules(C_MOLECULES, "C", molecules, temperature=TEMPERATURE)
    simulation.run(molecules)