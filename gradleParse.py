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

    for values in consolidatedDependencies.keys():
        print(values)




