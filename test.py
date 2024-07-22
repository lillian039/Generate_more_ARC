import numpy as np
import random

def generate_input() -> np.ndarray:
    # Define grid size randomly (minimum 3x3 to allow 3x3 blocks)
    rows = random.randint(3, 30)
    cols = random.randint(3, 30)
    
    # Create an empty grid full of black (0)
    grid = np.zeros((rows, cols), dtype=int)
    
    # Add several blue (1) 3x3 squares, ensuring they fit within the grid boundaries
    for _ in range(random.randint(1, 10)):  # Random number of blocks
        r = random.randint(0, rows-3)
        c = random.randint(0, cols-3)
        grid[r:r+3, c:c+3] = 1  # Create a 3x3 block of blue

    # Potentially add some existing orange (7) borders randomly
    for _ in range(random.randint(0, 5)):
        r = random.randint(0, rows-3)
        c = random.randint(0, cols-3)
        grid[r:r+3, c:c+3] = 7
        grid[r+1, c+1] = 1  # Make sure the central element is blue
        
    return grid

def transform_grid(input_grid: np.ndarray) -> np.ndarray:
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)
    
    # Check each possible 3x3 area
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Check if the center of the current 3x3 block is blue
            if input_grid[r+1, c+1] == 1:
                # Surround with orange but leave the 3x3 block untouched in the middle
                if r > 0:
                    output_grid[r, c:c+3] = 7
                if r < rows-3:
                    output_grid[r+3, c:c+3] = 7
                if c > 0:
                    output_grid[r+1, c] = 7
                    output_grid[r+2, c] = 7
                if c < cols-3:
                    output_grid[r+1, c+3] = 7
                    output_grid[r+2, c+3] = 7

    return output_grid

input_grid = generate_input()
output_grid = transform_grid(input_grid)  
print(input_grid)
print("************")
print(output_grid)