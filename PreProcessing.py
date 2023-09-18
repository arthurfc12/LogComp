import re

class PreProcessing:
    @staticmethod
    def filter(code):
        return re.sub("/\*.*?\*/", "", code)