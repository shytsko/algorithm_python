"""
Реализация АВЛ-дерева
За основу взят пример отсюда: https://habr.com/ru/post/150732/
"""


class AVLTree:
    class Node:
        def __init__(self, value: int) -> None:
            super().__init__()
            self.value: int = value
            self.height: int = 1
            self.left: AVLTree.Node = None
            self.right: AVLTree.Node = None

        def __repr__(self) -> str:
            return str(self.value)

    def __init__(self) -> None:
        super().__init__()
        self.root: AVLTree.Node = None

    def __height(self, node: Node) -> int:
        """
        Вернет высоту дерева относительно заданного узла
        :return: Высота относительно заданного узла. Если поддерево пустое, вернет 0
        """
        return node.height if node else 0

    def __balance_factor(self, node: Node) -> int:
        """
        Определяет, насколько левое и правое поддеревья разбаллансированы
        """
        return self.__height(node.right) - self.__height(node.left)

    def __fix_height(self, node: Node):
        """
        Пересчет высоты дерева
        """
        height_left = self.__height(node.left)
        height_right = self.__height(node.right)
        node.height = max(height_right, height_left) + 1

    def __rotate_right(self, p_node: Node) -> Node:
        """
        Правый поворот относительно заданного узла
                P       --->        Q
               / \                 / \
              Q   c               a   P
             / \                     / \
            a   b                   b   c
        """
        q_node = p_node.left
        p_node.left = q_node.right
        q_node.right = p_node
        self.__fix_height(p_node)
        self.__fix_height(q_node)
        return q_node

    def __rotate_left(self, q_node: Node) -> Node:
        """
        Левый поворот относительно заданного узла
             Q      --->        P
            / \                / \
           a   P              Q   c
              / \            / \
             b   c          a   b
        """
        p_node = q_node.right
        q_node.right = p_node.left
        p_node.left = q_node
        self.__fix_height(q_node)
        self.__fix_height(p_node)
        return p_node

    def __balance(self, node: Node) -> Node:
        self.__fix_height(node)
        if self.__balance_factor(node) == 2:
            if self.__balance_factor(node.right) < 0:
                node.right = self.__rotate_right(node.right)
            return self.__rotate_left(node)
        if self.__balance_factor(node) == -2:
            if self.__balance_factor(node.left) > 0:
                node.left = self.__rotate_left(node.left)
            return self.__rotate_right(node)
        return node

    def __insert(self, node: Node, value: int) -> Node:
        if not node:
            return AVLTree.Node(value)
        if value < node.value:
            node.left = self.__insert(node.left, value)
        else:
            node.right = self.__insert(node.right, value)
        return self.__balance(node)

    def insert(self, value):
        self.root = self.__insert(self.root, value)

    def insert_all(self, values: set):
        for value in values:
            self.root = self.__insert(self.root, value)

    def __find_min(self, node: Node) -> Node:
        return self.__find_min(node.left) if node.left else node

    def __remove_min(self, node: Node) -> Node:
        if not node.left:
            return node.right
        node.left = self.__remove_min(node.left)
        return self.__balance(node)

    def __remove(self, node: Node, value: int) -> Node:
        if not node:
            return None
        elif value < node.value:
            node.left = self.__remove(node.left, value)
        elif value > node.value:
            node.right = self.__remove(node.right, value)
        else:  # value == node.value
            node_q = node.left
            node_r = node.right
            del node
            if not node_r:
                return node_q
            node_min = self.__find_min(node_r)
            node_min.right = self.__remove_min(node_r)
            node_min.left = node_q
            return self.__balance(node_min)
        return self.__balance(node)

    def remove(self, value: int):
        self.root = self.__remove(self.root, value)

    def __is_contains(self, node: Node, value: int) -> bool:
        if not node:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self.__is_contains(node.left, value)
        else:
            return self.__is_contains(node.right, value)

    def is_contains(self, value: int) -> bool:
        return self.__is_contains(self.root, value)


tree = AVLTree()
tree.insert_all({30, 15, 8, 1, 5, 10, 20, 35, 21, 3, 21, 40})
print(tree.is_contains(30))
tree.remove(30)
print(tree.is_contains(30))
tree.remove(20)
print(tree.is_contains(10))
print(tree.is_contains(18))
print(tree.is_contains(40))
print(tree.is_contains(2))
print()
