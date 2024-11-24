import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import rotate

def image_Grid(h, w, img):
    """
    Function to divide an image into a grid and analyze each cell for navigability.

    Parameters:
    h (int): Number of vertical divisions.
    w (int): Number of horizontal divisions.
    img (2D array): Grayscale image array.

    Returns:
    map_cost (2D list): Grid with 0 for road and 1 for wall.
    cell_height (int): Height of each grid cell.
    cell_width (int): Width of each grid cell.
    """
    img_height, img_width = img.shape
    grid_size = (h, w)

    # Calculate grid cell size
    cell_height = img_height // grid_size[0]
    cell_width = img_width // grid_size[1]

    map_cost = []
    for i in range(grid_size[0]):
        map_col = []
        for j in range(grid_size[1]):
            # Get the grid cell boundaries
            cell_top = i * cell_height
            cell_left = j * cell_width
            cell_bottom = cell_top + cell_height
            cell_right = cell_left + cell_width

            # Handle the last row/column if uneven division
            if i == h - 1:
                cell_bottom = img_height
            if j == w - 1:
                cell_right = img_width

            # Extract cell and analyze pixel values
            cell = img[cell_top:cell_bottom, cell_left:cell_right]
            wall = np.sum(cell <= 210)  # Count darker pixels (walls)
            road = np.sum(cell > 210)  # Count lighter pixels (roads)

            # Determine navigability of the cell
            if road > wall:
                map_col.append(0)  # Road
            else:
                map_col.append(1)  # Wall
        map_cost.append(map_col)

    return map_cost, cell_height, cell_width

# Load the grayscale image
pgm_file = "C:/Users/mil07/Downloads/result.pgm"  # Update the path to your PGM file
img = Image.open(pgm_file).convert("L")
map_img = np.array(img)

# Rotate the map by 12.7 degrees
rotated_map = rotate(map_img, 12.7, reshape=True)

# Parameters for grid division
grid_h, grid_w = 50, 100  # Smaller, more detailed grid divisions

# Generate the grid-based map
my_map, cell_height, cell_width = image_Grid(grid_h, grid_w, rotated_map)

# Visualize the rotated map
plt.figure(figsize=(10, 10))
plt.imshow(rotated_map, cmap='gray', origin='upper')
plt.title("Rotated Map with Grid Overlay")

# Overlay the grid lines
for i in range(1, grid_h):
    plt.axhline(y=i * cell_height, color='red', linewidth=0.5)
for j in range(1, grid_w):
    plt.axvline(x=j * cell_width, color='red', linewidth=0.5)
plt.show()

# Print the grid map
print("Grid Map (0 = Road, 1 = Wall):")
for row in my_map:
    print(row)

# Visualize the analyzed grid
grid_visual = np.array(my_map)
plt.figure(figsize=(10, 10))
plt.imshow(grid_visual, cmap='gray_r', origin='upper')
plt.title("Grid Map Visualization (0 = Road, 1 = Wall)")
plt.xlabel("Grid Columns")
plt.ylabel("Grid Rows")
plt.colorbar(label="Navigability")
plt.grid(False)
plt.show()