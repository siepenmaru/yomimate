import jamdict
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

    def get_entries(self) -> list[jamdict.util.LookupResult]:
        entries = []
        for entry in self.lookupResult.entries:
            entries.append(entry)
        return entries
    
    def get_related(self) -> list[jamdict.util.Character]:
        entries = []
        for ch in self.lookupResult.chars:
            entries.append(ch)
        return entries

    def get_romaji(self, original: str) -> str:
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
