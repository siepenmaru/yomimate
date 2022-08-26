import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class Landing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('landing.ui', self)
        self.setWindowTitle("Yomimate")

    def openFileNameDialog(self) -> str:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Images (*.jpg *.jpeg *.png)", options=options)
        if fileName:
            return fileName

    def switchUi(self):
        uic.loadUi('another.ui', self)
        self.show()
        self.setWindowTitle("you\'re winner")

class Another(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('another.ui', self)


class Frontend(QtWidgets.QStackedWidget):
    landing: Landing
    another: Another

    def __init__(self):
        super().__init__()
        self.landing = Landing()
        self.another = Another()
        self.addWidget(self.landing)
        self.addWidget(self.another)
        self.landing.selectImageButton.clicked.connect(self.handleImage)

    def handleImage(self):
        name = self.landing.openFileNameDialog()
        self.setCurrentIndex(1)
        self.another.outputLabel.setText("You selected the file: %s" % name)
        self.setWindowTitle("you\'re winner")
    
    """ 
    window centering function taken from:
    https://python-commandments.org/pyqt-center-window
    """
    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    frontend = Frontend()
    frontend.resize(400,300)
    frontend.centerWindow()
    frontend.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
