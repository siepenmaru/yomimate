import easyocr

class OCR:
    reader: easyocr.Reader
    results: list

    # index constants to access result data
    POS_INDEX = 0
    TEXT_INDEX = 1
    CONFIDENCE_INDEX = 2

    def __init__(self, lang: str, gpu: bool):
        self.reader = easyocr.Reader([lang], gpu=gpu)

    def readImage(self, fileLocation: str) -> None:
        self.results = reader.readtext(fileLocation)

    # join together resulting text into one string
    def getText(self) -> str:
        outText = ""
        for entry in self.results:
            outText += entry[self.TEXT_INDEX] + '\n'
        return outText

    # prune results under a given confidence value
    def pruneResults(self, minConfidence: int) -> None:
        for entry in self.results:
            if entry[self.CONFIDENCE_INDEX] < minConfidence:
                self.results.remove[entry]

if __name__ == '__main__':
    reader = easyocr.Reader(['ja'], gpu=False) # this needs to run only once to load the model into memory
    result = reader.readtext('images/chainsawman.jpeg')

    for i in result:
        print(i)