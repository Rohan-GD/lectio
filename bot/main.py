import tweepy
from dotenv import load_dotenv
from fpdf import FPDF

import os

load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

search_words = "israel"+" -filter:retweets"
date_since = "2021-3-1"
# Collect tweets
# tweets = tweepy.Cursor(api.search,
#               q=search_words,
#               lang="en",
#               since=date_since).items(5)

# Iterate and print tweets
#print([tweet.text for tweet in tweets])
# user_loc = [[tweet.user.screen_name,tweet.user.location] for tweet in tweets]
# print(user_loc)
# tweet_text = pd.DataFrame(data = user_loc, columns=["user","location"])
# print(tweet_text)
# user = api.get_user('twitter')
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

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
    while res.in_reply_to_status_id is not None:
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
def generate_list(tweets):
    a = []
    if len(tweets)>0:
        print("Thread Messages include:-")
        for tweetId in range(len(tweets)):
            a.append(str(tweetId+1)+". "+tweets[tweetId].full_text)
    return a

# def check_emojis(elts):
#     for elt in elts:
#         for c in elt:
#             try:
#                 c = c.decode('utf-8')
#             except UnicodeDecodeError:
#                 pass
#     return NameObject(c)
#     return elts
# def list_to_str(l):
  
#     # using list comprehension
#     listToStr = ' '.join(map(str, l))
  
#     return listToStr
def generate_pdf(elts):
    pdf = FPDF()
    # Add a page
    pdf.add_page()
    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Arial", size = 10)
    i =1
    for elt in elts:
        pdf.cell(200, 10, txt = elt,ln = i, align = 'C')
        i +=1
    # save the pdf with name .pdf
    pdf.output("tweets.pdf")   


if __name__ == '__main__':
  tweetId = '1393545179479511042' #'1393971490912014340'
  allTweets = getAllTweetsInThread(tweetId)
  printAllTweet(allTweets)
  list_of_elts = generate_list(allTweets)
  print(list_of_elts)
  generate_pdf(list_of_elts)