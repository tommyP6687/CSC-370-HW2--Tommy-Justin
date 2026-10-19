"""Implementation of the Tree class

Contains functions to represent and manipulate individuals/trees in our population
"""
import copy # tree cloning
import random # for random selections
import operator 
import sympy # for simplifying expressions
import math # for checking finite values

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
        self.a = 0 # linear scaling intercept (set by fitness)
        self.b = 1 # linear scaling slope (set by fitness)
    
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
                # case 2: replace with value (constant = int/real) otherwise
                else:
                    new = Tree.random_constant(clone.int_constants, clone.const_range)
                    
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
    
    def predict(self, x_list, y_list, x1_list=None, x2_list=None, x3_list=None):
        """Evaluates the tree on each data row

        Returns:
            List: tree output for each row
        """
        preds = []
        for index in range(len(y_list)):
            if x1_list: # dataset 2
                preds.append(self.compute_tree(self.root, x1=x1_list[index], x2=x2_list[index], x3=x3_list[index]))
            else: # dataset 1
                preds.append(self.compute_tree(self.root, x=x_list[index]))
        return preds
        
    # Fitness function and relevant helpers
    def fitness(self, x_list, y_list, x1_list=None, x2_list=None, x3_list=None, a=None, b=None):
        """Computes scaled MSE value for a given expression tree
        
        1) Calculate y' = f(x) for each data point (row) in the dataset and collect into y_primes (via predict)
        2) Calculate best slope b and intercept a for the tree (linear scaling): b = cov(y', y) / var(y'), a = mean(y) - b * mean(y')
        3) Calculate yΔ (difference between scaled y' (= a + b * y') and y in data set, then squared) for each point
        4) Calculate mean squared error via Σ(yΔ)/# of data points
        
        Args:
            x_list (List): contains all x-values in dataset
            y_list (List): contains all y-values in dataset    
            x1_list, x2_list, x3_list (List, optional): contains all x1, x2, x3 values (dataset 2)
            a (float, optional): intercept to use instead of computing it (e.g., training a on test data)
            b (float, optional): slope to use instead of computing it (e.g., training b on test data)        

        Returns:
            float: scaled MSE value computed
        """
        mse = 0
        
        # 1) Traverse the tree for each data point and evaluate y'
        y_primes = self.predict(x_list, y_list, x1_list, x2_list, x3_list)
        
        # 2) Compute best slope b and intercept a (linear scaling), unless given 
        if a is None or b is None:
            mean_y_prime = sum(y_primes) / len(y_list)
            mean_y = sum(y_list) / len(y_list)
            cov = sum((y_primes[index] - mean_y_prime) * (y_list[index] - mean_y) for index in range(len(y_list)))
            var = sum((y_primes[index] - mean_y_prime) ** 2 for index in range(len(y_list)))
            # constant tree (no variance) -> b = 0, a = mean(y)
            b = cov / var if var != 0 else 0
            a = mean_y - b * mean_y_prime
            # store on tree (for final formula & test MSE)
            self.a, self.b = a, b
        
        # 3) Iterate through each y' and y value in the dataset 
        for index in range(len(y_list)):
            # compute yΔ using scaled y'
            diff = y_list[index] - (a + b * y_primes[index])
            y_delta = diff * diff
            
            # add to total MSE 
            mse += y_delta
        
        # 4) Divide by total # of points to get real MSE
        mse /= len(y_list)
        
        # 5) trees with inf/nan outputs get worst score (nan breaks sorting)
        if not math.isfinite(mse):
            return float('inf')
        
        # return MSE value
        return mse
    
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
    
    def to_sympy(self, root=None):
        """Converts expression tree to a sympy expression (uses same protected division as compute_tree)
        
        Args:
            root (TreeNode, optional): starting node. Defaults to the tree's root.
        
        Returns:
            sympy expression of the tree
        """
        if root is None:
            root = self.root
        
        # base case: leaf node (variable = symbol, constant = number)
        if root.is_leaf():
            if isinstance(root.value, str):
                return sympy.Symbol(root.value)
            return sympy.sympify(root.value)
        
        # post-order traversal
        left = self.to_sympy(root.left)
        right = self.to_sympy(root.right)
        
        # protected division
        if root.value == '/' and right == 0:
            return sympy.Integer(1)
        
        # combine subtrees using root operator
        return OPERATORS[root.value](left, right)
    
    def tree_depth(self, node):
        """Recursively find the max depth of a subtree from node

        Args:
            node (TreeNode): starting point node

        Returns:
            int: depth of subtree from node
        """
        # base case: beyond leaf
        if node is None:
            return 0
        
        # recursive case: increment depth by 1 and take max of recursive traversal left and right
        return 1 + max(self.tree_depth(node.left), self.tree_depth(node.right))
    
    def tree_size(self):
        """Returns the number of nodes in the tree"""
        nodes = []
        self.collect_nodes(self.root, nodes)
        return len(nodes)
    
    def has_variable(self):
        """Checks if tree uses at least one variable
        
        Returns:
            bool: True if any leaf is a variable, False if tree is constants only
        """
        nodes = []
        self.collect_nodes(self.root, nodes)
        return any(node.is_leaf() and isinstance(node.value, str) for node in nodes)
    
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
            # case 2: value (constant = int/real) otherwise
            else: 
                leaf = Tree.random_constant(int_constants, const_range)
            
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
    
    @staticmethod
    def random_constant(int_constants, const_range):
        """Generate random constant: integer in const_range, or reals on a log scale

        Args:
            int_constants (bool): True for integer, False for reals
            const_range (tuple): (low, high) values for integers, or (low, high) exponents of 10 for reals
            
        Returns:
            int/float: random constant
        """
        low, high = const_range
        # integer constant (dataset 1): same as before 
        if int_constants:
            return random.randint(low, high)
        # real-valued constant (dataset 2)
        return random.choice([-1, 1]) * 10 ** random.uniform(low, high)

# you have x, y, y_tree

# .eval --> turns string expression into an expression tree (roundabout way of doing things)

# STEPS
# 1) generate random tree 
# 2) add to set 
# 3) substitute variables with values and evaluate using post-order traversal (compute left then right subtree)
# 4) record y_tree value and compare with fitness function to determine keep or discard
# Final) turn into a string using in-order traversal to present the final expression