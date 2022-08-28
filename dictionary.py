import jamdict
from jamdict.kanjidic2 import Character
from jamdict.jmdict import JMDEntry
from pykakasi import kakasi
"""
HEAVILY utilizes the JamDict library
https://github.com/neocl/jamdict

huge thanks to the illustrious neocl for saving my hackathon
"""
class YomiDict(jamdict.Jamdict):
    lookupResult: jamdict.util.LookupResult
    kks: kakasi

    def __init__(self):
        super().__init__()
        self.kks = kakasi()

    def updateLookup(self, input: str) -> None:
        self.lookupResult = self.lookup(input)

    def getEntries(self) -> list[jamdict.util.LookupResult]:
        entries = []
        for entry in self.lookupResult.entries:
            entries.append(entry)
        return entries

    def getEntryDicts(self) -> list[dict]:
        entryDicts = []
        for entry in self.lookupResult.entries:
            entryDicts.append(entry.to_dict())
        return entryDicts
    
    def getNames(self) -> list[JMDEntry]:
        names = []
        for name in self.lookupResult.names:
            names.append(name)
        return names

    def getCharacters(self) -> list[Character]:
        chars = []
        for c in self.lookupResult.chars:
            chars.append(c)
        return chars

    def getKanjiRadicals(self, kanji: str):
        return self.krad[kanji]

    # abandoned
    def getRadicalKanji(self, radical: str) -> list[tuple]:
        chars = self.radk[radical]
        if chars:
            result = self.lookup(''.join(chars))
            charsOut = []
            for c in result.chars:
                meanings = []
                if c.meanings():
                    meanings = c.meanings()[0]
                    charsOut.append((c, meanings))
            return charsOut
        return []
    
    def toRomaji(self, original: str) -> str:
        result = self.kks.convert(original)
        out = ''
        for item in result:
            out += item['hepburn']
        return out

if __name__ == '__main__':
    jam = jamdict.Jamdict()
    """ 
    Example JamDict usage from github page
    https://github.com/neocl/jamdict
    """
    # use wildcard matching to find anything starts with 食べ and ends with る
    result = jam.lookup('食べる')

    # print all word entries
    for entry in result.entries:
         print(repr(entry))

    # print all related characters
    for c in result.chars:
        print(c)

    # Find all writing components (often called "radicals") of the character 雲
    print(jam.krad['雲'])
    # ['一', '雨', '二', '厶']

    # Find all characters with the component 鼎
    chars = jam.radk['鼎']
    print(chars)
    # {'鼏', '鼒', '鼐', '鼎', '鼑'}

    # look up the characters info
    result = jam.lookup(''.join(chars))
    for c in result.chars:
        print(c, c.meanings())
    # 鼏 ['cover of tripod cauldron']
    # 鼒 ['large tripod cauldron with small']
    # 鼐 ['incense tripod']
    # 鼎 ['three legged kettle']
    # 鼑 []
