from gradleParsing.gradleFunctions import *
from database.sqlHandler import sqlHandler
from projectFunctions import *
import time

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
        dependencyName = dependencies[productName].dependencyName
        print(productName)

        for entries in imports:
            importName = entries.importLine
            versionNumber = dependencies[productName].version

            sqlDatabase.queryWithCommit("""
            INSERT INTO ScanResults VALUES(?,?,?,?,?,?,?,?)
            """,(scanId,productName,importName,
                 versionNumber,importId,
                 cveId,cpeId,dependencyName))

            insertSet = []
            for keys in entries.importFile:
                insertSet.append((importId,keys,str(keys).rsplit("\\",1)[-1],entries.importFile[keys]))

            sqlDatabase.queryManyWithCommit("""
            INSERT INTO Imports VALUES(?,?,?,?)
            """,insertSet)

            importId += 1

        cpeList = getRelatedCpeData(dependencyName,sqlDatabase,versionNumber)

        for cpes in cpeList:
            sqlDatabase.queryWithCommit('''
            INSERT INTO Cpes VALUES (?,?)
            ''',(cpeId,cpes))

        cveList = getRelatedCveData(cpeList,sqlDatabase)

        for cves in cveList:
            sqlDatabase.queryWithCommit('''
            INSERT INTO cves VALUES(?,?)''',(cveId,cves))
        cveId += 1
        cpeId += 1







