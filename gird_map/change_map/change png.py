import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = "C:/Users/mil07/Downloads/result.png"  # Replace with the correct path to your image
map_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale

# Create a color version of the grayscale image
color_map = cv2.cvtColor(map_img, cv2.COLOR_GRAY2BGR)

# Define thresholds for gray, white, and black
gray_min, gray_max = 200, 210  # Gray range
white_min = 255  # Minimum value for white

# Convert gray areas to green
color_map[(map_img >= gray_min) & (map_img <= gray_max)] = [0, 255, 0]  # Green

# Convert white areas to yellow
color_map[map_img > white_min] = [255, 255, 0]  # Yellow

# Display the result
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(color_map, cv2.COLOR_BGR2RGB))
plt.title("Gray to Green, White to Yellow")
plt.axis("off")
plt.show()

# Save the processed image
output_path = "C:/Users/mil07/Downloads/processed_result.png"
cv2.imwrite(output_path, color_map)
print(f"Processed image saved to {output_path}")