# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
from stackedbarplots.tools import cumu1d, cumu2d, ColourGradient

class TestCumu1d(unittest.TestCase):
    """Unit tests for method cumu1d() in tools.py."""
    def test_basic(self):
        example_data = [4, 3, 6, 1, 3]
        long_data = [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3]
        short_data = [1, 4]
        self.assertEqual(cumu1d(example_data), [4, 7, 13, 14, 17])
        self.assertEqual(cumu1d(long_data), [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188])
        self.assertEqual(cumu1d(short_data), [1, 5])

    def test_decimal(self):
        example_data = [4.5, 3.3, 6.22, 1.111111, 3.9]
        cum_data = cumu1d(example_data)
        solution = [4.5, 7.8, 14.02, 15.131111, 19.031111]
        for data, sol in zip(cum_data, solution):
            self.assertAlmostEqual(data, sol, 5)

    def test_negative(self):
        example_data = [-4, -3, -6, -1, -3]
        self.assertEqual(cumu1d(example_data), [-4, -7, -13, -14, -17])

    def test_deep_copy(self):
        example_data = [4, 3, 6, 1, 3]
        cumu1d(example_data)
        self.assertEqual(example_data, [4, 3, 6, 1, 3])

class TestCumu2d(unittest.TestCase):
    """Unit tests for method cumu2d() in tools.py."""
    def test_basic(self):
        example_data = [[4, 3, 6, 1, 3],
                        [4, 3, 6, 1, 3],
                        [4, 3, 6, 1, 3]]
        self.assertEqual(cumu2d(example_data), [[4, 7, 13, 14, 17],
                                                [4, 7, 13, 14, 17],
                                                [4, 7, 13, 14, 17]])

        long_data = [[9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3],
                     [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3],
                     [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3],
                     [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3],
                     [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3],
                     [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3]]
        self.assertEqual(cumu2d(long_data), [[9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188],
                                             [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188],
                                             [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188],
                                             [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188],
                                             [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188],
                                             [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188]])

        short_data = [[1, 4]]
        self.assertEqual(cumu2d(short_data), [[1, 5]])

class TestColourGradient(unittest.TestCase):
    """Unit tests for method gradient() in class ColourGradient in tools.py, 
    without passing param center_colour."""
    def test_create_two_gradient(self):
        col_obj = ColourGradient()
        col_obj.gradient(4, (100, 100, 100), (250, 250, 250))
        self.assertEqual(col_obj.get_gradient_list(), [(100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250)])

        col_obj.gradient(2, (1, 1, 1), (4, 4, 4))
        self.assertEqual(col_obj.get_gradient_list(), [(1, 1, 1), (4, 4, 4)])

        col_obj.gradient(4, (1, 1, 1), (4, 4, 4))
        self.assertEqual(col_obj.get_gradient_list(), [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)])

        col_obj.gradient(4, (1, 3, 4), (4, 2, 1))
        self.assertEqual(col_obj.get_gradient_list(), [(1, 3, 4), (2, 2, 3), (3, 2, 2), (4, 2, 1)])
        del col_obj

    def test_create_three_gradient(self):
        """Unit tests for method gradient() in class ColourGradient in tools.py, 
        passing param center_colour."""
        col_obj = ColourGradient()
        col_obj.gradient(3, (0, 0, 0), (200, 200, 200), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (100, 100, 100), (200, 200, 200)])

        col_obj.gradient(5, (0, 0, 0), (200, 200, 200), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (50, 50, 50), (100, 100, 100), (150, 150, 150), (200, 200, 200)])

        col_obj.gradient(7, (0, 0, 0), (200, 200, 200), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (33, 33, 33), (66, 66, 66), (100, 100, 100), (133, 133, 133), (166, 166, 166), (200, 200, 200)])

        col_obj.gradient(5, (0, 100, 200), (200, 100, 0), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 100, 200), (50, 100, 150), (100, 100, 100), (150, 100, 50), (200, 100, 0)])
        del col_obj

    def test_grayscale_gradient(self):
        """Unit tests for method grayscale_gradient() in class ColourGradient in tools.py"""
        col_obj = ColourGradient()
        col_obj.grayscale_gradient(3, 0, 1)
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (.5, .5, .5), (1, 1, 1)])

        col_obj.grayscale_gradient(5, 0, 1)
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (.25, .25, .25), (.5, .5, .5), (.75, .75, .75), (1, 1, 1)])
        del col_obj

    def test_get_normalised_gradient_list(self):
        """Unit tests for method test_get_normalised_gradient_list() in class ColourGradient in tools.py"""
        col_obj = ColourGradient()
        col_obj.set_colour_gradient_list([(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)])
        self.assertEqual(col_obj.get_normalised_gradient_list(), [(0, 0, 0), (0, 0, 0), (1, 1, 1), (1, 1, 1)])

        col_obj.set_colour_gradient_list([(0, 51, 255)])
        self.assertEqual(col_obj.get_normalised_gradient_list(), [(0, .2, 1)])
        del col_obj

    def test_set_colour_gradient_list(self):
        """Unit tests for method set_colour_gradient_list() in class ColourGradient in tools.py"""
        col_obj = ColourGradient()
        col_obj.set_colour_gradient_list([(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)])
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)])
        self.assertEqual(col_obj.get_normalised_gradient_list(), [(0, 0, 0), (0, 0, 0), (1, 1, 1), (1, 1, 1)])

if __name__ == '__main__':
    unittest.main()