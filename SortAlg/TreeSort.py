from SortBase import SortBase


class Tree:
    def __init__(self, key=None, data=None, left=None, right=None):
        self.key = key
        self.data = data
        if key is None:
            self.left = left
            self.right = right
        else:
            self.left = Tree()
            self.right = Tree()

    def find(self, key):
        if self.key is None:
            return

        if key == self.key:
            return self
        if key > self.key:
            return self.right.find(key)
        if key < self.key:
            return self.left.find(key)

    def insert(self, key, data=None):
        if self.key is None:
            self.key = key
            self.data = data
            self.left = Tree()
            self.right = Tree()

        elif key == self.key:
            self.data = data

        elif key > self.key:
            self.right.insert(key, data)
        elif key < self.key:
            self.left.insert(key, data)

    def infix_traverse(self, f=print, reverse: bool = False):
        if self.key is None:
            return
        if not reverse:
            self.left.infix_traverse(f, reverse)
            f(self.key, self.data)
            self.right.infix_traverse(f, reverse)
        else:
            self.left.infix_traverse(f, reverse)
            f(self.key, self.data)
            self.right.infix_traverse(f, reverse)

    def __str__(self):
        return f"<({type(self).__name__}) key: {self.key}, data: {self.data}>"


class TreeSort(SortBase):
    def __init__(self):
        super().__init__()

    @staticmethod
    def sort_list(a: list, reverse: bool = False):
        """

        :param a: UNIQ list
        :param reverse:
        :return:
        """

        def f(x, data=None):
            a[start_index[0]] = x
            start_index[0] += 1

        tree = Tree()
        for elem in a:
            tree.insert(elem)
        start_index = [0]
        tree.infix_traverse(f, reverse)

        return start_index[0]


if __name__ == "__main__":
    trs = TreeSort()
    test_arr = trs.create_test_list(10, mx=50)

    print(trs.sort_list(test_arr))

    print(test_arr)
