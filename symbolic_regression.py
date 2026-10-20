"""Executes genetic programming to discover an expression that best fits a given dataset
"""
import random
import sympy # for evaluating expression string
from tree import Tree
from read_data import read_data
import time
import math

# set constants (population size, # of generations, # of survivors at each generation, and mutation/crossover rates)
POP_SIZE = 100
GEN = 50
SURVIVORS = 20 
EXTERNAL = 10 # fresh random trees added every generation (promote diversity)
MUTATION_RATE = 0.1
# linear scaling switch
LINEAR_SCALING = True
# relative error switch
RELATIVE_ERROR = False

# dataset 2: minimum x3 kept (x3 rounded to 2 decimals, so small x3 values have large relative error in 1/x3^2)
X3_MIN = 0.5

# penalty per node for complex expression trees
PEN = 0.001

def train_test_split(x, x1, x2, x3, y, test_frac=0.2, seed=0):
    """Shuffles the dataset rows and splits every list the same way (80% train, 20% test)"""
    index = list(range(len(y)))
    random.Random(seed).shuffle(index)
    cut = int(len(index) * (1 - test_frac))
    
    def pick(lst, ids):
        return [lst[i] for i in ids] if lst else []
    
    train = [pick(lst, index[:cut]) for lst in (x, y, x1, x2, x3)]
    test = [pick(lst, index[cut:]) for lst in (x, y, x1, x2, x3)]
    
    return train, test

def sr(file_name, use_split=True):
    # 0) load data/populate relevant lists
    x, x1, x2, x3, y = read_data(file_name)
    
    # dataset 2 has x1, x2, x3. dataset 1 has x
    variables = ('x1', 'x2', 'x3') if x1 else ('x',)
    
    # only apply linear scaling for dataset 2
    scaling = LINEAR_SCALING and bool(x1)
    
    # relative error only for dataset 2
    relative = RELATIVE_ERROR and bool(x1)
    
    # dataset 2: real-valued constants 
    int_constants = not x1
    const_range = (-10, 10)
    
    # dataset 2: exclude outliers rows where x3 <= X3_MIN (real x3 values lost due to rounding)
    if x1:
        before = len(y)
        keep = [i for i in range(len(y)) if x3[i] > X3_MIN]
        x1 = [x1[i] for i in keep]
        x2 = [x2[i] for i in keep]
        x3 = [x3[i] for i in keep]
        y = [y[i] for i in keep]
        print(f"excluded {before-len(y)} rows with x3 <= {X3_MIN}")
    
    # divide dataset into train (evolve expression) and test (check for overfitting)
    if use_split:
        train, test = train_test_split(x, x1, x2, x3, y)
    else: 
        # not split: evolve on all data (for comparison purposes)
        train = [x, y, x1, x2, x3]
        test = train
    
    # 0.5 (Added)) normalize MSE so result is comparable across datasets
    
    # variance of training y 
    y_train = train[1] # y column 
    w = [1 / max(v * v, 1.0) for v in y_train] if relative else [1.0] * len(y_train)
    mean_y = sum(wi * v for wi, v in zip(w, y_train)) / sum(w)
    var_y = sum(wi * (v - mean_y) ** 2 for wi, v in zip(w, y_train)) / sum(w)
    
    def penalized_fitness(t):
        """Normalizes train MSE and size penalty (lower is better)"""
        if scaling:
            mse = t.fitness(*train, relative=relative) # linear scaling enabled
        else:
            mse = t.fitness(*train, a=0, b=1, relative=relative) # linear scaling disabled
        return mse / var_y + PEN * t.tree_size()
    
    # 1) build initial population of random trees & add set to prevent recurring trees
    population = []
    seen = set()
    
    while len(population) < POP_SIZE:       
        # generate trees and add to set
        tree = Tree.random_tree(max_depth=4, variables=variables, int_constants=int_constants, const_range=const_range)
        expression = tree.inorder()
        
        # require at least 3 nodes in the tree (prevent degradation to a single-node tree, constant only)
        if expression not in seen and tree.has_variable():
            seen.add(expression)
            population.append(tree)
    
    # 2) iterate through each generation 
    for g in range(GEN):
        # rank each tree by fitness score (sorted by lowest MSE trees first)
        population.sort(key=penalized_fitness)
        
        # keep best trees (arbitrary, could be 20 best trees)
        survivors = population[:SURVIVORS]
        population = list(survivors)
        
        # add fresh random trees every generation to retain diversity
        for e in range(EXTERNAL):
            tree = Tree.random_tree(max_depth=4, variables=variables, int_constants=int_constants, const_range=const_range)
            expression = tree.inorder()
            if expression not in seen and tree.has_variable():
                seen.add(expression)
                population.append(tree)
        
        # prevent infinite loop
        attempts = 0
        
        # generate children using survivors until full
        while len(population) < POP_SIZE:
            attempts += 1
            rand = random.random()
                    
            # stuck (survivors only produce duplicates) --> add a fresh random tree
            if attempts > 10 * POP_SIZE:
                children = [Tree.random_tree(max_depth=4, variables=variables, int_constants=int_constants, const_range=const_range)]
            
            # mutation
            elif rand < MUTATION_RATE:
                children = [random.choice(survivors).mutate()]
            
            # crossover
            else:                
                parent1, parent2 = random.sample(survivors, 2)
                children = parent1.crossover(parent2)
        
            for child in children:
                # discard bloated trees and duplicates
                if child.tree_depth(child.root) > child.max_depth:
                    continue
                # skip trees with < 3 nodes (prevent loss of diversity)
                if not child.has_variable():
                    continue                
                expression = child.inorder()
                if expression not in seen and len(population) < POP_SIZE:
                    seen.add(expression)
                    population.append(child)
            
    # 3) output best tree expression (str form)
    population.sort(key=penalized_fitness)
    best = population[0]
    best_inorder = best.inorder()
    
    # train MSE (with scaling)
    if scaling:
        train_mse = best.fitness(*train, relative=relative)
    
    train_mse = best.fitness(*train, a=best.a, b=best.b)
    
    # test MSE reuses trained a, b (a=0, b=1 when scaling disabled)
    test_mse = best.fitness(*test, a=best.a, b=best.b)
    # relative error (mean square % error) ontest
    test_rel = best.fitness(*test, a=best.a, b=best.b, relative=True)
    
    # final formula = a + b * tree (simplified, readable form)
    simple = sympy.expand(best.a + best.b * best.to_sympy())
    
    # print MSE on train and test data
    print(f"Train MSE: {train_mse:.6f}")
    print(f"Test MSE: {test_mse:.6f}")
    print(f"Test relative error (RMS %): {math.sqrt(test_rel) * 100:.3f}%")
    
    # size (# of nodes) of best tree
    print(f"Tree size: {best.tree_size()} nodes")
    
    # best expression: raw tree, linear scaling coefficients, and final simplified formula
    print(f"Best expression (inorder): {best_inorder}")
    print(f"Linear scaling: a = {best.a}, b = {best.b}")
    print(f"Best expression (a + b * tree, simplified): {simple}")
    
    # return best model of this run, its test MSE, and its simplified expression
    return best, test_mse, simple

if __name__ == '__main__':
    RUNS = 10 # test how reliable expressions are (multiple convergences to same expression or does it vary)
    # run both datasets (1 & 2 )
    for file in [
        'data/dataset1.csv',
        'data/dataset2.csv'
        ]:
        durations = []
        results = [] # (test MSE, run #, simplified expression) for each run
    
        for run in range(RUNS):
            scaled = LINEAR_SCALING and 'dataset2' in file
            print(f"\n{file} (80/20 split, linear scaling = {scaled}), run {run + 1}/{RUNS}:")
            
            start = time.time()
            best, test_mse, simple = sr(file, use_split=True)
            duration = time.time() - start
            durations.append(duration)
            results.append((test_mse, run + 1, simple))
            print(f"Run time: {duration:.1f} s")
            
        # select overall best model across runs by test MSE
        best_test_mse, best_run, best_expr = min(results, key=lambda r: r[0])
        
        # per-dataset summary 
        print(f"\n-----{file} summary ({RUNS} runs)-----")
        print(f"Run times (s): {[round(d, 1) for d in durations]}")
        print(f"Average: {sum(durations) / RUNS:.1f} s")
        print(f"Test MSEs: {[round(r[0], 6) for r in results]}")
        print(f"Best model (lowest test MSE): run {best_run}, test MSE = {best_test_mse:.6f}")
        print(f"Best expression: {best_expr}")