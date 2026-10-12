"""Executes genetic programming to discover an expression that best fits a given dataset
"""
import random
from tree import Tree
from read_data import read_data

# set constants (population size and # of generations)
POP_SIZE = 100
GEN = 50

def sr(file_name):
    # 0) load data/populate relevant lists
    x, x1, x2, x3, y = read_data(file_name)
    
    # 1) build initial population of random trees & add set to prevent recurring trees
    population = []
    seen = set()
    
    while len(population) < POP_SIZE:
        # generate trees and add to set
        pass # placeholder
    
    # 2) iterate through each generation 
    for g in range(GEN):
        # apply fitness function to each tree and obtain score
        # keep best trees (arbitrary, could be 20 best trees)
        # generate new trees using mutate()/crossover() until POP_SIZE is full
        pass # placeholder
    
    # 3) output best tree (expression) --> use inorder() to get expression in str form

if __name__ == '__main__':
    sr('data/dataset1.csv')