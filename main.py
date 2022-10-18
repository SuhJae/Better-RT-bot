import configparser
import threading
import tweepy
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
    # check if the tweet is a retweet
    newline = '\n'
    if tweet.text.startswith('RT @'):
        # print(f'{BC.FAIL}[RT]{BC.OKBLUE}{BC.WARNING} {(tweet.text.replace("RT @", "")).replace(newline, "")}{BC.RESET}')
        pass
    else:
        if tweet.text.startswith('@'):
            print(f'{BC.FAIL}[RE]{BC.OKBLUE}{BC.WARNING} {tweet.text.replace(newline, "")}')
        else:
            # check if tweet includes more than 3 newlines
            if tweet.text.count(newline) > 4:
                print(f'{BC.OKCYAN}[SP]{BC.OKBLUE}{BC.FAIL} {tweet.text.replace(newline, "")}')
            else:
                #fetch the tweet
                tweet = api.get_status(tweet.id)
                # check if user has more than 30 followers
                if tweet.user.followers_count > 30:
                    print(f'{BC.OKGREEN}[OK]{BC.RESET} {tweet.text.replace(newline, "")}')
                    #like and retweet the tweet
                    tweet.favorite()
                    tweet.retweet()
                else:
                    print(f'{BC.OKCYAN}[FL]{BC.OKBLUE}{BC.FAIL} {tweet.text.replace(newline, "")}')

    return None

class MyStream(tweepy.StreamingClient):
    def on_connect(self):
        print(f'Stream connection {BC.BOLD}{BC.OKGREEN}OK{BC.RESET}')
        print(f'Time took on setup: {BC.BOLD}{BC.OKGREEN}{round((time.time() - start) * 1000):,}ms{BC.RESET}')
        print('=============== Stream started ===============')

    def on_tweet(self, tweet):
        # execute the process_tweet function in a thread, so it doesn't block the stream
        threading.Thread(target=process_tweet, args=(tweet,)).start()

    def on_disconnect(self):
        print(f'Stream connection {BC.BOLD}{BC.FAIL}DISCONNECTED{BC.RESET}')
        stream.disconnect()

    def on_on_limit(self, notice):
        print(f'{BC.BOLD}{BC.WARNING}Limit notice: {notice}{BC.RESET}')

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

# Set rule for the stream
local_rules = config['STREAM']['keyword'].split(', ')

stream = MyStream(bearer_token=config['CREDENTIALS']['bearer_token'])
print(f'{BC.HEADER}Trying to set rules for streaming...{BC.RESET}')
rules = stream.get_rules()

server_rules = []
for i in range(len(rules.data)):
    server_rules.append(rules.data[i].value)

print(f'Rules on server:{BC.OKCYAN} {f"{BC.RESET}, {BC.OKCYAN}".join(i for i in server_rules)}{BC.RESET}')
print(f'Rules set on local:{BC.OKCYAN} {f"{BC.RESET}, {BC.OKCYAN}".join(i for i in local_rules)}{BC.RESET}')

#check if the rules are the same
if local_rules == server_rules:
    print(f'Rule already exists, skipping...')
else:
    if len(rules.data) != 0:
        print(f'{BC.WARNING}Rules are different, deleting old rules and adding new rules...{BC.RESET}')
        for rule in rules.data:
            stream.delete_rules(rule.id)
    else:
        print(f'{BC.WARNING}No rules found, adding new rules...{BC.RESET}')

    for i in range(len(local_rules)):
        stream.add_rules(tweepy.StreamRule(local_rules[i]))
    print('Rules restored')

print(f'Setting rule for streaming {BC.OKGREEN}{BC.BOLD}OK{BC.RESET}')
print(f'{BC.HEADER}Trying to start streaming...{BC.RESET}')

# Start the stream
stream.filter(tweet_fields=["referenced_tweets"])

