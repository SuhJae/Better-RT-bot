import configparser

config = configparser.ConfigParser()

config['CREDENTIALS'] = {
    'api_key': 'API_KEY',
    'api_secret_key': 'API_SECRET_KEY',
    'access_token': 'ACCESS_TOKEN',
    'access_token_secret': 'ACCESS_TOKEN_SECRET',
    'bearer_token': 'BEARER_TOKEN'
}

config['STREAM'] = {
    'keyword': 'Python, programming, coding',
    'language': 'en',
}

with open('../config.ini', 'w') as configfile:
    config.write(configfile)