import sys
from PyQt5 import QtGui, QtWidgets
from ocr import YomimateOCR
from dictionary import YomiDict, Character, JMDEntry
import cv_highlight
from widgets.OCRPage import OCRPage

from widgets.landing import Landing


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
        self.landing.dragDropArea.dropFail.connect(self.popupErrorMessage)
        self.ocrPage.imageDropped.connect(self.handleDroppedImage)
        self.ocrPage.dropFail.connect(self.popupErrorMessage)

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

    # adapted from:
    # https://www.pythonguis.com/tutorials/pyqt-dialogs/
    def popupErrorMessage(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Uh oh!")
        dlg.setText("Sorry! As of version 0.1, Yomi-mate does not support drag and drop from web browsers. You can instead save your image locally, and drag the image from your system's file explorer.")
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Ok:
            dlg.close()

    """ 
    code smells
    won't fix
    for now
    """
    def handleDroppedImage(self, fileLocation: str):
        try:
            self.landing.label_2.setText("Please wait... Yomi-mate is scanning your image!")
            extractedText = self.readImage(fileLocation)
            self.ocrPage.ocrOutputLabel.setText(extractedText)
            self.ocrPage.ocrOutputLabel.selectionChanged.connect(self.handleSelection)
            self.switchToOCRPage(fileLocation)
        except:
            self.landing.label_2.setText("Oh no! something went wrong.")


    def switchToOCRPage(self, fileLocation: str):
        self.setCurrentIndex(1)
        # FIXME: this use of magic numbers STINKS! please fix this
        self.resize(1128, 1000)
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

        entries = self.yomiDict.getEntryDicts()
        chars = self.yomiDict.getCharacters()
        names = self.yomiDict.getNames()

        if not entries and not chars:
            self.ocrPage.translation.setText("Uh oh! Yomi-mate couldn't find an entry for that selection.")
            return

        out = self.formatDictionaryDisplay(entries)
        out += self.formatCharactersDisplay(chars)
        out += self.formatNamesDisplay(names)
        self.ocrPage.translation.setMarkdown(out)

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
        return out

    def formatCharactersDisplay(self, chars: list[Character]) -> str:
        out = ""
        for ch in chars:
            out += f"# **{ch.literal}**\n"
            tags = []
            if ch.jlpt: tags.append(f"JLPT {ch.jlpt}")
            if ch.grade: tags.append(f"Jōyō Kanji taught in Grade {ch.grade}")
            out += " ⋅ ".join(tags) + "\n\n"

            if ch.rad_names:
                out += f"Names: {', '.join(ch.rad_names)}\n\n"

            out += f"Radicals: {', '.join(rad for rad in self.yomiDict.getKanjiRadicals(ch.literal))}\n\n"

            for rmg in ch.rm_groups:
                kunReadings = [r.value for r in rmg.readings if r.r_type == 'ja_kun'] 
                kunRomajiReadings = [self.yomiDict.toRomaji(r) for r in kunReadings]
                onReadings = [r.value for r in rmg.readings if r.r_type == 'ja_on'] 
                onRomajiReadings = [self.yomiDict.toRomaji(r) for r in onReadings]

                kunList = [f'{kunReadings[i]} ({kunRomajiReadings[i]})' for i in range(len(kunReadings))]
                onList = [f'{onReadings[i]} ({onRomajiReadings[i]})' for i in range(len(onReadings))]
                out += f"Kunyomi: {', '.join(kunList)}\n\n" if kunList else ""
                out += f"Onyomi: {', '.join(onList)}\n\n" if onList else ""

            out += f"\n\nMeanings: {', '.join(ch.meanings(english_only=True))}"
            
            out += '\n\n' + 50*'-' + '\n\n'
        return out
    
    def formatNamesDisplay(self, names: list[JMDEntry]):
        out = ""
        nameStr = ""
        for name in names:
            nameStr += f"{name.text(compact=True)}\n\n"
        if nameStr:
            out += "# **Names**\n\n"
            out += nameStr
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
