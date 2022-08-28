from PyQt5 import QtWidgets, QtCore, uic

from widgets.dragdrop import DragDropWidget


class OCRPage(QtWidgets.QWidget):
    imageDropped = QtCore.pyqtSignal(str)
    dropFail = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi('templates/ocr.ui', self)
        self.translation.setReadOnly(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        DragDropWidget.dragEnterEvent(event)

    def dragMoveEvent(self, event):
        DragDropWidget.dragMoveEvent(event)

    def dropEvent(self, event):
        file_path = DragDropWidget.dropEvent(event)
        if file_path:
            self.imageDropped.emit(file_path)
        else:
            self.dropFail.emit('uh oh!')
