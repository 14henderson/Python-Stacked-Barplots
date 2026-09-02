import matplotlib.pyplot as plt

from core import StackedBarplot, DEFAULT_BAR_FONT, DEFAULT_BAR_STYLE, DEFAULT_LEGEND_STYLE, DEFAULT_FIG_STYLE, DEFAULT_VERTLINE_STYLE, StackedPlotStyle
from tools import *



def basic(
        data:ResultsType, 
        legendLabels:LegendLabelsType,
        title:str = None,
        figsize:list[int, int] = [10, 5],
        fontsize:int = DEFAULT_BAR_FONT.size,
        fontcolour:str = DEFAULT_BAR_FONT.colour,
        barvalueformat:str = DEFAULT_BAR_FONT.format,
        barvaluealign:str = DEFAULT_BAR_FONT.align,
        barcolours:list[tuple[float, float, float]] = None,
        legendloc:str = None,
        xaxislim:tuple[int, int] = None,
        xaxisstep:int = None,
        barheight:float = 0.8
        ):

    stackedBarStyle = StackedPlotStyle()
    stackedBarStyle.figstored["title"] = title
    stackedBarStyle.barfontstored["fontsize"] = fontsize
    stackedBarStyle.barfontstored["fontcolour"] = fontcolour
    stackedBarStyle.barfontstored["fontformat"] = barvalueformat
    stackedBarStyle.barfontstored["fontalign"] = barvaluealign
    stackedBarStyle.barfontstored["endthreshpadd"] = True
    stackedBarStyle.barfontstored["paddthresh"] = 4

    if(xaxislim != None): stackedBarStyle.axisstored["xlim"] = xaxislim
    if(xaxisstep != None): stackedBarStyle.axisstored["step"] = xaxisstep
    if(barcolours != None): stackedBarStyle.barstored["barcolours"] = barcolours
    if(legendloc != None): stackedBarStyle.legendstored["location"] = legendloc

    stackedBarStyle.legendstored["fontsize"] = fontsize
    stackedBarStyle.figstored["size"] = figsize
    stackedBarStyle.barstored["align"] = "left"
    stackedBarStyle.barstored["barheight"] = barheight
    stackedBarStyle.figstored["spinedisplay"] = (False, False, False, True)

    plot = StackedBarplot(data, legendLabels)
    plot.setStyle(stackedBarStyle)

    return plot

def centered(
        data:ResultsType, 
        legendLabels:LegendLabelsType,
        title:str = None,
        figsize:list[int, int] = [10, 5],
        fontsize:int = DEFAULT_BAR_FONT.size,
        fontcolour:str = DEFAULT_BAR_FONT.colour,
        barvalueformat:str = DEFAULT_BAR_FONT.format,
        barvaluealign:str = DEFAULT_BAR_FONT.align,
        barcolours:list[tuple[float, float, float]] = None,
        legendloc:str = None,
        xaxislim:tuple[int, int] = None,
        xaxisstep:int = None,
        barheight:float = 0.8
        ):
    
    stackedBarStyle = StackedPlotStyle()
    stackedBarStyle.figstored["title"] = title
    stackedBarStyle.barfontstored["fontsize"] = fontsize
    stackedBarStyle.barfontstored["fontcolour"] = fontcolour
    stackedBarStyle.barfontstored["fontformat"] = barvalueformat
    stackedBarStyle.barfontstored["fontalign"] = barvaluealign
    stackedBarStyle.barfontstored["endthreshpadd"] = True
    stackedBarStyle.barfontstored["paddthresh"] = 4

    if(xaxislim != None): stackedBarStyle.axisstored["xlim"] = xaxislim
    if(xaxisstep != None): stackedBarStyle.axisstored["step"] = xaxisstep
    if(barcolours != None): stackedBarStyle.barstored["barcolours"] = barcolours
    if(legendloc != None): stackedBarStyle.legendstored["location"] = legendloc

    stackedBarStyle.legendstored["fontsize"] = fontsize
    stackedBarStyle.figstored["size"] = figsize
    stackedBarStyle.barstored["align"] = "center"
    stackedBarStyle.barstored["barheight"] = barheight
    stackedBarStyle.vertlinestored["show"] = True
    stackedBarStyle.figstored["spinedisplay"] = (False, False, False, True)

    plot = StackedBarplot(data, legendLabels)
    plot.setStyle(stackedBarStyle)

    return plot

#Not yet implemented
def normalised():
    pass

#Not yet implemented
def normcentered():
    pass

if __name__ == "__main__":
    results = {'Pre-test (T1)': [22.27118644067797, 22.88135593220339, 16.101694915254235, 18.64406779661017, 2.16949152542373, 5.084745762711865, 0.847457627118644], 'Immediate post-test (T2)': [21.367521367521366, 28.205128205128204, 15.11111111111111, 15.384615384615385, 12.94871794871795, 1.128205128205128, 0.8547008547008548], 'Longitudinal post-test (T3)': [2.22222222222222, 26.666666666666668, 17.77777777777778, 16.666666666666664, 6.666666666666667, 10.0, 0.0], 'Original Control\n(Roozenbeek & van der Linden, 2019)': [10.526315789473683, 21.052631578947366, 10.789473684210526, 21.052631578947366, 15.789473684210526, 13.157894736842104, 2.631578947368421], 'Original Post-Test\n(Roozenbeek & van der Linden, 2019)': [16.666666666666664, 2.074074074074073, 18.51851851851852, 20.37037037037037, 18.51851851851852, 1.8518518518518516, 0.0]}
    reliability_category_names = ['Completely\nunreliable', 'Mostly\nunreliable', 'Somewhat\nunreliable', 'Neither reliable\nnor unreliable', 'Somewhat\nreliable', 'Mostly\nreliable', 'Completely\nreliable']


    
    plot = centered(results, reliability_category_names)
    plot.setBarStyle(barcolours=colourGradient(len(reliability_category_names), (100, 200, 10), (50, 100, 150), (150, 75, 80)))
    plot.setLegendStyle(show=True, fontsize=8, spacing=1, markershape='o', backgroundcolour="white", bordercolour="white")

    plot.render()
    plot.show()
