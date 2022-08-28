from PyQt5 import QtWidgets, uic

from widgets.dragdroparea import DragDropArea


class Landing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('templates/landing.ui', self)
        self.setWindowTitle("Yomi-mate")
        self.dragDropArea = DragDropArea()
        self.dragDropLayout.addWidget(self.dragDropArea)
        # self.setLayout(self.dragDropLayout)

    def openFileNameDialog(self) -> str:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Images (*.jpg *.jpeg *.png)", options=options)
        if fileName:
            return fileName
