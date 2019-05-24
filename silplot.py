#!/usr/bin/python3

###################################################################
#    File name     : silplot.py
#    Author        : sha-ou
#    Date          : Thu 16 May 2019 13:21:23 CST
#    Description   :
###################################################################

import pandas as pd
import matplotlib.pyplot as plt


class ScaleClass():
    def __init__(self, scale):
        self.__valide = ['linear', 'log']
        self.__scale = None
        self.set(scale)

    def get(self):
        return self.__scale

    def set(self, scale):
        if str(scale) in self.__valide:
            self.__scale = str(scale)
        else:
            raise ValueError(str(self.__valide))


class FigureClass():
    def __init__(self, df):
        self.__df = df
        self.__rectangle = [0.15, 0.15, 0.8, 0.75]
        self.__xscale = ScaleClass('linear')
        self.__yscale = ScaleClass('linear')
        self.__xlabel = 'x'
        self.__ylabel = 'y'
        self.__title = 'title'
        self.__labelsize = 15
        self.__titlesize = 15
        self.__x = 'x'
        self.__y = 'y'
        self.__t = 't'
        self.__fname = 'figure.tiff'
        self.__fig = plt.figure()
        self.__axes = None
        self.__labelfunc = None

    def plotlines(self, t=None):
        if t is not None:
            self.t = t
        self.initfig()
        ts = self.df[self.t].drop_duplicates().sort_values()
        for t in ts:
            label = self.getlabel(t)
            mask = (self.df[self.t] == t)
            plotdf = self.df[mask].loc[:, [self.x, self.y]]
            plotdf = plotdf.sort_values(by=self.x)
            x = plotdf[self.x]
            y = plotdf[self.y]
            self.__axes.plot(x, y, 's--', label=label)
        self.__axes.legend()
        self.__fig.savefig(self.fname)
        return self.__fig

    def plotline(self):
        self.initfig()
        plotdf = self.df.loc[:, [self.x, self.y]].sort_values(by=self.x)
        x = plotdf[self.x]
        y = plotdf[self.y]
        self.__axes.plot(x, y, 's--')
        self.__fig.savefig(self.fname)
        return self.__fig

    def initfig(self):
        self.__axes = None
        self.__fig.clear()
        self.__axes = self.__fig.add_axes(self.rectangle)
        self.__axes.set_xlabel(self.xlabel, fontsize=self.labelsize)
        self.__axes.set_ylabel(self.ylabel, fontsize=self.labelsize)
        self.__axes.set_xscale(self.xscale)
        self.__axes.set_yscale(self.yscale)
        self.__axes.set_title(self.title, fontsize=self.titlesize)

    def getlabel(self, t):
        if self.labelfunc is None:
            return '$' + str(t) + '$'
        else:
            return self.labelfunc(t)

    @property
    def labelsize(self):
        return self.__labelsize

    @labelsize.setter
    def labelsize(self, size):
        self.__labelsize = int(size)

    @property
    def titlesize(self):
        return self.__titlesize

    @titlesize.setter
    def titlesize(self, size):
        self.__titlesize = int(size)

    @property
    def fig(self):
        return self.__fig

    @property
    def rectangle(self):
        return self.__rectangle

    @rectangle.setter
    def rectangle(self, rect):
        if isinstance(rect, list or tuple) and len(rect) == 4:
            self.__rectangle = list(rect)
        else:
            raise ValueError('rect should be list or tuple')

    @property
    def labelfunc(self):
        return self.__labelfunc

    @labelfunc.setter
    def labelfunc(self, labelfunc):
        if callable(labelfunc):
            self.__labelfunc = labelfunc
        else:
            raise ValueError('%s is not callable' % str(labelfunc))

    @property
    def fname(self):
        return self.__fname

    @fname.setter
    def fname(self, fname):
        self.__fname = str(fname)

    @property
    def t(self):
        return self.__t

    @t.setter
    def t(self, t):
        if str(t) in self.df.columns:
            self.__t = str(t)
        else:
            raise ValueError('No %s in %s' % (str(t), self.df.columns))

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if str(y) in self.df.columns:
            self.__y = str(y)
        else:
            raise ValueError('No %s in %s' % (str(y), self.df.columns))

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if str(x) in self.df.columns:
            self.__x = str(x)
        else:
            raise ValueError('No %s in %s' % (str(x), self.df.columns))

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = str(title)

    @property
    def ylabel(self):
        return self.__ylabel

    @ylabel.setter
    def ylabel(self, label):
        self.__ylabel = str(label)

    @property
    def xlabel(self):
        return self.__xlabel

    @xlabel.setter
    def xlabel(self, label):
        self.__xlabel = str(label)

    @property
    def yscale(self):
        return self.__yscale.get()

    @yscale.setter
    def yscale(self, scale):
        self.__yscale.set(scale)

    @property
    def xscale(self):
        return self.__xscale.get()

    @xscale.setter
    def xscale(self, scale):
        self.__xscale.set(scale)

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, dataframe):
        self.__df = pd.DataFrame(dataframe)


class BVFigureClass(FigureClass):
    def __init__(self, df):
        FigureClass.__init__(self, df)
        self.yscale = 'linear'
        self.ylabel = '$Breakdown\ Voltage\ (V)$'
        self.title = '$Breakdown\ Voltage$'
        self.y = 'bv'
        self.fname = 'bv.tiff'


class RFigureClass(FigureClass):
    def __init__(self, df):
        FigureClass.__init__(self, df)
        self.yscale = 'linear'
        self.ylabel = '$R_{on,sp}\ m\Omega·cm^{2}$'
        self.title = '$R_{on,sp}$'
        self.y = 'ronsp'
        self.fname = 'r.tiff'


class FoMFigureClass(FigureClass):
    def __init__(self, df):
        FigureClass.__init__(self, df)
        self.yscale = 'linear'
        self.ylabel = '$FoM\ (MW/cm^{2})$'
        self.title = '$FoM$'
        self.y = 'fom'
        self.fname = 'fom.tiff'


if __name__ == '__main__':
    df = pd.read_csv('alldf.csv')

    bvfig = BVFigureClass(df)
    bvfig.x = 'jfetw'
    bvfig.xlabel = '$jfetw\ (cm^{-3})$'
    bvfig.plotline()

    rfig = RFigureClass(df)
    rfig.x = 'jfetw'
    rfig.xlabel = '$jfetw\ (cm^{-3})$'
    rfig.plotline()

    fomfig = FoMFigureClass(df)
    fomfig.x = 'jfetw'
    fomfig.xlabel = '$jfetw\ (cm^{-3})$'
    fomfig.plotline()

    plt.show()
