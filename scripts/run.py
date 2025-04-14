import subprocess
import sys


def run(script):
    try:
        subprocess.run([sys.executable, script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e}")
        exit(1)

def main():
    if input("Reset workspace? (y/n): ").lower() == "y":
        run("scripts/reset.py")

    run("generator/generate_puzzle.py")

    run("solver/brute_force.py")
    run("solver/frequency_heuristic.py")
    run("solver/diagonal_bias.py")
    run("solver/pattern_match.py")
    run("solver/custom.py")

    run("scripts/summarizer.py")
    run("scripts/visualizer.py")

    print("Done.")

if __name__ == "__main__":
    main()
