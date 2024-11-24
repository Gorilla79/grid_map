import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import yaml
from scipy.ndimage import rotate

# Load the PGM map
pgm_file = "C:/Users/mil07/Downloads/result.pgm"  # Update the path to your file
yaml_file = "C:/Users/mil07/Downloads/result.yaml"  # Update the path to your file
img = Image.open(pgm_file).convert("L")
map_array = np.array(img)

# Load metadata from YAML
with open(yaml_file, 'r') as file:
    metadata = yaml.safe_load(file)

resolution = metadata['resolution']  # Meters per pixel
origin = metadata['origin']  # Origin of the map (real-world coordinate system)
free_thresh = metadata.get('free_thresh', 0.2)
occupied_thresh = metadata.get('occupied_thresh', 0.65)

# Convert map to navigability binary map
# White = Navigable (1), Black = Wall (0), Gray = Blocked but not walls
binary_map = np.zeros_like(map_array)

# Define thresholds for each area
white_threshold = 200  # Example: Pixels >200 are white (free)
gray_threshold = 100   # Example: Pixels between 100-200 are gray (blocked)
black_threshold = 50   # Example: Pixels <50 are black (walls)

# Assign values
binary_map[map_array > white_threshold] = 1  # Navigable (white areas)
binary_map[(map_array > black_threshold) & (map_array <= gray_threshold)] = 2  # Blocked (gray areas)
binary_map[map_array <= black_threshold] = 0  # Walls (black areas)

# Rotate the map if necessary
rotated_map = rotate(binary_map, 12.7, reshape=True)

# Define grid size in meters
grid_size_m = 0.5  # Adjust this value for smaller/larger grid cells
grid_size_px = int(grid_size_m / resolution)  # Convert grid size to pixels

# Calculate grid dimensions
rows = rotated_map.shape[0] // grid_size_px
cols = rotated_map.shape[1] // grid_size_px
grid_map = np.zeros((rows, cols), dtype=int)

# Create grid map
for i in range(rows):
    for j in range(cols):
        # Extract the cell
        cell = rotated_map[
            i * grid_size_px:(i + 1) * grid_size_px,
            j * grid_size_px:(j + 1) * grid_size_px
        ]
        # Determine majority content
        wall_count = np.sum(cell == 0)  # Walls
        gray_count = np.sum(cell == 2)  # Blocked
        free_count = np.sum(cell == 1)  # Navigable

        # Assign grid value based on majority
        if free_count > (wall_count + gray_count):  # Predominantly free
            grid_map[i, j] = 1  # Navigable
        else:
            grid_map[i, j] = 0  # Not navigable

# Visualize rotated map with grid overlay
plt.figure(figsize=(10, 10))
plt.imshow(rotated_map, cmap='gray', origin='upper')
plt.title("Rotated Map with Grid Overlay")
for i in range(1, rows):
    plt.axhline(y=i * grid_size_px, color='red', linewidth=0.5)
for j in range(1, cols):
    plt.axvline(x=j * grid_size_px, color='red', linewidth=0.5)
plt.show()

# Visualize the final grid map
plt.figure(figsize=(10, 10))
plt.imshow(grid_map, cmap='gray_r', origin='upper')
plt.title("Grid Map (1 = Navigable, 0 = Not Navigable)")
plt.colorbar(label="Grid Value")
plt.show()

# Save the grid map
np.save("gridded_map.npy", grid_map)
print("Grid map saved as 'gridded_map.npy'")