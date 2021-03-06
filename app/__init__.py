from flask import Flask
from database.sqlHandler import sqlHandler
import sys

app = Flask(__name__)

@app.route("/showCveList/<cveId>")
def showCveList(cveId):
    sqlDatabase = sqlHandler()
    results = sqlDatabase.queryWithReturn("SELECT * FROM cves WHERE cveId=?", (cveId,))

    returnBody = '''
                <html>
                <body>
                <table style="width:100%">
                <tr>
                    <th>CVE</th>
                </tr>
                '''

    for row in results:
        returnBody += '''
            <tr>
            <td>''' + row[1] + '''</td>
            </tr>
            '''

    returnBody += '''
                </table>
                </body>
                </html>'''

    return returnBody

@app.route("/showImportList/<importId>")
def showImportList(importId):
    sqlDatabase = sqlHandler()
    results = sqlDatabase.queryWithReturn("SELECT * FROM Imports WHERE ImportId=?", (importId,))

    returnBody = '''
            <html>
            <body>
            <table style="width:100%">
            <tr>
                <th>File Name</th>
                <th>File Location</th>
                <th>Line Number</th>
            </tr>
            '''

    for row in results:
        returnBody += '''
        <tr>
        <td>''' + row[1] + '''</td>
        <td>''' + row[2] + '''</td>
        <td>''' + row[3] + '''</td>
        </tr>
        '''

    returnBody += '''
            </table>
            </body>
            </html>'''

    return returnBody

@app.route("/loadScan/<scanId>")
def loadScan(scanId):
    sqlDatabase = sqlHandler()
    results = sqlDatabase.queryWithReturn("SELECT * FROM ScanResults WHERE ScanId=?", (scanId,))

    returnBody = '''
            <html>
            <body>
            <table style="width:100%">
            <tr>
                <th>Product Name</th>
                <th>Import Name</th>
                <th>version Number </th>
                <th>Code Import</th>
                <th>Import List</th>
                <th>CVE List</th>
            </tr>
            '''

    for row in results:
        returnBody += '''
                <tr>
                    <td>''' + row[1] + '''</td>
                    <td>''' + str(row[2]) + '''</td>
                    <td>''' + str(row[3]) + '''</td>
                    <td>''' + str(row[7]) + '''</td>
                    <td><a href="/showImportList/''' +str(row[4]) + '''"> Click to view import list</td>
                    
                '''
        cveData = sqlDatabase.queryWithReturn('''
        SELECT COUNT(*) FROM Cves WHERE CveId = ?''',(row[5],))

        for res in cveData:
            if res[0] >= 1:
                returnBody += '''<td><a href="/showCveList/''' +str(row[5]) + '''"> Click to view CVE list</td></tr>'''
            else:
                returnBody += '<td>No CVEs Found</td></tr>'
    returnBody += '''
            </table>
            </body>
            </html>'''

    return returnBody

@app.route("/loadScanList/<projectId>")
def scanHome(projectId):
    sqlDatabase = sqlHandler()
    results = sqlDatabase.queryWithReturn("SELECT * FROM scans WHERE ProjectId=?", (projectId,))

    returnBody = '''
        <html>
        <body>
        <table style="width:100%">
        <tr>
            <th>Scans</th>
        </tr>
        '''

    for row in results:
        returnBody += '''
            <tr>
                <td><a href="/loadScan/''' + row[1] + '''">''' + row[1] + '''</td>
            </tr>
            '''

    returnBody += '''
        </table>
        </body>
        </html>'''

    return returnBody

@app.route("/")
def home():
    sqlDatabase = sqlHandler()
    results = sqlDatabase.queryWithReturn("SELECT * FROM projects",())

    returnBody = '''
    <html>
    <body>
    <table style="width:100%">
    <tr>
        <th>Project Name</th>
        <th>Project Location</th>
        <th>Project Language</th>
        <th>Project Build Tool </th>
    </tr>
    '''

    for row in results:
        returnBody += '''
        <tr>
            <td><a href="/loadScanList/''' + str(row[0]) + '''">''' + row[1] + '''</a></td>
            <td>''' + row[2] + '''</td>
            <td>''' + row[3] + '''</td>
            <td>''' + row[4] + '''</td>
        </tr>
        '''

    returnBody += '''
    </table>
    </body>
    </html>'''

    return returnBody

if __name__ == "__main__":
    app.run()