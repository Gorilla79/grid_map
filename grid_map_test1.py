import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the processed map image
image_path = "C:/Users/mil07/Downloads/processed_result.png"  # Replace with your file path
map_img = cv2.imread(image_path)  # Load as color image

# Define grid dimensions
grid_size = 10  # Adjust grid size for more/less detail
rows = map_img.shape[0] // grid_size
cols = map_img.shape[1] // grid_size

# Initialize the result grid
result_grid = np.zeros((rows, cols), dtype=int)

# Define thresholds for classification
green_threshold = 150  # Threshold for green detection
white_threshold = 200  # Threshold for white detection
black_threshold = 50   # Threshold for black detection

# Iterate over grid cells
for i in range(rows):
    for j in range(cols):
        # Extract the cell area
        cell = map_img[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]
        
        # Split into color channels
        R = cell[:, :, 2]  # Red channel
        G = cell[:, :, 1]  # Green channel
        B = cell[:, :, 0]  # Blue channel

        # Count the number of green, white, and black pixels
        green_count = np.sum((G > green_threshold) & (G > R) & (G > B))
        white_count = np.sum((R > white_threshold) & (G > white_threshold) & (B > white_threshold))
        black_count = np.sum((R < black_threshold) & (G < black_threshold) & (B < black_threshold))

        # Determine the majority color in the cell
        if green_count > white_count and green_count > black_count:
            result_grid[i, j] = 0  # Green (non-navigable)
        elif white_count > green_count and white_count > black_count:
            result_grid[i, j] = 1  # White (navigable)
        else:
            result_grid[i, j] = 0  # Black (wall)

# Display the resulting grid
plt.figure(figsize=(10, 10))
plt.imshow(result_grid, cmap="gray", origin="upper")
plt.title("Resulting Grid (0 = Green, 1 = White, -1 = Black)")
plt.axis("off")
plt.show()

# Save the grid as a .npy file for further use
np.save("result_grid.npy", result_grid)
print("Resulting grid saved as 'result_grid.npy'.")

# Print the resulting grid
print("Grid Data:")
print(result_grid)