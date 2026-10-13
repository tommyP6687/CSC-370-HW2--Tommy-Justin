"""Executes genetic programming to discover an expression that best fits a given dataset
"""
import random
import sympy # for evaluating expression string
from tree import Tree
from read_data import read_data

# set constants (population size, # of generations, # of survivors at each generation, and mutation/crossover rates)
POP_SIZE = 100
GEN = 50
SURVIVORS = 20 
MUTATION_RATE = 0.4

def sr(file_name):
    # 0) load data/populate relevant lists
    x, x1, x2, x3, y = read_data(file_name)
    
    # 1) build initial population of random trees & add set to prevent recurring trees
    population = []
    seen = set()
    
    while len(population) < POP_SIZE:
        # generate trees and add to set
        tree = Tree.random_tree(max_depth=4)
        expression = tree.inorder()
        
        if expression not in seen:
            seen.add(expression)
            population.append(tree)
    
    # 2) iterate through each generation 
    for g in range(GEN):
        # rank each tree by fitness score (sorted by lowest MSE trees first)
        population.sort(key=lambda t: t.fitness(x, y))
        
        # keep best trees (arbitrary, could be 20 best trees)
        survivors = population[:SURVIVORS]
        population = list(survivors)
        
        # generate children using survivors until full
        while len(population) < POP_SIZE:
            rand = random.random()
            
            # mutation
            if rand < MUTATION_RATE:
                children = [random.choice(survivors).mutate()]
            
            # crossover
            else:                
                parent1, parent2 = random.sample(survivors, 2)
                children = parent1.crossover(parent2)
        
            for child in children:
                # discard bloated trees and duplicates
                if child.tree_depth(child.root) > child.max_depth:
                    continue
                expression = child.inorder()
                if expression not in seen and len(population) < POP_SIZE:
                    seen.add(expression)
                    population.append(child)
            
    # 3) output best tree expression (str form)
    population.sort(key=lambda t: t.fitness(x, y))
    best = population[0]
    best_inorder = best.inorder()
    
    # get more readable form of best expression 
    simple = sympy.expand(sympy.sympify(best_inorder))
    
    print(f"Best expression (inorder): {best_inorder}")
    print(f"Best expression (inorder + simplified): {simple}")
    print(f"MSE: {best.fitness(x, y):.6f}") # round value to six decimal places
    return best

if __name__ == '__main__':
    sr('data/dataset1.csv')