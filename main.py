#!/bin/env python

import sys, traceback, functools

import numpy as np

from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, uic


def dialogue_on_error(func):
    """
    Wrapps callback methods to report errors rather than crashing GUI
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as exception:
            QtWidgets.QMessageBox.about(self,
                                        type(exception).__name__,
                                        traceback.format_exc())

    return wrapper


class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        uic.loadUi('test.ui', self)

        self.statusbar.showMessage("testing")

        ### Qt Widget setup
        self.canv1, self.fig1, self.ax1 = self.add_axes(self.preview.layout())
        self.canv2, self.fig2, self.ax2 = self.add_axes(self.preview_2.layout())
        ###

        self.tab1_func = np.sin
        self.tab2_funcs = dict(log=np.log, exp=np.exp)
        self.t = np.linspace(1e-3, 10, 500)

        ### Callbacks (for buttons set up in test.ui, which was created in qt designer)
        self.sinButton.clicked.connect( lambda: self.set_t1f(np.sin) )
        self.cosButton.clicked.connect( lambda: self.set_t1f(np.cos) )
        self.phaseBox.valueChanged.connect( lambda: self.plotOffset(self.tab1_func) )
        self.funcDropdown.activated.connect(self.handleActivated)

        self.action_Quit.triggered.connect( self.close )
        self.action_About.triggered.connect( self.about )
        ###

    def set_t1f(self, f):
        self.tab1_func = f
        self.plotOffset(f)

    def plotOffset(self, f):
        o = self.phaseBox.value()
        self.plot(self.canv1, self.t, f(self.t+o))

    @dialogue_on_error
    def handleActivated(self, i):
        key = self.funcDropdown.itemText(i)
        f = self.tab2_funcs[key]
        self.plot(self.canv2, self.t, f(self.t))

    ### Qt Widget setup

    def add_canvas(self, layout):
        canvas = FigureCanvas(Figure(figsize=(5, 3)))
        navbar = NavigationToolbar(canvas, self)

        layout.addWidget( canvas )
        layout.addWidget( navbar )

        return canvas, navbar

    def add_axes(self, layout):
        canvas, navbar = self.add_canvas(layout)
        axes = canvas.figure.subplots()
        return canvas, navbar, axes

    def plot(self, canvas, *args, **kwargs):
        ax = canvas.figure.axes[0]
        ax.clear() # <<< usually wont want to clear every time...
        ax.plot(*args, **kwargs)
        canvas.draw()

    ###

    def about(self):
        QtWidgets.QMessageBox.about(self,
                                    "About",
"""A simple Qt5 embedded matplotlib plots demo...
"""
                                )

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Window()
    #widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
