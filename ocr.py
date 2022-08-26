import easyocr

reader = easyocr.Reader(['ja'], gpu=True) # this needs to run only once to load the model into memory
result = reader.readtext('images/chainsawman.jpeg')

print(result)