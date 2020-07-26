import os
from gradleDependancy import gradleDep
from importLine import importLine
def getAllSourceCode(directory):
    fileList = []

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if ".java" in file:
                fileList.append(os.path.join(subdir, file))
    return fileList

def findGradleFiles(directory):
    fileList = []

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if "build.gradle" in file:
                fileList.append(os.path.join(subdir, file))
    return fileList

def parseDependencies(file):
    dependencyList = []

    f = open(file, "r")
    inDependency = False
    bracketCount = 0
    for lines in f.readlines():
        if inDependency:
            if "{" in lines:
                bracketCount += 1
            if "}" in lines:
                bracketCount -= 1

            if bracketCount == 0:
                inDependency = False
            else:
                dependencyList.append(lines.strip())
        if "dependencies {" in lines:
            inDependency = True
            bracketCount += 1

    return dependencyList

def getAllDependencies(fileList):
    dependencies = dict()

    for files in fileList:
        depList = parseDependencies(files)
        for lines in depList:
            if "(" in lines:
                identifier = lines[0:lines.index("(")].strip()
                if '"' in lines and '")' in lines:
                    depString = lines[lines.index('"')+1:lines.index('")')]
                    newDep = gradleDep()

                    depSplit = depString.split(":")
                    if len(depSplit) == 3:
                        newDep.codeImport = depSplit[0]
                        newDep.dependencyName = depSplit[1]
                        newDep.dependencyType = identifier
                        newDep.version = depSplit[2]
                    elif len(depSplit) == 2:
                        newDep.codeImport = depSplit[0]
                        newDep.dependencyName = depSplit[1]
                        newDep.dependencyType = identifier
                    elif len(depSplit) == 1:
                        newDep.codeImport = depSplit[0]
                        newDep.dependencyType = identifier

                    if newDep.codeImport not in dependencies:
                        newDep.gradleBuildFile = files
                        dependencies[newDep.codeImport] = newDep
    return dependencies

def getAllImports(allFiles):
    importDict = dict()

    for file in allFiles:
        lineNumber = 0
        f = open(file, "r", encoding='utf-8')
        for lines in f.readlines():
            lines = lines.strip()
            lineNumber += 1
            if "import" in lines.split(" ")[0]:
                if lines not in importDict:
                    line = importLine()
                    line.importLine = lines
                    line.importFile[file] = lineNumber
                    importDict[lines] = line
                else:
                    importDict[lines].importFile[file] = lineNumber

    return importDict