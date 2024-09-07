import sys

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key):
        if not root:
            return AVLNode(key)
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

    def delete(self, root, key):
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

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def pre_order(self, root):
        res = []
        if root:
            res.append(root.key)
            res.extend(self.pre_order(root.left))
            res.extend(self.pre_order(root.right))
        return res

    def in_order(self, root):
        res = []
        if root:
            res.extend(self.in_order(root.left))
            res.append(root.key)
            res.extend(self.in_order(root.right))
        return res

    def post_order(self, root):
        res = []
        if root:
            res.extend(self.post_order(root.left))
            res.extend(self.post_order(root.right))
            res.append(root.key)
        return res



if __name__ == "__main__":
    # create empty AVL tree
    Tree = AVLTree()
    root = None

    # get user input  
    input = sys.stdin.read()
    commands = input.split(' ',100)

    # for each command
    for command in commands:
        # insert
        if command.startswith('A'):
            value = int(command[1:])
            root = Tree.insert(root, value)
        #delete
        elif command.startswith('D'):
            value = int(command[1:])
            root = Tree.delete(root, value)
               
    #get output
    finishing_move = commands[-1]
    # if tree not empty
    if root:
        if finishing_move == 'PRE':
            print(' '.join(map(str, Tree.pre_order(root))))
        elif finishing_move == 'IN':
            print(' '.join(map(str, Tree.in_order(root))))
        elif finishing_move == 'POST':
            print(' '.join(map(str, Tree.post_order(root))))
    else: # if tree empty
        print("EMPTY")
