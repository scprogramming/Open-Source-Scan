def createNewProject(projectName,projectLanguage,projectBuildTool,sqlDatabase,rootdir):
    projectId = sqlDatabase.getNextId("Projects", "Id")

    sqlDatabase.queryWithCommit("""
        INSERT INTO Projects VALUES(?,?,?,?,?)
        """, (projectId, projectName, rootdir, projectLanguage, projectBuildTool))

    scanId = sqlDatabase.getNextId("Scans", "scanId")

    sqlDatabase.queryWithCommit("""
        INSERT INTO Scans VALUES(?,?)
        """, (scanId, projectId))

    return projectId,scanId

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

def indexMappedDependencies(mappedDependencies):
    depDict = dict()

    for items in mappedDependencies:
        product = items[0]
        productReference = items[1]

        if product not in depDict:
            depDict[product] = [productReference]
        elif product in depDict:
            depDict[product].append(productReference)

    return depDict

def getRelatedCpeData(productName,sqlDatabase,versionNumber):
    data = sqlDatabase.queryWithReturn('''
    SELECT * FROM nvdCpes WHERE product LIKE ?''',('%' + productName + '%',))
    cpeList = []

    for rows in data:
        rowSplit = rows[1].split(":")

        if versionNumber != "":
            if rowSplit[4] == productName and (rowSplit[5] == versionNumber or rowSplit[5] == "-"):
                cpeList.append(rows[1])
        else:
            if rowSplit[4] == productName:
                cpeList.append(rows[1])

    return cpeList

def getRelatedCveData(cpeList,sqlDatabase):
    cveList = []

    for cpe in cpeList:
        data = sqlDatabase.queryWithReturn('''
            SELECT * FROM nvdCve WHERE cpe=?
        ''',(cpe,))

        for row in data:
            cveList.append(row[0])

    return cveList