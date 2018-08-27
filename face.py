import twitter
import pprint
import json
from pprint import pprint
import mysql.connector
from mysql.connector import errorcode
import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from googleapiclient.discovery import build
from collections import Counter
from prettytable import PrettyTable
import matplotlib.pyplot as plt

WORLD_WOE_ID = 1


class TwitterClient(object):
    def __init__(self):
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_token_secret = ''
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))


def load():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)

    print(twitter_api)
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    print("-" * 171)
    print("\t\t\t\t\t\t\t\t\t\t World Trends")
    print("-" * 171)
    print('\n')

    count = 0
    for i in world_trends[0][u'trends']:
        print(i[u'name'])
        count = count + 1
        if count == 10:
            break

    ch = 1
    while ch != 2:
        print("-" * 171)
        print('\n\n 1) Login \n\n 2) Exit ')
        ch = input('\n\n Enter your choice : ')
        if ch == 1:
            login()
        elif ch == 2:
            print(' \n Sentiment Analyzer will now close .... ')
        else:
            print(' \n Wrong Choice Entered, Please try again .... ')


def add_user():
    try:
        cnx = mysql.connector.connect(user='root', password="", database='jatin')
        cursor = cnx.cursor()
        usen = str(input('Enter Username for the new user : '))
        passn = str(input('Enter Password for the new user : '))
        cursor.execute("""insert into jatin.login values(%s,%s)""", (usen, passn))
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


def view_user():
    try:
        use = []
        passes = []
        cnx = mysql.connector.connect(user='root', password="", database='jatin')
        query = "SELECT username,password from jatin.login"
        cursor = cnx.cursor()
        cursor.execute(query)
        for (username, password) in cursor:
            use.append(str(username))
            passes.append(str(password))

        print('\n\t\t Username \t\t Password')
        for i in use:
            print('\t\t' + i + '\t\t\t' + passes[use.index(i)])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


def del_user():
    try:
        view_user()
        cnx = mysql.connector.connect(user='root', password="", database='jatin')
        cursor = cnx.cursor()
        usen = str(input('Enter Username to delete : '))
        cursor.execute("delete from jatin.login where username='%s'" % usen)
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


def view_trends():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    print('\n World Trends : \n')
    for i in world_trends[0][u'trends']:
        print(i[u'name'])


def change_trends():
    global WORLD_WOE_ID
    WORLD_WOE_ID = int(input('Enter the WOEID to change the tweet trends : '))
    # US_WOE_ID = 23424977
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
    print('\n Altered Trends : \n')
    for i in world_trends[0][u'trends']:
        print(i[u'name'])


def admin():
    os.system('cls')
    print("-" * 171)
    print("\t\t\t\t\t\t\t\t\t\t Admin Menu")
    print("-" * 171)
    ch = 1
    while ch != 5:
        print(
            '\n\n \t 1) Add New User \n\n \t 2) View Users \n\n \t 3) Delete a User \n\n \t 4) Change Trends \n\n \t 5) Exit')
        ch = int(input('\n\n \t Enter your choice : '))
        if ch == 1:
            add_user()
        elif ch == 2:
            view_user()
        elif ch == 3:
            del_user()
        elif ch == 4:
            change_trends()
        elif ch == 5:
            print('\n\n About to exit admin menu')
        else:
            print('\n\n Wrong choice entered, Please try again')


def advance_analysis():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    q = str(input('Enter a Name to Search : '))
    count = int(input('\n Enter the number of tweets to fetch : '))
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']

    for _ in range(5):
        print "Length of statuses", len(statuses)
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:  # No more results when next_results doesn't exist
            break
        kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

    print('\n\n Sample JSON Metadata for a collected Tweet')
    #print json.dumps(statuses[0], indent=1)

    status_texts = [status['text']
                    for status in statuses]

    screen_names = [user_mention['screen_name']
                    for status in statuses
                    for user_mention in status['entities']['user_mentions']]

    hashtags = [hashtag['text']
                for status in statuses
                for hashtag in status['entities']['hashtags']]

    # Compute a collection of all words from all tweets
    words = [w
             for t in status_texts
             for w in t.split()]

    # Explore the first 5 items for each...
    print(' \n\n Texts From top 5 Tweets : ')
    print json.dumps(status_texts[0:5], indent=1)
    print(' \n\n User Names For top 5 Tweets : ')
    print json.dumps(screen_names[0:5], indent=1)
    print(' \n\n Hashtags From top 5 Tweets : ')
    print json.dumps(hashtags[0:5], indent=1)
    print(' \n\n Collection of the words collected from the tweets : ')
    print json.dumps(words[0:5], indent=1)

    for item in [words, screen_names, hashtags]:
        c = Counter(item)
        print c.most_common()[:10]  # top 10
        print

    for label, data in (('Word', words),
                        ('Screen Name', screen_names),
                        ('Hashtag', hashtags)):
        pt = PrettyTable(field_names=[label, 'Count'])
        c = Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[:10]]
        pt.align[label], pt.align['Count'] = 'l', 'r'  # Set column alignment
        print pt

    def lexical_diversity(tokens):
        return 1.0 * len(set(tokens)) / len(tokens)

    # A function for computing the average number of words per tweet
    def average_words(statuses):
        total_words = sum([len(s.split()) for s in statuses])
        return 1.0 * total_words / len(statuses)

    print('\n\n Lexical Diversity in Words : ')
    print lexical_diversity(words)
    print('\n\n Lexical Diversity in Screen Names : ')
    print lexical_diversity(screen_names)
    print('\n\n Lexical Diversity in Hashtags : ')
    print lexical_diversity(hashtags)
    print('\n\n Lexical Diversity in Status Texts : ')
    print average_words(status_texts)

    retweets = [
        # Store out a tuple of these three values ...
        (status['retweet_count'],
         status['retweeted_status']['user']['screen_name'],
         status['text'])

        # ... for each status ...
        for status in statuses

        # ... so long as the status meets this condition.
        if status.has_key('retweeted_status')
    ]

    # Slice off the first 5 from the sorted results and display each item in the tuple

    pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
    [pt.add_row(row) for row in sorted(retweets, reverse=True)[:5]]
    pt.max_width['Text'] = 50
    pt.align = 'l'
    print pt

    print('\n\n Top Retweeters for the Tweet : ')
    retweets1 = twitter_api.statuses.retweets(id=317127304981667841)
    print [str(r['user']['screen_name']) for r in retweets1]

    word_counts = sorted(Counter(words).values(), reverse=True)

    for label, data in (('Words', words), ('Screen Names', screen_names), ('Hashtags', hashtags)):
        c = Counter(data)
        plt.hist(c.values())

        plt.title(label)
        plt.ylabel("Number of items in bin")
        plt.xlabel("Bins (number of times an item appeared)")

        plt.figure()
        plt.show()
        # plt.ion()


def analyze_tweets():
    api = TwitterClient()
    q = input('Enter a Name to Search : ')
    tweets = api.get_tweets(query=q, count=1000)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("\n\n \t Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("\n\n \t Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    print("\n\n \t Neutral tweets percentage: {} %".format(
        100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
    print("\n\n Positive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    print("\n\n Negative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


def search_tweet():
    api = TwitterClient()
    q = str(input('Enter a Name to Search : '))
    nu = int(input('\n Enter the number of tweets to fetch : '))
    tweets = api.get_tweets(query=q, count=nu)
    for tweet in tweets:
        print('\n')
        print(tweet['text'])


def extend_search():
    my_api_key = ""
    my_cse_id = ""

    def google_search(search_term, api_key, cse_id, **kwargs):
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
        # pprint.pprint(res)
        return res['items']

    que = str(input('\n Enter a search keyword to extend search to the Web : '))
    results = google_search(que, my_api_key, my_cse_id, num=10)

    for result in results:
        pprint.pprint(result)


def user():
    os.system('cls')
    print("-" * 171)
    print("\t\t\t\t\t\t\t\t\t\t User Menu")
    print("-" * 171)
    ch = 1
    while ch != 6:
        print(
            '\n\n \t 1) View Trends \n\n \t 2) Search Trends \n\n \t 3) Extensive Search \n\n \t 4) Analyze Tweet Stats \n\n \t 5) Advanced Tweet Analysis \n\n \t 6) Exit')
        ch = int(input('\n\n \t Enter your choice : '))
        if ch == 1:
            view_trends()
        elif ch == 2:
            search_tweet()
        elif ch == 3:
            extend_search()
        elif ch == 4:
            analyze_tweets()
        elif ch == 5:
            advance_analysis()
        elif ch == 6:
            print('\n\n About to exit admin menu')
        else:
            print('\n\n Wrong choice entered, Please try again')


def login():
    use = []
    passes = []
    try:
        cnx = mysql.connector.connect(user='root', password="", database='jatin')
        query = "SELECT username,password from jatin.login"
        cursor = cnx.cursor()
        cursor.execute(query)
        for (username, password) in cursor:
            use.append(str(username))
            passes.append(str(password))
        usename = str(input('Enter Username : '))
        passw = str(input('Enter Password : '))
        if usename in use:
            if passw == passes[use.index(usename)]:
                if usename == 'Admin':
                    admin()
                else:
                    user()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


# for i in us_trends[0][u'trends']:
#    print('\n')
#    print(i[u'name'])


def main():
    load()
    

main()

# us_trends = twitter_api.trends.place(_id=US_WOE_ID)

# print(world_trends)
# print ' \n'
# print us_trends

# print(json.dumps(world_trends, indent=1))
# print('\n')
# print(json.dumps(us_trends, indent=1))
# print('\n')
