#!/usr/bin/python3

import sys
import requests
import json


# set to 1 to pretty-print JSON output (for terminal printing)
pretty_json = 0

# get okta company name from args
okta_name = sys.argv[1]

# api url
api_base = 'https://' + okta_name + '.okta.com/api/v1/'

# get api key from args
api_key = sys.argv[2]

# get verb from args
verb = sys.argv[3]

# make api call, return json
def api_call(api_request):
    # request headers
    headers = {'authorization': 'SSWS ' + api_key}

    # make request
    response = requests.get(api_base + api_request, headers = headers)

    # return json
    return json.loads(response.text)

# search for users of a specific group
def group_search(group_search):
    # search for group using group_search
    group = api_call('groups?q=' + group_search)[0]

    # pull the group id from the result
    group_id = group['id']

    # pull the group name from the result
    group_name = group['profile']['name']

    # init users array
    users = []

    # get user ids
    for item in api_call('groups/' + group_id + '/users'):
        # initialize user
        user = {'{#ID}': None, '{#NAME_F}': None, '{#NAME_L}': None, '{#LOGIN}': None}

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

    # output users
    output(users)

# search for users who are STAGED or LOCKED_OUT
def user_search():
    # init users array
    users = []

    for item in api_call('users?filter=status eq "STAGED" or status eq "LOCKED_OUT"'):
        # initialize user
        user = {'{#ID}': None, '{#NAME_F}': None, '{#NAME_L}': None, '{#LOGIN}': None}

        # get id from json
        user['{#ID}'] = item['id']

        # get first name from json
        user['{#NAME_F}'] = item['profile']['firstName']

        # get last name from json
        user['{#NAME_L}'] = item['profile']['lastName']

        # get login from json
        user['{#LOGIN}'] = item['profile']['login']

        # add user to list
        users.append(user)

    # output users
    output(users)

# output json data
def output(data):
    if pretty_json == 1:
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        print(json.dumps(data))

# do something based on the verb
if verb == 'group':
    group_search(sys.argv[4])
elif verb == 'users':
    user_search()
