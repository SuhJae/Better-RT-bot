# Better-RT-bot
### A better retweet bot that will retweet tweets containing a specific keyword.
![](https://img.shields.io/pypi/pyversions/tweepy?style=flat-square)
![](https://img.shields.io/github/license/SuhJae/Better-RT-bot?style=flat-square)

This Twitter bot will retweet tweets that contain a specific keyword. It uses twitter's tweet stream API to get tweets in real time, making it more efficient than the search API run between a set interval.

## Requirements
* [Python 3.7+](https://www.python.org/downloads/)

**Python packages**

* [Tweepy](https://pypi.org/project/tweepy/) (`pip install tweepy`)

## Setup
1. Clone this repository. (`git clone https://github.com/SuhJae/Better-RT-bot.git`)
2. Create a Twitter app and get your API keys and tokens from [here](https://developer.twitter.com/en/apps).
3. Edit the `config.ini` file with your API keys and tokens.
4. Edit the `config.ini` file with your desired keyword.
5. Run the bot. (`python bot.py`)