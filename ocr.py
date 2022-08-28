import easyocr

class YomimateOCR:
    reader: easyocr.Reader
    results: list
    minConfidence: int

    # index constants to access result data
    POS_INDEX = 0
    TEXT_INDEX = 1
    CONFIDENCE_INDEX = 2

    def __init__(self, lang: str, gpu: bool, minConfidence: int=0.7):
        self.reader = easyocr.Reader([lang], gpu=gpu)
        self.minConfidence = minConfidence

    def readImage(self, fileLocation: str) -> None:
        self.results = self.reader.readtext(fileLocation)

    # join together resulting text into one string
    def getText(self) -> str:
        outText = ""
        for entry in self.results:
            outText += entry[self.TEXT_INDEX] + '\n'
        return outText

    # prune results under a given confidence value
    def pruneResults(self) -> None:
        for entry in self.results:
            if entry[self.CONFIDENCE_INDEX] < self.minConfidence:
                self.results.remove(entry)

if __name__ == '__main__':
    reader = easyocr.Reader(['ja'], gpu=False) # this needs to run only once to load the model into memory
    result = reader.readtext('images/chainsawman.jpeg')

    for i in result:
        print(i)