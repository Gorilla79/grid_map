import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the input map image
map_file = "C:/Users/mil07/Downloads/processed_result.png"  # Update this to the correct file path
map_img = cv2.imread(map_file, cv2.IMREAD_COLOR)  # Load as color image (BGR)

# Convert BGR to RGB for easier color handling
map_img = cv2.cvtColor(map_img, cv2.COLOR_BGR2RGB)

# Define RGB values for classification
yellow_rgb = [255, 255, 0]  # Navigable (yellow)
green_rgb = [0, 255, 0]  # Non-navigable (green)
black_rgb = [0, 0, 0]  # Wall (black)

# Initialize a binary map (default to non-navigable)
classified_map = np.zeros((map_img.shape[0], map_img.shape[1]), dtype=int)

# Classify pixels based on color
for i in range(map_img.shape[0]):
    for j in range(map_img.shape[1]):
        pixel = map_img[i, j]
        if np.array_equal(pixel, yellow_rgb):  # Yellow
            classified_map[i, j] = 1  # Navigable
        elif np.array_equal(pixel, green_rgb):  # Green
            classified_map[i, j] = 2  # Non-navigable
        elif np.array_equal(pixel, black_rgb):  # Black
            classified_map[i, j] = 0  # Wall

# Visualize the classified map
color_map = np.zeros((map_img.shape[0], map_img.shape[1], 3), dtype=np.uint8)

# Assign colors to the classified areas
for i in range(classified_map.shape[0]):
    for j in range(classified_map.shape[1]):
        if classified_map[i, j] == 1:  # Navigable
            color_map[i, j] = [255, 255, 0]  # Yellow
        elif classified_map[i, j] == 2:  # Non-navigable
            color_map[i, j] = [0, 255, 0]  # Green
        elif classified_map[i, j] == 0:  # Wall
            color_map[i, j] = [0, 0, 0]  # Black

# Display the final classified map
plt.figure(figsize=(10, 10))
plt.imshow(color_map)
plt.title("Classified Map (Yellow = Navigable, Green = Non-navigable, Black = Wall)")
plt.axis("off")
plt.show()

# Save the classified map as an image (optional)
output_file = "C:/Users/mil07/Downloads/classified_map.png"
cv2.imwrite(output_file, cv2.cvtColor(color_map, cv2.COLOR_RGB2BGR))
print(f"Classified map saved to {output_file}")