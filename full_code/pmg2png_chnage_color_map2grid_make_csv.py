from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def convert_pgm_to_png(input_file, output_file):
    """
    Converts a PGM or PPM file to a PNG file.

    Parameters:
        input_file (str): Path to the input PGM or PPM file.
        output_file (str): Path to save the output PNG file.
    """
    try:
        # Ensure the input file exists
        if not input_file:
            raise ValueError("Input file path is empty.")

        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file {input_file} does not exist.")

        # Open the file
        with Image.open(input_file) as img:
            # Ensure the input file is a PGM or PPM
            if img.format not in ['PGM', 'PPM']:
                raise ValueError(f"Input file {input_file} is not a PGM or PPM file.")

            # Ensure the output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Save the image as PNG
            img.save(output_file, "PNG")
            print(f"Converted {input_file} to {output_file} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_image(image_path, output_path):
    """
    Process the PNG file to identify navigable and non-navigable areas.

    Parameters:
        image_path (str): Path to the input PNG file.
        output_path (str): Path to save the processed PNG file.
    """
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return None

    # Load the image as grayscale
    map_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if map_img is None:
        print(f"Failed to load image from {image_path}")
        return None

    # Convert grayscale to color
    color_map = cv2.cvtColor(map_img, cv2.COLOR_GRAY2BGR)

    # Define thresholds for gray, white, and black
    gray_min, gray_max = 200, 210
    white_min = 254

    # Convert gray areas to green
    color_map[(map_img >= gray_min) & (map_img <= gray_max)] = [0, 255, 0]

    # Convert white areas to white
    color_map[map_img >= white_min] = [255, 255, 255]

    # Save the processed image
    cv2.imwrite(output_path, color_map)
    print(f"Processed image saved to {output_path}")

    return color_map

def generate_grid(color_map, grid_size, output_npy_path, output_csv_path):
    """
    Generate a grid representation of the map.

    Parameters:
        color_map (numpy array): Processed color map.
        grid_size (int): Size of each grid cell.
        output_npy_path (str): Path to save the grid as .npy file.
        output_csv_path (str): Path to save the grid as .csv file.
    """
    rows = color_map.shape[0] // grid_size
    cols = color_map.shape[1] // grid_size

    result_grid = np.zeros((rows, cols), dtype=int)

    # Define thresholds for classification
    green_threshold = 150
    white_threshold = 200
    black_threshold = 50

    for i in range(rows):
        for j in range(cols):
            # Extract the cell area
            cell = color_map[i * grid_size:(i + 1) * grid_size, j * grid_size:(j + 1) * grid_size]

            # Split into color channels
            R = cell[:, :, 2]
            G = cell[:, :, 1]
            B = cell[:, :, 0]

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

    # Save the resulting grid
    np.save(output_npy_path, result_grid)
    print(f"Resulting grid saved as .npy file: {output_npy_path}")

    df_grid = pd.DataFrame(result_grid)
    df_grid.to_csv(output_csv_path, index=False, header=False)
    print(f"Resulting grid saved as CSV file: {output_csv_path}")

    return result_grid

if __name__ == "__main__":
    input_file = "D:\\capstone\\24_12_11\\full_code\\result.pgm"
    png_file = "D:\\capstone\\24_12_11\\full_code\\result.png"
    processed_file = "D:\\capstone\\24_12_11\\full_code\\processed_result.png"
    grid_npy_path = "D:\\capstone\\24_12_11\\full_code\\result_grid.npy"
    grid_csv_path = "D:\\capstone\\24_12_11\\full_code\\result_grid.csv"

    # Step 1: Convert PGM to PNG
    convert_pgm_to_png(input_file, png_file)

    # Step 2: Process the PNG file
    color_map = process_image(png_file, processed_file)

    if color_map is not None:
        # Step 3: Generate the grid
        grid_size = 1  # Adjust grid size as needed
        result_grid = generate_grid(color_map, grid_size, grid_npy_path, grid_csv_path)

        # Display the resulting grid overlayed on the map
        plt.figure(figsize=(15, 15))
        plt.imshow(color_map)

        for x in range(0, color_map.shape[1], grid_size):
            plt.axvline(x=x, color='red', linewidth=0.5)
        for y in range(0, color_map.shape[0], grid_size):
            plt.axhline(y=y, color='red', linewidth=0.5)

        plt.title("Grid Overlay on Map")
        plt.axis("off")
        plt.show()
