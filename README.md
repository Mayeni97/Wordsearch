# 🧠 AI Word Search

## Reason
I was at work with nothing to do [^1], when I found an old word-search puzzle book. Only two pages were completed — by the end of my shift, I had finished 46. [^2] That got me thinking...

[^1]: I finished all my work for the day  
[^2]: It's been a while since I last did a word search  
[^3]: My approach involved letter searching, then expanding the grid 3x3 from the point of origin (first letter)  
[^4]: You choose the amount

## Thoughts
While flying through the puzzles, I started to notice some patterns:
1. How quickly I was solving them
2. The specific method I was using to find words [^3]
3. Are there other methods to search for words?
4. Could an AI replicate or test these methods — and show which one is most efficient?

## Idea
- Generate **n** x **n** grid
- Generate **n** word search puzzles with **n** words each [^4]
- Use different solving strategies to solve each puzzle
- Track performance metrics like time and search steps
- Visualize and compare the results to evaluate method efficiency

## Goals
- [ ] Word search puzzle generator  
- [ ] Implement multiple solving methods  
- [ ] Track performance for each method  
- [ ] Display results (graph)

## Solving Methods
I went online and found several strategies. I'm going to implement and test them within this project.

| Strategy Name       | Description |
|---------------------|-------------|
| **Brute Force**      | Check every cell and direction for possible matches |
| **Frequency Heuristic** | Prioritize words with uncommon starting letters |
| **Pattern Match**    | Scan rows/columns for regex-like word shapes |
| **Diagonal Bias**    | Focus only on diagonal matches (as a performance comparison) |
| **My Method**        | Start from identified letters and expand a 3x3 grid outward [^3] |


## Phase
### Step 1 – Build Puzzle Generator
- [ ] Generate a grid of size **n** x **n**
- [ ] Populate the grid with random letters
- [ ] Insert words from a word list into the grid
- [ ] Ensure words can be placed horizontally, vertically, and diagonally
- [ ] Handle edge cases like overlapping words
### Step 2 – Build Algorithm (Methods) Solver
- [ ] Brute Force Complete
- [ ] Diagonal_bias
- [ ] Frequency_heuristic
- [ ] Pattern_Match
- [ ] Custom
### Step 3 – Build Result Data Report
- [ ] Track performance metrics for each solving method:
  - Time taken to solve
  - Number of search steps
  - Accuracy
- [ ] Generate a comparison graph to visualize results
- [ ] Export results to a CSV file

## Result
After solving, you should get :
-  **Bar charts**: duration, accuracy, and solution counts
-  **Radar chart**: compares all metrics per method
-  **Heatmap**: accuracy per puzzle across all methods
-  **Line plot**: duration per puzzle ID, by method

    > Saved in '/graphs'

## Future 
- Add a user interface for generating and solving puzzles
- Allow users to input custom word lists
- Implement additional solving strategies
- Optimize algorithms for larger grids

### How to run
1. Clone the repo
2. python scripts/run.py 