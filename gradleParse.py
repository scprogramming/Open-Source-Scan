from gradleFunctions import *
from sqlHandler import sqlHandler

rootdir = 'C:\source\Python\Open Source Learning Set\Java\spring-boot-master'
sqlDatabase = sqlHandler()

userIn = "create"
projectName = "SpringBoot"
projectLanguage = "Java"
projectBuildTool = "Gradle"

if userIn == "create":
    projectId = sqlDatabase.getNextId("Projects","Id")

    sqlDatabase.queryWithCommit("""
    INSERT INTO Projects VALUES(?,?,?,?,?)
    """,(projectId,projectName,rootdir,projectLanguage,projectBuildTool))

    scanId = sqlDatabase.getNextId("Scans","scanId")

    sqlDatabase.queryWithCommit("""
    INSERT INTO Scans VALUES(?,?)
    """,(scanId,projectId))

    fileList = findGradleFiles(rootdir)

    dependencies = getAllDependencies(fileList)

    allFiles = getAllSourceCode(rootdir)

    importDict = getAllImports(allFiles)

    mappedDependencies = []
    removeList = []

    for keys in dependencies.keys():
        for imports in importDict.keys():
            if keys in imports:
                mappedDependencies.append((keys,importDict[imports]))
                removeList.append(imports)

    for items in removeList:
        if items in importDict:
            del importDict[items]


    for keys in importDict.keys():
        print(keys)



