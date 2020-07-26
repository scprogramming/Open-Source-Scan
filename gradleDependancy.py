class gradleDep:
    def __init__(self):
        self.dependencyType = ""
        self.codeImport = ""
        self.dependencyName = ""
        self.version = ""
        self.gradleBuildFile = ""
        self.importList = []

    def __str__(self):
        return self.codeImport + "," + self.dependencyName + "," + self.version

    def __len__(self):
        if self.dependencyType == "" and self.codeImport == "" and self.dependencyName == "":
            return 0
        else:
            return 1