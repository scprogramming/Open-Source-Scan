def createNewProject(projectName,projectLanguage,projectBuildTool,sqlDatabase,rootdir):
    projectId = sqlDatabase.getNextId("Projects", "Id")

    sqlDatabase.queryWithCommit("""
        INSERT INTO Projects VALUES(?,?,?,?,?)
        """, (projectId, projectName, rootdir, projectLanguage, projectBuildTool))

    scanId = sqlDatabase.getNextId("Scans", "scanId")

    sqlDatabase.queryWithCommit("""
        INSERT INTO Scans VALUES(?,?)
        """, (scanId, projectId))

def getMappedDependencies(dependencies,importDict):
    mappedDependencies = []
    removeList = []

    for keys in dependencies.keys():
        for imports in importDict.keys():
            if keys in imports:
                mappedDependencies.append((keys, importDict[imports]))
                removeList.append(imports)

    for items in removeList:
        if items in importDict:
            del importDict[items]

    return mappedDependencies,importDict