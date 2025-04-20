import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import time
import random
import copy
from typing import List, Tuple, Set
import math
from multiprocessing import Pool, cpu_count, freeze_support

# Sudoku boards (9x9): 0 represents empty cells
boards = {
    'easy': np.array([
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]),
    'medium': np.array([
        [0,2,0,6,0,8,0,0,0],
        [5,8,0,0,0,9,7,0,0],
        [0,0,0,0,4,0,0,0,0],
        [3,7,0,0,0,0,5,0,0],
        [6,0,0,0,0,0,0,0,4],
        [0,0,8,0,0,0,0,1,3],
        [0,0,0,0,2,0,0,0,0],
        [0,0,9,8,0,0,0,3,6],
        [0,0,0,3,0,6,0,9,0]
    ]),
    'advanced': np.array([
        [8,0,0,0,0,0,0,0,0],
        [0,0,3,6,0,0,0,0,0],
        [0,7,0,0,9,0,2,0,0],
        [0,5,0,0,0,7,0,0,0],
        [0,0,0,0,4,5,7,0,0],
        [0,0,0,1,0,0,0,3,0],
        [0,0,1,0,0,0,0,6,8],
        [0,0,8,5,0,0,0,1,0],
        [0,9,0,0,0,0,4,0,0]
    ])
}

# Helper function to check if a number is valid in a position
def is_valid(board: np.ndarray, row: int, col: int, num: int) -> bool:
    # Check row
    if num in board[row, :]:
        return False
    # Check column
    if num in board[:, col]:
        return False
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[box_row:box_row+3, box_col:box_col+3]:
        return False
    return True

# 1. Backtracking Algorithm
def backtracking(board: np.ndarray) -> Tuple[bool, np.ndarray, float, int]:
    nodes = [0]  # Track nodes explored
    def solve(board: np.ndarray) -> bool:
        nodes[0] += 1
        empty = None
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    empty = (i, j)
                    break
            if empty:
                break
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row, col] = num
                if solve(board):
                    return True
                board[row, col] = 0
        return False
    board_copy = board.copy()
    start_time = time.time()
    solved = solve(board_copy)
    time_taken = time.time() - start_time
    return solved, board_copy, time_taken, nodes[0]

# 2. Constraint Propagation with Backtracking
def constraint_propagation(board: np.ndarray) -> Tuple[bool, np.ndarray, float, int]:
    nodes = [0]  # Track nodes explored
    possibilities = [[set(range(1, 10)) if board[i, j] == 0 else {board[i, j]} 
                      for j in range(9)] for i in range(9)]
    
    def propagate(board: np.ndarray, possibilities: List[List[Set[int]]], row: int, col: int, num: int):
        possibilities[row][col] = {num}
        # Update row, column, and box
        for j in range(9):
            if j != col and num in possibilities[row][j]:
                possibilities[row][j].discard(num)
        for i in range(9):
            if i != row and num in possibilities[i][col]:
                possibilities[i][col].discard(num)
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row+3):
            for j in range(box_col, box_col+3):
                if (i != row or j != col) and num in possibilities[i][j]:
                    possibilities[i][j].discard(num)
    
    def solve(board: np.ndarray, possibilities: List[List[Set[int]]]) -> bool:
        nodes[0] += 1
        # Find cell with fewest possibilities
        min_poss, empty = float('inf'), None
        for i in range(9):
            for j in range(9):
                if board[i, j] == 0:
                    if len(possibilities[i][j]) < min_poss:
                        min_poss, empty = len(possibilities[i][j]), (i, j)
        if not empty:
            return True
        row, col = empty
        for num in possibilities[row][col].copy():
            if is_valid(board, row, col, num):
                board[row, col] = num
                old_poss = copy.deepcopy(possibilities)
                propagate(board, possibilities, row, col, num)
                if solve(board, possibilities):
                    return True
                board[row, col] = 0
                possibilities = old_poss
        return False
    
    board_copy = board.copy()
    start_time = time.time()
    solved = solve(board_copy, possibilities)
    time_taken = time.time() - start_time
    return solved, board_copy, time_taken, nodes[0]

# 3. Dancing Links (Algorithm X)
def dancing_links(board: np.ndarray) -> Tuple[bool, np.ndarray, float, int]:
    nodes = [0]  # Track nodes explored
    def create_matrix():
        matrix = []
        for r in range(9):
            for c in range(9):
                if board[r, c] == 0:
                    for n in range(1, 10):
                        if is_valid(board, r, c, n):
                            row = []
                            # Row constraints
                            row.extend([1 if i == r else 0 for i in range(9)])
                            # Column constraints
                            row.extend([1 if i == c else 0 for i in range(9)])
                            # Number constraints
                            row.extend([1 if i == n-1 else 0 for i in range(9)])
                            # Box constraints
                            box = 3 * (r // 3) + c // 3
                            row.extend([1 if i == box else 0 for i in range(9)])
                            matrix.append((r, c, n, row))
                else:
                    row = []
                    n = board[r, c]
                    row.extend([1 if i == r else 0 for i in range(9)])
                    row.extend([1 if i == c else 0 for i in range(9)])
                    row.extend([1 if i == n-1 else 0 for i in range(9)])
                    box = 3 * (r // 3) + c // 3
                    row.extend([1 if i == box else 0 for i in range(9)])
                    matrix.append((r, c, n, row))
        return matrix
    
    def select(matrix, col, covered):
        for row in matrix:
            if row[3][col] == 1:
                for c in range(len(row[3])):
                    if row[3][c] == 1:
                        covered.add(c)
    
    def deselect(matrix, col, covered):
        for row in matrix:
            if row[3][col] == 1:
                for c in range(len(row[3])):
                    if row[3][c] == 1 and c in covered:
                        covered.remove(c)
    
    def solve_dlx(matrix, solution, covered):
        nodes[0] += 1
        if not matrix:
            return True
        # Choose column with fewest 1s
        min_ones = float('inf')
        min_col = None
        for col in range(36):
            if col not in covered:
                ones = sum(1 for row in matrix if row[3][col] == 1)
                if ones < min_ones:
                    min_ones, min_col = ones, col
        if min_col is None:
            return False
        rows = [row for row in matrix if row[3][min_col] == 1]
        for row in rows:
            solution.append(row)
            select(matrix, min_col, covered)
            new_matrix = [r for r in matrix if all(r[3][c] == 0 for c in covered)]
            if solve_dlx(new_matrix, solution, covered):
                return True
            solution.pop()
            deselect(matrix, min_col, covered)
        return False
    
    board_copy = board.copy()
    matrix = create_matrix()
    solution = []
    covered = set()
    start_time = time.time()
    solved = solve_dlx(matrix, solution, covered)
    if solved:
        for r, c, n, _ in solution:
            if board_copy[r, c] == 0:
                board_copy[r, c] = n
    time_taken = time.time() - start_time
    return solved, board_copy, time_taken, nodes[0]

# 4. Simulated Annealing
def simulated_annealing(board: np.ndarray) -> Tuple[bool, np.ndarray, float, int]:
    iterations = [0]
    def get_conflicts(board: np.ndarray) -> int:
        conflicts = 0
        for i in range(9):
            conflicts += 9 - len(set(board[i, :]))
            conflicts += 9 - len(set(board[:, i]))
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                conflicts += 9 - len(set(board[box_row:box_row+3, box_col:box_col+3].flatten()))
        return conflicts
    
    def get_empty_cells(board: np.ndarray) -> List[Tuple[int, int]]:
        return [(i, j) for i in range(9) for j in range(9) if board[i, j] == 0]
    
    board_copy = board.copy()
    empty_cells = get_empty_cells(board_copy)
    # Initialize with random valid numbers
    for i, j in empty_cells:
        valid_nums = [n for n in range(1, 10) if is_valid(board_copy, i, j, n)]
        board_copy[i, j] = random.choice(valid_nums) if valid_nums else 1
    
    temp = 1000
    cooling_rate = 0.995
    start_time = time.time()
    
    while temp > 0.1 and get_conflicts(board_copy) > 0:
        iterations[0] += 1
        i, j = random.choice(empty_cells)
        old_num = board_copy[i, j]
        valid_nums = [n for n in range(1, 10) if is_valid(board_copy, i, j, n)]
        if not valid_nums:
            continue
        new_num = random.choice(valid_nums)
        old_conflicts = get_conflicts(board_copy)
        board_copy[i, j] = new_num
        new_conflicts = get_conflicts(board_copy)
        if new_conflicts > old_conflicts and random.random() > math.exp((old_conflicts - new_conflicts) / temp):
            board_copy[i, j] = old_num
        temp *= cooling_rate
    
    time_taken = time.time() - start_time
    solved = get_conflicts(board_copy) == 0
    return solved, board_copy, time_taken, iterations[0]

# 5. Genetic Algorithm
def genetic_algorithm(board: np.ndarray) -> Tuple[bool, np.ndarray, float, int]:
    iterations = [0]
    population_size = 50
    mutation_rate = 0.1
    max_generations = 1000
    
    def fitness(board: np.ndarray) -> int:
        conflicts = 0
        for i in range(9):
            conflicts += 9 - len(set(board[i, :]))
            conflicts += 9 - len(set(board[:, i]))
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                conflicts += 9 - len(set(board[box_row:box_row+3, box_col:box_col+3].flatten()))
        return -conflicts
    
    def initialize_population(board: np.ndarray) -> List[np.ndarray]:
        empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i, j] == 0]
        population = []
        for _ in range(population_size):
            new_board = board.copy()
            for i, j in empty_cells:
                valid_nums = [n for n in range(1, 10) if is_valid(new_board, i, j, n)]
                new_board[i, j] = random.choice(valid_nums) if valid_nums else 1
            population.append(new_board)
        return population
    
    def crossover(parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
        child = parent1.copy()
        empty_cells = [(i, j) for i in range(9) for j in range(9) if parent1[i, j] == 0]
        for i, j in empty_cells:
            if random.random() < 0.5:
                child[i, j] = parent2[i, j]
        return child
    
    def mutate(board: np.ndarray):
        empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i, j] == 0]
        for i, j in empty_cells:
            if random.random() < mutation_rate:
                valid_nums = [n for n in range(1, 10) if is_valid(board, i, j, n)]
                board[i, j] = random.choice(valid_nums) if valid_nums else board[i, j]
    
    population = initialize_population(board)
    start_time = time.time()
    
    for _ in range(max_generations):
        iterations[0] += 1
        population = sorted(population, key=fitness, reverse=True)
        if fitness(population[0]) == 0:
            break
        new_population = population[:10]  # Elitism
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:20], k=2)
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)
        population = new_population
    
    time_taken = time.time() - start_time
    best_board = population[0]
    solved = fitness(best_board) == 0
    return solved, best_board, time_taken, iterations[0]

# Wrapper function for multiprocessing
def run_algorithm(args):
    diff, algo_name, algo_func, board = args
    solved, solved_board, time_taken, nodes = algo_func(board)
    return diff, algo_name, {
        'solved': solved,
        'board': solved_board,
        'time': time_taken,
        'nodes': nodes
    }

# Plot Sudoku board
def plot_board(board: np.ndarray, title: str, ax: plt.Axes):
    ax.set_title(title, fontsize=12)
    ax.axis('off')
    ax.table(cellText=[[str(num) if num != 0 else '' for num in row] for row in board],
             loc='center', cellLoc='center', bbox=[0, 0, 1, 1])
    for i in range(10):
        ax.axhline(i, color='black', linewidth=1 if i % 3 == 0 else 0.5)
        ax.axvline(i, color='black', linewidth=1 if i % 3 == 0 else 0.5)

# Plot performance comparison
def plot_comparison(results: dict, pdf: PdfPages):
    algorithms = ['Backtracking', 'Constraint Prop.', 'Dancing Links', 'Sim. Annealing', 'Genetic Alg.']
    difficulties = ['easy', 'medium', 'advanced']
    
    # Time taken bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(difficulties))
    width = 0.15
    for i, algo in enumerate(algorithms):
        times = [results[diff][algo]['time'] for diff in difficulties]
        ax.bar(x + i * width, times, width, label=algo)
    ax.set_xlabel('Difficulty')
    ax.set_ylabel('Time Taken (seconds)')
    ax.set_title('Algorithm Time Comparison')
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels([d.capitalize() for d in difficulties])
    ax.legend()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    
    # Metrics table
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    table_data = [['Algorithm', 'Difficulty', 'Solved', 'Time (s)', 'Nodes/Iterations']]
    for diff in difficulties:
        for algo in algorithms:
            res = results[diff][algo]
            table_data.append([
                algo,
                diff.capitalize(),
                'Yes' if res['solved'] else 'No',
                f"{res['time']:.4f}",
                f"{res['nodes']:,}"
            ])
    ax.table(cellText=table_data, colWidths=[0.25, 0.15, 0.1, 0.15, 0.35], loc='center')
    ax.set_title('Algorithm Performance Summary')
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    freeze_support()  # Required for Windows multiprocessing with executables
    random.seed(42)
    os.makedirs('plots', exist_ok=True)
    pdf_path = 'plots/sudoku_solver_results.pdf'

    results = {diff: {} for diff in boards}
    algorithms = {
        'Backtracking': backtracking,
        'Constraint Prop.': constraint_propagation,
        'Dancing Links': dancing_links,
        'Sim. Annealing': simulated_annealing,
        'Genetic Alg.': genetic_algorithm
    }

    # Prepare tasks for multiprocessing
    tasks = [(diff, algo_name, algo_func, boards[diff]) 
             for diff in boards for algo_name, algo_func in algorithms.items()]

    # Run algorithms in parallel
    print(f"Using {cpu_count()} CPU cores for multiprocessing")
    with Pool(processes=cpu_count()) as pool:
        task_results = pool.map(run_algorithm, tasks)

    # Collect results
    for diff, algo_name, result in task_results:
        results[diff][algo_name] = result

    with PdfPages(pdf_path) as pdf:
        for diff in boards:
            for algo_name in algorithms:
                res = results[diff][algo_name]
                solved, solved_board, time_taken, nodes = res['solved'], res['board'], res['time'], res['nodes']
                
                # Plot initial and solved boards
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
                plot_board(boards[diff], f"{diff.capitalize()} Initial Board", ax1)
                plot_board(solved_board, f"{diff.capitalize()} Solved ({algo_name})", ax2)
                fig.suptitle(f"{algo_name} on {diff.capitalize()} Board\n"
                             f"Time: {time_taken:.4f}s, Nodes/Iterations: {nodes:,}", fontsize=12)
                pdf.savefig(fig, bbox_inches='tight')
                plt.close(fig)
        
        # Plot comparison
        plot_comparison(results, pdf)

    print(f"PDF saved to {pdf_path}")