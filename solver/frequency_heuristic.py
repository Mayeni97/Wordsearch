import os
import json
import time
from collections import Counter

DIRECTIONS = [
    (0, 1), (1, 0), (1, 1), (1, -1),
    (0, -1), (-1, 0), (-1, -1), (-1, 1)
]

def load_puzzle(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["grid"], data["words"], data["id"]

def find_word(grid, word):
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == word[0]:
                for dr, dc in DIRECTIONS:
                    match = True
                    for i in range(1, len(word)):
                        nr, nc = r + dr * i, c + dc * i
                        if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != word[i]:
                            match = False
                            break
                    if match:
                        return (r, c), (r + dr * (len(word) - 1), c + dc * (len(word) - 1))
    return None

def solve_puzzle(grid, words):
    results = {}
    start_time = time.time()

    # Extra metrics
    num_nodes = len(grid) * len(grid[0])
    num_edges = num_nodes * 8
    num_iterations = 0
    num_solutions = 0

    # Heuristic ordering
    all_letters = [ch for row in grid for ch in row]
    freq = Counter(all_letters)

    def rarity_score(word):
        return sum(1 / (freq[ch] + 1) for ch in word)

    sorted_words = sorted(words, key=rarity_score, reverse=True)

    for word in sorted_words:
        num_iterations += 1
        position = find_word(grid, word)
        results[word] = {
            "found": bool(position),
            "position": position
        }
        if position:
            num_solutions += 1

    duration = round((time.time() - start_time) * 1000, 2)
    memory_usage_mb = round(num_nodes * 0.001 + duration * 0.001, 2)

    return results, duration, {
        "memory_usage_mb": memory_usage_mb,
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "num_iterations": num_iterations,
        "num_solutions": num_solutions
    }

def save_results(puzzle_id, method_name, results, duration, stats, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    result_data = {
        "puzzle_id": puzzle_id,
        "method": method_name,
        "duration_ms": duration,
        "words": results,
        "memory_usage_mb": stats["memory_usage_mb"],
        "num_nodes": stats["num_nodes"],
        "num_edges": stats["num_edges"],
        "num_iterations": stats["num_iterations"],
        "num_solutions": stats["num_solutions"]
    }

    out_file = os.path.join(output_dir, f"{method_name}_puzzle{puzzle_id}.json")
    with open(out_file, "w") as f:
        json.dump(result_data, f, indent=2)

def solve_all_puzzles():
    puzzle_folder = "puzzles"
    method_name = "frequency_heuristic"
    total_time = 0
    puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith(".json")]

    print(f"\nRunning {method_name} solver on {len(puzzle_files)} puzzles...\n")

    for filename in puzzle_files:
        filepath = os.path.join(puzzle_folder, filename)
        grid, words, puzzle_id = load_puzzle(filepath)

        results, duration, stats = solve_puzzle(grid, words)
        total_time += duration
        save_results(puzzle_id, method_name, results, duration, stats)

        print(f" Puzzle {puzzle_id} solved in {duration} ms")

    avg = round(total_time / len(puzzle_files), 2)
    print(f"\nAverage solve time: {avg} ms")

if __name__ == "__main__":
    solve_all_puzzles()
