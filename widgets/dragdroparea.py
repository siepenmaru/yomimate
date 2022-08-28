from PyQt5 import QtWidgets, QtCore

from widgets.dragdrop import DragDropWidget


class DragDropArea(QtWidgets.QLineEdit):
    imageDropped = QtCore.pyqtSignal(str)
    dropFail = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName(u"dragDropArea")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText("Drag and drop your image here!")
        self.setReadOnly(True)
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
