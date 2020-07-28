import requests

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

def getRelatedCveData(cpeList):
    cveList = []

    for cpes in cpeList:
        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0?startIndex=0&resultsPerPage=20&cpeMatchString="+cpes)
        data = response.json()

        if response.status_code == 200:
            totalResults = data['totalResults']
            currentIndex = 0

            for items in data['result']['CVE_Items']:
                cveList.append(items['cve']['CVE_data_meta']['ID'])
                #items['cve']['description'][0]['value']
                #items['impact']['baseMetricV3']['cvssV3']['vectorString']
    return cveList