grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]


def rotate(matrix):
    return list(zip(*matrix))[::-1]


if __name__ == "__main__":
    for j in range(len(grid[0])):
        for i in range(len(grid)):
            print(grid[i][j])
