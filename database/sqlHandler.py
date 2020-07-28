import sqlite3
import os
import requests

class sqlHandler:

    def __init__(self):
        runCpe = False

        if not os.path.exists("../Deps.db"):
            runCpe = True

        self.conn = sqlite3.connect("../Deps.db")
        self.checkInitalize(runCpe)

    def checkInitalize(self,runCpe):
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Projects(
        Id int PRIMARY KEY,
        ProjectName text,
        ProjectLocation text,
        ProjectLanguage text,
        ProjectBuildTool text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Scans(
        ScanId int PRIMARY KEY,
        ProjectId text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS ScanResults(
        ScanId int,
        ProductName text,
        ImportName text,
        versionNumber text,
        ImportId int,
        CveId int,
        CpeId int,
        dependencyName text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS imports(
        ImportId int,
        FileName text,
        FileLocation text,
        LineNumberReference text)''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS cves(
        CveId int,
        CveNumber text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS cpes(
        CpeId int,
        Cpe text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS nvdCpes(
        product text,
        Cpe text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS nvdCve(
        cveId text,
        Cpe text)
        ''')

        if runCpe:
            print("Creating CPE Database")
            self.setupCpeDatabase()
            print("Creating CVE Database")
            self.setupCveDatabase()

        self.conn.commit()

    def queryWithReturn(self,sql,params):
        c = self.conn.cursor()
        result = c.execute(sql,params)

        return result

    def queryWithCommit(self,sql,params):
        c = self.conn.cursor()
        c.execute(sql,params)
        self.conn.commit()

    def queryManyWithCommit(self,sql,params):
        c = self.conn.cursor()
        c.executemany(sql,params)
        self.conn.commit()

    def getNextId(self,table,Id):
        c = self.conn.cursor()
        data = c.execute("SELECT MAX(" + Id + ") FROM " + table)

        for row in data:
            if row[0] is None:
                maxId = 1
            else:
                maxId = 1 + row[0]

        return maxId

    def setupCpeDatabase(self):
        f = open("../official-cpe-dictionary_v2.3.xml", "r", encoding="utf8")

        itemList = []

        cursor = self.conn.cursor()

        for line in f.readlines():
            if "<cpe-item" in line:
                title = ""
            if "<title" in line:
                title = line[line.index('">') + 2:line.index("</title>")]
            if "<cpe-23:cpe23-item" in line:
                cpe = line[line.index('="') + 2:line.index(">") - 2]
            if "</cpe-item" in line:
                itemList.append((title,cpe))

        i = 0

        while i < len(itemList):
            sql = "INSERT INTO nvdCpes VALUES(?,?)"
            if i + 50 < len(itemList):
                cursor.executemany(sql, itemList[i:i + 50])
            else:
                cursor.executemany(sql, itemList[i:])

            self.conn.commit()
            print(i)
            i += 50

        f.close()

    def setupCveDatabase(self):

        response = requests.get("https://services.nvd.nist.gov/rest/json/cves/1.0?startIndex=20&resultsPerPage=20")

        if response.status_code != 404:
            data = response.json()
            totalResults = data['totalResults']
            currentIndex = 0
            tupleList = []

            while currentIndex + 1000 < totalResults:
                try:
                    response = requests.get(
                        "https://services.nvd.nist.gov/rest/json/cves/1.0?startIndex=" + str(
                            currentIndex) + "&resultsPerPage=1000")
                    data = response.json()
                    if response.status_code != 404:
                        for items in data['result']['CVE_Items']:
                            currentCve = items['cve']['CVE_data_meta']['ID']
                            if 'configurations' in items:
                                for configs in items['configurations']['nodes']:

                                    if 'children' in configs:
                                        for children in configs['children']:
                                            for cpeMatches in children['cpe_match']:
                                                tupleList.append((currentCve, cpeMatches['cpe23Uri']))
                                                # print(currentCve + "," + cpeMatches['cpe23Uri'])
                                    else:
                                        if 'cpe_match' in configs:
                                            for cpeMatches in configs['cpe_match']:
                                                tupleList.append((currentCve, cpeMatches['cpe23Uri']))
                                                # print(currentCve + "," + cpeMatches['cpe23Uri'])
                except:
                    print("failed")
                currentIndex += 1000
                print(currentIndex)

            i = 0

            while i < len(tupleList):
                cursor = self.conn.cursor()

                sql = "INSERT INTO nvdCve VALUES(?,?)"
                if i + 50 < len(tupleList):
                    cursor.executemany(sql, tupleList[i:i + 50])
                else:
                    cursor.executemany(sql, tupleList[i:])

                self.conn.commit()
                print(i)
                i += 50