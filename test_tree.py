"""Functions to test the tree class added functionalities at each incremental change
"""
from tree import TreeNode, Tree

def test_root():
    """Builds (x^2 + 5)"""
    return TreeNode('+', # root
                    TreeNode('*', TreeNode('x'), TreeNode('x')), # left child
                    TreeNode(3)) # right child

root = test_root()
# test leaf nodes ('x', 'x', 3) --> should all be True
print(root.left.left.is_leaf())
print(root.left.right.is_leaf())
print(root.right.is_leaf())
# test terminal nodes with is_leaf() --> should be false
print(root.is_leaf())
print(root.left.is_leaf())
print(test_root())