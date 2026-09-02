import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.artist import Artist
import os

from tools import *
from defaults import *


__all__ = [
    "StackedBarplot"
]


class StackedBarplot:
    def __init__(self, data:ResultsType, legendLabels:LegendLabelsType):
        self.data = list(data.values())
        self.data_cum = cumu2d(self.data)
        self.categories = legendLabels
        self.labels = list(data.keys())

        self.textbarvarartists = [] #Now redundant

        self.fig = None
        self.ax = None

        self.style = StackedPlotStyle()
        self.style.barstored["barcolours"] = greyscaleGradient(len(self.categories), 0.3, 0.9)
        self._setLegendMarkers()



    def setStyle(self, style:StackedPlotStyle):
        self.style = style
        #Bar colours must be generated after the data is provided, as the number of colours must match the number of categories
        self._setFigColours(colourGradient(len(self.categories), DEFAULT_BAR_STYLE.startcolour, DEFAULT_BAR_STYLE.endcolour, DEFAULT_BAR_STYLE.midcolour))
        self._setLegendMarkers()


    def plotbars(self):#, barheight:int = None, figsize:list[int, int] = None, align:str = None, ordered:str = None):
        self.fig, self.ax = plt.subplots(figsize=(self.style.figstored["size"][0], self.style.figstored["size"][1]))
        #plt.subplots_adjust(left=0.3)

        middle_index = len(self.data[0]) // 2

        if(self.style.figstored.get("ordered") != "unordered"):
            if(self.style.figstored.get("ordered") == "ascending"): reverse = True
            elif(self.style.figstored.get("ordered") == "descending"): reverse = False
            if(self.style.barstored.get("align") == "left"):
                self.labels, self.data = zip(*sorted(zip(self.labels, self.data), key=lambda category: sum(category[1]), reverse=reverse)) #Making sure the labels get ordered with the data
            elif(self.style.barstored.get("align") == "center"):
                if(len(self.data[0]) % 2 == 0):
                    self.labels, self.data = zip(*sorted(zip(self.labels, self.data), key=lambda category: sum(category[1][:middle_index]), reverse=reverse))
                else:
                    self.labels, self.data = zip(*sorted(zip(self.labels, self.data), key=lambda category: sum(category[1][:middle_index]) + category[1][middle_index]/2, reverse=reverse))
            self.data_cum = cumu2d(self.data)

        offsets = [0]*len(self.data)
        if(self.style.barstored.get("align") == "center"):
            offsets = []
            for(row_index, row) in enumerate(self.data):
                if(len(self.data[0]) % 2 == 0):
                    offsets.append(sum(self.data[row_index][0:middle_index]))
                else:
                    offsets.append(sum(self.data[row_index][0:middle_index]) + self.data[row_index][middle_index]/2)

        for col_index, (colname, colour) in enumerate(zip(self.categories, self.style.barstored.get("barcolours"))):
            print(col_index, colname, colour)
            widths = [bar[col_index] for bar in self.data]
            #offsets = self.data[:, range(middle_index)].sum(axis=1) + self.data[:, middle_index]/2
            starts = [bar[col_index] for bar in self.data_cum]
            for bar_index in range(len(widths)):
                if(self.style.barstored.get("align") == "left"):
                    starts[bar_index] = starts[bar_index]-widths[bar_index]
                elif(self.style.barstored.get("align") == "center"):
                    starts[bar_index] = starts[bar_index]-widths[bar_index]-offsets[bar_index]
                elif(self.style.barstored.get("align") == "right"):
                    raise NotImplementedError("Right-aligned bars not yet implemented")
                else:
                    raise ValueError("Invalid alignment value, must be 'left', 'center', or 'right'")
            rects = self.ax.barh(self.labels, 
                                 widths, 
                                 left=starts, 
                                 height=self.style.barstored.get("height"), 
                                 color = colour, 
                                 label=colname, 
                                 zorder=1)    

        for tick in self.ax.get_yticklabels():
            tick.set_fontfamily(self.style.figstored.get("fontfamily"))
        self.fig.set_facecolor(self.style.figstored.get("backgroundcolour"))
        self.ax.set_facecolor(self.style.figstored.get("backgroundcolour"))

        if(self.style.figstored.get("verline")):
            self.ax.axvline(0, linestyle="--", color="black", alpha=0.25, zorder=0)


    def drawLabels(self):
        #self.clearBarText() #The whole figure gets destroyed so this is no longer necessary
        for col_index, c in enumerate(self.ax.containers):
            bar_labels = []

            #Formatting bar value labels
            for val in c.datavalues:
                display = True
                if(self.style.barfontstored.get("fontdisplaythresh")[0] != None): #Threshold for displaying labels, if value is below or above given threshold, don't display label
                    if(val <= self.style.barfontstored.get("fontdisplaythresh")[0]): display = False
                if(self.style.barfontstored.get("fontdisplaythresh")[1] != None):
                    if(val >= self.style.barfontstored.get("fontdisplaythresh")[1]): display = False
                if(display): bar_labels.append(str.format(self.style.barfontstored.get("fontformat"), val))
                else: bar_labels.append("")

            #Positioning bar value labels
            for row_index, (rect, text) in enumerate(zip(c.patches, bar_labels)):
                ha, va = "center", "center" #Where the coords refer to on the text 
                y = rect.get_y() + rect.get_height() / 2 #Y coordinate is usually the same no matter the alignment, but this can be changed later
                x = None #X coordinate will be set based on alignment

                #Threshold for first and last bar on a row, if value is below threshold, move label to outside of bar
                topadd = False
                if(col_index == 0 and self.style.barfontstored.get("fontpaddthresh") != None and self.style.barfontstored.get("fontendthreshpadd")): #Leftmost bar label
                    if(c.datavalues[row_index] <= self.style.barfontstored.get("fontpaddthresh")):
                        topadd = True
                        ha = "right"
                        x = rect.get_x() - self.style.barfontstored.get("fontpadd")
                elif(col_index == len(self.data[0])-1 and self.style.barfontstored.get("fontpaddthresh") != None and self.style.barfontstored.get("fontendthreshpadd")): #Rightmost bar label
                    if(c.datavalues[row_index] <= self.style.barfontstored.get("fontpaddthresh")):
                        topadd = True
                        ha = "left"
                        x = rect.get_x() + rect.get_width() + self.style.barfontstored.get("fontpadd")

                if (not topadd): #Normal alignment for all other bars, or if no outside-of-bar threshold is set    
                    if(self.style.barfontstored.get("fontalign") == "center"):
                        x = rect.get_x() + rect.get_width() / 2
                    elif(self.style.barfontstored.get("fontalign") == "left"):
                        x = rect.get_x() + self.style.barfontstored.get("fontpadd")
                        ha = "left"
                    elif(self.style.barfontstored.get("fontalign") == "right"):
                        x = rect.get_x() + rect.get_width() - self.style.barfontstored.get("fontpadd")
                        ha = "right"

                #TODO
                #if(rect.get_width() <= 3): y -= ((rect.get_height() / 2) +0.07) #raising labels above the bar if the bar is too small, so that it doesn't overlap with the bar boundary

                #BUG if text is made white and shifted outside of bar, it becomes white text on white background.
                if(self.style.barfontstored.get("fontcolourinvert")):
                    luminence = 0.2126*rect.get_facecolor()[0] + 0.7152*rect.get_facecolor()[1] + 0.0722*rect.get_facecolor()[2]
                    print(luminence)
                    if(luminence < 0.4): fontcolour = "white"
                    else: fontcolour = "black"
                else: fontcolour = self.style.barfontstored.get("fontcolour")

                textartist = self.ax.annotate(
                    text,
                    (x, y), 
                    textcoords="offset points",
                    xytext=(0, 0), 
                    ha=ha, va=va, 
                    fontsize=self.style.barfontstored.get("fontsize"),
                    color=fontcolour,
                    fontfamily=self.style.figstored.get("fontfamily")
                    )
                self.textbarvarartists.append(textartist)
                
        self.ax.invert_yaxis() #Required for some reason?

    def drawAxes(self):
        if(self.style.axisstored.get("xlim") != None and self.style.axisstored.get("step") != None):
            self.ax.set_xlim(self.style.axisstored.get("xlim")[0], self.style.axisstored.get("xlim")[1])
            self.ax.set_xticks([i for i in range(self.style.axisstored.get("xlim")[0], self.style.axisstored.get("xlim")[1]+1, self.style.axisstored.get("step"))])

        self.ax.xaxis.set_major_formatter(lambda x, pos: self.style.axisstored.get("xaxisformat").format(x))

        self.ax.tick_params(axis='x', labelsize=int(self.style.axisstored.get("xfontsize")), labelfontfamily=self.style.figstored.get("fontfamily"))
        self.ax.tick_params(axis='y', labelsize=int(self.style.axisstored.get("yfontsize")), labelfontfamily=self.style.figstored.get("fontfamily"))

        if not self.style.figstored.get("spinedisplay")[0]: self.ax.spines['left'].set_visible(False)
        if not self.style.figstored.get("spinedisplay")[1]: self.ax.spines['top'].set_visible(False)
        if not self.style.figstored.get("spinedisplay")[2]: self.ax.spines['right'].set_visible(False)
        if not self.style.figstored.get("spinedisplay")[3]: self.ax.spines['bottom'].set_visible(False)

        if(self.style.figstored.get("title") != None):
            self.ax.set_title(self.style.figstored.get("title"), 
                              fontsize=self.style.figstored.get("titlefontsize"), 
                              color=self.style.figstored.get("titlecolour"), 
                              fontfamily=self.style.figstored.get("fontfamily"))
        if(self.style.axistitlestored.get("xlabel") != None):
            self.ax.set_xlabel(self.style.axistitlestored.get("xlabel"), 
                               fontsize=self.style.axistitlestored.get("axislabelfontsize"), 
                               color=self.style.axistitlestored.get("axislabelfontcolour"), 
                               fontfamily=self.style.figstored.get("fontfamily"))
        if(self.style.axistitlestored.get("ylabel") != None):
            self.ax.set_ylabel(self.style.axistitlestored.get("ylabel"), 
                               fontsize=self.style.axistitlestored.get("axislabelfontsize"), 
                               color=self.style.axistitlestored.get("axislabelfontcolour"), 
                               fontfamily=self.style.figstored.get("fontfamily"))

    def plotlegend(self):
        if("horizontal" in self.style.legendstored.get("placement")): ncol = len(self.categories)
        else: ncol = 1

        bbox_to_anchor = list(DEFAULT_LEGEND_STYLE.placementoptions[self.style.legendstored.get("placement")][1])
        bbox_to_anchor[0] += self.style.legendstored.get("transform")[0]
        bbox_to_anchor[1] += self.style.legendstored.get("transform")[1]

        print(self.style.legendstored.get("bordercolour"))
 
        leg = self.ax.legend(handles=self.style.legendstored["markers"],
                       ncol=ncol, 
                       bbox_to_anchor=bbox_to_anchor,
                       loc=DEFAULT_LEGEND_STYLE.placementoptions[self.style.legendstored.get("placement")][0],
                       fontsize=self.style.legendstored.get("fontsize"), 
                       labelspacing = self.style.legendstored.get("spacing"),
                       labelcolor=self.style.legendstored.get("fontcolour"),
                       facecolor=self.style.legendstored.get("backgroundcolour"),
                       edgecolor = self.style.legendstored.get("bordercolour"),
                       framealpha=1,
                       shadow=False
        )


        

    def _render(self):
        self.plotbars()
        self.drawLabels()
        self.drawAxes()
        if(self.style.legendstored.get("show")): self.plotlegend()
        if(self.style.vertlinestored.get("show")): self.plotvertline()
        
        self.fig.tight_layout()



    def setBarLabelStyle(self, 
                fontsize:int=None, 
                fontcolour:str = None,
                fontcolourinvert:bool = False,
                barvalueformat:str = None, 
                displaythresh:tuple[float, float] = (None, None), 
                paddthresh:float = None, 
                endthreshpadd:bool = None,
                align:str=None,
                padding:float = None):
        if fontsize != None: self.style.barfontstored["fontsize"] = fontsize
        if fontcolour != None: self.style.barfontstored["fontcolour"] = fontcolour
        if fontcolourinvert != None: self.style.barfontstored["fontcolourinvert"] = fontcolourinvert
        if barvalueformat != None: self.style.barfontstored["fontformat"] = barvalueformat
        if displaythresh != None: self.style.barfontstored["fontdisplaythresh"] = displaythresh
        if paddthresh != None: self.style.barfontstored["fontpaddthresh"] = paddthresh
        if endthreshpadd != None: self.style.barfontstored["fontendthreshpadd"] = endthreshpadd
        if align != None: self.style.barfontstored["fontalign"] = align
        if padding != None: self.style.barfontstored["fontpadd"] = padding

    def setBarStyle(self, 
                    barheight:int = None, 
                    align:str = None, 
                    ordered:str = None,
                    barcolours:ColourType = None
                    ):
        if barheight != None: self.style.barstored["barheight"] = barheight
        if align != None: self.style.barstored["align"] = align
        if ordered != None: self.style.figstored["ordered"] = ordered
        if barcolours != None: #There should be some error checking that there are enough colours (i.e., matching shape of data.)
            self._setFigColours(barcolours)

    def setAxisTitleStyle(self, 
                          xlabel:str = None, 
                          ylabel:str = None, 
                          axislabelfontsize:int = None, 
                          axislabelfontcolour:str = None):
        if xlabel != None: self.style.axistitlestored["xlabel"] = xlabel
        if ylabel != None: self.style.axistitlestored["ylabel"] = ylabel
        if axislabelfontsize != None: self.style.axistitlestored["axislabelfontsize"] = axislabelfontsize
        if axislabelfontcolour != None: self.style.axistitlestored["axislabelfontcolour"] = axislabelfontcolour

    def setFigStyle(self,
                    title:str = None,
                    titlefontsize:int = None,
                    titlecolour:str = None,
                    fontfamily:str = None,
                    figsize:list[int, int] = None
                    ):
        if title != None: self.style.figstored["title"] = title
        if titlefontsize != None: self.style.figstored["titlefontsize"] = titlefontsize
        if titlecolour != None: self.style.figstored["titlecolour"] = titlecolour
        if fontfamily != None: self.style.figstored["fontfamily"] = fontfamily
        if figsize != None: self.style.figstored["size"] = figsize


    def setVertLineStyle(self,
                    show:bool = None,
                    linestyle:str = None,
                    colour:str = None,
                    alpha:float = None):
        if show != None: self.style.vertlinestored["show"] = show
        if linestyle != None: self.style.vertlinestored["linestyle"] = linestyle
        if colour != None: self.style.vertlinestored["colour"] = colour
        if alpha != None: self.style.vertlinestored["alpha"] = alpha



    def setLegendStyle(self, 
                       show:bool = None,
                       fontsize:int = None, 
                       location:str = None, 
                       spacing:float = None,
                       fontcolour:str = None,
                       backgroundcolour:str = None,
                       bordercolour:str = None,
                       placement:str = None,
                       markershape:str = None,
                       transform:list[int] = None                
                       ):
        if show != None: self.style.legendstored["show"] = show
        if fontsize != None: self.style.legendstored["fontsize"] = fontsize
        if location != None: self.style.legendstored["location"] = location
        if spacing != None: self.style.legendstored["spacing"] = spacing
        if fontcolour != None: self.style.legendstored["fontcolour"] = fontcolour
        if backgroundcolour != None: self.style.legendstored["backgroundcolour"] = backgroundcolour
        if bordercolour != None: self.style.legendstored["bordercolour"] = bordercolour
        if placement != None: self.style.legendstored["placement"] = placement
        if markershape != None: 
            self.style.legendstored["markershape"] = markershape
            self._setLegendMarkers()
        if transform != None: self.style.legendstored["transform"] = transform



    def setAxisStyle(self, xlim:tuple[int, int] = None, step:int = None, xfontsize:int = None, yfontsize:int = None, xaxisformat:str = None):
        if xlim != None: self.style.axisstored["xlim"] = xlim
        if step != None: self.style.axisstored["step"] = step
        if xfontsize != None: self.style.axisstored["xfontsize"] = xfontsize
        if yfontsize != None: self.style.axisstored["yfontsize"] = yfontsize
        if xaxisformat != None: self.style.axisstored["xaxisformat"] = xaxisformat
        

        
    def plotvertline(self):
        if(len(self.categories) %2 == 0): z = 2
        else: z = 0
        self.ax.axvline(0, 
                        linestyle=self.style.vertlinestored.get("linestyle"), 
                        color=self.style.vertlinestored.get("colour"), 
                        alpha=self.style.vertlinestored.get("alpha"), 
                        zorder=z)


    def render(self):
        self._destroyFig()
        self._render()

    def show(self):
        plt.show()

    def _destroyFig(self):
        if(self.fig != None):
            if(len(self.textbarvarartists) != 0): self.clearBarText()
            self._destroyAxes()
            self.fig.clear()
            plt.close(self.fig)
    
    
    def save(self, filename:str, transparent:bool=None, dpi='figure', bbox_inches='tight', pad_inches=0.1, format:str="png"):
        path = os.path.dirname(os.path.abspath(__file__))
        self.fig.savefig(os.path.join(path, filename), transparent=transparent, dpi=dpi, bbox_inches=bbox_inches, pad_inches=pad_inches, format=format)


    #_initFigColours()?
    def _setFigColours(self, colours:list[tuple[int, int, int]]):
        self.style.barstored["barcolours"]  = [(col[0]/255.0, col[1]/255.0, col[2]/255.0) for col in colours]

    #_initLegendMarkers()?
    def _setLegendMarkers(self):
        self.style.legendstored["markers"] = []
        for i, cat in enumerate(self.categories):
            self.style.legendstored["markers"].append(mlines.Line2D([], 
                                                                    [], 
                                                                    color=self.style.barstored.get("barcolours")[i], 
                                                                    marker=self.style.legendstored.get("markershape"), 
                                                                    linestyle='None', 
                                                                    markersize=10, 
                                                                    label=cat
                                                                    ))
            

    def clearBarText(self):
        for i in range(len(self.textbarvarartists)):
            Artist.remove(self.textbarvarartists[i])
            #del self.textbarvarartists[i]
        self.fig.canvas.draw()
        self.textbarvarartists = []

    
