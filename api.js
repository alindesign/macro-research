const axios = require('axios');
const moment = require('moment');
const fs = require('fs');

const API_KEY = 'RGAPI-42192401-1b3b-4dfb-b6af-1c895ea838ba';
const NAME = 'FocusMePlss';
const HOST = 'https://eun1.api.riotgames.com';

const ROUTES = {
    summoner: (name) => `${HOST}/lol/summoner/v3/summoners/by-name/${name}`,
    account: (id) => `${HOST}/lol/summoner/v3/summoners/by-account/${id}`,
    summonerId: (id) => `${HOST}/lol/summoner/v3/summoner/${id}`,
    champion: (id) => `${HOST}/lol/champion-mastery/v3/champion-masteries/by-summoner/${id}`,
    championScores: (id) => `${HOST}/lol/champion-mastery/v3/scores/by-summoner/${id}`,
    positions: (id) => `${HOST}/lol/league/v3/positions/by-summoner/${id}`,
    matches: (id) => `${HOST}/lol/match/v3/matchlists/by-account/${id}`,
    match: (id) => `${HOST}/lol/match/v3/matches/${id}`,
    spectator: (id) => `${HOST}/lol/spectator/v3/active-games/by-summoner/${id}`,
}

// Simulate edit

const api = (method, url, params = {}, options = {}) => {
    console.log(`Send ${method.toUpperCase()} ${url}`);

    return (
        axios[method](url, {
            ...options,
            params: {
                api_key: API_KEY,
                ...params
            }
        })
    );
};

const fetchGame = (accountId) => (
    api('get', ROUTES.matches(accountId))
        .then(({ data: matches }) => {
            const [match, ...list] = matches.matches;

            const { gameId } = match;
            api('get', ROUTES.match(gameId))
                .then(({ data: match }) => {
                    const { gameCreation } = match;
                    const date = moment(gameCreation);

                    console.log(date.toString());

                    fs.writeFileSync('last_match.json', JSON.stringify(match, null, '     '));
                });
        })
);

api('get', ROUTES.summoner(NAME))
    .then(({ data }) => {
        const { id, accountId } = data;

        api('get', ROUTES.spectator(id))
            .then(({ data: game }) => {
                fs.writeFileSync('live.json', JSON.stringify(game, null, '     '));
                fetchGame(accountId);
            }, () => {
                fs.writeFileSync('live.json', '{}');
                fetchGame(accountId)
            });
    });
