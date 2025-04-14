import os
import json
import time

DIRECTIONS = [
    (0, 1), (1, 0), (1, 1), (1, -1),
    (0, -1), (-1, 0), (-1, -1), (-1, 1)
]

# Load a single puzzle JSON
def load_puzzle(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["grid"], data["words"], data["id"]

# Find a word in the grid
# This function checks for the word in all 8 possible directions
def find_word(grid, word):
    rows = len(grid)
    cols = len(grid[0])
    reversed_word = word[::-1]

    # Row-wise
    for r in range(rows):
        row_string = ''.join(grid[r])
        for target, reverse in [(word, False), (reversed_word, True)]:
            index = row_string.find(target)
            if index != -1:
                start = (r, index)
                end = (r, index + len(word) - 1)
                if reverse:
                    end, start = start, end
                return start, end

    # Column-wise
    for c in range(cols):
        col_string = ''.join(grid[r][c] for r in range(rows))
        for target, reverse in [(word, False), (reversed_word, True)]:
            index = col_string.find(target)
            if index != -1:
                start = (index, c)
                end = (index + len(word) - 1, c)
                if reverse:
                    end, start = start, end
                return start, end

    return None

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

# Solve one puzzle and return results
def solve_puzzle(grid, words):
    results = {}
    start_time = time.time()

    for word in words:
        position = find_word(grid, word)
        results[word] = {
            "found": bool(position),
            "position": position
        }

    duration = round((time.time() - start_time) * 1000, 2)
    return results, duration

# Save results for graphing/analysis later
def save_results(puzzle_id, method_name, results, duration, output_dir="results"):
    os.makedirs(output_dir, exist_ok=True)
    result_data = {
        "puzzle_id": puzzle_id,
        "method": method_name,
        "duration_ms": duration,
        "words": results
    }

    out_file = os.path.join(output_dir, f"{method_name}_puzzle{puzzle_id}.json")
    with open(out_file, "w") as f:
        json.dump(result_data, f, indent=2)

# Solve all JSON puzzles in /puzzles folder
def solve_all_puzzles():
    puzzle_folder = "puzzles"
    method_name = "pattern_match"
    total_time = 0
    puzzle_files = [f for f in os.listdir(puzzle_folder) if f.endswith(".json")]

    print(f"\n Running {method_name} solver on {len(puzzle_files)} puzzles...\n")

    for filename in puzzle_files:
        filepath = os.path.join(puzzle_folder, filename)
        grid, words, puzzle_id = load_puzzle(filepath)

        results, duration = solve_puzzle(grid, words)
        total_time += duration
        save_results(puzzle_id, method_name, results, duration)

        print(f" Puzzle {puzzle_id} solved in {duration} ms")

    avg = round(total_time / len(puzzle_files), 2)
    print(f"\n Average solve time: {avg} ms")

if __name__ == "__main__":
    solve_all_puzzles()
