"""Implementation of the Tree class

Contains functions to represent and manipulate individuals/trees in our population
"""
import copy # tree cloning
import random # for random selections

# Operators 
OPERATORS = ['+', '-', '*', '/']

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
                    new = random.choice(clone.variables)
                # case 2 & 3: replace with value (constant = int/real) otherwise
                elif clone.int_constants:
                    new = random.randint(low, high)
                else: 
                    new = random.uniform(low, high)
            
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
    
    # Traversal functions
    def inorder(self):
        """In-order traversal for string expression representation
        """
        if self.value is None:
            return 
        
                
        
# you have x, y, y_tree

# .eval --> turns string expression into an expression tree (roundabout way of doing things)

# STEPS
# 1) generate random tree 
# 2) add to set 
# 3) substitute variables with values and evaluate using post-order traversal (compute left then right subtree)
# 4) record y_tree value and compare with fitness function to determine keep or discard
# Final) turn into a string using in-order traversal to present the final expression