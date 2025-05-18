import pygame
def get_all_neighbors(molecules: dict, width: int, height: int, grid_size: int) -> None:
    """
    Assign neighbors to each molecule using spatial hashing (uniform grid).
    molecules: dict[Molecule, list[Molecule]]
    width: simulation width
    height: simulation height
    grid_size: size of grid cell
    """

    grid = {}

    for mol in molecules:
        cell_x = int(mol.position.x // grid_size)
        cell_y = int(mol.position.y // grid_size)
        grid.setdefault((cell_x, cell_y), []).append(mol)

    # Clear neighbors first
    for mol in molecules:
        molecules[mol].clear()

    # Neighbor offsets (self cell + 8 neighbors)
    neighbor_offsets = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0), (0,  0), (1,  0),
        (-1,  1), (0,  1), (1,  1),
    ]

    # For each molecule, find neighbors from own and adjacent cells
    for (cell_x, cell_y), cell_molecules in grid.items():
        # For each molecule in this cell
        for mol in cell_molecules:
            neighbors = []
            # Check all neighbor cells
            for dx, dy in neighbor_offsets:
                neighbor_cell = (cell_x + dx, cell_y + dy)
                if neighbor_cell in grid:
                    # Add molecules from neighboring cell except self
                    for other_mol in grid[neighbor_cell]:
                        if other_mol != mol:
                            neighbors.append(other_mol)
            molecules[mol] = neighbors

def draw_grid(surface: pygame.Surface, width: int, height: int, grid_size: float) -> None:
    # Draw vertical grid lines
    x = 0
    while x <= width:
        pygame.draw.line(surface, (200, 200, 200), (x, 0), (x, height))
        x += grid_size

    # Draw horizontal grid lines
    y = 0
    while y <= height:
        pygame.draw.line(surface, (200, 200, 200), (0, y), (width, y))
        y += grid_size
