import numpy as np

def generate_velocities(num_particles, temperature, mass):
    # Boltzmann constant
    k = 1.38e-23  # J/K
    
    # Calculate average speed
    avg_speed = np.sqrt(3 * k * temperature / mass)
    
    # Generate velocities from a Gaussian distribution
    velocities = np.random.normal(loc=avg_speed, scale=0.1*avg_speed, size=(num_particles, 2))  # 2D velocities

    print(velocities)
    
    # Adjust total kinetic energy
    current_kinetic_energy = 0.5 * mass * np.sum(velocities**2)
    target_kinetic_energy = num_particles * 0.5 * mass * avg_speed**2
    scaling_factor = np.sqrt(target_kinetic_energy / current_kinetic_energy)
    velocities *= scaling_factor
    print(scaling_factor)

    #velocities /= 2
    
    return velocities

# Example usage
num_particles = 10
temperature = 300  # Kelvin
mass = 1e-26  # Example mass of a particle (adjust as needed)
velocities = generate_velocities(num_particles, temperature, mass)

print(velocities[0][0], velocities[0][1])

# Print the average speed (should be close to the expected value)
avg_speed = np.sqrt(np.mean(np.sum(velocities**2, axis=1)))
print("Average speed:", avg_speed)

