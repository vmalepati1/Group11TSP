"""
TSP Genetic Algorithm

This module implements a genetic algorithm for solving the Traveling Salesman Problem.
It uses evolutionary principles with population-based search, fitness-proportional selection,
crossover, mutation, and elitism to find good TSP tours.

Algorithm:
1. Initialize population of random TSP routes
2. Repeat until exit condition:
   a. Calculate fitness (inverse of tour length)
   b. Select parents proportional to fitness
   c. Perform crossover to create children
   d. Apply mutation to children
   e. Form new population with elitism
3. Return best tour found
"""

import random
import time
import copy
from tsp_utils import calculate_tour_distance


def initialize_population(vertices, population_size, seed):
    """
    Initialize a population of random TSP routes.
    
    Args:
        vertices: List of vertex IDs
        population_size: Number of individuals in population
        seed: Random seed for reproducibility
        
    Returns:
        list: Population of random tours (each is a list of vertex IDs)
    """
    random.seed(seed)
    population = []
    
    for _ in range(population_size):
        # Create a random permutation of vertices
        tour = vertices.copy()
        random.shuffle(tour)
        population.append(tour)
    
    return population


def calculate_fitness(population, coordinates):
    """
    Calculate fitness for each route in the population.
    Fitness is the inverse of tour length (shorter tours = higher fitness).
    
    Args:
        population: List of tours (each is a list of vertex IDs)
        coordinates: Dictionary mapping vertex_id -> (x, y)
        
    Returns:
        tuple: (fitness_array, distances_array, best_tour, best_distance)
        fitness_array: Normalized fitness values (sum to 1)
        distances_array: Tour distances for each individual
        best_tour: Best tour found
        best_distance: Best distance found
    """
    distances = []
    fitness = []
    
    for tour in population:
        distance = calculate_tour_distance(tour, coordinates)
        distances.append(distance)
        # Fitness is inverse of distance (avoid division by zero)
        fitness.append(1.0 / (distance + 1e-10))
    
    # Normalize fitness values so they sum to 1
    total_fitness = sum(fitness)
    if total_fitness > 0:
        normalized_fitness = [f / total_fitness for f in fitness]
    else:
        normalized_fitness = [1.0 / len(fitness)] * len(fitness)
    
    # Find best tour
    best_idx = min(range(len(distances)), key=lambda i: distances[i])
    best_tour = population[best_idx]
    best_distance = distances[best_idx]
    
    return normalized_fitness, distances, best_tour, best_distance


def select_parents(population, fitness, num_pairs):
    """
    Select parent pairs using fitness-proportional selection (roulette wheel).
    
    Args:
        population: List of tours
        fitness: Normalized fitness values (sum to 1)
        num_pairs: Number of parent pairs to select
        
    Returns:
        list: List of (parent1_idx, parent2_idx) tuples
    """
    parent_pairs = []
    
    for _ in range(num_pairs):
        # Select first parent
        r1 = random.random()
        cumsum = 0
        parent1_idx = 0
        for i, f in enumerate(fitness):
            cumsum += f
            if r1 <= cumsum:
                parent1_idx = i
                break
        
        # Select second parent (different from first)
        r2 = random.random()
        cumsum = 0
        parent2_idx = 0
        for i, f in enumerate(fitness):
            cumsum += f
            if r2 <= cumsum:
                parent2_idx = i
                break
        
        # Ensure parents are different
        if parent1_idx == parent2_idx:
            parent2_idx = (parent1_idx + 1) % len(population)
        
        parent_pairs.append((parent1_idx, parent2_idx))
    
    return parent_pairs


def crossover(parent1, parent2):
    """
    Perform crossover between two parents to create a child.
    Copy a subset of positions from parent1, then fill remaining cities
    in order from parent2, skipping cities already used.
    
    Args:
        parent1: First parent tour (list of vertex IDs)
        parent2: Second parent tour (list of vertex IDs)
        
    Returns:
        list: Child tour
    """
    n = len(parent1)
    
    # Select random subset from parent1
    start = random.randint(0, n - 1)
    length = random.randint(1, n // 2)
    end = min(start + length, n)
    
    # Copy subset from parent1
    child = [None] * n
    used_cities = set()
    
    # Copy the selected segment from parent1
    for i in range(start, end):
        child[i] = parent1[i]
        used_cities.add(parent1[i])
    
    # Fill remaining positions from parent2 in order
    parent2_idx = 0
    for i in range(n):
        if child[i] is None:
            # Find next unused city from parent2
            while parent2[parent2_idx] in used_cities:
                parent2_idx = (parent2_idx + 1) % n
            child[i] = parent2[parent2_idx]
            used_cities.add(parent2[parent2_idx])
            parent2_idx = (parent2_idx + 1) % n
    
    return child


def mutate(tour, mutation_probability):
    """
    Mutate a tour by swapping two randomly chosen cities with given probability.
    
    Args:
        tour: Tour to potentially mutate (list of vertex IDs)
        mutation_probability: Probability of mutation (0.0 to 1.0)
        
    Returns:
        list: Mutated tour (or original if no mutation)
    """
    if random.random() < mutation_probability:
        # Create a copy to avoid modifying original
        mutated = tour.copy()
        # Swap two random cities
        i, j = random.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated
    return tour


def apply_elitism(population, distances, num_elite):
    """
    Select the best N routes from the population for elitism.
    
    Args:
        population: List of tours
        distances: List of tour distances
        num_elite: Number of elite individuals to keep
        
    Returns:
        list: Elite tours
    """
    # Sort by distance (ascending)
    sorted_indices = sorted(range(len(distances)), key=lambda i: distances[i])
    elite = [population[i] for i in sorted_indices[:num_elite]]
    return elite


def solve_tsp(coordinates, cutoff_time, seed):
    """
    Solve TSP using genetic algorithm.
    
    Args:
        coordinates: Dictionary mapping vertex_id -> (x, y)
        cutoff_time: Maximum time in seconds to run
        seed: Random seed for reproducibility
        
    Returns:
        tuple: (best_tour, best_distance)
    """
    if not coordinates:
        return [], 0.0
    
    vertices = sorted(coordinates.keys())
    n = len(vertices)
    
    if n == 0:
        return [], 0.0
    if n == 1:
        return vertices, 0.0
    
    # Algorithm parameters
    population_size = max(50, min(100, n * 5))  # Scale with problem size
    mutation_probability = 0.02  # 2% mutation rate
    elite_size = max(5, population_size // 10)  # Top 10% or at least 5
    stagnation_threshold = 50  # Stop if no improvement for 50 generations
    
    # Initialize random number generator with seed
    random.seed(seed)
    
    # Initialize population
    population = initialize_population(vertices, population_size, seed)
    
    # Track best solution
    global_best_tour = None
    global_best_distance = float('inf')
    generations_without_improvement = 0
    
    start_time = time.time()
    generation = 0
    
    print(f"Running Genetic Algorithm (population: {population_size}, seed: {seed})...")
    
    while True:
        generation += 1
        
        # Check cutoff time
        elapsed = time.time() - start_time
        if elapsed > cutoff_time:
            print(f"Cutoff time ({cutoff_time}s) reached at generation {generation}")
            break
        
        # Calculate fitness
        fitness, distances, best_tour, best_distance = calculate_fitness(population, coordinates)
        
        # Update global best
        if best_distance < global_best_distance:
            global_best_distance = best_distance
            global_best_tour = best_tour.copy()
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        
        # Check stagnation
        if generations_without_improvement >= stagnation_threshold:
            print(f"Stagnation reached: no improvement for {stagnation_threshold} generations")
            break
        
        # Apply elitism - keep best routes
        elite = apply_elitism(population, distances, elite_size)
        
        # Select parents for crossover
        num_children = population_size - elite_size
        parent_pairs = select_parents(population, fitness, num_children)
        
        # Create children through crossover
        children = []
        for parent1_idx, parent2_idx in parent_pairs:
            child = crossover(population[parent1_idx], population[parent2_idx])
            # Apply mutation
            child = mutate(child, mutation_probability)
            children.append(child)
        
        # Form new population: elite + children
        population = elite + children
        
        # Progress update every 10 generations
        if generation % 10 == 0:
            print(f"Generation {generation}: Best distance = {global_best_distance:.2f}, "
                  f"Current best = {best_distance:.2f}")
    
    if global_best_tour is None:
        # Fallback: return best from final population
        _, distances, best_tour, best_distance = calculate_fitness(population, coordinates)
        return best_tour, best_distance
    
    print(f"Final best distance: {global_best_distance:.2f} (found in {generation} generations)")
    return global_best_tour, global_best_distance

