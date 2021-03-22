#!/usr/bin/python3

import http.client
import urllib
import json
import pyodbc
import os
import sys

centreon_user = ''
centreon_pass = ''
centreon_host = ''
sql_user = ""
sql_pass = ""
sql_host = ""
sql_database = ""

def main():
        token=getauthtoken()
        changed=0
        try: 
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+sql_host+';DATABASE='+sql_database+';UID='+sql_user+';PWD='+ sql_pass)
        except Exception as e:
                print('SQL Connection Error: {}'.format(e));
                sys.exit(2);
        cursor = cnxn.cursor()
        cursor.execute("SELECT CentreonName,CentreonLink FROM [Centreon] WHERE CentreonStatus='Monitorowany' and CentreonLink IS NOT NULL") 
        row = cursor.fetchone() 
        while row:
                host = row[0]
                url = row[1]
                db_url = get_url(row[0], token)
                if db_url != url and url is not None:
                        set_url(host, url, token)
                        changed = 1
                row = cursor.fetchone()
        if changed == 1:
                os.system("centreon -u "+centreon_user+" -p "+centreon_pass+" -a APPLYCFG -v 1")

def authenticate():
        params = urllib.parse.urlencode({'username': centreon_user, 'password': centreon_pass})
        return params

def getauthtoken():
        centreon_connection = http.client.HTTPConnection(centreon_host, 80, timeout = 5);
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
        centreon_connection.request('POST', '/centreon/api/index.php?action=authenticate', authenticate(), headers);
        res = centreon_connection.getresponse();
        if res.status != http.client.OK:
                sys.exit(2);

        auth_token = json.loads(res.read())["authToken"]
        return auth_token

def get_url(host, token):
        headers = {'Content-Type': 'application/json', 'centreon-auth-token': token}
        # BUG CENTREON REST API - RETURNS STARTING FROM SECOND PARAM
        params ="{\"action\": \"getparam\", \"object\": \"host\", \"values\": \""+host+";alias|notes_url\"}"
        centreon_connection = http.client.HTTPConnection(centreon_host, 80, timeout = 5);
        centreon_connection.request('POST', '/centreon/api/index.php?action=action&object=centreon_clapi', params, headers);
        res = centreon_connection.getresponse();
        data = json.loads(res.read())
        if not "Object not found" in data:
                return data["result"][0][12:]

def set_url(host, url, token):
        headers = {'Content-Type': 'application/json', 'centreon-auth-token': token}
        params ="{\"action\": \"setparam\", \"object\": \"host\", \"values\": \""+host+";notes_url;"+url+"\"}"
        centreon_connection = http.client.HTTPConnection(centreon_host, 80, timeout = 5);
        centreon_connection.request('POST', '/centreon/api/index.php?action=action&object=centreon_clapi', params, headers);

if __name__ == '__main__':
    main();
