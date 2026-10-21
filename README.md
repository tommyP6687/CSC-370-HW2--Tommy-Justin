# CSC 370 - Machine Reasoning
## Homework 2
An implementation of symbolic regression using genetic programming (GP). 

Specifically, we will use symbolic regression to determine the mystery functions $f$ applied to each point in the datasets provided (`dataset1.csv`, `dataset2.csv`, `dataset3.csv`).

Contributors: Tommy Pham and Justin Caudle

## Files and Functions

### Read_Data.py

Reads the CSV files and separates the inputs and target outputs into lists.

- read_data(file_name): Returns the lists (x, x1, x2, x3, y). Input lists that do not apply to a dataset remain empty.

### tree.py

Defines expression trees and the operations used to evaluate and evolve them. 

- TreeNode Class: Represents an operator, variable, or constant. Contains `is_leaf`
- Tree Class: Stores an expression tree and its configuration. Contains `Mutate`, `collect_nodes`, `crossover`, `predict`, `fitness`, `inorder`, `compute_tree`, `to_sympy`, `tree_depth`, `tree_size`, `has_variable`, ` random_tree`, `random_node`, `random_constant`. 

### symbolic_regression.py

Runs the genetic programming algorithm to discover expressions that fit the datasets.

- `train_test_split()`: Shuffles and divides the data into 80% training and 20% testing sets.
- `sr()`: Loads the data, generates the initial population, evaluates fitness, selects survivors, creates offspring, and evaluates the final model.
- **Main Block:** Runs 10 searches per dataset and summarizes the expressions, test errors, and runtimes.


### test_tree.py

Contains manual checks for tree construction, leaf detection, numerical evaluation, expression printing, and crossover.

### submit.sh

Runs the experiments on a Slurm cluster and records the total execution time.

### output

Contains saved results from previous experiments. Settings may differ between output files.

 

## Supplementary Files

- `data/dataset1.csv`: Contains 25,000 data points. Each row has an input $x$ and its corresponding output $f(x)$. The unknown function uses arithmetic operators and integer constants.
- `data/dataset2.csv`: Contains 25,000 data points. Each row has inputs $x_1$, $x_2$, and $x_3$, and the corresponding output $f(x_1,x_2,x_3)$. The unknown function uses arithmetic operators and real-valued constants.
- `data/dataset3.csv`: An optional extra-credit dataset that may require additional functions such as $e^x$, $\sin(x)$, and $\log(x)$.

## How to Run

Requires Python 3 and SymPy.

Install SymPy:

```bash
python3 -m pip install sympy
```

Run the program from the repository's root directory:

```bash
python3 symbolic_regression.py
```

Run the manual tree checks:

```bash
python3 test_tree.py
```

On a Slurm cluster:

```bash
sbatch submit.sh
```

## How to Save Results

The input data is provided in the CSV files. To run the experiments and save the printed results:

```bash
mkdir -p output
python3 -u symbolic_regression.py > output/experiment.out 2>&1
```

Use a different filename for each experiment to preserve previous results.

The program reports training MSE, test MSE, test relative error, tree size, the discovered expression, scaling coefficients, and runtime.
