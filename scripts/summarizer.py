import os
import json
import csv

def summarize_results(results_folder="results", output_file="results/summary.csv"):
    summary = []

    files = [f for f in os.listdir(results_folder) if f.endswith(".json") and not f.startswith("summary")]
    files.sort()

    for file in files:
        path = os.path.join(results_folder, file)
        with open(path, "r") as f:
            data = json.load(f)

        puzzle_id = data.get("puzzle_id")
        method = data.get("method")
        duration = data.get("duration_ms", 0)
        words = data.get("words", {})

        total_words = len(words)
        found_words = sum(1 for w in words.values() if w["found"])
        accuracy = round((found_words / total_words) * 100, 2) if total_words > 0 else 0

        # NEW: Additional metrics with fallback defaults
        summary.append({
            "puzzle_id": puzzle_id,
            "method": method,
            "duration_ms": duration,
            "words_found": found_words,
            "total_words": total_words,
            "accuracy_percent": accuracy,
            "memory_usage_mb": data.get("memory_usage_mb", 0),
            "num_nodes": data.get("num_nodes", 0),
            "num_edges": data.get("num_edges", 0),
            "num_iterations": data.get("num_iterations", 0),
            "num_solutions": data.get("num_solutions", 0),
        })

    # Save to CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary[0].keys())
        writer.writeheader()
        writer.writerows(summary)

    print(f"Summary saved to: {output_file}")

if __name__ == "__main__":
    summarize_results()
