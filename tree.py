"""Implementation of the Tree class

Contains functions to represent and manipulate individuals/trees in our population
"""
import copy # tree cloning
import random # for random selections
import operator 

# Operators 
OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

# Variables 
VARIABLES = ['x', 'x1', 'x2', 'x3']

# Definition for a tree node
class TreeNode:
    def __init__(self, value, left=None, right=None):
        """Initializes initial tree node

        Args:
            value (int/float/str): an operator (e.g., '+'), variable (e.g., 'x'), or constant 
            left (TreeNode, optional): left child, None if leaf
            right (TreeNode, optional): right child, None if leaf
        """
        self.value = value
        self.left = left
        self.right = right
    
    def is_leaf(self):
        """Determines if a tree node is a leaf (no children)

        Returns:
            bool: True if leaf, False otherwise
        """
        return self.left is None and self.right is None

# Expression tree class
class Tree:    
    def __init__(self, root, variables=('x',), int_constants=True, 
                 const_range=(-10, 10), max_depth=10):
        """Initialize initial tree state

        Args:
            root (TreeNode): root node of the expression tree
            variables (tuple): variables included, ('x',) or ('x1', 'x2', 'x3') --> why tuple?
            int_constants (bool): True for integer constants, False for real-valued constants
            const_range (tuple): (low, high) range for random constants --> arbitrary?
            max_depth (int): trees with depth beyond this are discarded (limits bloat) --> why/how limit bloat?
        """
        self.root = root
        self.variables = tuple(variables)
        self.int_constants = int_constants
        self.const_range = const_range
        self.max_depth = max_depth
    
    # Genetic operations
    def mutate(self):
        """Modifies an operation in the tree?
        """
        # 0) Create a copy of the old tree to get a new tree --> need copy method
        clone = copy.deepcopy(self) # deepcopy because we want the trees to be independent (as they're separate individuals in the population)
    
        # 1) Collect the nodes in the copy into a list --> need recursive helper to populate list
        nodes = []
        clone.collect_nodes(clone.root, nodes)
        
        # 2) Randomly select one node --> use random.choice() as we have a list of nodes
        target = random.choice(nodes)
        
        # 3) Use 'is_leaf' function to determine node's category (leaf or operator)
        old = target.value
        
        # 4a) If leaf, randomly select constant or a variable from a range --> use random.randint() (ints) or random.uniform() (reals) for constants, and random.choice() for variables 
        if target.is_leaf(): 
            # leaf node (random select constant or variable, excluding old value)
            low, high = clone.const_range # obtain min & max constant values from tree
            new = old
            
            # repeat until we get a new value
            while new == old:
                # case 1: replace with variable (e.g., 'x') if probability < 0.5
                if random.random() < 0.5:
                    new = random.choice(clone.variables) # break if only have 'x'
                # case 2 & 3: replace with value (constant = int/real) otherwise
                elif clone.int_constants:
                    new = random.randint(low, high)
                else: 
                    new = random.uniform(low, high)
                    
            # instead of repeatedly trying to create a unique tree, just compare to set at the end and quit (think)
            
            # replace
            target.value = new
            
        # 4b) If operator, randomly select operator --> use random.choice() for operators
        else: 
            # terminal node (random select operator, excluding old operator)
            choices = [op for op in OPERATORS if op != old]
            
            # replace 
            target.value = random.choice(choices)
        
        # 5) Apply the changes to the new tree and return
        return clone
        
    
    def collect_nodes(self, root, nodes):
        """Pre-order traversal to collect nodes for random node selection

        Args:
            root (TreeNode): root node of expression tree
            nodes (List): list to store all nodes in the expression tree
        """
        # OOB: just return
        if root is None:
            return 
        # otherwise, collect node and recursive traverse left & right
        nodes.append(root)
        self.collect_nodes(root.left, nodes)
        self.collect_nodes(root.right, nodes)
    
    def crossover(self):
        """Joins a part of one tree with the other part of another tree?
        """
        
    # Fitness function and relevant helpers
    def fitness(self, root, x_list, y_list, population, seen, x1_list=None, x2_list=None, x3_list=None): # mine
        """Determines if a randomly generated function is 'acceptable' for a given dataset
        
        1) Calculate y' = f(x) for each data point in the dataset
        2) Calculate yΔ (difference between y' and y in data set, then squared) for each point
        3) Calculate mean squared error via Σ(yΔ)/# of data points
        4) Keep/Discard function/expression tree based on whether its MSE falls within the acceptable range
        
        Args:
            root (TreeNode): root node of expression tree
            x_list (List): contains all x-values in dataset
            y_list (List): contains all y-values in dataset
            population (Array List): contains current population 
            seen (Set): contains all encountered specimen in the population
            

        Returns:
            bool: True if acceptable. False otherwise
        """
        mse = 0
        
        # 0) Iterate through each x and y value in the dataset
        for index in range(len(x_list)):
            # 1) Traverse the tree, substitute variables with 'x' values, and evaluate y'
            y_prime = self.compute_tree(root, x_list[index])
            
            # 2) Compute yΔ
            y_delta  = (y_list[index] - y_prime) ** 2
            
            # 3) Add to total MSE
            mse += y_delta
        
        # divide by total # of points to get real MSE
        mse /= len(x_list)
        
        # 4) Determine if our mse value falls within the acceptable range (off by 10 is max? arbitrary)
        if mse <= 10: 
            # if acceptable, check set (if DNE yet, add to population list and set)
            if root not in seen:
                population.append(self)
                seen.add(root)
                return True
            # otherwise, already in set, don't add to population (already exists)
        
        # return False if not acceptable MSE or already exists
        return False
    
    # Traversal functions
    def inorder(self):
        """In-order traversal for string expression representation
        """
        if self.value is None:
            return 
        
    def compute_tree(self, root, x=None, x1=None, x2=None, x3=None): # mine
        """Post-order traversal for expression tree computation

        Args:
            root (TreeNode): root node of expression tree
            x (float, optional): variable (dataset 1). Defaults to None.
            x1 (float, optional): variable (dataset 2). Defaults to None.
            x2 (float, optional): variable (dataset 2). Defaults to None.
            x3 (float, optional): variable (dataset 2). Defaults to None.
        """
        # base case 1: beyond leaf node
        if root is None:
            return 
        
        # base case 2: leaf node (constant or variable)
        if root.is_leaf():
            var = root.value
            # if variable, substitute & return 
            sub = {'x': x, 'x1': x1, 'x2': x2, 'x3': x3}
            if var in sub:
                return sub[var]            
            # otherwise, if constant, just return
            return var
            
        # left subtree 
        left = self.compute_tree(root.left, x=x, x1=x1, x2=x2, x3=x3)
        
        # right subtree
        right = self.compute_tree(root.right, x=x, x1=x1, x2=x2, x3=x3)
        
        # compute left & right subtrees using root operator
        op = root.value
        
        # prevent undefined 
        if op == '/' and right == 0:
            return 1
        
        return OPERATORS[op](left, right)
                
        
# you have x, y, y_tree

# .eval --> turns string expression into an expression tree (roundabout way of doing things)

# STEPS
# 1) generate random tree 
# 2) add to set 
# 3) substitute variables with values and evaluate using post-order traversal (compute left then right subtree)
# 4) record y_tree value and compare with fitness function to determine keep or discard
# Final) turn into a string using in-order traversal to present the final expression