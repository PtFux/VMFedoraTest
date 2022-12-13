from SortBase import SortBase


class BubbleSort(SortBase):

    def __init__(self):
        super().__init__()

    @staticmethod
    def sort_list(a: list, reverse: bool = False):
        n = len(a)
        for i in range(n):
            for j in range(1, n-i):
                if (a[j] < a[j - 1]) != reverse:
                    a[j], a[j - 1] = a[j - 1], a[j]


if __name__ == "__main__":
    bs = BubbleSort()
    ar = [7, 8, 4, 7, 2, 8, 4, 9, 43534, 9876, 4235, 65, 3, 7, 8]
    bs.sort_list(ar, reverse=False)
    print(*ar)
