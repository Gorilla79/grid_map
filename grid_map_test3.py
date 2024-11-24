import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the processed map image
image_path = "C:/Users/mil07/Downloads/processed_result.png"  # Replace with your file path
map_img = cv2.imread(image_path)  # Load as color image
gray_img = cv2.cvtColor(map_img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

# Define a smaller grid size for finer detail
grid_size = 1  # Smaller grid size for finer divisions
rows = gray_img.shape[0] // grid_size
cols = gray_img.shape[1] // grid_size

# Initialize the result grid
result_grid = np.zeros((rows, cols), dtype=int)

# Define thresholds for classification
green_threshold = 150  # Threshold for green detection
white_threshold = 200  # Threshold for white detection
black_threshold = 50   # Threshold for black detection

# Detect edges in the entire image (for blurry area detection)
edges = cv2.Laplacian(gray_img, cv2.CV_64F)
edge_threshold = 50  # Define a threshold for edge intensity

# Iterate over grid cells
for i in range(rows):
    for j in range(cols):
        # Extract the cell area
        cell = map_img[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]
        cell_gray = gray_img[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]
        cell_edges = edges[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]
        
        # Split into color channels
        R = cell[:, :, 2]  # Red channel
        G = cell[:, :, 1]  # Green channel
        B = cell[:, :, 0]  # Blue channel

        # Count the number of green, white, and black pixels
        green_count = np.sum((G > green_threshold) & (G > R) & (G > B))
        white_count = np.sum((R > white_threshold) & (G > white_threshold) & (B > white_threshold))
        black_count = np.sum((R < black_threshold) & (G < black_threshold) & (B < black_threshold))
        
        # Detect blurry areas
        edge_density = np.mean(cell_edges > edge_threshold)  # Proportion of strong edges
        intensity_variance = np.var(cell_gray)  # Variance of pixel intensity

        # Determine the majority color in the cell
        if edge_density > 0.2 or intensity_variance < 50:  # If blurry or low variance
            result_grid[i, j] = 0  # Non-navigable
        elif green_count > white_count and green_count > black_count:
            result_grid[i, j] = 0  # Green (non-navigable)
        elif white_count > green_count and white_count > black_count:
            result_grid[i, j] = 1  # White (navigable)
        else:
            result_grid[i, j] = 0  # Black (wall)

# Display the resulting grid
plt.figure(figsize=(10, 10))
plt.imshow(result_grid, cmap="gray", origin="upper")
plt.title("Resulting Grid with Blurry Areas Marked Non-Navigable")
plt.axis("off")
plt.show()

# Save the grid as a .npy file for further use
np.save("result_grid_blurry.npy", result_grid)
print("Resulting grid saved as 'result_grid_blurry.npy'.")

# Save the resulting grid as a CSV file
csv_output_path = "C:/Users/mil07/Downloads/result_grid2.csv"
df_grid = pd.DataFrame(result_grid)  # Convert the numpy array to a pandas DataFrame
df_grid.to_csv(csv_output_path, index=False, header=False)  # Save as CSV without index and headers
print(f"Resulting grid saved as CSV: {csv_output_path}")

# Print the resulting grid
print("Grid Data:")
print(result_grid)