# CSC 370 - Machine Reasoning
## Homework 2
An implementation of symbolic regression using genetic programming (GP). 

Specifically, we will use symbolic regression to determine the mystery functions $f$ applied to each point in the datasets provided (`dataset1.csv`, `dataset2.csv`, `dataset3.csv`).

Contributors: Tommy Pham and Justin Caudle

## Files and Functions

### Read_Data.py

Reads the CSV files and separates the inputs and target outputs into lists.

- read_data(file_name): Returns the lists (X, X1, X2, X3, Y). Input lists that do not apply to a dataset remain empty.

### tree.py

Defines expression trees and the operations used to evaluate and evolve them. 

- Class TreeNode: Represents an operator, variable, or constant. Contains `is_leaf`
- Class Tree: Stores an expression tree and its configuration. Contains `Mutate`, `collect_nodes`, `crossover`, `predict`, `fitness`, `inorder`, `compute_tree`, `to_sympy`, `tree_depth`, `tree_size`, `has_variable`, ` random_tree`, `random_node`, `random_constant`. 
- 


 

### Supplementary Files 
- `dataset1.csv` - 25,000 data points, one point per line, each line has an $x$ value and a corresponding mystery $f(x)$ value. Determine $f$ using symbolic regression. <br>
$f$ *can be expressed by composing* $+, -, ×, ÷$*, and **integer** constants.* 
<br><br>
- `dataset2.csv` - 25,000 data points, one point per line, first three columns contain the measured values of variables $x_1$, $x_2$, $x_3$ and the last column is the measured value of $y=f(x_1,x_2,x_3)$. Determine $f$ using symbolic regression. <br>
$f$ *can be expressed by composing* $+, -, ×, ÷$*, and **real-valued** constants.* 
<br><br>
- `dataset3.csv` - similar to `dataset1.csv`. Determine $f$ using symbolic regression.<br>
$f$ *can be expressed by composing* $+, -, ×, ÷$, ***integer** constants, and be a combination of analytic functions such as* $e^x, \sin(x), \log(x)$*, etc.*

### Our Files

## How to collect data... ?
