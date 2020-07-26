class importLine:

    def __init__(self):
        self.importLine = ""
        self.importFile = dict() #maps file directory to line in file of import

    def print(self):
        print(self.importLine)
        for keys in self.importFile.keys():
            print(keys + "," + str(self.importFile[keys]))