# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Went through the unitlist. For each item in the unitlist, created a reverse dictionary, counted each instance of unique contents.
	If there is a naked twin pair, there should be two counts of the same unique contents, and the length of either contents should be two.
	Then set all other boxes in the row, column, square or main diagonal (which is the item in "unitlist"), to not contain contents of the naked twin pair

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Manually created 2 more items for the diagonals, and added them to unitlist.
	So unitlist is now 29 for diagonal sudoku.
	Then just reused lesson's code as it mostly was. Program will now have unit dictionary, and peers dictionary, which accounts for these diagonals.
	The other functions will still work, as structure will remain the same.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.