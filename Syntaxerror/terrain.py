import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the terrain types as integers
TILES = {
    0: ("Grass", Fore.GREEN),    # Grass tile (Green color)
    1: ("Water", Fore.BLUE),     # Water tile (Blue color)
    2: ("Mountain", Fore.RED),    # Mountain tile (Red color)
    3: ("Tree", Fore.YELLOW)     # Tree tile (Yellow color)
}

# Define tile constraints - which tiles can be adjacent to each other
ADJACENCY_RULES = {
    0: [0, 2],  # Grass can be next to Grass or Mountain
    2: [0, 2],  # Mountain can be next to Grass or Mountain
    1: [0, 1]   # Water can only be adjacent to Water
}

class WFCTerrainGenerator:
    def __init__(self, width, height, mountain_rate, tree_chance):
        self.width = width
        self.height = height
        self.mountain_rate = mountain_rate
        self.tree_chance = tree_chance
        # Initialize grid with all possible tiles (uncollapsed)
        self.grid = [[list(TILES.keys()) for _ in range(width)] for _ in range(height)]
    
    def is_collapsed(self, cell):
        return len(cell) == 1

    def collapse(self, x, y):
        # Weighted random choice: Grass (0) more likely than Mountain (2)
        tile_weights = {0: 1- self.mountain_rate, 2: self.mountain_rate}  # Adjust weights here (higher 0 = more grass)
        possible_tiles = [tile for tile in self.grid[y][x] if tile in tile_weights]
        
        if possible_tiles:
            weighted_tiles = [tile for tile in possible_tiles for _ in range(int(tile_weights[tile] * 10))]
            self.grid[y][x] = [random.choice(weighted_tiles)]

    def get_neighbors(self, x, y, diagonals=False):
        """Get neighboring cells, including diagonals if needed."""
        neighbors = []
        if x > 0:  # Left
            neighbors.append((x - 1, y))
        if x < self.width - 1:  # Right
            neighbors.append((x + 1, y))
        if y > 0:  # Up
            neighbors.append((x, y - 1))
        if y < self.height - 1:  # Down
            neighbors.append((x, y + 1))

        if diagonals:
            if x > 0 and y > 0:  # Top-left
                neighbors.append((x - 1, y - 1))
            if x < self.width - 1 and y > 0:  # Top-right
                neighbors.append((x + 1, y - 1))
            if x > 0 and y < self.height - 1:  # Bottom-left
                neighbors.append((x - 1, y + 1))
            if x < self.width - 1 and y < self.height - 1:  # Bottom-right
                neighbors.append((x + 1, y + 1))
        
        return neighbors

    def propagate_constraints(self, x, y):
        queue = [(x, y)]
        while queue:
            cx, cy = queue.pop(0)
            tile = self.grid[cy][cx][0]  # Collapsed tile
            
            for nx, ny in self.get_neighbors(cx, cy):
                if not self.is_collapsed(self.grid[ny][nx]):
                    # Filter possible tiles for neighbor based on adjacency rules
                    allowed_tiles = ADJACENCY_RULES[tile]
                    self.grid[ny][nx] = [t for t in self.grid[ny][nx] if t in allowed_tiles]
                    # If a neighbor collapses, add it to the queue to propagate further
                    if len(self.grid[ny][nx]) == 1:
                        queue.append((nx, ny))

    def generate_random_path(self, start, end):
        """Generate a random path with diagonal moves from start to end."""
        path = []
        current = start

        while current != end:
            path.append(current)
            x, y = current

            # Determine the direction to move towards the end
            dx = end[0] - x
            dy = end[1] - y

            # List possible directions with diagonals
            possible_moves = []
            if dx > 0:
                possible_moves.append((x + 1, y))
            if dx < 0:
                possible_moves.append((x - 1, y))
            if dy > 0:
                possible_moves.append((x, y + 1))
            if dy < 0:
                possible_moves.append((x, y - 1))
            if dx > 0 and dy > 0:
                possible_moves.append((x + 1, y + 1))
            if dx < 0 and dy > 0:
                possible_moves.append((x - 1, y + 1))
            if dx > 0 and dy < 0:
                possible_moves.append((x + 1, y - 1))
            if dx < 0 and dy < 0:
                possible_moves.append((x - 1, y - 1))
                
            if random.random() < 0.9:  # 30% chance to introduce a random deviation
                jitter_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                jitter = random.choice(jitter_moves)
                possible_moves.append(jitter)
            # Introduce more randomness by adding unrelated directions (to drift)
            drift_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), 
                        (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
            
            # 50% chance to add a drift move, making the path more random and wavy
            if random.random() < 0.9:
                random_drift = random.choice(drift_moves)
                possible_moves.append(random_drift)
                random_drift = random.choice(drift_moves)
                possible_moves.append(random_drift)

            # Randomly pick one of the possible moves to add some winding randomness
            current = random.choice(possible_moves)

            # Ensure the new move stays within grid boundaries
            current = (max(0, min(self.width - 1, current[0])),
                       max(0, min(self.height - 1, current[1])))

        path.append(end)

        # Set the path tiles to "G" (Grass, 0)
        for x, y in path:
            self.grid[y][x] = [0]

        return path

    def generate(self):
        # Set the paths from all 4 corners to the center
        center = (self.width // 2, self.height // 2)  # Middle of the grid
        corners = [(0, 0), (self.width - 1, 0), (0, self.height - 1), (self.width - 1, self.height - 1)]
        
        for corner in corners:
            self.generate_random_path(corner, center)

        # Collapse the rest of the grid
        while any(not self.is_collapsed(cell) for row in self.grid for cell in row):
            # Pick a random uncollapsed cell with the least entropy (fewest possibilities)
            uncollapsed_cells = [(x, y) for y in range(self.height) for x in range(self.width) if not self.is_collapsed(self.grid[y][x])]
            if not uncollapsed_cells:
                break
            x, y = random.choice(uncollapsed_cells)

            # Collapse it
            self.collapse(x, y)
            # Propagate constraints to neighbors
            self.propagate_constraints(x, y)

    def ensure_grass_middle(self, scale):
        """Ensure the middle section is plain grass (0) of the given size."""
        mid_x = self.width // 2
        mid_y = self.height // 2
        size = int(min(mid_x, mid_y) * scale) 
        half_size = size // 2
        
        # Set the middle square to grass
        for y in range(mid_y - half_size, mid_y + half_size):
            for x in range(mid_x - half_size, mid_x + half_size):
                self.grid[y][x] = [0]

    def replace_isolated_mountains(self):
        """Replace mountains surrounded by grass with water."""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == [2]:  # Mountain (2)
                    neighbors = self.get_neighbors(x, y)
                    if all(self.grid[ny][nx] == [0] for nx, ny in neighbors):  # All neighbors are grass (0)
                        # Replace the mountain with water
                        self.grid[y][x] = [1]  # Water (1)
    def convert_isolated_tiles(self):
        """Convert all mountains and water tiles surrounded by grass into grass."""
        for y in range(1, self.height - 1):  # Avoid edges
            for x in range(1, self.width - 1):
                if self.grid[y][x] in ([1], [2]):  # Water (1) or Mountain (2)
                    neighbors = self.get_neighbors(x, y)
                    # Check if all neighbors are grass (0)
                    if all(self.grid[ny][nx] == [0] for nx, ny in neighbors):
                        # Convert the tile to grass
                        self.grid[y][x] = [0]

    def grass_to_water(self):
        """Turn grass into water if two or more adjacent neighbors are water."""
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == [0]:  # Grass (0)
                    neighbors = self.get_neighbors(x, y)
                    water_count = sum(1 for nx, ny in neighbors if self.grid[ny][nx] == [1])  # Count water neighbors
                    if water_count >= 2:  # Relaxed condition for grass to turn into water
                        self.grid[y][x] = [1]  # Grass turns into water
    
    def generate_trees(self):
        """Replace random grass tiles with trees based on a given chance (0-1)."""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == [0]:  # If the tile is grass (0)
                    if random.random() < self.tree_chance:  # tree_chance is the likelihood of placing a tree
                        self.grid[y][x] = [3]  # Set the tile to tree (3)
    
    def clear_corners(self, proportion=0.125):
        """
        Clear proportional-sized areas in all four corners of the grid for enemy spawning.
        Default proportion is 1/8 (0.125) of the grid size for each corner.
        """
        spawn_width = int(self.width * proportion)
        spawn_height = int(self.height * proportion)

        # Clear top-left corner
        self.clear_area(0, 0, spawn_width, spawn_height)
        # Clear top-right corner
        self.clear_area(self.width - spawn_width, 0, self.width, spawn_height)
        # Clear bottom-left corner
        self.clear_area(0, self.height - spawn_height, spawn_width, self.height)
        # Clear bottom-right corner
        self.clear_area(self.width - spawn_width, self.height - spawn_height, self.width, self.height)

    def clear_area(self, start_x, start_y, end_x, end_y):
        """Set the area from (start_x, start_y) to (end_x, end_y) to grass (0)."""
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                self.grid[y][x] = [0]  # Set the tile to grass (0)


    def print_grid(self):
        # Display the final grid with colors
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.grid[y][x][0]
                color = TILES[tile][1]  # Get the color associated with the tile
                row.append(color + str(tile) + Style.RESET_ALL)  # Apply the color
            print(" ".join(row))

    def create_terrain(self, scale):
        self.generate()
        self.replace_isolated_mountains()
        self.grass_to_water()
        self.convert_isolated_tiles()
        self.generate_trees()
        self.ensure_grass_middle(scale)
        self.clear_corners(0.125)
        self.print_grid()
        self.print_formatted_grid()
        
    def output_formatted_grid(self):
        formatted_grid = [[tile[0] for tile in row] for row in self.grid]
        for i in range(len(formatted_grid)):
            for j in range(len(formatted_grid[i])):
                if formatted_grid[i][j] == 0 or formatted_grid[i][j] == 3:
                    formatted_grid[i][j] = 1
                elif formatted_grid[i][j] == 1 or formatted_grid[i][j] == 2:
                    formatted_grid[i][j] = 0
        return formatted_grid
        
    def print_formatted_grid(self):
        formatted_grid = self.output_formatted_grid()
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = formatted_grid[y][x]
                color = TILES[tile][1]  # Get the color associated with the tile
                row.append(color + str(tile) + Style.RESET_ALL)  # Apply the color
            print(" ".join(row))
