from SortBase import SortBase


class ShakerSort(SortBase):

    def __init__(self):
        super().__init__()

    @staticmethod
    def sort_list(a: list, reverse: bool = False):
        n = len(a)
        for i in range(n // 2):
            for j in range(1, n - i):
                if (a[j] < a[j - 1]) != reverse:
                    a[j], a[j - 1] = a[j - 1], a[j]

            for j in range(n - i - 1, 0, -1):
                if (a[j] < a[j - 1]) != reverse:
                    a[j], a[j - 1] = a[j - 1], a[j]


if __name__ == "__main__":
    bs = ShakerSort()
    ar = [9999, 888, 77, 66, 55, 44, 33, 22, 11, 9, 6, 5, 3]
    bs.sort_list(ar, reverse=False)
    bs.sort_list(ar, reverse=True)
    print(*ar, len(ar))
    print(bs.check_sort_list(ar, reverse=False))
