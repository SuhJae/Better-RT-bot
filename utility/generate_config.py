import configparser

config = configparser.ConfigParser()

config['CREDENTIALS'] = {
    'api_key': 'API_KEY',
    'api_secret_key': 'API_SECRET_KEY',
    'access_token': 'ACCESS_TOKEN',
    'access_token_secret': 'ACCESS_TOKEN_SECRET',
    'bearer_token': 'BEARER_TOKEN'
}

config['REDIS'] = {
    'host': 'localhost',
    'port': '6379',
    'password': 'YOUR_PASSWORD_HERE',
    'db': '0'
}

with open('../config.ini', 'w') as configfile:
    config.write(configfile)