from pprint import pprint

import requests
from lib import settings

ROUTES = {
    'summoner': '[HOST]/lol/summoner/v3/summoners/by-name/[NAME]',
    'account': '[HOST]/lol/summoner/v3/summoners/by-account/[ID]',
    'summonerId': '[HOST]/lol/summoner/v3/summoner/[ID]',
    'champion': '[HOST]/lol/champion-mastery/v3/champion-masteries/by-summoner/[ID]',
    'championScores': '[HOST]/lol/champion-mastery/v3/scores/by-summoner/[ID]',
    'positions': '[HOST]/lol/league/v3/positions/by-summoner/[ID]',
    'matches': '[HOST]/lol/match/v3/matchlists/by-account/[ID]',
    'match': '[HOST]/lol/match/v3/matches/[ID]',
    'spectator': '[HOST]/lol/spectator/v3/active-games/by-summoner/[ID]'
}


def replace(string, key, value):
    value = str(value)
    string = string.replace("[" + str.upper(key) + "]", value)
    string = string.replace("[" + key + "]", value)

    return string


def build_url(url, params):
    url = replace(url, 'host', settings.get_value('HOST'))

    params['api_key'] = settings.get_value('API_KEY')

    for key, value in params.items():
        url = replace(url, key, value)

    return url


def _request(method, url, params, **options):
    url = build_url(url, params)

    print("Request: " + method + " " + url)
    return requests.request(method, url, params=params, **options)


def get_summoner(name, server=settings.get_value('SERVER')):
    req = _request('GET', ROUTES['summoner'], {
        'SERVER': server,
        'NAME': name
    })

    if req.status_code == 200:
        return req.json()
    else:
        return {}


def get_match(summoner, server=settings.get_value('SERVER')):
    req = _request('GET', ROUTES['matches'], {
        'SERVER': server,
        'ID': summoner['accountId'],
        'endIndex': 1
    })

    data = req.json()

    if req.status_code == 200:
        if len(data['matches']) > 0:
            data = data['matches'][0]
            req = _request('GET', ROUTES['match'], {
                'SERVER': server,
                'ID': data['gameId'],
            })

            data = req.json()
        else:
            return {
                'error': 'No Matches'
            }

    return data


def get_summoner_match(summoner, server=settings.get_value('SERVER')):
    req = _request('GET', ROUTES['spectator'], {
        'SERVER': server,
        'ID': summoner['id']
    })

    if req.status_code == 200:
        return req.json()
    else:
        return get_match(summoner, server)
