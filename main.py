import configparser
import threading
import tweepy
import redis
import time

start = time.time()
first = True
# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

#class for the formatting on terminal
class BC:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def process_tweet(tweet):
    tweet = api.get_status(tweet.id)

    if hasattr(tweet, 'retweeted_status'):  # Check if Retweet
        print(f'{BC.FAIL}[RT]{BC.OKBLUE} {tweet.user.screen_name}{BC.RESET}: {BC.WARNING}{tweet.text}')
    elif tweet.in_reply_to_status_id is None:  # Check if Reply
        print(f'{BC.FAIL}[NR]{BC.OKBLUE} {tweet.user.screen_name}{BC.RESET}: {BC.WARNING}{tweet.text}')
    # Check if the user of current tweet is same as the user of tweet of reply
    elif tweet.in_reply_to_screen_name == tweet.user.screen_name:
        print(f'{BC.OKGREEN}[OK]{BC.OKBLUE} {tweet.user.screen_name}{BC.RESET}: {tweet.text}')
        #check if the bot already retweeted the in reply to tweet
        try:
            api.retweet(tweet.in_reply_to_status_id)
        except:
            print(f'{BC.FAIL}Already retweeted{BC.RESET}')
    else:
        print(f'{BC.FAIL}[WU]{BC.OKBLUE} {tweet.user.screen_name}{BC.RESET}: {BC.WARNING}{tweet.text}')

class MyStream(tweepy.StreamingClient):
    def on_connect(self):
        print(f'Stream connection {BC.BOLD}{BC.OKGREEN}OK{BC.RESET}')
        print(f'Time took on setup: {BC.BOLD}{BC.OKGREEN}{round((time.time() - start) * 1000):,}ms{BC.RESET}')

    def on_tweet(self, tweet):
        # execute the process_tweet function in a thread, so it doesn't block the stream
        threading.Thread(target=process_tweet, args=(tweet,)).start()

    def on_disconnect(self):
        print(f'Stream connection {BC.BOLD}{BC.FAIL}DISCONNECTED{BC.RESET}')
        stream.disconnect()

    def on_on_limit(self, notice):
        print(f'{BC.BOLD}{BC.WARNING}Limit notice: {notice}{BC.RESET}')

# Connect to Redis
print(f'{BC.HEADER}Trying to connect to Redis...{BC.RESET}')
r = redis.Redis(host=config['REDIS']['host'], port=int(config['REDIS']['port']), db=int(config['REDIS']['db']), password=config['REDIS']['password'])
try:
    r.ping()
    print(f'Redis connection {BC.OKGREEN}{BC.BOLD}OK{BC.RESET}')
    
except:
    print(f'{BC.FAIL}Error during connection.\nCheck your REDIS in {BC.UNDERLINE}config.ini{BC.RESET}{BC.FAIL}.{BC.RESET}')
    exit()

# Authenticate check to twitter
print(f'{BC.HEADER}Trying to connect to Twitter API...{BC.RESET}')
client = tweepy.Client(config['CREDENTIALS']['bearer_token'], config['CREDENTIALS']['api_key'], config['CREDENTIALS']['api_secret_key'], config['CREDENTIALS']['access_token'], config['CREDENTIALS']['access_token_secret'])
auth = tweepy.OAuth1UserHandler(config['CREDENTIALS']['api_key'], config['CREDENTIALS']['api_secret_key'], config['CREDENTIALS']['access_token'], config['CREDENTIALS']['access_token_secret'])
api = tweepy.API(auth)
try:
    user = api.verify_credentials()
    print(f'Authentication {BC.OKGREEN}{BC.BOLD}OK{BC.RESET}')
    print(f'Logged in as {user.name} ({BC.OKBLUE}@{user.screen_name}{BC.RESET})')
except:
    print(f'{BC.FAIL}Error during authentication.\nCheck your CREDENTIALS in {BC.UNDERLINE}config.ini{BC.RESET}{BC.FAIL}.{BC.RESET}')

# get the limit of the api
print(f'{BC.HEADER}Getting the limit of the API...{BC.RESET}')
limit = api.rate_limit_status()
for i in limit['resources']:
    for j in limit['resources'][i]:
        #if remaining and limit is same
        if limit['resources'][i][j]['remaining'] != limit['resources'][i][j]['limit']:
            print(f'{j}: {BC.OKGREEN}{limit["resources"][i][j]["remaining"]}{BC.RESET}/{BC.OKCYAN}{limit["resources"][i][j]["limit"]}{BC.RESET}')

#Start the stream
stream = MyStream(bearer_token=config['CREDENTIALS']['bearer_token'])
print(f'{BC.HEADER}Trying to set rules for streaming...{BC.RESET}')
rules = stream.get_rules()

if len(rules.data) == 0:
    print(f'{BC.WARNING}No rules found, adding a rule...{BC.RESET}')
    stream.add_rules(tweepy.StreamRule(f'@{user.screen_name}'))
    print(f'Rule added.')
elif len(rules.data) == 1 and rules.data[0].value == f'@{user.screen_name}':
    print(f'Rule already exists, skipping...')
else:
    print(f'{BC.WARNING}More than one rule found, restoring rules.{BC.RESET}')
    for rule in rules.data:
        stream.delete_rules(rule.id)
    stream.add_rules(tweepy.StreamRule(f'@{user.screen_name}'))
    print(f'Rule has been restored.')

print(f'Setting rule for streaming {BC.OKGREEN}{BC.BOLD}OK{BC.RESET}')

print(f'{BC.HEADER}Trying to start streaming...{BC.RESET}')
# Start the stream
stream.filter(tweet_fields=["referenced_tweets"])

