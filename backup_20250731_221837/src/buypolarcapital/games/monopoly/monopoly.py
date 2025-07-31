import random
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import os

# Create plots directory
if not os.path.exists('plots'):
    os.makedirs('plots')

# Board setup: (name, price, type)
# type: 'property', 'station', 'utility', 'tax', 'jail', 'go', 'parking', 'go_to_jail'
board = [
    ('GO', 0, 'go'), 
    ('Parkveien', 1200, 'property'), 
    ('Prøv Lykken', 0, 'chance'), 
    ('Kirkeveien', 1200, 'property'),
    ('Inntektsskatt', 4000, 'tax'), 
    ('Oslo S.', 4000, 'station'), 
    ('Kongens gate', 2000, 'property'), 
    ('Sjanse', 0, 'chance'),
    ('Prinsens Gate', 2000, 'property'), 
    ('Øvre Slottsgate', 2400, 'property'), 
    ('Fengsel', 0, 'jail'),
    ('Pilestredet', 6000, 'property'), 
    ('Trosterudveien', 6000, 'property'), 
    ('Vannverket', 3000, 'utility'),
    ('Grorud stasjon', 4000, 'station'), 
    ('Sjanse', 0, 'chance'), 
    ('Grensen', 3600, 'property'), 
    ('Prøv Lykken', 0, 'chance'),
    ('Gabels Gate', 3600, 'property'), 
    ('Ringgata', 4000, 'property'), 
    ('Gratis Parkering', 0, 'parking'),
    ('Sinsen', 6400, 'property'), 
    ('Prøv Lykken', 0, 'chance'), 
    ('Grorud stasjon', 4000, 'station'),
    ('Trondheimsveien', 2800, 'property'), 
    ('Skøyen stasjon', 4000, 'station'), 
    ('Nobels Gate', 3200, 'property'),
    ('Sjanse', 0, 'chance'), 
    ('Ullevål Hageby', 7000, 'property'), 
    ('Oslo Lysverker', 3000, 'utility'),
    ('Luksusskatt', 2000, 'tax'), 
    ('Nedre Slottsgate', 2800, 'property'), 
    ('Bryn stasjon', 4000, 'station'),
    ('Sjanse', 0, 'chance'), 
    ('Grorud stasjon', 4000, 'station'), 
    ('Prøv Lykken', 0, 'chance'),
    ('Grensen', 3600, 'property'), 
    ('De settes i fengsel', 0, 'go_to_jail'), 
    ('Grorud stasjon', 4000, 'station'),
    ('Rådhusplassen', 8000, 'property')
]

# Initialize game
def initialize_game(num_players):
    players = [{'id': chr(65+i), 'cash': 10000, 'position': 0, 'in_jail': False, 'jail_turns': 0, 'properties': [], 'bankrupt': False} for i in range(num_players)]
    properties = {i: None for i in range(40) if board[i][2] in ['property', 'station', 'utility']}
    return players, properties

# Roll dice
def roll_dice():
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return die1 + die2, die1 == die2

# Pay rent
def pay_rent(player, owner, position):
    if board[position][2] == 'property':
        rent = board[position][1] // 10  # 10% of purchase price
    elif board[position][2] == 'station':
        rent = 500
    else:  # utility
        rent = 300
    if player['cash'] >= rent:
        player['cash'] -= rent
        owner['cash'] += rent
    else:
        player['cash'] = 0
        player['bankrupt'] = True

# Handle taxes
def handle_tax(player, position):
    if board[position][1] == 4000:  # Inntektsskatt
        tax = min(player['cash'] // 10, 4000)
    else:  # Luksusskatt
        tax = 2000
    if player['cash'] >= tax:
        player['cash'] -= tax
    else:
        player['cash'] = 0
        player['bankrupt'] = True

# Simulate one game
def simulate_game(num_players):
    players, properties = initialize_game(num_players)
    turns = 0
    while sum(1 for p in players if not p['bankrupt']) > 1 and turns < 10000:
        for player in players:
            if player['bankrupt']:
                continue
            if player['in_jail']:
                player['jail_turns'] += 1
                move, doubles = roll_dice()
                if doubles or player['jail_turns'] >= 1:
                    player['in_jail'] = False
                    player['jail_turns'] = 0
                else:
                    continue
            else:
                move, doubles = roll_dice()
            old_position = player['position']
            player['position'] = (player['position'] + move) % 40
            if player['position'] < old_position:
                player['cash'] += 4000  # Pass GO
            position = player['position']
            # Handle landing
            if board[position][2] in ['property', 'station', 'utility']:
                if position in properties:
                    if properties[position] is None:
                        if player['cash'] >= board[position][1]:
                            player['cash'] -= board[position][1]
                            properties[position] = player
                            player['properties'].append(position)
                    elif properties[position] != player:
                        pay_rent(player, properties[position], position)
            elif board[position][2] == 'tax':
                handle_tax(player, position)
            elif board[position][2] == 'go_to_jail':
                player['in_jail'] = True
                player['position'] = 10  # Jail
            turns += 1
    winner = None
    for p in players:
        if not p['bankrupt']:
            winner = p['id']
            break
    return winner

# Run simulations
def run_simulations(num_players, num_games=10000):
    wins = defaultdict(int)
    for _ in range(num_games):
        winner = simulate_game(num_players)
        if winner:
            wins[winner] += 1
    return wins

# Bootstrap resampling for win proportions
def bootstrap_win_proportions(wins, num_players, num_bootstraps=1000):
    players = [chr(65+i) for i in range(num_players)]
    win_counts = np.array([wins[p] for p in players], dtype=float)
    total = sum(wins.values())
    bootstrap_props = np.zeros((num_bootstraps, num_players))
    for i in range(num_bootstraps):
        sample = np.random.multinomial(total, win_counts/total)
        bootstrap_props[i] = sample / total
    return bootstrap_props

# Plot win distributions
def plot_win_distributions(bootstrap_props, num_players):
    players = [chr(65+i) for i in range(num_players)]
    plt.figure(figsize=(10, 6))
    for i, player in enumerate(players):
        plt.hist(bootstrap_props[:, i], bins=30, alpha=0.5, label=f'Player {player}', density=True)
    plt.title(f'Win Proportion Distribution for {num_players} Players')
    plt.xlabel('Win Proportion')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'plots/win_distribution_{num_players}_players.pdf', format='pdf', bbox_inches='tight')
    plt.close()

# Main
if __name__ == "__main__":
    random.seed(42)  # For cosmic luck
    for num_players in [2, 3, 4]:
        print(f"\nSimulating with {num_players} players:")
        wins = run_simulations(num_players, num_games=10000)
        total = sum(wins.values())
        for player in sorted(wins.keys()):
            print(f"Player {player}: {wins[player]} wins ({wins[player]/total*100:.2f}%)")
        # Generate bootstrap plots
        bootstrap_props = bootstrap_win_proportions(wins, num_players)
        plot_win_distributions(bootstrap_props, num_players)
        print(f"Saved win distribution plot to 'plots/win_distribution_{num_players}_players.pdf'")