from collections import namedtuple
from fractions import Fraction

Swap = namedtuple('Swap', ['swap_type', 'first', 'second'])
RowAddition = namedtuple('RowAddition', ['source', 'target', 'coefficient'])
MaxValueWithPlace = namedtuple('MaxValueWithPlace', ['place', 'value'])


def check_matrix(m):
    if not isinstance(m, list):
        raise TypeError("matrix must be 'list' of 'list's of 'Fraction's")
    if len(m) == 0:
        raise ValueError('empty matrix')
    for line in m:
        if not isinstance(line, list):
            raise TypeError("matrix must be 'list' of 'list's of 'Fraction's")
        if not all(map(lambda x: isinstance(x, Fraction), line)):
            raise TypeError("matrix must be 'list' of 'list's of 'Fraction's")
    row_len = len(m[0])
    if row_len == 0 or any(map(lambda x: len(x) != row_len, m)):
        raise ValueError('all rows must have constant non-zero length')


def swap_rows(m, i, j):
    m[i], m[j] = m[j], m[i]


def swap_columns(m, i, j):
    for row in m:
        row[i], row[j] = row[j], row[i]


def add_row(matrix, source, target, coefficient):
    for i in range(len(matrix[0])):
        matrix[target][i] += coefficient * matrix[source][i]


def find_max(m, start):
    res = MaxValueWithPlace(place=(start, start), value=abs(m[start][start]))
    for i in range(start, len(m)):
        for j in range(start, len(m[i])):
            current_value = abs(m[i][j])
            if current_value > res.value:
                res = MaxValueWithPlace(place=(i, j), value=current_value)
    return res


def to_row_echelon_form(m):
    check_matrix(m)
    actions = []
    for i in range(min(len(m), len(m[0]))):
        max_elem = find_max(m, i)
        max_row, max_column = max_elem.place

        if max_elem.value == 0:
            return actions

        if max_row != i:
            actions.append(Swap(swap_type='row', first=i,
                                second=max_row))
            swap_rows(m, i, max_row)

        if max_column != i:
            actions.append(Swap(swap_type='column', first=i,
                                second=max_column))
            swap_columns(m, i, max_column)

        for row in range(i + 1, len(m)):
            if m[row][i] == 0:
                continue
            coef = -m[row][i] / m[i][i]
            actions.append(RowAddition(source=i, target=row, coefficient=coef))
            add_row(m, i, row, coef)

    return actions


def solve(matrix, free_column):
    actions = to_row_echelon_form(matrix)
    for action in actions:
        if isinstance(action, Swap) and action.swap_type == 'row':
            free_column[action.first], free_column[action.second] = \
                free_column[action.second], free_column[action.first]
        elif isinstance(action, RawAddition):
            free_column[action.target] += action.coefficient * \
                                          free_column[action.source]

    col_num = len(matrix[0])
    row_num = len(matrix)
    solution = [None] * col_num
    for row in range(row_num - 1, -1, -1):
        new_vars = 0
        left_sum = 0
        new_var_pos = 0
        for column in range(col_num):
            if matrix[row][column] != 0:
                if solution[column] is None:
                    new_vars += 1
                    new_var_pos = column
                else:
                    left_sum += solution[column] * matrix[row][column]

        if new_vars == 0 and left_sum != free_column[row]:
            raise ValueError('the equation has no solution')
        if new_vars > 1:
            raise ValueError('the equation has more then one solution')
        if new_vars == 0:
            continue

        solution[new_var_pos] = (free_column[row] - left_sum) / matrix[row][
            new_var_pos]

    for action in reversed(actions):
        if isinstance(action, Swap) and action.swap_type == 'column':
            solution[action.first], solution[action.second] = \
                solution[action.second], solution[action.first]
    return solution
