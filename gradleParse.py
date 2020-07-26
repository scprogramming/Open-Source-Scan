from gradleFunctions import *
from sqlHandler import sqlHandler

rootdir = 'C:\source\Python\Open Source Learning Set\Java\spring-boot-master'
sqlDatabase = sqlHandler()

userIn = "create"
projectName = "SpringBoot"
projectLanguage = "Java"
projectBuildTool = "Gradle"

if userIn == "create":

    data = sqlDatabase.queryWithReturn("SELECT MAX(Id) FROM Projects",())

    for row in data:
        if row[0] is None:
            maxId = 1
        else:
            maxId = 1+ row[0]

    sqlDatabase.queryWithCommit("""
    INSERT INTO Projects VALUES(?,?,?,?,?)
    """,(maxId,projectName,rootdir,projectLanguage,projectBuildTool))

    fileList = findGradleFiles(rootdir)

    dependencies = getAllDependencies(fileList)

    allFiles = getAllSourceCode(rootdir)

    importDict = getAllImports(allFiles)

    for keys in dependencies.keys():
        print(dependencies[keys])

    #for keys in importDict.keys():
        #print('"' + keys.strip()+ '"')



