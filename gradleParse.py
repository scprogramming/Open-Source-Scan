from gradleFunctions import *
from sqlHandler import sqlHandler

rootdir = 'C:\source\Python\Open Source Learning Set\Java\spring-boot-master'
sqlDatabase = sqlHandler()


fileList = findGradleFiles(rootdir)

dependencies = getAllDependencies(fileList)

allFiles = getAllSourceCode(rootdir)

importDict = getAllImports(allFiles)

for keys in dependencies.keys():
    print(dependencies[keys])

#for keys in importDict.keys():
    #print('"' + keys.strip()+ '"')



