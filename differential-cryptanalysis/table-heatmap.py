import numpy as np
import matplotlib.pyplot as plt

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = [line.strip().split() for line in lines]
    return data

def convert_hex_to_signed_int(matrix):
    matrix = np.array(matrix, dtype=str)
    matrix = np.vectorize(lambda x: int(x, 16))(matrix)
    matrix = np.vectorize(lambda x: x if x < 0x80 else x - 0x100)(matrix)
    return matrix

def plot_heatmap(matrix):
    plt.figure(figsize=(10, 8))
    plt.title("4-bit S-box Linear Approximation Table (LAT) Heatmap")
    plt.xlabel("Output Mask")
    plt.ylabel("Input Mask")
    plt.imshow(matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar()
    plt.show()

# Replace with the path to your .txt file
file_path = 'lat.txt'

# Read and process the data
data = read_data_from_file(file_path)
matrix = convert_hex_to_signed_int(data)

# Plot the heatmap
plot_heatmap(matrix)