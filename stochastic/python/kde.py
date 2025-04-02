from scipy.stats import gaussian_kde

fig, ax = plt.subplots(figsize=(12, 6))
for label, samples in posterior_samples_dict.items():
    samples = np.array(samples).flatten()
    kde = gaussian_kde(samples)
    x = np.linspace(samples.min() * 0.8, samples.max() * 1.2, 200)
    ax.plot(x, kde(x), label=label, linewidth=2)

ax.set_title("Posterior Volatility KDEs (per asset)", fontsize=14)
ax.set_xlabel("Volatility (σ)")
ax.set_ylabel("Density")
ax.legend()
fig.text(0.01, 0.01, "Source: Posterior KDE | Strategy: BuyPolar Capital",
         fontsize=9, style="italic", color="#333333")
fig.tight_layout(rect=[0, 0.02, 1, 0.95])
pdf.savefig(fig)
plt.close(fig)
