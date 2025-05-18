HEIGHT = 900
WIDTH = 1200

TEMPERATURE = 50 # temperature in Kelvin, 50 recommended, 273.15 possible if grid scale is high enough
A_MOLECULES = 100 # number of starting A molecules # 2 fuse to a B molecule
B_MOLECULES = 10 # number of starting B molecules # they decay to 2 A molecules
C_MOLECULES = 0 # number of starting C molecules # they dont react

if C_MOLECULES != 0:
    GRID_SCALE = 1.2  # scaling factor for the grid size, 1.4 recommended, 1.2 if C molecules are used, 1.6 if temperature is around 273.15
else: GRID_SCALE = 1.4

CHANCE_DECAY = 0.005 # 0.5% chance per frame for B to decay into 2 A
CHANCE_COMBINE = 0.05 # 5% chance on A+A collision to combine into B

"""
velocities are in m/s
mass is in AMU
1 AMU = 1.660539E-27 kg
"""