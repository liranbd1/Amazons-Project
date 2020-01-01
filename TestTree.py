from treelib import Node, Tree

tree = Tree()
i = 1


def createRoot():
    tree.create_node(i, i)


def createTree():
    for k in range(2, 10):
       temp = tree.create_node(k, k, i)


createRoot()
createTree()
tree.show()
