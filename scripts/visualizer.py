import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def load_summary(filepath="results/summary.csv"):
    if not os.path.exists(filepath):
        print("Summary file not found.")
        return None
    return pd.read_csv(filepath)

def highlight_best_worst(df, metric):
    grouped = df.groupby("method")[metric].mean().reset_index()
    best = grouped.loc[grouped[metric].idxmin() if "duration" in metric else grouped[metric].idxmax()]
    worst = grouped.loc[grouped[metric].idxmax() if "duration" in metric else grouped[metric].idxmin()]
    return grouped, best, worst

def plot_bar(grouped, best, worst, metric, ylabel, title, filename):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(grouped["method"], grouped[metric], color="lightgray")
    for bar, method in zip(bars, grouped["method"]):
        if method == best["method"]:
            bar.set_color("green")
        elif method == worst["method"]:
            bar.set_color("red")
    plt.xlabel("Method")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"graphs/{filename}")
    plt.close()
    print(f"Saved graph: graphs/{filename}")

def normalize(df, cols, invert=[]):
    norm_df = df.copy()
    for col in cols:
        col_min = df[col].min()
        col_max = df[col].max()
        norm_df[col] = (df[col] - col_min) / (col_max - col_min + 1e-6)
        if col in invert:
            norm_df[col] = 1 - norm_df[col]
    return norm_df

def make_radar_chart(df, metrics, title="Solver Comparison Radar", filename="graphs/radar_chart.png"):
    methods = df["method"]
    N = len(metrics)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    for _, row in df.iterrows():
        values = [row[m] for m in metrics]
        values += values[:1]
        ax.plot(angles, values, label=row["method"])
        ax.fill(angles, values, alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=10)
    ax.set_yticklabels([])
    ax.set_title(title, size=14, y=1.1)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved radar chart: {filename}")

def plot_heatmap(df, value_col="accuracy_percent", filename="graphs/accuracy_heatmap.png"):
    pivot = df.pivot(index="method", columns="puzzle_id", values=value_col)
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, annot=True, cmap="YlGnBu", fmt=".1f", cbar_kws={'label': 'Accuracy (%)'})
    plt.title("Accuracy per Puzzle by Method")
    plt.xlabel("Puzzle ID")
    plt.ylabel("Method")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved heatmap: {filename}")

def plot_line_per_puzzle(df, value_col="duration_ms", filename="graphs/duration_by_puzzle.png"):
    plt.figure(figsize=(12, 6))

    methods = df["method"].unique()
    puzzle_ids = sorted(df["puzzle_id"].unique())

    for method in methods:
        method_df = df[df["method"] == method].sort_values("puzzle_id")

        # ✅ Reduce clutter: only plot every other puzzle if there are many
        if len(puzzle_ids) > 20:
            method_df = method_df[method_df["puzzle_id"] % 2 == 0]

        plt.plot(
            method_df["puzzle_id"],
            method_df[value_col],
            label=method,
            linestyle="--",
            linewidth=1.2,
            marker="o",
            markersize=4
        )

    plt.xlabel("Puzzle ID")
    plt.ylabel("Solve Time (ms)")
    plt.title("Solve Time per Puzzle by Method")
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved simplified line plot: {filename}")

    plt.figure(figsize=(12, 6))
    for method in df["method"].unique():
        method_df = df[df["method"] == method]
        plt.plot(method_df["puzzle_id"], method_df[value_col], label=method, marker="o")
    plt.xlabel("Puzzle ID")
    plt.ylabel("Solve Time (ms)")
    plt.title("Solve Time per Puzzle by Method")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Saved line plot: {filename}")

def main():
    df = load_summary()
    if df is None:
        return

    # Bar charts
    time_grouped, best_time, worst_time = highlight_best_worst(df, "duration_ms")
    plot_bar(time_grouped, best_time, worst_time, "duration_ms", "Average Solve Time (ms)", "Average Solve Time by Method", "avg_solve_time.png")

    acc_grouped, best_acc, worst_acc = highlight_best_worst(df, "accuracy_percent")
    plot_bar(acc_grouped, best_acc, worst_acc, "accuracy_percent", "Average Accuracy (%)", "Average Accuracy by Method", "avg_accuracy.png")

    for metric in ["num_edges", "num_solutions"]:
        if metric in df.columns:
            g, b, w = highlight_best_worst(df, metric)
            plot_bar(g, b, w, metric, metric.replace("_", " ").title(), f"Average {metric.replace('_', ' ').title()} by Method", f"avg_{metric}.png")

    # Radar chart
    radar_metrics = ["duration_ms", "accuracy_percent", "num_solutions"]
    if all(m in df.columns for m in radar_metrics):
        grouped = df.groupby("method")[radar_metrics].mean().reset_index()
        normalized = normalize(grouped, radar_metrics, invert=["duration_ms"])
        make_radar_chart(normalized, radar_metrics)

    # Puzzle-by-puzzle
    if "puzzle_id" in df.columns and "accuracy_percent" in df.columns:
        plot_heatmap(df)
    if "puzzle_id" in df.columns and "duration_ms" in df.columns:
        plot_line_per_puzzle(df)

if __name__ == "__main__":
    main()
