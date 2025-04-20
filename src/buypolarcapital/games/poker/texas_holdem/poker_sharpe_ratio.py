import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from treys import Evaluator, Card, Deck
from multiprocessing import Pool, cpu_count
from matplotlib.patches import Patch

# --- Constants ---
os.makedirs("plots", exist_ok=True)
RANKS = '23456789TJQKA'
SUITS = 'cdhs'
evaluator = Evaluator()

# --- Generate 169 Starting Hands ---
def starting_hands():
    combos = []
    for i, r1 in enumerate(RANKS):
        for j, r2 in enumerate(RANKS):
            if i > j:
                continue
            if i == j:
                combos.append((r1 + r2, 'pair'))  # e.g., AA
            elif i < j:
                combos.append((r1 + r2 + 's', 'suited'))   # AKs
                combos.append((r1 + r2 + 'o', 'offsuit'))  # AKo
    return combos

# --- Combo Count for Frequency ---
def get_combo_count(hand_str):
    if len(hand_str) == 2:
        return 6   # pairs
    elif hand_str[2] == 's':
        return 4   # suited
    else:
        return 12  # offsuit

# --- Card Conversion ---
def get_card(rank, suit):
    return Card.new(rank + suit)

def generate_hole_cards(hand_str):
    rank1, rank2 = hand_str[0], hand_str[1]
    if len(hand_str) == 2:  # pair
        suits = ['h', 'd']
    elif hand_str[2] == 's':
        suits = ['h', 'h']
    else:
        suits = ['h', 'd']
    return [get_card(rank1, suits[0]), get_card(rank2, suits[1])]

# --- Simulation for One Hand Combo ---
def simulate_hand_combo(hand_combo):
    hand_str, _ = hand_combo
    player_hand = generate_hole_cards(hand_str)
    wins, ties, trials = 0, 0, 10000

    for _ in range(trials):
        deck = Deck()
        for card in player_hand:
            deck.cards.remove(card)

        opponent_hand = deck.draw(2)
        board = deck.draw(5)

        p_score = evaluator.evaluate(board, player_hand)
        o_score = evaluator.evaluate(board, opponent_hand)

        if p_score < o_score:
            wins += 1
        elif p_score == o_score:
            ties += 1

    winrate = (wins + 0.5 * ties) / trials
    combo_count = get_combo_count(hand_str)
    psr = winrate * combo_count
    return {
        'hand': hand_str,
        'winrate': winrate,
        'combo_count': combo_count,
        'psr': psr
    }

# --- Visualization: Poker Sharpe Ratio Ranking ---
def plot_psr_ranked_hands(data, hands_per_page=60, pdf_path="plots/texas_holdem_psr_bpc.pdf"):
    sorted_data = sorted(data, key=lambda d: d['psr'], reverse=True)
    x_max = max(d['psr'] for d in sorted_data) * 1.05  # consistent across pages
    mean_psr = sum(d['psr'] for d in sorted_data) / len(sorted_data)
    pages = (len(sorted_data) + hands_per_page - 1) // hands_per_page

    with PdfPages(pdf_path) as pdf:
        for p in range(pages):
            start = p * hands_per_page
            end = min((p + 1) * hands_per_page, len(sorted_data))
            batch = sorted_data[start:end]

            hands = [d['hand'] for d in batch]
            psrs = [d['psr'] for d in batch]
            winrates = [d['winrate'] for d in batch]

            colors = []
            for hand in hands:
                if len(hand) == 2:
                    colors.append("#377eb8")  # pair
                elif hand[2] == 's':
                    colors.append("#4daf4a")  # suited
                else:
                    colors.append("#e41a1c")  # offsuit

            fig, ax = plt.subplots(figsize=(11, 0.3 * len(batch) + 2))
            bars = ax.barh(hands[::-1], psrs[::-1], color=colors[::-1], edgecolor='black', alpha=0.9)

            for i, (bar, psr, wr) in enumerate(zip(bars, psrs[::-1], winrates[::-1])):
                if i < 15:
                    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                            f"{psr:.2f} | {wr*100:.1f}%", va='center', fontsize=9)

            ax.set_title("BuyPolar Capital: Poker Sharpe Ratio (Winrate × Frequency)", fontsize=14, weight='bold')
            ax.set_xlabel("Poker Sharpe Ratio (PSR)", fontsize=12)
            ax.set_ylabel("Starting Hand", fontsize=12)
            ax.set_xlim(0, x_max)
            ax.axvline(mean_psr, linestyle='--', color='gray', alpha=0.5, label='Mean PSR')
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6, axis='x')
            ax.tick_params(labelsize=9)

            # Legend
            legend_handles = [
                Patch(color="#377eb8", label="Pair"),
                Patch(color="#4daf4a", label="Suited"),
                Patch(color="#e41a1c", label="Offsuit"),
                Patch(color='gray', linestyle='--', label="Mean PSR")
            ]
            ax.legend(handles=legend_handles, title="Hand Type", loc="lower right")

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

    print(f"✅ Poker Sharpe Ratio PDF saved to {pdf_path}")

# --- Run Everything ---
if __name__ == "__main__":
    print("🔥 Simulating winrates and computing Poker Sharpe Ratios...")
    combos = starting_hands()
    with Pool(cpu_count()) as pool:
        results = pool.map(simulate_hand_combo, combos)

    plot_psr_ranked_hands(results)


