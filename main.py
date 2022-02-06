import os
import discord
import tweepy
from keepItAlive import keepAlive
from discord.ext import commands
from threading import Thread
from discord.utils import find
import time

client = discord.Client() 
token = os.getenv('token')
intents = discord.Intents.all()
intents.members = True
lastTweet = None
firstRun = True
channelIdentity = 0
channelSet = False

client = commands.Bot(command_prefix='&', intents=intents)

#Tells us if the bot is up and running in console 
@client.event 
async def on_ready():
  print ('We have logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(guild):
  embed=discord.Embed(title="VT Alerts Forwarder", url="https://github.com/mbrenn07/VTAlertsForwarding#readme", description = "use &setThisChannel to set the bot's alerts to output in that channel", color=discord.Color.green())
  await guild.text_channels[0].send(embed=embed)

#Basic interactive in channel 
@client.event
async def on_message(message):
	if message.content.startswith('&utProsim'):
		embed = discord.Embed(title = "ut prosim", url = "https://give.vt.edu/giving-societies/ut-prosim-society.html", description = "that I may serve! go hokies!", color = discord.Color.gold())
		channel = message.channel
		await channel.send(embed=embed)
	if message.content.startswith('&setThisChannel'):
			global channelIdentity
			channelIdentity = message.channel
			embed=discord.Embed(title="channel set", url="", description = "the channel has been set", color=discord.Color.green())
			channel = message.channel
			await channel.send(embed=embed)
	if message.content.startswith('&help'):
		embed=discord.Embed(title="help", url="https://github.com/mbrenn07/VTAlertsForwarding#readme", description = """
		- use &latest @[handle] to get the latest tweet of the specified account
    
    - use &setThisChannel to use the bot in this channel 

		- use &utProsim to display your hokie pride
		""", color=discord.Color.green())
		channel = message.channel
		await channel.send(embed=embed)
	if message.content.startswith('&latest @'):
		tempUsername = message.content[9:]
		tempTweets = api.user_timeline(screen_name= tempUsername, tweet_mode = "extended")
		embed=discord.Embed(title=tempUsername + " tweet", url="https://twitter.com", description = tempTweets[0].full_text, color=discord.Color.magenta())
		channel = message.channel
		await channel.send(embed=embed)
	elif message.content.startswith('&latest'):
		channel = message.channel
		await channel.send("what is the twitter handle you would like the latest message of?, use &latest @[handle]")
    
# Twitter Keys
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')

search_words = "#virginia tech"

tweets = tweepy.Cursor(api.search_tweets,
              q=search_words,
              lang="en").items(20)

tweets_copy = []
for tweet in tweets:  
    tweets_copy.append(tweet)

print("Total Tweets Fetched:", len(tweets_copy))

async def printHelper(tmp):
	if channelIdentity != 0:
		await client.wait_until_ready()
		channel = channelIdentity # channel ID goes here
		embed=discord.Embed(title="vt alerts tweet", url="https://twitter.com/vtalerts?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor", description = tmp, color=discord.Color.orange())
		await channel.send(embed=embed)

def get_tweets(username):
	global lastTweet
	global firstRun
	tweets = api.user_timeline(screen_name= username, tweet_mode = "extended")
	if not lastTweet == tweets[0] and not firstRun:
		client.loop.create_task(printHelper(tweets[0].full_text))
	lastTweet = tweets[0]
	firstRun = False


class BackgroundTimer(Thread):
	def run(self):
		while 1:
			get_tweets("mgbparrot")
			time.sleep(60)

timer = BackgroundTimer()
timer.start() 

keepAlive()
client.run(token)