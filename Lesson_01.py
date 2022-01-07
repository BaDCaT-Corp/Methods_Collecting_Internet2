import requests
import json
from pprint import pprint

def lesson_01():
    url = "https://oauth.vk.com/authorize"

    params = { 'client_id': '8028496',
               'display': 'page',
               'redirect_uri': 'https://oauth.vk.com/blank.html',
               'scope': 'friends',
               'response_type': 'token',
               'v': '5.52'
    }

    response = requests.get(url, params=params)
    #print(response.text)


    url = 'https://api.vk.com/method/groups.get'
    params_getgroups = {
        'access_token': '6f4b61e40f4637669e94ee09b1f89ee50abd69b6b0c2dcbcfe732c593afcec24470fe5a7c2587f8ef8b9c',
        'user_id': '22319937',
        'v': '5.131',
        'count': '100'
    }

    response = requests.get(url, params_getgroups)
    j_data = response.json()
    pprint(j_data)
    with open('data.txt', 'w') as outfile:
        json.dump(j_data, outfile)
    #https://vk.com/public33621085
