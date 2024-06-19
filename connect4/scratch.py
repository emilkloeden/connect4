grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]


def rotate(matrix):
    return list(zip(*matrix))[::-1]


if __name__ == "__main__":
    rotated = rotate(grid)
    for row in rotated:
        print(row)
