type ResultsType = dict[str, list[float]]
type LegendLabelsType = list[str]
type ColourType = list[tuple[int, int, int]]


class DEFAULT_BAR_FONT:
    size = 12
    colour = "black"
    format = "{0:.1f}"
    align = "center"
    padding = 1.5
    displaythresh = (0, None)
    colourinvert = False
    paddingthresh = 0 #The threshold for if a label should be moved
    endthreshpadd = False

class DEFAULT_BAR_STYLE:
    align = "left"
    height = 0.8
    startcolour = (227, 108, 85)
    endcolour = (106, 139, 239)
    midcolour = (220, 221, 221)
    
class DEFAULT_FIG_STYLE:
    size = None
    title = None
    titlefontsize = 12
    titlecolour = "black"
    fontfamily = "sans-serif"
    backgroundcolour = "#ffffff"
    ordered = "unordered"
    spinedisplay = (False, False, False, True) #left, top, right, bottom

class DEFAULT_AXIS_STYLE:
    xlim = None
    step = None
    xfontsize = 12
    yfontsize = 12
    xaxisformat = "{0}"
    
class DEFAULT_AXIS_TITLE_STYLE:
    xlabel = None
    ylabel = None
    axislabelfontsize = 12
    axislabelfontcolour = "black"

class DEFAULT_LEGEND_STYLE:
    show = False
    fontsize = 12
    labelspacing = 0.5
    location = "upper left" #Which corner of the legend box is the anchor
    fontcolour = "black"
    markershape = "s" #see for different marker shapes https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html
    bordercolour = "#ededed"
    backgroundcolour = "#ededed"
    placement = "right-vertical"
    placementoptions = { 
        "right-vertical": ["upper left", (1.12, 1)],
        "left-vertical": ["upper right", (-0.12, 1)],
        "below-horizontal": ["upper center", (0.5, -0.12)],
        "above-horizontal": ["lower center", (0.5, 1.02)]
    }
    placementtransform = [0, 0]

class DEFAULT_VERTLINE_STYLE:
    show = False
    linestyle = "-"
    colour = "black"
    alpha = 1


class StackedPlotStyle:
    def __init__(self):
        self.barfontstored = {
            "fontsize": DEFAULT_BAR_FONT.size,
            "fontcolour": DEFAULT_BAR_FONT.colour,
            "fontformat": DEFAULT_BAR_FONT.format,
            "fontalign": DEFAULT_BAR_FONT.align,
            "fontpadd": DEFAULT_BAR_FONT.padding,
            "fontcolourinvert": DEFAULT_BAR_FONT.colourinvert,
            "fontdisplaythresh": DEFAULT_BAR_FONT.displaythresh,
            "fontpaddthresh": DEFAULT_BAR_FONT.paddingthresh,
            "fontendthreshpadd": DEFAULT_BAR_FONT.endthreshpadd
        }

        self.barstored = {
            "height": DEFAULT_BAR_STYLE.height,
            "align": DEFAULT_BAR_STYLE.align,
            "barcolours": [], #Requires data to create correct length gradient
            "startcolour": DEFAULT_BAR_STYLE.startcolour,
            "endcolour": DEFAULT_BAR_STYLE.endcolour,
            "midcolour": DEFAULT_BAR_STYLE.midcolour
        }

        self.legendstored = {
            "show": DEFAULT_LEGEND_STYLE.show,
            "fontsize": DEFAULT_LEGEND_STYLE.fontsize,
            "location": DEFAULT_LEGEND_STYLE.location,
            "spacing": DEFAULT_LEGEND_STYLE.labelspacing,
            "fontcolour": DEFAULT_LEGEND_STYLE.fontcolour,
            "backgroundcolour": DEFAULT_LEGEND_STYLE.backgroundcolour,
            "bordercolour": DEFAULT_LEGEND_STYLE.bordercolour,
            "placement": DEFAULT_LEGEND_STYLE.placement,
            "markershape": DEFAULT_LEGEND_STYLE.markershape,
            "markers": [],
            "transform": DEFAULT_LEGEND_STYLE.placementtransform
        }

        self.figstored = {
            "title": DEFAULT_FIG_STYLE.title,
            "titlefontsize": DEFAULT_FIG_STYLE.titlefontsize,
            "titlecolour": DEFAULT_FIG_STYLE.titlecolour,
            "fontfamily": DEFAULT_FIG_STYLE.fontfamily,
            "size": DEFAULT_FIG_STYLE.size,
            "backgroundcolour": DEFAULT_FIG_STYLE.backgroundcolour,
            "ordered": DEFAULT_FIG_STYLE.ordered,
            "spinedisplay": DEFAULT_FIG_STYLE.spinedisplay
        }

        self.axistitlestored = {
            "xlabel": DEFAULT_AXIS_TITLE_STYLE.xlabel,
            "ylabel": DEFAULT_AXIS_TITLE_STYLE.ylabel,
            "axislabelfontsize": DEFAULT_AXIS_TITLE_STYLE.axislabelfontsize,
            "axislabelfontcolour": DEFAULT_AXIS_TITLE_STYLE.axislabelfontcolour
        }

        self.vertlinestored = {
            "show": DEFAULT_VERTLINE_STYLE.show,
            "linestyle": DEFAULT_VERTLINE_STYLE.linestyle,
            "colour": DEFAULT_VERTLINE_STYLE.colour,
            "alpha": DEFAULT_VERTLINE_STYLE.alpha
        }

        self.axisstored = {
            "xlim": DEFAULT_AXIS_STYLE.xlim,
            "step": DEFAULT_AXIS_STYLE.step,
            "xfontsize": DEFAULT_AXIS_STYLE.xfontsize,
            "yfontsize": DEFAULT_AXIS_STYLE.yfontsize,
            "xaxisformat": DEFAULT_AXIS_STYLE.xaxisformat,
        }
