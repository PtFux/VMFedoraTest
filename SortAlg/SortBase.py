from random import randint

class SortBase:
    def __init__(self):
        pass

    @staticmethod
    def check_sort_list(a: list, reverse: bool = False):
        for i in range(1, len(a)):
            if a[i] < a[i-1] == reverse:
                return False
        return True

    @staticmethod
    def create_test_list(n: int, mn: int = 0, mx: int = 10**5):
        a = []
        for i in range(n):
            a.append(randint(mn, mx))
        return a