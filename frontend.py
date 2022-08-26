import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ocr import YomimateOCR
from dictionary import YomiDict

TEMPLATE_PATH = "templates/"

class Landing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(TEMPLATE_PATH+'landing.ui', self)
        self.setWindowTitle("Yomimate")

    def openFileNameDialog(self) -> str:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Images (*.jpg *.jpeg *.png)", options=options)
        if fileName:
            return fileName

    def switchUi(self):
        uic.loadUi(TEMPLATE_PATH+'another.ui', self)
        self.show()
        self.setWindowTitle("you\'re winner")

class OCRPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(TEMPLATE_PATH+'ocr.ui', self)

class Frontend(QtWidgets.QStackedWidget):
    landing: Landing
    ocrPage: OCRPage
    reader: YomimateOCR
    result: str
    yomiDict: YomiDict

    def __init__(self):
        super().__init__()
        self.reader = YomimateOCR('ja', False)
        self.yomiDict = YomiDict()
        self.landing = Landing()
        self.ocrPage = OCRPage()
        self.addWidget(self.landing)
        self.addWidget(self.ocrPage)
        self.landing.selectImageButton.clicked.connect(self.handleImage)

    def handleImage(self):
        fileLocation = self.landing.openFileNameDialog()
        try:
            self.landing.label_2.setText("Please wait... Yomimate is scanning your image!")
            extractedText = self.readImage(fileLocation)
            self.ocrPage.ocrOutputLabel.setText(extractedText)
            self.ocrPage.ocrOutputLabel.selectionChanged.connect(self.handleSelection)
            self.switchToOCRPage(fileLocation)
        except:
            self.landing.label_2.setText("Oh no! something went wrong.")

    def switchToOCRPage(self, fileLocation: str):
        self.setCurrentIndex(1)
        self.resize(1128, 883)
        self.centerWindow()
        self.setWindowTitle("you\'re winner")
        img = QtGui.QPixmap(fileLocation)
        self.ocrPage.outImage.resize(img.width(), img.height())
        self.ocrPage.outImage.setPixmap(img)
    
    def handleSelection(self):
        cursor = self.ocrPage.ocrOutputLabel.textCursor()
        selection = self.result[cursor.selectionStart():cursor.selectionEnd()]
        self.displaySelectionInfo(selection)

    def displaySelectionInfo(self, selection: str):
        try:
            self.yomiDict.updateLookup(selection)
        except:
            return

        entries = self.yomiDict.get_entries()

        if not entries:
            self.ocrPage.translation.setText("Uh oh! Yomimate couldn't find an entry for that selection.")
            return

        out = ""
        for entry in entries:
            out += str(entry) + '\n'
        self.ocrPage.translation.setText(out)

    def readImage(self, fileLocation: str) -> str:
        self.reader.readImage(fileLocation)
        self.result = self.reader.getText()
        return self.result

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
