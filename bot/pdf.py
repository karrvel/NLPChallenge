from pypdf import PdfReader
import re

class ReadPDF():
    def __init__(self, file: str):
        self.reader = PdfReader(file)

    async def read(self):
        self.txt = ''
        for page in self.reader.pages:
            self.txt += ' ' + page.extract_text()
        self.txt.replace("\n", " ")
        self.txt.replace("\t", " ")

if __name__ == "__main__":
    #testing
    book = ReadPDF("files/Hacking.pdf")
    book.read()
