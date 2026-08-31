from cmath import rect

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import copy
#import seaborn as sns

import numpy as np

#Things to add
#Category labels in legend or annotated over graph
#mixed height and width
#Mixed orientation
#Data cleaning


# DONE stretch/scale bars into speciic width, or center around mid
# DONE Data values on bars or not
    # DONE data value colour inverse for dark coloured bars
    # DONE Left-align, mid-align, or right-align
    # DONEformatting (rounding, % sign, etc.)
    # DONE Hide data values on overlap

#DONE different bar colours (also greyscale)
#DONE Mid line style

#Different axis scales
#normalise into percentages
#Aligning bars on bar number
    #Ordering bars based on left/right total
#Category
#More explicit stats on bars (see https://www.datarevelations.com/rethinkingdivergent/)


#Types of bar graph
    #Basic
    #Vertical
    #Normalised

#Bar basics
    #auto ticks
    #bars left aligned

#Many functions for different types of stacked bar chart, one class that can do everything
#Each function should do all the basic stuff, but also return a StackedBarplot obj which can be further customised

def cumu1d(data:list[float]):
    cumu_data = copy.deepcopy(data)
    for x in range(len(cumu_data)):
        if(x == 0): continue
        else: cumu_data[x] = cumu_data[x] + cumu_data[x-1]
    return cumu_data
    
def cumu2d(data:list[list[float]]):
    cumu_data = copy.deepcopy(data)
    for y in range(len(cumu_data)):
        for x in range(len(cumu_data[y])):
            if(x == 0): continue
            else: cumu_data[y][x] = cumu_data[y][x] + cumu_data[y][x-1]
    return cumu_data




type ResultsType = dict[str, list[float]]
type LegendLabelsType = list[str]

class StackedBarplot:
    def __init__(self, data:ResultsType, legendLabels:LegendLabelsType):
        self.data = list(data.values())
        self.data_cum = cumu2d(self.data)
        self.categories = legendLabels
        self.labels = list(data.keys())

        self.vert_line = False
        self.bar_colours = []

        self.fig = None
        self.ax = None
        
        
    def plotlabels(
            self, 
            fontsize:int=12, 
            fontcolour:str = "black",
            fontcolourinvert:bool = False,
            barvalueformat:str = "{0}", 
            displaythresh:tuple[float, float] = (None, None), 
            paddthresh:float = None, 
            endthreshpadd:bool = False,
            align:str="center",
            padding:float = 0.1
            ):
        for col_index, c in enumerate(self.ax.containers):
            bar_labels = []

            #Formatting bar value labels
            for val in c.datavalues:
                display = True
                if(displaythresh[0] != None): #Threshold for displaying labels, if value is below or above given threshold, don't display label
                    if(val < displaythresh[0]): display = False
                if(displaythresh[1] != None):
                    if(val > displaythresh[1]): display = False
                if(display): bar_labels.append(str.format(barvalueformat, val))
                else: bar_labels.append("")

            #Positioning bar value labels
            for row_index, (rect, text) in enumerate(zip(c.patches, bar_labels)):
                ha, va = "center", "center" #Where the coords refer to on the text 
                y = rect.get_y() + rect.get_height() / 2 #Y coordinate is usually the same no matter the alignment, but this can be changed later
                x = None #X coordinate will be set based on alignment

                #Threshold for first and last bar on a row, if value is below threshold, move label to outside of bar
                topadd = False
                if(col_index == 0 and paddthresh != None and endthreshpadd): #Leftmost bar label
                    if(c.datavalues[row_index] < paddthresh):
                        topadd = True
                        ha = "right"
                        x = rect.get_x() - padding
                elif(col_index == len(self.data[0])-1 and paddthresh != None and endthreshpadd): #Rightmost bar label
                    if(c.datavalues[row_index] < paddthresh):
                        topadd = True
                        ha = "left"
                        x = rect.get_x() + rect.get_width() + padding

                if (not topadd): #Normal alignment for all other bars, or if no outside-of-bar threshold is set    
                    if(align == "center"):
                        x = rect.get_x() + rect.get_width() / 2
                    elif(align == "left"):
                        x = rect.get_x() + padding
                        ha = "left"
                    elif(align == "right"):
                        x = rect.get_x() + rect.get_width() - padding
                        ha = "right"

                #TODO
                #if(rect.get_width() <= 3): y -= ((rect.get_height() / 2) +0.07) #raising labels above the bar if the bar is too small, so that it doesn't overlap with the bar boundary

                #BUG if text is made white and shifted outside of bar, it becomes white text on white background.
                if(fontcolourinvert):
                    luminence = 0.2126*rect.get_facecolor()[0] + 0.7152*rect.get_facecolor()[1] + 0.0722*rect.get_facecolor()[2]
                    print(luminence)
                    if(luminence < 0.4): fontcolour = "white"
                    else: fontcolour = "black"

                self.ax.annotate(
                    text,
                    (x, y), 
                    textcoords="offset points",
                    xytext=(0, 0), 
                    ha=ha, va=va, 
                    fontsize=fontsize,
                    color=fontcolour
                    )
                
        self.ax.invert_yaxis() #Required for some reason?
        
        
    def plotlegend(self, fontsize:int=12, location:str = "lower left"):
        # Ledgend
        self.ax.legend(ncol=len(self.labels), bbox_to_anchor=(0, 1), loc=location, fontsize=fontsize)


    def xTicks(self, xlim:tuple[int, int], step:int, xfontsize:int=12, xaxisformat:str = "{0}"):
        self.ax.set_xlim(xlim[0], xlim[1])
        self.ax.set_xticks(np.arange(xlim[0], xlim[1]+1, step))
        self.ax.xaxis.set_major_formatter(lambda x, pos: xaxisformat.format(x))
        self.ax.tick_params(axis='x', labelsize=int(xfontsize))


    def yTicks(self, yfontsize:int=12):
        self.ax.tick_params(axis='y', labelsize=int(yfontsize))


    def figStyle(self, spine=(False, False, False, True)):
        # Remove spines
        if not spine[0]: self.ax.spines['left'].set_visible(False)
        if not spine[1]: self.ax.spines['top'].set_visible(False)
        if not spine[2]: self.ax.spines['right'].set_visible(False)
        if not spine[3]: self.ax.spines['bottom'].set_visible(False)


    def createColourGradient(self, total:int, startcolour:tuple[float, float, float], endcolour:tuple[float, float, float], centercolour:tuple[float, float, float] = (150, 150, 150)):
        if(total %2 != 0 and centercolour == None):
            raise ValueError("If total number of colours is odd, a center colour must be provided")
        
        colours = []
        if(centercolour == None):
            col_step = [(end-start)/(total-1.0) for start, end in zip(startcolour, endcolour)]
            for i in range(total):
                colours.append(tuple([start+col_step[j]*i for j, start in enumerate(startcolour)]))
        else:
            col_step1 = [(center-start)/(total//2.0) for start, center in zip(startcolour, centercolour)]
            col_step2 = [(end-center)/(total//2.0) for end, center in zip(endcolour, centercolour)]
            for i in range(total):
                if(i < total//2):
                    colours.append(tuple([start+col_step1[j]*i for j, start in enumerate(startcolour)]))
                else:
                    colours.append(tuple([center+col_step2[j]*(i-(total//2)) for j, center in enumerate(centercolour)]))
        return colours
        
    def createColours(self, total):
        colours = []
        col_min = 0.3
        col_max = 0.9
        col_step = (col_max-col_min)/(total-1.0)
        for i in range(total):
            colours.append((col_min+col_step*i, col_min+col_step*i, col_min+col_step*i))
        return colours

    def toggleVertLine(self, linestyle:str = "--", colour:str = "black", alpha:float = 0.25):
        if(self.vert_line == False):
            self.vert_line = True
            self.ax.axvline(0, linestyle=linestyle, color=colour, alpha=alpha)
        else:
            self.vert_line = False
            self.ax.lines.remove(self.ax.lines[-1]) #Remove last line added to axis

    def show(self):
        if self.fig == None or self.ax == None:
            raise RuntimeError(".plot() must be called to create Figure and Axis objects")
        plt.show()
        #self.fig.clear()
        plt.close('all')


    def save(self, filename:str):
        pass
    def setFigSize(self, size:tuple[float, float]):
        pass

    def setFigColours(self, colours:list[tuple[float, float, float]]):
        self.bar_colours = colours

    def plotbars(self, barheight:float = 0.8, figsize:list[int, int] = [10, 5], align="left"):
        self.fig, self.ax = plt.subplots(figsize=(figsize[0], figsize[1]))
        if(self.bar_colours == []):
            colours = self.createColours(len(self.data[0]))
            self.bar_colours = colours
        else:
            colours = self.bar_colours

        middle_index = len(self.data[0]) // 2
        offsets = [0]*len(self.data)
        if(align == "center"):
            offsets = []
            for(row_index, row) in enumerate(self.data):
                if(len(self.data[0]) % 2 == 0):
                    offsets.append(sum(self.data[row_index][0:middle_index]))
                else:
                    offsets.append(sum(self.data[row_index][0:middle_index]) + self.data[row_index][middle_index]/2)

        for col_index, (colname, colour) in enumerate(zip(self.categories, colours)):
            print(col_index, colname, colour)
            widths = [bar[col_index] for bar in self.data]

            
        
            #offsets = self.data[:, range(middle_index)].sum(axis=1) + self.data[:, middle_index]/2
            starts = [bar[col_index] for bar in self.data_cum]
            for bar_index in range(len(widths)):
                if(align == "left"):
                    starts[bar_index] = starts[bar_index]-widths[bar_index]
                elif(align == "center"):
                    starts[bar_index] = starts[bar_index]-widths[bar_index]-offsets[bar_index]
                elif(align == "right"):
                    raise NotImplementedError("Right-aligned bars not yet implemented")
                else:
                    raise ValueError("Invalid alignment value, must be 'left', 'center', or 'right'")
            #starts = data_cum_np[:, i] - widths# - offsets
            #colours = self.createColours(len(self.data[0]))
            #print(colours)
          #  widths = tmpnp[:, i]
          #  starts = data_cum_np[:, i] - widths# - offsets

            
            
            rects = self.ax.barh(self.labels, widths, left=starts, height=barheight, color = colour, label=colname, zorder=1)    
        self.fig.set_facecolor('#FFFFFF')




cats = ["A lot", "A bit", "Neither", "Not much", "Not at all"]

#results = {
#    'One': [5, 5, 9, 1],
#    'Two': [2, 8, 5, 5],
#    'Three': [5, 5, 1, 9]
#}

results = {
    'Student': [25, 15, 10, 8, 12],
    'Software Developer': [40, 12, 8, 10, 5],
    'Teacher': [30, 18, 7, 12, 8],
    'Doctor': [45, 10, 6, 8, 4],
    'Nurse': [42, 14, 5, 10, 3],
    'Graphic Designer': [32, 15, 10, 12, 6],
    'Accountant': [38, 14, 7, 9, 5],
    'Marketing Manager': [35, 16, 9, 11, 4],
    'Engineer': [40, 13, 8, 9, 5],
    'Journalist': [28, 20, 9, 13, 6],
    'Lawyer': [43, 11, 6, 8, 4],
    'Chef': [45, 12, 5, 7, 3],
    'Architect': [36, 14, 9, 10, 5],
    'Police Officer': [44, 13, 5, 8, 4],
    'Researcher': [34, 17, 11, 9, 6]
}

#results = {lab: [(cum/sum(data))*100 for cum in data] for lab, data in results.items()}  #Changes cumulative values to percent


plot = StackedBarplot(results, cats)
#plot.setFigColours(plot.createColourGradient(len(cats), (0.9, 0.4, 0.4), (0.4, 0.4, 0.9), (0.8, 0.8, 0.8)))
#plot.plotbars(barheight=.9, figsize=[15, 7], align="left")
plot.plotbars()
plot.plotlabels()
#plot.plotlabels(fontsize=10, barvalueformat="{0}%", align="center", endthreshpadd = True, paddthresh=4, fontcolourinvert=True, displaythresh=(2, None))
#plot.plotlegend()
#plot.xTicks((-60, 30), 10, xaxisformat="{0}%")
#plot.xTicks((0, 100), 10, xaxisformat="{0}%")
plot.yTicks()
plot.figStyle((False, False, False, True))
#plot.toggleVertLine()
plot.show()