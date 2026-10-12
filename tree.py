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
    
    def crossover(self, other):
        """swaps a part of one tree with the other part of another tree?
        """
        #copy both trees
        clone1 = copy.deepcopy(self)
        clone2 = copy.deepcopy(other)

        # collect nodes 
        nodes1 = []
        nodes2 = []

        clone1.collect_nodes(clone1.root, nodes1)
        clone2.collect_nodes(clone2.root, nodes2)

        #random select a node from each tree
        target1 = random.choice(nodes1)
        target2 = random.choice(nodes2)

        #swap the nodes selected values and their children
        target1.value, target2.value = target2.value, target1.value
        target1.left, target2.left = target2.left, target1.left
        target1.right, target2.right = target2.right, target1.right

        #new trees are returned
        return clone1, clone2 


        
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
    def inorder(self, root=None):
        """In-order traversal for string expression representation
        """

        if root is None:
            root = self.root

        #Base case- leaf node
        if root.is_leaf():
            return str(root.value)

        # traverse the left subtree
        left = self.inorder(root.left)

        #traverse the right subtree
        right = self.inorder(root.right)

        # combine left, root, and right
        return f"({left} {root.value} {right})"
        
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
    
    @classmethod
    def random_tree(cls, max_depth=5, variables=('x',), int_constants=True, const_range=(-10, 10)):
        """Generate random expression tree
        """
        root = cls.random_node(max_depth, variables, int_constants, const_range)
        return cls(root, variables, int_constants, const_range)
    
    @staticmethod
    def random_node(depth, variables, int_constants, const_range):
        """Recursively build a random substree of at most 'depth' levels
        """
        low, high = const_range
        # base case: depth == 0 or probability < 0.2
        if depth == 0 or random.random() < 0.2:
            # random leaf (random variable or constant)
            leaf = None
            # case 1: variable (e.g., 'x') if probability < 0.5
            if random.random() < 0.5:
                leaf = random.choice(variables) # break if only have 'x'
            # case 2 & 3: value (constant = int/real) otherwise
            elif int_constants:
                leaf = random.randint(low, high)
            else: 
                leaf = random.uniform(low, high)
            
            return TreeNode(leaf)
            
        # recursive case: depth > 0
        
        # terminal node (random select operator, excluding old operator)
        choices = [op for op in OPERATORS]
        
        # choose
        op = random.choice(choices)
        
        # recursively traverse with two child nodes
        left = Tree.random_node(depth-1, variables, int_constants, const_range)
        right = Tree.random_node(depth-1, variables, int_constants, const_range)
        
        return TreeNode(op, left, right)

# you have x, y, y_tree

# .eval --> turns string expression into an expression tree (roundabout way of doing things)

# STEPS
# 1) generate random tree 
# 2) add to set 
# 3) substitute variables with values and evaluate using post-order traversal (compute left then right subtree)
# 4) record y_tree value and compare with fitness function to determine keep or discard
# Final) turn into a string using in-order traversal to present the final expression