import sqlite3

class sqlHandler:

    def __init__(self):
        self.conn = sqlite3.connect("Deps.db")
        self.checkInitalize()

    def checkInitalize(self):
        c = self.conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Projects(
        Id text PRIMARY KEY,
        ProjectName text,
        ProjectLocation text,
        ProjectLanguage text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS Scans(
        ScanId text PRIMARY KEY,
        ProjectId text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS ScanResults(
        ScanId text,
        ProductName text,
        ImportName text,
        versionNumber text,
        ImportsInProject text,
        ImportId text,
        CveId text,
        CveCount text,
        CpeId text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS imports(
        ImportId text,
        FileName text,
        FileLocation text,
        LineNumberReference text)''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS cves(
        CveId text,
        CveNumber text)
        ''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS cves(
        CpeId text,
        Cpe text)
        ''')

