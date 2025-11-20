# TSP Solver

A Python implementation for solving the Traveling Salesman Problem (TSP) using three different algorithms: Brute Force, MST-based Approximation, and Genetic Algorithm (Local Search).

## Project Structure

```
.
├── tsp_solver.py          # Main executable script
├── tsp_parser.py          # TSPLIB file parser
├── tsp_utils.py            # Utility functions (distance calculations)
├── tsp_brute_force.py     # Brute force algorithm
├── tsp_approx.py          # MST-based approximation algorithm
├── tsp_genetic.py         # Genetic algorithm (local search)
├── DATA/                   # TSP instance files (.tsp format)
└── README.md              # This file
```

## Requirements

-   Python 3.6 or higher
-   No external dependencies (uses only Python standard library)

## Usage

### Basic Command Format

```bash
python tsp_solver.py -inst <filename> -alg <method> -time <cutoff> [-seed <seed>]
```

### Parameters

-   `-inst`: TSP instance filename (without `.tsp` extension)

    -   Files must be in the `DATA/` directory
    -   Example: `Atlanta`, `Boston`, `NYC`

-   `-alg`: Algorithm method (required)

    -   `BF`: Brute Force (optimal solution, very slow)
    -   `Approx`: MST-based 2-approximation (fast, not optimal)
    -   `LS`: Genetic Algorithm / Local Search (heuristic, requires seed)

-   `-time`: Cutoff time in seconds (required)

    -   Must be a positive number
    -   Algorithm will stop when cutoff time is reached

-   `-seed`: Random seed (optional for BF and Approx, **required for LS**)
    -   Used for reproducibility
    -   Must be an integer

## Algorithms

### 1. Brute Force (BF)

-   **Description**: Checks all possible permutations to find the optimal solution
-   **Best For**: Small instances (≤10 cities)
-   **Note**: For larger instances, will likely hit cutoff time and return best solution found so far

### 2. Approximation Algorithm (Approx)

-   **Description**: Uses Minimum Spanning Tree (MST) with Prim's algorithm and preorder DFS traversal
-   **Approximation Ratio**: 2-approximation (solution is at most 2× optimal)
-   **Best For**: Quick solutions for any instance size

### 3. Genetic Algorithm / Local Search (LS)

-   **Description**: Evolutionary algorithm with population-based search, crossover, mutation, and elitism
-   **Best For**: Finding good solutions for medium to large instances
-   **Note**: Requires seed parameter for reproducibility

## Example Commands

### Test All Three Algorithms on Same Dataset

```bash
# Approximation Algorithm (fast)
python tsp_solver.py -inst Atlanta -alg Approx -time 60

# Genetic Algorithm (requires seed)
python tsp_solver.py -inst Atlanta -alg LS -time 60 -seed 42

# Brute Force (slow, may hit cutoff)
python tsp_solver.py -inst Atlanta -alg BF -time 60
```

### More Examples

```bash
# Run approximation on Boston
python tsp_solver.py -inst Boston -alg Approx -time 300

# Run genetic algorithm on NYC with different seed
python tsp_solver.py -inst NYC -alg LS -time 600 -seed 123

# Run brute force on small instance (Champaign)
python tsp_solver.py -inst Champaign -alg BF -time 30

# Approximation with seed (optional)
python tsp_solver.py -inst Toronto -alg Approx -time 300 -seed 42
```

## Output

### Output Files

Each run creates a solution file (`.sol`) in the current working directory with the following naming convention:

-   **BF**: `<instance> BF <cutoff>.sol`

    -   Example: `atlanta BF 60.sol`

-   **Approx**: `<instance> Approx.sol` or `<instance> Approx <seed>.sol`

    -   Example: `atlanta Approx.sol` or `atlanta Approx 42.sol`

-   **LS**: `<instance> LS <cutoff> <seed>.sol`
    -   Example: `atlanta LS 60 42.sol`

### Output File Format

Each `.sol` file contains exactly 2 lines:

1. **Line 1**: Best solution quality (total tour distance as floating point number)
2. **Line 2**: Comma-separated vertex IDs of the tour

**Example** (`atlanta Approx.sol`):

```
2380447.55
1, 2, 3, 17, 13, 9, 11, 5, 14, 8, 15, 19, 10, 16, 4, 18, 20, 6, 12, 7
```

## Error Handling

The solver will exit with an error message if:

-   TSP file not found in `DATA/` directory
-   Invalid algorithm method
-   Seed not provided for LS method
-   Cutoff time is not positive
-   Invalid file format

## Notes

-   Solution files (`.sol`) are automatically ignored by git (see `.gitignore`)
-   For large instances, Brute Force will likely not complete within cutoff time
-   Genetic Algorithm stops early if no improvement is found for 50 generations
-   All algorithms handle edge cases (empty instances, single city, etc.)

## Performance Tips

1. **Small instances (≤10 cities)**: Use BF for optimal solution
2. **Medium instances (10-50 cities)**: Use Approx for quick solution or LS for better quality
3. **Large instances (50+ cities)**: Use Approx or LS (BF will be too slow)
4. **Time constraints**: Adjust cutoff time based on instance size and algorithm

## License

This project is for educational purposes.
