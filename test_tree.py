"""Functions to test the tree class added functionalities at each incremental change
"""
from tree import TreeNode, Tree

def test_root():
    """Builds (x^2 + 3)"""
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

# test tree compute function
tree = Tree(root)
print(tree.compute_tree(tree.root, 2)) # should = 2^2 + 3 = 7
print(tree.compute_tree(tree.root, 3)) # should = 3^2 + 3 = 12
print(tree.compute_tree(tree.root, -5)) # should = (-5)^2 + 3 = 28

#in order test
print(tree.inorder()) # should = ((x * x) + 3)

#cross over test 
# Create a second tree
root2 = TreeNode('*',
    TreeNode('+', TreeNode('x'), TreeNode(2)),TreeNode(5))

tree2 = Tree(root2)

# Test crossover
child1, child2 = tree.crossover(tree2)

# Print the results
print("Parent 1:", tree.inorder(tree.root))
print("Parent 2:", tree2.inorder(tree2.root))

print("Child 1:", child1.inorder(child1.root))
print("Child 2:", child2.inorder(child2.root))