class GridPoints(object):
    def __init__(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey

        self.minx = sizex / 3
        self.maxx = (2*sizex) / 3
        self.miny = sizey / 3
        self.maxy = (2*sizey) / 3

'''
    def minx_line(self):
        return ((self.minx, 0), (self.minx, self.sizey))

    def maxx_line(self):
        return ((self.maxx, 0), (self.maxx, self.sizey))

    def miny_line(self):
        return ((0, self.miny), (self.sizex, self.miny))

    def maxy_line(self):
        return ((0, self.maxy), (self.sizex, self.maxy))
'''