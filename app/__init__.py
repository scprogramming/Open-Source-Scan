from flask import Flask
from database.sqlHandler import sqlHandler
import sys

app = Flask(__name__)

@app.route("/loadScan/<scanId>")
def scanHome(scanId):
    return "<h1>" + str(scanId) + "</h1>"

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
            <td><a href="/loadScan/''' + str(row[0]).strip() + '''">''' + row[1] + '''</a></td>
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