import unittest

from fractions import Fraction
import gaussian_method


def elem_to_fraction(num):
    if isinstance(num, tuple):
        return Fraction(*num)
    else:
        return Fraction(num)


def to_fraction(matrix, column):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = elem_to_fraction(matrix[i][j])
    for i in range(len(column)):
        column[i] = elem_to_fraction(column[i])


class SimpleTests(unittest.TestCase):
    def test_simple(self):
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        column = [1, 0, 1]
        to_fraction(matrix, column)

        solution = gaussian_method.solve(matrix, column)
        self.assertEqual(solution, [1, 0, 1])

    def test_multiple(self):
        matrix = [[1, 0, 0], [0, 1, 1], [0, 4.5, 4.5]]
        column = [0, 2, 9]
        to_fraction(matrix, column)

        solution = gaussian_method.solve(matrix, column)
        self.assertIn(solution,
                      ([0, [0, 0, -1, 2], None], [0, None, [0, -1, 0, None]]))

    def test_no_solution(self):
        matrix = [[2, 3], [3, 2], [1, 0]]
        column = [1, 1, 1]
        to_fraction(matrix, column)

        self.assertRaisesRegex(ValueError, 'the equation has no solution',
                               gaussian_method.solve, matrix, column)


if __name__ == '__main__':
    unittest.main()
