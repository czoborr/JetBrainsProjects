from copy import deepcopy


def read_matrix(row_number):
    matrix = []
    for i in range(0, row_number):
        matrix.append(list(map(float, input().split())))
    return matrix


def read_inputs():
    size = input()
    M = read_matrix(int(size[0]))
    size2 = input()
    M2 = read_matrix(int(size2[0]))
    return M, size, M2, size2


def print_result(matrix):
    print("The result is:")
    for i in matrix:
        print(' '.join(list(map(str, i))))


def add_matrix(matrix, size1, matrix2, size2):
    if size1 != size2:
        print('The operation cannot be performed.')
    else:
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = matrix[i][j] + matrix2[i][j]
        print_result(matrix)


def scalar_multiplication(matrix, scalar):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = matrix[i][j] * scalar
    print_result(matrix)


def multiply_matrix(matrix, size1, matrix2, size2):
    if size1[2] != size2[0]:
        print('The operation cannot be performed.')
    else:
        result = [[0] * int(size1[0])] * int(size2[2])
        result = [[sum(i * j for i, j in zip(matrix_row, matrix2_col)) for matrix2_col in zip(*matrix2)] for matrix_row
                  in matrix]
        print_result(result)


def transpose_matrix(number, matrix):
    row = len(matrix)
    col = len(matrix[0])
    if number == 1:
        result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        return result
    elif number == 2:
        for i in range(0, row - 1):
            for j in range(0, col - 1):
                matrix[i][j], matrix[(col - 1) - j][(row - 1) - i] = matrix[(col - 1) - j][(row - 1) - i], matrix[i][j]
        return matrix
    elif number == 3:
        result = []
        for i in range(0, len(matrix)):
            result.append([elem for elem in reversed(matrix[i])])
        return result
    else:
        result = [j for j in reversed(matrix)]
        return result


def determinant_recursive(matrix, total=0):
    indices = list(range(len(matrix)))
    if len(matrix) == 1 and len(matrix[0]) == 1:
        return matrix[0][0]
    if len(matrix) == 2 and len(matrix[0]) == 2:
        val = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return val
    for fc in indices:
        As = deepcopy(matrix)
        As = As[1:]
        height = len(As)
        for i in range(height):
            As[i] = As[i][0:fc] + As[i][fc + 1:]
        sign = (-1) ** (fc % 2)  # F)
        sub_det = determinant_recursive(As)
        total += sign * matrix[0][fc] * sub_det
    return total


def get_matrix_minor(matrix, i, j):
    return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]


def inverse_matrix(matrix):
    determinant = determinant_recursive(matrix)
    if len(matrix) == 2:
        return [[matrix[1][1] / determinant, -1 * matrix[0][1] / determinant],
                [-1 * matrix[1][0] / determinant, matrix[0][0] / determinant]]
    cofactors = []
    for r in range(len(matrix)):
        cofactorrow = []
        for c in range(len(matrix)):
            minor = get_matrix_minor(matrix, r, c)
            cofactorrow.append(((-1) ** (r + c)) * determinant_recursive(minor))
        cofactors.append(cofactorrow)
    cofactors = transpose_matrix(1, cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return cofactors


while True:
    print(
        '1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n4. Transpose matrix\n5. Calculate a determinant\n6. Calculate Inverse\n0. Exit')
    choice = int(input())
    print(f"Your choice: > {choice}")

    if choice == 1:
        size = input()
        M = read_matrix(int(size[0]))
        size2 = input()
        M2 = read_matrix(int(size2[0]))
        add_matrix(M, size, M2, size2)
        continue
    elif choice == 2:
        size = input()
        M = read_matrix(int(size[0]))
        scalar = float(input())
        scalar_multiplication(M, scalar)
        continue
    elif choice == 3:
        size = input()
        M = read_matrix(int(size[0]))
        size2 = input()
        M2 = read_matrix(int(size2[0]))
        multiply_matrix(M, size, M2, size2)
        continue
    elif choice == 4:
        print('1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line')
        choice2 = int(input())
        print(f"Your choice: > {choice2}")
        size = input()
        M = read_matrix(int(size[0]))
        print(print_result(transpose_matrix(choice2, M)))
    elif choice == 5:
        size = input()
        M = read_matrix(int(size[0]))
        print(determinant_recursive(M, total=0))
    elif choice == 6:
        size = input()
        M = read_matrix(int(size[0]))
        print(print_result(inverse_matrix(M)))
    else:
        break
