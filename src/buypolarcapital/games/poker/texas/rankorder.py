import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from treys import Evaluator, Card, Deck
from multiprocessing import Pool, cpu_count

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
    return hand_str, winrate


# --- Visualization: Styled & Paginated ---
def plot_ranked_hands_bpc(sorted_results, hands_per_page=60, pdf_path="plots/texas_holdem_hand_rankings_bpc.pdf"):
    pages = (len(sorted_results) + hands_per_page - 1) // hands_per_page

    with PdfPages(pdf_path) as pdf:
        for p in range(pages):
            start = p * hands_per_page
            end = min((p + 1) * hands_per_page, len(sorted_results))
            batch = sorted_results[start:end]

            hands = [k for k, _ in batch]
            winrates = [v for _, v in batch]
            colors = []

            for hand in hands:
                if len(hand) == 2:
                    colors.append("#377eb8")  # pair: blue
                elif hand[2] == 's':
                    colors.append("#4daf4a")  # suited: green
                else:
                    colors.append("#e41a1c")  # offsuit: red

            fig, ax = plt.subplots(figsize=(11, 0.3 * len(batch) + 2))
            bars = ax.barh(hands[::-1], winrates[::-1], color=colors[::-1], edgecolor='black', alpha=0.9)

            # Annotate top hands
            for i, (bar, wr) in enumerate(zip(bars, winrates[::-1])):
                if i < 10:
                    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
                            f"{wr*100:.1f}%", va='center', fontsize=9)

            ax.set_title("BuyPolar Capital: Pre-Flop Win Rates vs Random Hand (Heads-Up)", fontsize=14, weight='bold')
            ax.set_xlabel("Win Probability", fontsize=12)
            ax.set_ylabel("Starting Hand", fontsize=12)
            ax.set_xlim(0, 1)
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6, axis='x')
            ax.tick_params(labelsize=9)

            # Legend proxy
            from matplotlib.patches import Patch
            legend_handles = [
                Patch(color="#377eb8", label="Pair"),
                Patch(color="#4daf4a", label="Suited"),
                Patch(color="#e41a1c", label="Offsuit")
            ]
            ax.legend(handles=legend_handles, title="Hand Type", loc="lower right")

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

    print(f"✅ Styled PDF saved to {pdf_path}")


# --- Run Everything ---
if __name__ == "__main__":
    print("🔥 Running simulations in parallel...")
    combos = starting_hands()
    with Pool(cpu_count()) as pool:
        results = pool.map(simulate_hand_combo, combos)

    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    plot_ranked_hands_bpc(sorted_results)
