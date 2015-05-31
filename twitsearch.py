import tweepy
from tweepy import Stream, OAuthHandler, Cursor
from tweepy.streaming import StreamListener
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import time
import json
from HTMLParser import HTMLParser
import csv


ckey = 'xHPB5wMHmxP5KNzV2brbdfCp6' #private
csecret = 'F7qCZ5Vrm0mzZs5IERziZAcRLygV5vqolGlhWkdGZswjGeghbA'
atoken = '185044419-nu83wmFcwdrZHwqhZDrIWMSeprJhsyHC82Ao2vJQ'
asecret = '368hMVnP7AnNVnvsfHyuCQNxSjnZgYKvu3HAk37WLc875'

#Create map template to display tweet locations
m = Basemap(projection='merc', llcrnrlat=30, urcrnrlat=50,\
        llcrnrlon=-100, urcrnrlon=-70, resolution ='c')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF')
m.drawmapboundary(fill_color='#FFFFFF')

#define Twitter Search function
def TwitSearch(search_terms):
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth)

    x = []          #objects to plot and save tweet information
    y = []
    temp = []
    twits = tweepy.Cursor(api.search, q=search_terms).items(400)
    for tweet in twits:
        if tweet.coordinates:
            print tweet.coordinates['coordinates']
            print tweet.text
            print("\n")
            ln = tweet.coordinates['coordinates'][0]
            lt = tweet.coordinates['coordinates'][1]
            
            xt,yt = m(ln, lt)               
            x.append(xt)
            y.append(yt)
            m.plot(x, y, 'g^', markersize=8)
            temp.extend([tweet.created_at, (tweet.text).encode('ascii', 'ignore'), tweet.coordinates['coordinates']])

            with open('searchresults.csv', 'w') as f:
                f.write('Date,Text,Coordinates')
                writer = csv.writer(f)
                writer.writerow(temp)

            f.close()
            
        pass

    plt.show()    



TwitSearch(["april", "spring", "weather"])
