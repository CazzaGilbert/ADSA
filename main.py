import sys

class Node: #leaves
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class Tree: #stump
    def insert(self, root, key): # add leaf
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        else:
            return root  # Duplicate keys are not allowed

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        # Left Heavy
        if balance > 1:
            if key < root.left.key:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        # Right Heavy
        if balance < -1:
            if key > root.right.key:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root

    def delete(self, root, key): # remove leaf
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        balance = self.get_balance(root)

        if balance > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)

        if balance < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)

        return root

    def left_rotate(self, root): # rotate left
        leaf = root.right
        temp = leaf.left

        leaf.left = root
        root.right = temp

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        leaf.height = 1 + max(self.get_height(leaf.left), self.get_height(leaf.right))

        return leaf

    def right_rotate(self, root): #rotate right
        leaf = root.left
        temp = leaf.right

        leaf.right = root
        root.left = temp

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        leaf.height = 1 + max(self.get_height(leaf.left), self.get_height(leaf.right))

        return leaf

    def get_height(self, root): # get height
        if not root:
            return 0
        return root.height

    def get_balance(self, root): # check balance
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root): # get smallest leaf
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def pre_order(self, root):# pre-order traversal
        res = []
        if root:
            res.append(root.key)
            res.extend(self.pre_order(root.left))
            res.extend(self.pre_order(root.right))
        return res

    def in_order(self, root): # in-order traversal
        res = []
        if root:
            res.extend(self.in_order(root.left))
            res.append(root.key)
            res.extend(self.in_order(root.right))
        return res

    def post_order(self, root):  # post-order traversal
        res = []
        if root:
            res.extend(self.post_order(root.left))
            res.extend(self.post_order(root.right))
            res.append(root.key)
        return res



if __name__ == "__main__":
    # create empty AVL tree
    AVL = Tree()
    root = None

    # get user input  
    input = sys.stdin.read()
    commands = input.split(' ',100)

    # for each command
    for command in commands:
        # insert
        if command.startswith('A'):
            value = int(command[1:])
            root = AVL.insert(root, value)
        #delete
        elif command.startswith('D'):
            value = int(command[1:])
            root = AVL.delete(root, value)
               
    #get output
    finishing_move = commands[-1]
    # if tree not empty
    if root:
        if finishing_move == 'PRE':
            print(' '.join(map(str, AVL.pre_order(root))))
        elif finishing_move == 'IN':
            print(' '.join(map(str, AVL.in_order(root))))
        elif finishing_move == 'POST':
            print(' '.join(map(str, AVL.post_order(root))))
    else: # if tree empty
        print("EMPTY")