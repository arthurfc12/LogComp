import re
class PreProcessing:
    def filter_expression(code):
        return re.sub("/\*.*?\*/", "", code)
