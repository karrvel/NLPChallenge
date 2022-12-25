from gtts import gTTS
import sys

class Voice():
    def __init__(self):
            sys.setrecursionlimit(1500000)
    async def toEng(self, txt, file):
        audio = gTTS(text=txt, lang="en", slow=False)
        audio.save(file)
