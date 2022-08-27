import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
import cv2

# https://stackoverflow.com/a/68417901
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QtCore.QLibraryInfo.location(
    QtCore.QLibraryInfo.PluginsPath
)

class CanvasWidget(QtWidgets.QWidget):
    def __init__(self, w: int, h: int):
        super().__init__()

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        
    def plot(self, imgPath: str, boxes: list[tuple]):
        self.ax.clear()
        self.ax.plot()