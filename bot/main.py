import tweepy
import os
import time
from dotenv import load_dotenv

load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True)##the object api in a way communicates with twitter being able to read from and write to it

##REMEMBER TO MAKE CHANGES IF REQIRED TO THE TEXT FILE BEFORE RUNNING


def get_all_tweets(tweet):
    screen_name = tweet.user.screen_name
    lastTweetId = tweet.id
    #initialize a list to hold all the tweepy Tweets
    allTweets = []
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    allTweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    oldest = allTweets[-1].id - 1
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and oldest >= lastTweetId:
        print(f"getting tweets before {oldest}")
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        #save most recent tweets
        allTweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest =allTweets[-1].id - 1
        print(f"...{len(allTweets)} tweets downloaded so far")
    outtweets = [tweet.id for tweet in allTweets]
    return outtweets

def getAllTweetsInThreadAfterThis(tweetId):
    thread = []
    hasReply = True
    res = api.get_status(tweetId, tweet_mode='extended')
    allTillThread = get_all_tweets(res)
    thread.append(res)
    if allTillThread[-1] > res.id:
        print("Not able to retrieve so older tweets")
        return thread
    print("downloaded required tweets")
    startIndex = allTillThread.index(res.id)
    print("Finding useful tweets")
    quietLong = 0
    while startIndex!=0 and quietLong<25:
        nowIndex = startIndex-1
        nowTweet = api.get_status(allTillThread[nowIndex], tweet_mode='extended')
        if nowTweet.in_reply_to_status_id == thread[-1].id:
            quietLong = 0
            #print("Reached a useful tweet to be included in thread")
            thread.append(nowTweet)
        else:
            quietLong = quietLong + 1
        startIndex = nowIndex
    return thread

def getAllTweetsInThreadBeforeThis(tweetId):
    thread = []
    hasReply = True
    res = api.get_status(tweetId, tweet_mode='extended')
    while res.in_reply_to_status_id is not None:##as long as the thread doesnt end
        res = api.get_status(res.in_reply_to_status_id, tweet_mode='extended')
        thread.append(res)
    return thread[::-1]

def getAllTweetsInThread(tweetId):
    tweetsAll = []
    print("Getting all tweets before this tweet")
    tweetsAll = getAllTweetsInThreadBeforeThis(tweetId)
    print(len(tweetsAll))
    print("Getting all tweets after this tweet")
    tweetsAll.extend(getAllTweetsInThreadAfterThis(tweetId))
    return tweetsAll

def printAllTweet(tweets):
    if len(tweets)>0:
        print("Thread Messages include:-")
        for tweetId in range(len(tweets)):
            print(str(tweetId+1)+". "+tweets[tweetId].full_text)
            print("")
    else:
        print("No Tweet to print")

def dm(tweets,sname):##DM function
  if len(tweets)>0:
    print("DMing..")
    message=""
    ##message = message + sname.author.name + "\n" ##tweets from
    u=api.get_user(sname.user.screen_name)##fetching the user tag name
    for t in range(len(tweets)):
      message= message+ str(t+1)+". "+tweets[t].full_text +"\n"
      
    api.send_direct_message(recipient_id=u.id_str,text=message)##everything in 1 mssg
  else:
    print("Nothing to dm")


def retrieve():##reads from txt

  f=open("id.txt","r")
  last=int(f.read().strip())
  f.close()
  return last

def store(lt):##writes on txt

  q=open("id.txt","w")
  q.write(str(lt))
  q.close()
  
while True:##start of main loop
  l=retrieve()
  
  mentions=api.mentions_timeline(l,tweet_mode="extended",count=200)##testing
  if len(mentions)>0:##looking for mentions
    
    mentions=mentions[::-1]##respond to older tweets first
    for m in mentions:
      ##print(len(mentions),type(mentions),vars(m))
      h=m.full_text.lower()
      check=h.find("unroll")##looking for keyword
      if check>0:
        print("Responding...")
        store(m.id)
        ##calling necessary functions

        if __name__ == '__main__':

          j=m.in_reply_to_status_id
          TweetId = str(m.in_reply_to_status_id)
          ##the difference maker right here
          
          if j != None:
            ##if the bot is simply called instead of being tagged as a reply to a thread

          
            
            allTweets = getAllTweetsInThread(TweetId)
            printAllTweet(allTweets)
            ##time.sleep(15)
            dm(allTweets,m)##additional parameter?
            
          ## api.send_direct_message(recipient_id=mentions[0].id,text=allTweets)##other parameters are attachment type and media
          else:
            o=api.get_user(m.user.screen_name)
            
            
            api.send_direct_message(recipient_id=o.id_str,text="Please choose a thread and try again.\nFor instructions check out my bio")##everything in 1 mssg
            time.sleep(5)

  else:
    time.sleep(15)
    continue

  

  


  



