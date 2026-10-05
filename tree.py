"""Implementation of the Tree class

Contains functions to represent and manipulate individuals/trees in our population
"""

# Definition for a binary tree node
class TreeNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

# Expression tree class
class Tree:    
    def __init__(self, tree):
        """Initialize initial tree state

        Args:
            tree (_type_): _description_
        """
    
    def mutate(self):
        """Modifies an operation in the tree?
        """
        # ...
        # copy = self.clone()
        # return copy
    
    def crossover(self):
        """Joins a part of one tree with the other part of another tree?
        """