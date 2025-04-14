import os
import shutil

def clear_folder(folder, exclude=[]):
    if not os.path.exists(folder):
        return

    for filename in os.listdir(folder):
        if filename in exclude:
            continue

        path = os.path.join(folder, filename)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Could not delete {path}: {e}")

def main():
    print("Resetting workspace...")

    clear_folder("results", exclude=["summary.json", "summary.csv"])
    clear_folder("puzzles")
    clear_folder("graphs")
    clear_folder("generator", exclude=["Words.txt", "generate_puzzle.py"])

    print("Reset complete.")

if __name__ == "__main__":
    main()
