from datetime import datetime
from bot.lib import readIO

if __name__ == "__main__":
    data = readIO.read_database('FocusMePlss', 'na1')
    gameCreation = data['gameCreation']

    # gameDuration = data['gameDuration']
    # participantIdentities = data['participantIdentities']
    # gameId = data['gameId']
    # gameMode = data['gameMode']
    # gameType = data['gameType']
    # teams = data['teams']
    # participants = data['participants']

    print(datetime.utcfromtimestamp(int(gameCreation) / 1000).strftime('%d-%m-%Y %H:%M:%S'))
