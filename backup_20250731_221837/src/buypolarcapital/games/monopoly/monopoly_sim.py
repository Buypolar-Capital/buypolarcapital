import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
import random
from scipy.optimize import minimize

# Board setup: (name, price, type, rent)
board = [
    ('GO', 0, 'go', 0), 
    ('Parkveien', 1200, 'property', 120), 
    ('Prøv Lykken', 0, 'chance', 0), 
    ('Kirkeveien', 1200, 'property', 120),
    ('Inntektsskatt', 4000, 'tax', 0), 
    ('Oslo S.', 4000, 'station', 500), 
    ('Kongens gate', 2000, 'property', 200), 
    ('Sjanse', 0, 'chance', 0),
    ('Prinsens Gate', 2000, 'property', 200), 
    ('Øvre Slottsgate', 2400, 'property', 240), 
    ('Fengsel', 0, 'jail', 0),
    ('Pilestredet', 6000, 'property', 600), 
    ('Trosterudveien', 6000, 'property', 600), 
    ('Vannverket', 3000, 'utility', 300),
    ('Grorud stasjon', 4000, 'station', 500), 
    ('Sjanse', 0, 'chance', 0), 
    ('Grensen', 3600, 'property', 360), 
    ('Prøv Lykken', 0, 'chance', 0),
    ('Gabels Gate', 3600, 'property', 360), 
    ('Ringgata', 4000, 'property', 400), 
    ('Gratis Parkering', 0, 'parking', 0),
    ('Sinsen', 6400, 'property', 640), 
    ('Prøv Lykken', 0, 'chance', 0), 
    ('Grorud stasjon', 4000, 'station', 500),
    ('Trondheimsveien', 2800, 'property', 280), 
    ('Skøyen stasjon', 4000, 'station', 500), 
    ('Nobels Gate', 3200, 'property', 320),
    ('Sjanse', 0, 'chance', 0), 
    ('Ullevål Hageby', 7000, 'property', 700), 
    ('Oslo Lysverker', 3000, 'utility', 300),
    ('Luksusskatt', 2000, 'tax', 0), 
    ('Nedre Slottsgate', 2800, 'property', 280), 
    ('Bryn stasjon', 4000, 'station', 500),
    ('Sjanse', 0, 'chance', 0), 
    ('Grorud stasjon', 4000, 'station', 500), 
    ('Prøv Lykken', 0, 'chance', 0),
    ('Grensen', 3600, 'property', 360), 
    ('De settes i fengsel', 0, 'go_to_jail', 0), 
    ('Grorud stasjon', 4000, 'station', 500),
    ('Rådhusplassen', 8000, 'property', 800)
]

# Property indices for portfolio
property_indices = [i for i, space in enumerate(board) if space[2] in ['property', 'station', 'utility']]
property_names = [board[i][0] for i in property_indices]

# Roll dice
def roll_dice():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1 + die2, die1 == die2

# Simulate player movement
def simulate_movement(steps=10000):
    visit_counts = np.zeros(40)
    position = 0
    in_jail = False
    jail_turns = 0
    doubles_count = 0
    
    for _ in range(steps):
        if in_jail:
            jail_turns += 1
            move, doubles = roll_dice()
            if doubles or jail_turns >= 3:
                in_jail = False
                jail_turns = 0
                doubles_count = 1 if doubles else 0
            else:
                visit_counts[10] += 1  # Jail
                continue
        else:
            move, doubles = roll_dice()
            if doubles:
                doubles_count += 1
            else:
                doubles_count = 0
            if doubles_count >= 3:
                position = 10  # Jail
                in_jail = True
                jail_turns = 0
                doubles_count = 0
                visit_counts[position] += 1
                continue
        
        old_position = position
        position = (position + move) % 40
        if position < old_position:
            visit_counts[0] += 1  # Pass GO
        
        if board[position][2] == 'go_to_jail':
            position = 10
            in_jail = True
            jail_turns = 0
        
        visit_counts[position] += 1
    
    return visit_counts

# Calculate returns and risk
def get_property_stats(visit_counts, num_simulations=100):
    visit_frequencies = visit_counts / visit_counts.sum()
    returns = []
    visit_samples = np.zeros((num_simulations, len(property_indices)))
    
    for i, idx in enumerate(property_indices):
        price = board[idx][1]
        rent = board[idx][3]
        # Expected ROI = (rent * visit frequency) / price
        expected_roi = (rent * visit_frequencies[idx]) / price if price > 0 else 0
        returns.append(expected_roi)
        
        # Run multiple simulations for volatility
        for sim in range(num_simulations):
            sim_counts = simulate_movement()
            sim_freq = sim_counts[idx] / sim_counts.sum()
            visit_samples[sim, i] = sim_freq
    
    # Calculate covariance matrix
    cov_matrix = np.cov(visit_samples.T)
    return np.array(returns), cov_matrix, visit_frequencies

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

# Plot board heatmap
def plot_heatmap(visit_frequencies, stats, pdf):
    board_layout = np.zeros((4, 11))  # 4x11 board for visualization
    # Define positions for exactly 40 spaces (clockwise from GO)
    positions = [
        # Bottom row: GO (0) to Jail (10) - 11 spaces
        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
        # Right side: Jail (11) to Free Parking (20) - 10 spaces
        (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1),
        # Top row: Free Parking (21) to Go to Jail (30) - 10 spaces
        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
        # Left side: Go to Jail (31) to Rådhusplassen (39) - 9 spaces
        (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2)
    ]
    
    # Ensure we don't exceed array bounds
    if len(visit_frequencies) != len(positions):
        raise ValueError(f"Mismatch: visit_frequencies has {len(visit_frequencies)} elements, but positions has {len(positions)}")
    
    for i, (row, col) in enumerate(positions):
        board_layout[row, col] = visit_frequencies[i]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(board_layout, cmap='hot', interpolation='nearest')
    ax.set_title('Monopoly Board Visit Frequency Heatmap')
    ax.set_xticks(np.arange(11))
    ax.set_yticks(np.arange(4))
    ax.set_xticklabels(['GO', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Jail/Free'])
    ax.set_yticklabels(['Left', 'Top', 'Right', 'Bottom'])
    plt.colorbar(im, label='Visit Frequency')
    
    stats_text = (f"Total Visits: {stats['total_visits']:,.0f}\n"
                  f"Avg Visit Frequency: {stats['avg_frequency']:.4f}\n"
                  f"Std Dev Frequency: {stats['std_frequency']:.4f}\n"
                  f"Board Coverage: {stats['coverage']:.1f}%")
    fig.text(0.02, 0.02, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

# Plot portfolio weights
def plot_portfolio_weights(weights, property_names, pdf):
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(property_names, weights)
    ax.set_title('Optimal Property Portfolio Weights')
    ax.set_ylabel('Weight')
    ax.set_xticklabels(property_names, rotation=90)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2%}',
                ha='center', va='bottom')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)

# Calculate statistics
def get_statistics(visit_counts):
    total_visits = visit_counts.sum()
    visit_frequencies = visit_counts / total_visits
    avg_frequency = visit_frequencies.mean()
    std_frequency = visit_frequencies.std()
    coverage = (visit_counts > 0).sum() / len(board) * 100
    
    stats = {
        'total_visits': total_visits,
        'avg_frequency': avg_frequency,
        'std_frequency': std_frequency,
        'coverage': coverage
    }
    return stats

# Main execution
random.seed(42)
os.makedirs('plots', exist_ok=True)
pdf_path = 'plots/monopoly_portfolio_sim.pdf'

with PdfPages(pdf_path) as pdf:
    # Simulate movement
    visit_counts = simulate_movement()
    stats = get_statistics(visit_counts)
    
    # Plot visit frequency heatmap
    plot_heatmap(visit_counts / visit_counts.sum(), stats, pdf)
    
    # Portfolio optimization
    returns, cov_matrix, visit_frequencies = get_property_stats(visit_counts)
    weights = optimize_portfolio(returns, cov_matrix)
    
    # Plot portfolio weights
    plot_portfolio_weights(weights, property_names, pdf)

print(f"PDF saved to {pdf_path}")