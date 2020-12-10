#!/usr/bin/python2

import httplib
import urllib
import json
import argparse

centreon_user = ''
centreon_pass = ''
location = ''


def main():
    inventory_list = {}
    inventory_list["all"] = {}
    inventory_list["all"]["hosts"] = []
    inventory_list["all"]["vars"] = {}
    inventory_list["t01"] = {}
    inventory_list["t01"]["hosts"] = []
    inventory_list["t01"]["vars"] = {}
    inventory_list["t02"] = {}
    inventory_list["t02"]["hosts"] = []
    inventory_list["t02"]["vars"] = {}
    inventory_list["t03"] = {}
    inventory_list["t03"]["hosts"] = []
    inventory_list["t03"]["vars"] = {}
    inventory_list["t04"] = {}
    inventory_list["t04"]["hosts"] = []
    inventory_list["t04"]["vars"] = {}
    inventory_list["t05"] = {}
    inventory_list["t05"]["hosts"] = []
    inventory_list["t05"]["vars"] = {}
    inventory_list["t06"] = {}
    inventory_list["t06"]["hosts"] = []
    inventory_list["t06"]["vars"] = {}
    inventory_list["t07"] = {}
    inventory_list["t07"]["hosts"] = []
    inventory_list["t07"]["vars"] = {}
    inventory_list["fw"] = {}
    inventory_list["cisco_fw"]["hosts"] = []
    inventory_list["cisco_fw"]["vars"] = {"ansible_connection": "network_cli", "ansible_network_os": "ios"}
    inventory_list["kiosk"] = {}
    inventory_list["kiosk"]["hosts"] = []
    inventory_list["kiosk"]["vars"] = {}
    inventory_list["switch"] = {}
    inventory_list["switch"]["hosts"] = []
    inventory_list["switch"]["vars"] = {}
    inventory_list["_meta"] = {}
    inventory_list["_meta"]["hostvars"] = {}

    data = getinventory('TERMINALE')
    for i in range(0, len(data["result"])):
        name = data["result"][i]["name"].strip()
        element_name = "{}{}".format( name[0:5], name [-3:])
        inventory_list[element_name[-3:]]["hosts"].append(element_name)
        inventory_list["all"]["hosts"].append(element_name)

    data = getinventory('KIOSKI')
    for i in range(0, len(data["result"])):
        name = data["result"][i]["name"].strip()
        element_name = "{}{}".format( name[0:5], name [-5:])
        inventory_list[element_name[-5:]]["hosts"].append(element_name)
        inventory_list["all"]["hosts"].append(element_name)

    data = getinventory('CISCO_891')
    for i in range(0, len(data["result"])):
        name = data["result"][i]["name"].strip()
        element_name = "{}{}".format( name[0:5], name [-2:])
        inventory_list["cisco_fw"]["hosts"].append(element_name)
        inventory_list["all"]["hosts"].append(element_name)

    #data = getinventory('JUNIPER_SSG5')
    #for i in range(0, len(data["result"])):
    #    name = data["result"][i]["name"].strip()
    #    element_name = "{}{}".format( name[0:5], name [-2:])
    #    inventory_list[element_name[-2:]]["hosts"].append(element_name)
    #    inventory_list["all"]["hosts"].append(element_name)

    data = getinventory('SWITCHE')
    for i in range(0, len(data["result"])):
        name = data["result"][i]["name"].strip()
        element_name = "{}{}".format( name[0:5], name [-6:])
        inventory_list[element_name[-6:]]["hosts"].append(element_name)
        inventory_list["all"]["hosts"].append(element_name)

    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host', action='store')
    args = parser.parse_args()
    if args.list:
        print("{}".format(json.dumps(inventory_list)))
    elif args.host and args.host in inventory_list["_meta"]["hostvars"]:
        print("{}".format(json.dumps(inventory_list["_meta"]["hostvars"][args.host])))
    else:
        print("{}".format(json.dumps(inventory_list)))

def authenticate():
    params = urllib.urlencode({'username': centreon_user, 'password': centreon_pass})
    return params

def getauthtoken():
    centreon_connection = httplib.HTTPConnection(location, 80, timeout = 5);
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}
    centreon_connection.request('POST', '/centreon/api/index.php?action=authenticate', authenticate(), headers);
    res = centreon_connection.getresponse();
    if res.status != httplib.OK:
        sys.exit(2);

    auth_token = json.loads(res.read())["authToken"]
    return auth_token

def getinventory(typ):
    token=getauthtoken()
    headers = {'Content-Type': 'application/json', 'centreon-auth-token': token}
    params ="{\"action\": \"getmember\", \"object\": \"HG\", \"values\": \""+typ+"\"}"
    centreon_connection = httplib.HTTPConnection(location, 80, timeout = 5);
    centreon_connection.request('POST', '/centreon/api/index.php?action=action&object=centreon_clapi', params, headers);
    res = centreon_connection.getresponse();
    if res.status != httplib.OK:
        sys.exit(2);
    data = json.loads(res.read())
    return data

if __name__ == '__main__':
    main();
