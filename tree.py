"""Implementation of the Tree class

Contains functions to represent and manipulate individuals/trees in our population
"""

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
        
        # 1) Collect the nodes in the copy into a list --> need recursive helper to populate list
        
        # 2) Randomly select one node --> use random.choice() as we have a list of nodes
        
        # 3) Use 'is_leaf' function to determine node's category (leaf or operator)
        
        # 4a) If leaf, randomly select constant or a variable from a range --> use random.randint() (ints) or random.uniform() (reals) for constants, and random.choice() for variables 
        # 4b) If operator, randomly select operator --> use random.choice() for operators
        
        # 5) Apply the changes to the new tree and return
    
    def crossover(self):
        """Joins a part of one tree with the other part of another tree?
        """