import tweepy
import json
import os
import time

from math import ceil

import matplotlib.pyplot as plt


with open(os.path.join(os.path.dirname(__file__), "credentials", "twitter.json")) as jf:
    creds = json.load(jf)


oauth = tweepy.OAuthHandler(creds['api_key'], creds['api_secret'])
oauth.set_access_token(creds['access_key'], creds['access_secret'])
api =  tweepy.API(oauth)

timestamps = {}

class TwitterStream(tweepy.StreamListener):
    def __init__(self, time_limit=30):
        self.start_time = time.time()
        self.limit = time_limit
        super(TwitterStream, self).__init__()
    def on_status(self, status):
        global timestamps
        if (time.time() - self.start_time) < self.limit:
            ts = status.created_at.strftime("%H:%M:%S")
            if ts in timestamps: timestamps[ts] += 1
            else: timestamps[ts] = 1
        else:
            make_plot()
            api.update_with_media("trump_tracker.png", status="Trump Tracker:")
            self.start_time = time.time()
            timestamps = {}

    def on_error(self, status_code):
        if status_code == 420:
            return False


def make_plot():
    global timestamps
    keys = list(timestamps)
    keys.sort()

    x = [key for key in keys]
    y = [int(timestamps[key]) for key in x]


    plt.plot(x, y, 'b-')
    ticks = plt.gca().xaxis.get_major_ticks()

    for i in range(len(ticks)):
        if i % ceil(len(ticks) / 10) != 0:
            ticks[i].set_visible(False)

    plt.gcf().autofmt_xdate()
    plt.gca().set_ylim([0, max(y)+5]) #set y range to scale correctly

    plt.title("Trump Tracker")
    plt.xlabel("Time")
    plt.ylabel("Trumps")
    plt.savefig("trump_tracker.png")

keyword_streamer = tweepy.Stream(auth=api.auth, listener=TwitterStream(time_limit=60))
keyword_streamer.filter(track=['donald', 'trump'], is_async=True, stall_warnings=True)


if __name__ == '__main__':
    pass
