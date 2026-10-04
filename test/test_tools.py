# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,missing-function-docstring,missing-class-docstring,line-too-long,disable=consider-using-enumerate

import unittest
from stackedbarplots.tools import cumu1d, cumu2d, ColourGradient, ChartDataSorting

class TestCumu1d(unittest.TestCase):
    """Unit tests for method cumu1d() in tools.py."""

    def test_basic(self):
        example_data = [4, 3, 6, 1, 3]
        long_data = [9, 4, 5, 2, 1, 5, 6, 3, 1, 6, 11, 32, 100, 3]
        short_data = [1, 4]
        self.assertEqual(cumu1d(example_data), [4, 7, 13, 14, 17], "Error in basic cumu1d() functionality.")
        self.assertEqual(cumu1d(long_data), [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188], "Error in cumu1d() functionality with long lists.")
        self.assertEqual(cumu1d(short_data), [1, 5], "Error in cumu1d() functionality with short lists (len 2).")


    def test_decimal(self):
        example_data = [4.5, 3.3, 6.22, 1.111111, 3.9]
        cum_data = cumu1d(example_data)
        solution = [4.5, 7.8, 14.02, 15.131111, 19.031111]
        for data, sol in zip(cum_data, solution):
            self.assertAlmostEqual(data, sol, 5, "Error in cumu1d() functionality with floating point data.")


    def test_negative(self):
        example_data = [-4, -3, -6, -1, -3]
        self.assertEqual(cumu1d(example_data), [-4, -7, -13, -14, -17], "Error in basic cumu1d() functionality with negative data.")


    def test_deep_copy(self):
        example_data = [4, 3, 6, 1, 3]
        cumu1d(example_data)
        self.assertEqual(example_data, [4, 3, 6, 1, 3], "Error related to cumu1d() deep memory copying.")




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
                                             [9, 13, 18, 20, 21, 26, 32, 35, 36, 42, 53, 85, 185, 188]],
                                             "Error in basic cumu2d() functionality.")

        short_data = [[1, 4]]
        self.assertEqual(cumu2d(short_data), [[1, 5]], "Error in basic cumu2d() functionality with short 2D list.")




class TestColourGradient(unittest.TestCase):
    """Unit tests for method gradient() in class ColourGradient in tools.py, 
    without passing param centre_colour."""

    def test_create_two_gradient(self):
        col_obj = ColourGradient()
        col_obj.gradient(4, (100, 100, 100), (250, 250, 250))
        self.assertEqual(col_obj.get_gradient_list(), [(100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250)],
                         "Error in basic gradient() functionality.")

        col_obj.gradient(2, (1, 1, 1), (4, 4, 4))
        self.assertEqual(col_obj.get_gradient_list(), [(1, 1, 1), (4, 4, 4)],
                         "Error in basic gradient() functionality with only two colours.")

        col_obj.gradient(4, (1, 1, 1), (4, 4, 4))
        self.assertEqual(col_obj.get_gradient_list(), [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)],
                         "Error in basic gradient() functionality.")

        col_obj.gradient(4, (1, 3, 4), (4, 2, 1))
        self.assertEqual(col_obj.get_gradient_list(), [(1, 3, 4), (2, 2, 3), (3, 2, 2), (4, 2, 1)],
                         "Error in basic gradient() functionality with RGB values moving in opposite directions.")
        del col_obj


    def test_create_three_gradient(self):
        """Unit tests for method gradient() in class ColourGradient in tools.py, 
        passing param centre_colour."""
        col_obj = ColourGradient()
        col_obj.gradient(3, (0, 0, 0), (200, 200, 200), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (100, 100, 100), (200, 200, 200)],
                         "Error in basic gradient() functionality with central colour.")

        col_obj.gradient(5, (0, 0, 0), (200, 200, 200), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (50, 50, 50), (100, 100, 100), (150, 150, 150), (200, 200, 200)],
                         "Error in basic gradient() functionality with 5 colours including central colour.")

        col_obj.gradient(7, (0, 0, 0), (200, 200, 200), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (33, 33, 33), (66, 66, 66), (100, 100, 100), (133, 133, 133), (166, 166, 166), (200, 200, 200)],
                         "Error in basic gradient() functionality with 7 colours including central colour.")

        col_obj.gradient(5, (0, 100, 200), (200, 100, 0), (100, 100, 100))
        self.assertEqual(col_obj.get_gradient_list(), [(0, 100, 200), (50, 100, 150), (100, 100, 100), (150, 100, 50), (200, 100, 0)],
                         "Error in basic gradient() functionality with 5 colours including central colour with RGB values moving in opposite directions.")
        del col_obj


    def test_grayscale_gradient(self):
        """Unit tests for method grayscale_gradient() in class ColourGradient in tools.py"""
        col_obj = ColourGradient()
        col_obj.grayscale_gradient(3, 0, 1)
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (.5, .5, .5), (1, 1, 1)],
                         "Error in basic grayscale_gradient() functionality.")

        col_obj.grayscale_gradient(5, 0, 1)
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (.25, .25, .25), (.5, .5, .5), (.75, .75, .75), (1, 1, 1)],
                         "Error in basic grayscale_gradient() functionality with 5 colours.")
        del col_obj


    def test_get_normalised_gradient_list(self):
        """Unit tests for method test_get_normalised_gradient_list() in class ColourGradient in tools.py"""
        col_obj = ColourGradient()
        col_obj.set_colour_gradient_list([(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)])
        self.assertEqual(col_obj.get_normalised_gradient_list(), [(0, 0, 0), (0, 0, 0), (1, 1, 1), (1, 1, 1)],
                         "Error in get_normalised_gradient_list() method.")

        col_obj.set_colour_gradient_list([(0, 51, 255)])
        self.assertEqual(col_obj.get_normalised_gradient_list(), [(0, .2, 1)],
                         "Error in get_normalised_gradient_list() method.")
        del col_obj


    def test_set_colour_gradient_list(self):
        """Unit tests for method set_colour_gradient_list() in class ColourGradient in tools.py"""
        col_obj = ColourGradient()
        col_obj.set_colour_gradient_list([(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)])
        self.assertEqual(col_obj.get_gradient_list(), [(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)],
                         "Error in get_gradient_list() method.")
        self.assertEqual(col_obj.get_normalised_gradient_list(), [(0, 0, 0), (0, 0, 0), (1, 1, 1), (1, 1, 1)],
                         "Error in get_normalised_gradient_list() method.")




class TestChartDataSorting(unittest.TestCase):
    """Unit tests for chart sorting functionality in ChartDataSorting class in tools.py"""

    def test_by_sum(self):
        """Unit tests for sort_by_sum() method in ChartDataSorting class in tools.py"""
        test_data = [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test that sorting method creates a deep copy of the data and category headings.
        sorted_data, sorted_category_headings = ChartDataSorting.by_sum(test_data, category_headings, reverse=False)
        self.assertEqual(test_data, [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]], "Error in by_sum() method related to deep copying in ChartDataSorting class in tools.py")
        self.assertEqual(category_headings, ["Category 1", "Category 2", "Category 3"], "Error in by_sum() method related to deep copying in ChartDataSorting class in tools.py")

        #Test for sorting with integers
        sorted_data, sorted_category_headings = ChartDataSorting.by_sum(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[4, 2, 9, 12], [10, 5, 3, 11], [11, 12, 3, 4]], "Error in by_sum() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_sum() method in ChartDataSorting class in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_sum(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[11, 12, 3, 4], [10, 5, 3, 11], [4, 2, 9, 12]], "Error in by_sum() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_sum() method in ChartDataSorting class in tools.py")

        test_data = [[1, .5, .3, 1.1], [.4, .2, .9, 1.2], [1.1, 1.2, .3, .4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test for sorting with floats
        sorted_data, sorted_category_headings = ChartDataSorting.by_sum(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[.4, .2, .9, 1.2], [1, .5, .3, 1.1], [1.1, 1.2, .3, .4]], "Error in by_sum() method with decimal values in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_sum() method in ChartDataSorting class with decimal values in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_sum(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[1.1, 1.2, .3, .4], [1, .5, .3, 1.1], [.4, .2, .9, 1.2]], "Error in by_sum() method in ChartDataSorting class with decimal values in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_sum() method in ChartDataSorting class with decimal values in tools.py")


    def test_by_average(self):
        """Unit tests for sort_by_average() method in ChartDataSorting class in tools.py"""
        test_data = [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test that sorting method creates a deep copy of the data and category headings.
        sorted_data, sorted_category_headings = ChartDataSorting.by_average(test_data, category_headings, reverse=False)
        self.assertEqual(test_data, [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]], "Error in by_average() method related to deep copying in ChartDataSorting class in tools.py")
        self.assertEqual(category_headings, ["Category 1", "Category 2", "Category 3"], "Error in by_average() method related to deep copying in ChartDataSorting class in tools.py")

        #Test for sorting with integers
        sorted_data, sorted_category_headings = ChartDataSorting.by_average(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[4, 2, 9, 12], [10, 5, 3, 11], [11, 12, 3, 4]], "Error in by_average() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_average() method in ChartDataSorting class in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_average(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[11, 12, 3, 4], [10, 5, 3, 11], [4, 2, 9, 12]], "Error in by_average() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_average() method in ChartDataSorting class in tools.py")

        test_data = [[1, .5, .3, 1.1], [.4, .2, .9, 1.2], [1.1, 1.2, .3, .4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test for sorting with floats
        sorted_data, sorted_category_headings = ChartDataSorting.by_average(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[.4, .2, .9, 1.2], [1, .5, .3, 1.1], [1.1, 1.2, .3, .4]], "Error in by_average() method with decimal values in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_average() method in ChartDataSorting class with decimal values in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_average(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[1.1, 1.2, .3, .4], [1, .5, .3, 1.1], [.4, .2, .9, 1.2]], "Error in by_average() method in ChartDataSorting class with decimal values in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_average() method in ChartDataSorting class with decimal values in tools.py")


    def test_by_left_half(self):
        """Unit tests for sort_by_left_half() method in ChartDataSorting class in tools.py"""
        test_data = [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test that sorting method creates a deep copy of the data and category headings.
        sorted_data, sorted_category_headings = ChartDataSorting.by_left_half(test_data, category_headings, reverse=False)
        self.assertEqual(test_data, [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]], "Error in by_left_half() method related to deep copying in ChartDataSorting class in tools.py")
        self.assertEqual(category_headings, ["Category 1", "Category 2", "Category 3"], "Error in by_left_half() method related to deep copying in ChartDataSorting class in tools.py")

        #Test for sorting with integers
        sorted_data, sorted_category_headings = ChartDataSorting.by_left_half(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[4, 2, 9, 12], [10, 5, 3, 11], [11, 12, 3, 4]], "Error in by_left_half() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_left_half() method in ChartDataSorting class in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_left_half(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[11, 12, 3, 4], [10, 5, 3, 11], [4, 2, 9, 12]], "Error in by_left_half() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_left_half() method in ChartDataSorting class in tools.py")

        test_data = [[1, .5, .3, 1.1], [.4, .2, .9, 1.2], [1.1, 1.2, .3, .4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test for sorting with floats
        sorted_data, sorted_category_headings = ChartDataSorting.by_left_half(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[.4, .2, .9, 1.2], [1, .5, .3, 1.1], [1.1, 1.2, .3, .4]], "Error in by_left_half() method with decimal values in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_left_half() method in ChartDataSorting class with decimal values in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_left_half(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[1.1, 1.2, .3, .4], [1, .5, .3, 1.1], [.4, .2, .9, 1.2]], "Error in by_left_half() method in ChartDataSorting class with decimal values in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_left_half() method in ChartDataSorting class with decimal values in tools.py")


    def test_by_right_half(self):
        """Unit tests for sort_by_right_half() method in ChartDataSorting class in tools.py"""
        test_data = [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test that sorting method creates a deep copy of the data and category headings.
        sorted_data, sorted_category_headings = ChartDataSorting.by_right_half(test_data, category_headings, reverse=False)
        self.assertEqual(test_data, [[10, 5, 3, 11], [4, 2, 9, 12], [11, 12, 3, 4]], "Error in by_right_half() method related to deep copying in ChartDataSorting class in tools.py")
        self.assertEqual(category_headings, ["Category 1", "Category 2", "Category 3"], "Error in by_right_half() method related to deep copying in ChartDataSorting class in tools.py")

        #Test for sorting with integers
        sorted_data, sorted_category_headings = ChartDataSorting.by_right_half(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[11, 12, 3, 4], [10, 5, 3, 11], [4, 2, 9, 12]], "Error in by_right_half() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_right_half() method in ChartDataSorting class in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_right_half(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[4, 2, 9, 12], [10, 5, 3, 11], [11, 12, 3, 4]], "Error in by_right_half() method in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_right_half() method in ChartDataSorting class in tools.py")

        test_data = [[1, .5, .3, 1.1], [.4, .2, .9, 1.2], [1.1, 1.2, .3, .4]]
        category_headings = ["Category 1", "Category 2", "Category 3"]

        #Test for sorting with floats
        sorted_data, sorted_category_headings = ChartDataSorting.by_right_half(test_data, category_headings, reverse=False)
        self.assertEqual(sorted_data, [[1.1, 1.2, .3, .4], [1.0, .5, .3, 1.1], [.4, .2, .9, 1.2]], "Error in by_right_half() method with decimal values in ChartDataSorting class in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 3", "Category 1", "Category 2"], "Error in by_right_half() method in ChartDataSorting class with decimal values in tools.py")

        sorted_data, sorted_category_headings = ChartDataSorting.by_right_half(test_data, category_headings, reverse=True)
        self.assertEqual(sorted_data, [[.4, .2, .9, 1.2], [1.0, .5, .3, 1.1], [1.1, 1.2, .3, .4]], "Error in by_right_half() method in ChartDataSorting class with decimal values in tools.py")
        self.assertEqual(sorted_category_headings, ["Category 2", "Category 1", "Category 3"], "Error in by_right_half() method in ChartDataSorting class with decimal values in tools.py")




if __name__ == '__main__':
    unittest.main()
