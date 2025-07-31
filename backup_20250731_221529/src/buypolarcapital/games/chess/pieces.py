import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from itertools import product

# Chess board setup
board_size = 8
pieces = {
    'pawn': [(6, i) for i in range(8)],  # White pawns
    'rook': [(7, 0), (7, 7)],
    'white_knight': [(7, 1), (7, 6)],  # White knights at b1, g1
    'black_knight': [(0, 1), (0, 6)],  # Black knights at b8, g8
    'white_square_bishop': [(7, 2)],  # Bishop at c1 (light squares)
    'black_square_bishop': [(7, 5)],  # Bishop at f1 (dark squares)
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

# Simulate moves and track visits
def simulate_moves(positions, move_func, steps=100000):
    visit_counts = np.zeros((board_size, board_size))
    current_positions = positions.copy()
    
    for _ in range(steps):
        for i, pos in enumerate(current_positions):
            r, c = pos
            visit_counts[r, c] += 1
            valid_moves = move_func(pos)
            if valid_moves:
                new_pos = valid_moves[np.random.randint(len(valid_moves))]
                current_positions[i] = new_pos
                visit_counts[new_pos[0], new_pos[1]] += 1
    
    return visit_counts

# Convert coordinates to chess notation
def to_chess_notation(row, col):
    files = 'abcdefgh'
    return f"{files[col]}{8-row}"

# Calculate statistics
def get_statistics(visit_counts):
    total_visits = visit_counts.sum()
    avg_visits = visit_counts.mean()
    std_visits = visit_counts.std()
    coverage = (visit_counts > 0).sum() / (board_size * board_size) * 100
    
    max_idx = np.unravel_index(np.argmax(visit_counts), visit_counts.shape)
    min_idx = np.unravel_index(np.argmin(visit_counts[visit_counts > 0]), visit_counts.shape)
    if visit_counts[min_idx] == 0:
        min_square = "None (unvisited squares)"
        min_count = 0
    else:
        min_square = to_chess_notation(*min_idx)
        min_count = visit_counts[min_idx]
    
    stats = {
        'total_visits': total_visits,
        'avg_visits': avg_visits,
        'std_visits': std_visits,
        'coverage': coverage,
        'max_square': to_chess_notation(*max_idx),
        'max_count': visit_counts[max_idx],
        'min_square': min_square,
        'min_count': min_count
    }
    return stats

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
    
    # Add statistics text
    stats_text = (f"Total Visits: {stats['total_visits']:,.0f}\n"
                  f"Avg Visits/Square: {stats['avg_visits']:,.2f}\n"
                  f"Std Dev: {stats['std_visits']:,.2f}\n"
                  f"Board Coverage: {stats['coverage']:,.1f}%\n"
                  f"Most Visited: {stats['max_square']} ({stats['max_count']:,.0f})\n"
                  f"Least Visited: {stats['min_square']} ({stats['min_count']:,.0f})")
    fig.text(0.02, 0.02, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

# Main execution
os.makedirs('plots', exist_ok=True)
pdf_path = 'plots/chess_piece_moves.pdf'

with PdfPages(pdf_path) as pdf:
    for piece, positions in pieces.items():
        visit_counts = simulate_moves(positions, move_functions[piece])
        stats = get_statistics(visit_counts)
        plot_heatmap(visit_counts, f'{piece.replace("_", " ").title()} Movement Heatmap', stats, pdf)

print(f"PDF saved to {pdf_path}")