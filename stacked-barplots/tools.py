import copy


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


def colourGradient(total:int, startcolour:tuple[float, float, float], endcolour:tuple[float, float, float], centercolour:tuple[float, float, float] = (150, 150, 150)):
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
    
def greyscaleGradient(total, min:int = 0.3, max:int = 0.9):
    col_min = min
    col_max = max
    col_step = (col_max-col_min)/(total-1.0)
    return [((col_min+col_step*i, col_min+col_step*i, col_min+col_step*i)) for i in range(total)]



if __name__ == "__main__":
    x = [[1, 1], [4, 4], [2, 2], [3, 3]]
    #x = [[25, 15, 10, 8, 12], [40, 12, 8, 10, 5], [30, 18, 7, 12, 8], [45, 10, 6, 8, 4], [42, 14, 5, 10, 3], [32, 15, 10, 12, 6], [38, 14, 7, 9, 5], [35, 16, 9, 11, 4], [40, 13, 8, 9, 5], [28, 20, 9, 13, 6], [43, 11, 6, 8, 4], [45, 12, 5, 7, 3], [36, 14, 9, 10, 5], [44, 13, 5, 8, 4], [34, 17, 11, 9, 6]]
    x = sorted(x, key=lambda category: sum(category))
    print(x)