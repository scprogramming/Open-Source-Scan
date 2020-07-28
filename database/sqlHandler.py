import sqlite3
import os

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

        if runCpe:
            self.setupCpeDatabase()

        self.conn.commit()

    def queryWithReturn(self,sql,params):
        c = self.conn.cursor()
        result = c.execute(sql,params)

        return result

    def queryWithCommit(self,sql,params):
        c = self.conn.cursor()
        c.execute(sql,params)
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