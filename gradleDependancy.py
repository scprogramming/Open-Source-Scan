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