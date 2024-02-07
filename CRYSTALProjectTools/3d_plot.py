import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Sample data (replace this with your actual data)
stacking_angles = np.linspace(20, 90, 5)  # Replace with your actual stacking angles
interplanar_distances = np.arange(3.4, 3.9, 0.05)  # Replace with your actual interplanar distances

# Create a meshgrid for the combinations of stacking angles and interplanar distances
stacking_angles, interplanar_distances = np.meshgrid(stacking_angles, interplanar_distances)

# Replace this with your actual flattened exchange energy data
exchange_energy_flat = np.random.rand(stacking_angles.size)  # Replace with your actual exchange energy data

# Reshape the exchange energy array to match the dimensions of the meshgrid
exchange_energy = exchange_energy_flat.reshape(stacking_angles.shape)

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(stacking_angles, interplanar_distances, exchange_energy, cmap='viridis')

# Add labels
ax.set_xlabel('Stacking Angle (degrees)')
ax.set_ylabel('Interplanar Distance')
ax.set_zlabel('Exchange Energy')

# Add a colorbar
fig.colorbar(surf, ax=ax, label='Exchange Energy')

# Show the plot
plt.show()
