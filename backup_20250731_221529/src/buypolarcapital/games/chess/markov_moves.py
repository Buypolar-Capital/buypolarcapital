import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from itertools import product
from scipy.optimize import minimize

# Chess board setup
board_size = 8
pieces = {
    'pawn': [(6, i) for i in range(8)],  # White pawns
    'rook': [(7, 0), (7, 7)],
    'white_knight': [(7, 1), (7, 6)],
    'black_knight': [(0, 1), (0, 6)],
    'white_square_bishop': [(7, 2)],
    'black_square_bishop': [(7, 5)],
    'queen': [(7, 3)],
    'king': [(7, 4)]
}

# Valid moves for each piece
def get_pawn_moves(pos):
    r, c = pos
    moves = []
    if r > 0:
        moves.append((r-1, c))
        if r == 6:
            moves.append((r-2, c))
    return moves

def get_rook_moves(pos):
    r, c = pos
    moves = []
    for i in range(board_size):
        if i != r:
            moves.append((i, c))
        if i != c:
            moves.append((r, i))
    return moves

def get_knight_moves(pos):
    r, c = pos
    moves = []
    offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < board_size and 0 <= nc < board_size:
            moves.append((nr, nc))
    return moves

def get_bishop_moves(pos):
    r, c = pos
    moves = []
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        for i in range(1, board_size):
            nr, nc = r + dr*i, c + dc*i
            if 0 <= nr < board_size and 0 <= nc < board_size:
                moves.append((nr, nc))
            else:
                break
    return moves

def get_queen_moves(pos):
    return get_rook_moves(pos) + get_bishop_moves(pos)

def get_king_moves(pos):
    r, c = pos
    moves = []
    for dr, dc in product([-1, 0, 1], repeat=2):
        if dr == 0 and dc == 0:
            continue
        nr, nc = r + dr, c + dc
        if 0 <= nr < board_size and 0 <= nc < board_size:
            moves.append((nr, nc))
    return moves

move_functions = {
    'pawn': get_pawn_moves,
    'rook': get_rook_moves,
    'white_knight': get_knight_moves,
    'black_knight': get_knight_moves,
    'white_square_bishop': get_bishop_moves,
    'black_square_bishop': get_bishop_moves,
    'queen': get_queen_moves,
    'king': get_king_moves
}

# Simulate moves and track control (number of legal moves from each position)
def simulate_control(positions, move_func, steps=10000):
    control_counts = np.zeros((board_size, board_size))  # Tracks visits
    control_values = []  # Tracks number of legal moves at each step
    current_positions = positions.copy()
    steps_per_position = steps // len(positions)  # Equal steps per piece
    
    for _ in range(steps_per_position):
        for i, pos in enumerate(current_positions):
            r, c = pos
            control_counts[r, c] += 1
            valid_moves = move_func(pos)
            control_values.append(len(valid_moves))  # Record control
            if valid_moves:
                new_pos = valid_moves[np.random.randint(len(valid_moves))]
                current_positions[i] = new_pos
                control_counts[new_pos[0], new_pos[1]] += 1
    
    return control_counts, np.array(control_values)

# Convert coordinates to chess notation
def to_chess_notation(row, col):
    files = 'abcdefgh'
    return f"{files[col]}{8-row}"

# Calculate statistics
def get_statistics(control_counts, control_values):
    total_visits = control_counts.sum()
    avg_control = control_values.mean()
    std_control = control_values.std()
    coverage = (control_counts > 0).sum() / (board_size * board_size) * 100
    
    max_idx = np.unravel_index(np.argmax(control_counts), control_counts.shape)
    min_idx = np.unravel_index(np.argmin(control_counts[control_counts > 0]), control_counts.shape)
    if control_counts[min_idx] == 0:
        min_square = "None (unvisited squares)"
        min_count = 0
    else:
        min_square = to_chess_notation(*min_idx)
        min_count = control_counts[min_idx]
    
    stats = {
        'total_visits': total_visits,
        'avg_control': avg_control,
        'std_control': std_control,
        'coverage': coverage,
        'max_square': to_chess_notation(*max_idx),
        'max_count': control_counts[max_idx],
        'min_square': min_square,
        'min_count': min_count,
        'sharpe_ratio': avg_control / std_control if std_control > 0 else 0
    }
    return stats

# Portfolio optimization (maximize Sharpe ratio)
def optimize_portfolio(returns, cov_matrix):
    n = len(returns)
    def neg_sharpe_ratio(weights):
        port_return = np.sum(returns * weights)
        port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -port_return / port_std if port_std > 0 else 0
    
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n))
    initial_guess = np.array([1/n] * n)
    
    result = minimize(neg_sharpe_ratio, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x

# Plot heatmap
def plot_heatmap(data, title, stats, pdf):
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(data, cmap='hot', interpolation='nearest')
    ax.set_title(title)
    ax.set_xticks(np.arange(board_size))
    ax.set_yticks(np.arange(board_size))
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticklabels(['8', '7', '6', '5', '4', '3', '2', '1'])
    plt.colorbar(im, label='Visit Count')
    
    stats_text = (f"Total Visits: {stats['total_visits']:,.0f}\n"
                  f"Avg Control: {stats['avg_control']:,.2f}\n"
                  f"Std Dev Control: {stats['std_control']:,.2f}\n"
                  f"Sharpe Ratio: {stats['sharpe_ratio']:,.2f}\n"
                  f"Board Coverage: {stats['coverage']:,.1f}%\n"
                  f"Most Visited: {stats['max_square']} ({stats['max_count']:,.0f})\n"
                  f"Least Visited: {stats['min_square']} ({stats['min_count']:,.0f})")
    fig.text(0.02, 0.02, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

# Plot portfolio weights
def plot_portfolio_weights(weights, piece_names, pdf):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(piece_names, weights)
    ax.set_title('Optimal Portfolio Weights')
    ax.set_ylabel('Weight')
    ax.set_xticklabels(piece_names, rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2%}',
                ha='center', va='bottom')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

# Main execution
os.makedirs('plots', exist_ok=True)
pdf_path = 'plots/chess_portfolio_sim.pdf'

# Collect data for portfolio optimization
piece_names = list(pieces.keys())
returns = []
control_values_all = []

with PdfPages(pdf_path) as pdf:
    for piece, positions in pieces.items():
        control_counts, control_values = simulate_control(positions, move_functions[piece])
        stats = get_statistics(control_counts, control_values)
        plot_heatmap(control_counts, f'{piece.replace("_", " ").title()} Control Heatmap', stats, pdf)
        returns.append(stats['avg_control'])
        # Store control values with fixed length (truncate or pad to match)
        control_values_all.append(control_values[:1000])  # Use first 1000 samples for consistency
    
    # Convert to NumPy array for covariance
    control_values_all = np.array(control_values_all)
    cov_matrix = np.cov(control_values_all)
    
    # Optimize portfolio
    weights = optimize_portfolio(np.array(returns), cov_matrix)
    
    # Plot portfolio weights
    plot_portfolio_weights(weights, piece_names, pdf)

print(f"PDF saved to {pdf_path}")