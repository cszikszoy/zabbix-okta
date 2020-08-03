#!/usr/bin/python3

import sys
import requests
import json

# get okta company name from args
okta_name = sys.argv[1]

# get api key from args
api_key = sys.argv[2]

# get group from args
group_name = sys.argv[3]

# api url
api_base = 'https://' + okta_name + '.okta.com/api/v1/'

# make api call, return json
def api_call(api_request):
    # request headers
    headers = {'authorization': 'SSWS ' + api_key}

    # make request
    response = requests.get(api_base + api_request, headers = headers)

    # return json
    return json.loads(response.text)


# search for group name
group_id = api_call('groups?q=' + group_name)[0]['id']

# users array
users = []

# get user ids
for item in api_call('groups/' + group_id + '/users'):
    # initialize user
    user = {'{#ID}': None, '{#NAME_F}': None, '{#NAME_L}': None, '{#LOGIN}': None}

    # debug
    #print(item['id'])

    # get id from json
    user['{#ID}'] = item['id']

    # get first name from json
    user['{#NAME_F}'] = item['profile']['firstName']

    # get last name from json
    user['{#NAME_L}'] = item['profile']['lastName']

    # get login from json
    user['{#LOGIN}'] = item['profile']['login']

    # feed the group name back so we can use this as an LLD Macro for application prototype in zabbix
    user['{#GROUP}'] = group_name

    # add user to list
    users.append(user)

# dump the result in a discovery array that zabbix understands
print(json.dumps(users))

# dump the results in human readale JSON form
#print(json.dumps(users, indent=4, sort_keys=True))
