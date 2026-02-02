#!/usr/bin/python
import requests
import json
import sys

def get_users(ids=None, names=None):
    url = "https://grupomaz.bitrix24.com/rest/49171/dcrc5uvz83uiac14/user.get"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    filter_data = {}

    if ids:
        filter_data["ID"] = ids  # lista de IDs

    if names:
        filter_data["NAME"] = names  # lista de nombres o patrones tipo "Misael%"

    payload = {
        "filter": filter_data
    }

    return requests.post(url, headers=headers, json=payload)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: ./get_user.py "username"')
        sys.exit(1)

    name_filter = sys.argv[1]
    response = get_users(names=[name_filter])

    print(json.dumps(response.json(), ensure_ascii=False, indent=2))