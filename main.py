import tweepy
import configparser

# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

# Authenticate to Twitter
client = tweepy.Client(config['CREDENTIALS']['bearer_token'], config['CREDENTIALS']['api_key'], config['CREDENTIALS']['api_secret_key'], config['CREDENTIALS']['access_token'], config['CREDENTIALS']['access_token_secret'])
auth = tweepy.OAuth1UserHandler(config['CREDENTIALS']['api_key'], config['CREDENTIALS']['api_secret_key'], config['CREDENTIALS']['access_token'], config['CREDENTIALS']['access_token_secret'])
api = tweepy.API(auth)

# Authenticate check to twitter
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    exit()
