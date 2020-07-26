import sqlite3

class sqlHandler:

    def __init__(self):
        self.conn = sqlite3.connect("../Deps.db")
        self.checkInitalize()

    def checkInitalize(self):
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