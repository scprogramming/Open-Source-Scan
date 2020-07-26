from gradleFunctions import *
from sqlHandler import sqlHandler
from projectFunctions import *

rootdir = 'C:\source\Python\Open Source Learning Set\Java\spring-boot-master'
sqlDatabase = sqlHandler()

userIn = "create"
projectName = "SpringBoot"
projectLanguage = "Java"
projectBuildTool = "Gradle"

if userIn == "create":

    projectId, scanId = createNewProject(projectName,projectLanguage,projectBuildTool,sqlDatabase,rootdir)
    fileList = findGradleFiles(rootdir)
    dependencies = getAllDependencies(fileList)
    allFiles = getAllSourceCode(rootdir)
    importDict = getAllImports(allFiles)

    mappedDependencies,importDict = getMappedDependencies(dependencies,importDict)

    consolidatedDependencies = indexMappedDependencies(mappedDependencies)

    importId = sqlDatabase.getNextId("Imports","ImportId")
    cveId = sqlDatabase.getNextId("Cves",'CveId')
    cpeId = sqlDatabase.getNextId("Cpes","CpeId")

    for productName in consolidatedDependencies.keys():
        imports = consolidatedDependencies[productName]
        print(productName)

        for entries in imports:
            importName = entries.importLine
            versionNumber = dependencies[productName].version

            sqlDatabase.queryWithCommit("""
            INSERT INTO ScanResults VALUES(?,?,?,?,?,?,?)
            """,(scanId,productName,importName,
                 versionNumber,importId,
                 cveId,cpeId))

            importId += 1

        cveId += 1
        cpeId += 1







