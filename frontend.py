import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ocr import YomimateOCR
from dictionary import YomiDict

TEMPLATE_PATH = "templates/"

class Landing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(TEMPLATE_PATH+'landing.ui', self)
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

class DragDropArea(QtWidgets.QLineEdit):
    imageDropped = QtCore.pyqtSignal(str)

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

    """ 
    drag and drop signal handling adapted from
    https://learndataanalysis.org/how-to-implement-image-drag-and-drop-feature-pyqt5-tutorial/
    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            print('valid')
            event.setDropAction(QtCore.Qt.CopyAction)
            # file_path = event.mimeData().urls()[0].toLocalFile()
            file_path = 'images/tmp.jpg'
            if QtGui.QImage(event.mimeData().imageData()).save(file_path):
                print(file_path)
                # self.set_image(file_path)
                self.imageDropped.emit(file_path)
            else:
                print('save fail')

            event.accept()
        else:
            print('invalid!!!')
            event.ignore()

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
        self.ocrPage.scanAnotherButton.clicked.connect(self.handleImage)
        self.landing.dragDropArea.imageDropped.connect(self.handleDroppedImage)

    def handleImage(self):
        fileLocation = self.landing.openFileNameDialog()
        try:
            self.landing.label_2.setText("Please wait... Yomi-mate is scanning your image!")
            extractedText = self.readImage(fileLocation)
            self.ocrPage.ocrOutputLabel.setText(extractedText)
            self.ocrPage.ocrOutputLabel.selectionChanged.connect(self.handleSelection)
            self.switchToOCRPage(fileLocation)
        except:
            self.landing.label_2.setText("Oh no! something went wrong.")

    """ 
    code smells
    won't fix
    for now
    """
    def handleDroppedImage(self, fileLocation: str):
        # try:
        self.landing.label_2.setText("Please wait... Yomi-mate is scanning your image!")
        print(fileLocation)
        return
        # extractedText = self.readImage(fileLocation)
        # self.ocrPage.ocrOutputLabel.setText(extractedText)
        # self.ocrPage.ocrOutputLabel.selectionChanged.connect(self.handleSelection)
        # self.switchToOCRPage(fileLocation)
        # except:
            # self.landing.label_2.setText("Oh no! something went wrong.")


    def switchToOCRPage(self, fileLocation: str):
        self.setCurrentIndex(1)
        # FIXME: this use of magic numbers STINKS! please fix this
        self.resize(1128, 922)
        self.centerWindow()
        self.setWindowTitle("Yomi-mate v0.1")
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

        dicts = self.yomiDict.getEntryDicts()

        if not dicts:
            self.ocrPage.translation.setText("Uh oh! Yomi-mate couldn't find an entry for that selection.")
            return

        out = self.formatDictionaryDisplay(dicts)
        # self.ocrPage.translation.setText(out)
        # self.ocrPage.translation.textCursor().insertHtml(out)
        self.ocrPage.translation.setMarkdown(out)
        # self.ocrPage.translation.textCursor().insertHtml("<b>Bold text. Wow!</b><p></p>")

    # format dictionary entries for better readibility
    def formatDictionaryDisplay(self, dicts: list[dict]) -> str:
        out = ""
        for entry in dicts:
            kanji = entry['kanji']
            kana = entry['kana'][0]['text']
            senses = entry['senses']
            reading = self.yomiDict.toRomaji(kana)

            # end me
            entryStr = ""
            entryStr += f"# **{kanji[0]['text']}**\n" if kanji else "" # entry may be kana only
            entryStr += f"{kana} ⋅ *{reading}*\n\n"

            for sense in senses:
                # what type of word is it?
                # noun, verb, adverb, etc.
                pos = sense['pos'][0]
                entryStr += f"1. ({pos})\n\n"

                # word definitions
                meanings = [meaning['text'] for meaning in sense['SenseGloss']]
                entryStr += '    ' + ', '.join(meanings) + '\n\n'

            out += entryStr + '\n\n' + 50*'-' + '\n\n'
            # out += f"kanji: {entry['kanji']}\nentry: {entry['kana']}\nsenses: {entry['senses']}\n"
        return out

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
