from lib import settings
from lib.api import get_summoner, get_summoner_match


def read_database(name, server):
    settings.set_value('SERVER', server)
    summoner = get_summoner(name)

    if 'id' in summoner.keys():
        return get_summoner_match(summoner)
    else:
        return {
            'error': 'Summoner not found!'
        }
