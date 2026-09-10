# pylint: disable=multiple-statements,too-many-positional-arguments,redefined-outer-name,line-too-long,disable=consider-using-enumerate
"""Tools module pertaining to stacked-barplots Python library.

tools.py contains non-member functions relating that emulate the Numpy 
cumsum() method (To keep this package lightweight, Numpy is not used). This
module also contains the ColourGradient class, which stores colour data
used by StackedBarplot. The StackedBarplot and ColourGradient classes maintain
a one-to-one relationship.

Typical usage example:
    results = {"Category 1": [10, 5, 3, 11], "Category 2": [4, 2, 9, 12], "Category 3": [11, 12, 3, 4]}
    series_labels = ["Series 1", "Series 2", "Series 3", "Series 4"]
    custom_plot = basic(results, series_labels, title="Custom Plot")

    custom_colours = ColourGradient()
    custom_colours.gradient(len(series_labels), (200, 100, 150), (100, 150, 200))
    custom_plot.set_bar_style(bar_height=.5, bar_gradient=custom_colours)

    custom_plot.render()
    custom_plot.show()
"""

import copy

def cumu1d(data:list[float]) -> list[float]:
    """Return the cumulative sum of the elements along one axis. Be aware that this 
    method may not represent floating point arithmetic precisely, having the same
    limitations as Python itself. For more information on this, see https://docs.python.org/3/tutorial/floatingpoint.html."""
    cumu_data = copy.deepcopy(data)
    for x in range(len(cumu_data)):
        if x == 0:
            continue
        cumu_data[x] = cumu_data[x] + cumu_data[x-1]
    return cumu_data

#TODO: Add documentation on why this process is necessary.
def cumu2d(data:list[list[float]]) -> list[list[float]]:
    """Iterates over y axis of 2-d list and returns the cumulative sum of the elements 
    along each one."""
    cumu_data = list(copy.deepcopy(data))
    for y in range(len(cumu_data)):
        cumu_data[y] = cumu1d(cumu_data[y])
    return cumu_data


class ColourGradient():
    """ColourGradient objects represent the colour gradients for one StackedBarplot object.
    
        Attributes:
            colour_gradient_list: List of stored RGB tuples with length matching the total
                number of series used in the StackedBarplot object.
        """

    def __init__(self):
        """Initializes the ColourGradient instance."""
        self.colour_gradient_list = []

    def get_normalised_gradient_list(self) -> list[tuple[float, float, float]]:
        """Returns stored colour gradient list matching data shape. RGB values are returned as fractions."""
        norm = [(col[0]/255.0, col[1]/255.0, col[2]/255.0) for col in self.colour_gradient_list]
        return norm

    def get_gradient_list(self) -> list[tuple[int, int, int]]:
        """Returns stored colour gradient list matching data shape.."""
        return self.colour_gradient_list
        #TODO: if it doesn't exist, throw error? Use default?

    def gradient(self,
                series_length:int,
                start_colour:tuple[int, int, int],
                end_colour:tuple[int, int, int],
                center_colour:tuple[int, int, int] = None):
        """Creates and stores a list of RGB colours in gradient matching length of 
        series
        
        Args:
            series_length: The length of the series used in the chart.
            start_colour: The intended RGB colour of the starting bar in each category.
            end_colour: The intended RGB colour of the end bar in each category.
            center_colour: The intended RGB colour of the central bar in each category.
                This argument is optional, unless the series_length is optional, when it
                is a required parameter. If defined, the created gradient will converge 
                from start_colour and end_colour on to center_colour.
        """
        if series_length < 1: raise ValueError("Argument series_length must be an integer of minimum value 1.")
        if not isinstance(start_colour, tuple) or len(start_colour) != 3:
            raise ValueError("Argument start_colour must be tuple of three integers between 0 and 255.")
        if not isinstance(end_colour, tuple) or len(end_colour) != 3:
            raise ValueError("Argument end_colour must be tuple of three integers between 0 and 255.")
        if center_colour is not None:
            if not isinstance(center_colour, tuple) or len(center_colour) != 3:
                raise ValueError("Argument center_colour must be tuple of three integers between 0 and 255.")
            if any(i > 255 or i < 0 for i in center_colour):
                raise ValueError("Argument center_colour must contain integers between 0 and 255.")
        if series_length %2 != 0 and center_colour is None:
            raise ValueError("If total number of colours is odd, a center colour must be provided")
        if any(i > 255 or i < 0 for i in start_colour):
            raise ValueError("Argument start_colour must contain integers between 0 and 255.")
        if any(i > 255 or i < 0 for i in end_colour):
            raise ValueError("Argument end_colour must contain integers between 0 and 255.")

        series_colours = []
        if center_colour is None:
            col_step = [(end-start)/(series_length-1.0) for start, end in zip(start_colour, end_colour)]
            for i in range(series_length):
                series_colours.append(tuple([int(start+col_step[j]*i) for j, start in enumerate(start_colour)]))
        else:
            col_step1 = [(center-start)/(series_length//2.0) for start, center in zip(start_colour, center_colour)]
            col_step2 = [(end-center)/(series_length//2.0) for end, center in zip(end_colour, center_colour)]
            for i in range(series_length):
                if i < series_length//2:
                    series_colours.append(tuple([int(start+col_step1[j]*i) for j, start in enumerate(start_colour)]))
                elif i == series_length//2 and series_length %2 == 1:
                    series_colours.append(center_colour)
                elif i >= series_length//2:
                    series_colours.append(tuple([int(end-col_step2[j]*((series_length-1)-i)) for j, end in enumerate(end_colour)]))
        self.colour_gradient_list = series_colours


    def grayscale_gradient(self,
                           series_length:int,
                           start_intensity:int = 0.3,
                           end_intensity:int = 0.9):
        """Creates and stores a list of RGB colours in a grayscale gradient matching 
        length of given series.
        
        Args:
            series_length: The length of the series used in the chart.
            start_intensity: The intended intensity of the starting bar in each 
                category. Value given as integer between 0 and 255. 
            end_intensity: The intended intensity of the ending bar in each category.
                Value given as integer between 0 and 255.
            """
        if series_length < 1: raise ValueError("Argument series_length must be an integer of minimum value 1.")
        if start_intensity < 0 or start_intensity > 1:
            raise ValueError("Argument start_intensity must be a float with value between 0 and 1.")
        if end_intensity < 0 or end_intensity > 1:
            raise ValueError("Argument end_intensity must be a float with value between 0 and 1.")

        col_step = (end_intensity-start_intensity)/(series_length-1.0)
        self.colour_gradient_list = [((start_intensity+col_step*i, start_intensity+col_step*i, start_intensity+col_step*i)) for i in range(series_length)]

    def set_colour_gradient_list(self, new_colour_gradient_list:list[tuple[int, int, int]]):
        """Allows the user to define a custom colour gradient list, instead of using
        a predefined gradient method.
        
        Arg: 
            new_colour_gradient_list: List of RGB tuples with values between 0 and 255. 
                Length must equal series length of corresponding StackedBarplot.             
            """
        self.colour_gradient_list = new_colour_gradient_list
