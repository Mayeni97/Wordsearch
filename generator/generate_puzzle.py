import os
import json
import random
import string

# Directions to place words (8 total)
DIRECTIONS = [
    (0, 1),    # right
    (1, 0),    # down
    (1, 1),    # diagonal down-right
    (1, -1),   # diagonal down-left
    (0, -1),   # left
    (-1, 0),   # up
    (-1, -1),  # diagonal up-left
    (-1, 1)    # diagonal up-right
]

# Load real words from file within length limits
def load_word_list(min_len=3, max_len=6):
    filepath = os.path.join(os.path.dirname(__file__), "Words.txt")
    with open(filepath, "r") as f:
        words = [w.strip().upper() for w in f.readlines()]
    return [w for w in words if min_len <= len(w) <= max_len and w.isalpha()]

# Create an empty grid
def generate_empty_grid(size):
    return [["" for _ in range(size)] for _ in range(size)]

# Try placing a word in the grid
def place_word_in_grid(grid, word):
    size = len(grid)
    attempts = 0

    while attempts < 100:
        attempts += 1
        dir_r, dir_c = random.choice(DIRECTIONS)
        start_r = random.randint(0, size - 1)
        start_c = random.randint(0, size - 1)

        end_r = start_r + dir_r * (len(word) - 1)
        end_c = start_c + dir_c * (len(word) - 1)

        if not (0 <= end_r < size and 0 <= end_c < size):
            continue  # Word goes out of bounds

        fits = True
        for i in range(len(word)):
            r = start_r + dir_r * i
            c = start_c + dir_c * i
            if grid[r][c] not in ("", word[i]):
                fits = False
                break

        if fits:
            for i in range(len(word)):
                r = start_r + dir_r * i
                c = start_c + dir_c * i
                grid[r][c] = word[i]
            return True

    return False

# Fill unused grid spaces with random letters
def fill_empty_spaces(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "":
                grid[r][c] = random.choice(string.ascii_uppercase)

# Generate a full puzzle
def generate_puzzle(id, grid_size, word_count, min_len, max_len):
    grid = generate_empty_grid(grid_size)
    word_bank = load_word_list(min_len, max_len)
    random.shuffle(word_bank)

    words = []
    for word in word_bank:
        if len(words) == word_count:
            break
        placed = place_word_in_grid(grid, word)
        if placed:
            words.append(word)

    fill_empty_spaces(grid)

    return {
        "id": id,
        "grid": grid,
        "words": words
    }

# Save puzzle to file
def save_puzzle(puzzle, folder="puzzles"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/puzzle{puzzle['id']}.json"
    with open(filename, "w") as f:
        json.dump(puzzle, f, indent=2)

# Optional: show the puzzle in terminal
def print_grid(grid):
    for row in grid:
        print(" ".join(row))

# Main execution
def main():
    print("Word Search Generator")

    grid_size = int(input("Grid size (10 for 10x10): "))
    num_puzzles = int(input("How many puzzles to generate? "))
    words_per_puzzle = int(input("How many words per puzzle? "))
    min_len = int(input("Minimum word length? "))
    max_len = int(input("Maximum word length? "))

    for i in range(1, num_puzzles + 1):
        puzzle = generate_puzzle(
            id=i,
            grid_size=grid_size,
            word_count=words_per_puzzle,
            min_len=min_len,
            max_len=max_len
        )
        save_puzzle(puzzle)
        print(f"\n✅ Puzzle {i} saved with {len(puzzle['words'])} words.")
        print("🧩 Grid Preview:")
        print_grid(puzzle["grid"])
        print(f"🔍 Words: {', '.join(puzzle['words'])}\n")

if __name__ == "__main__":
    main()
