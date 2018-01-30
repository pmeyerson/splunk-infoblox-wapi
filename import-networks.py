#!/usr/bin/python

import datetime
import requests
import csv
import json

url = 'https://infobloxhostname-or-ip/wapi/v2.0/'     # API URL to query.  Make sure API access is enabled on this host.
id = ''                                               # API enabled credentials.
pwd = ''  

response = requests.get(url + 'network', auth=(id, pwd), verify=False)
json_data = json.loads(response.text)
data = []
header='Network,Site,Vlan,Description\n'                # Update based on what you put in your infoblox networks' description text

for item in json_data:
        description = item['comment'].split(' - ')      # ' - ' is the delimiter I use in infoblox networks' description text
        data.append([item['network'], ",".join(str(x) for x in description)])

with open('networks.csv', 'w') as writefile:
        writefile.write(header)

        for item in data:
                writefile.write(str(item[0])+','+item[1]+'\n')

