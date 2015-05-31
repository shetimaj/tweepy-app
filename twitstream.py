from tweepy import Stream
from tweepy import OAuthHandler
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



m = Basemap(projection='mill', llcrnrlat=40, urcrnrlat=50,\
        llcrnrlon=-91, urcrnrlon=-75, resolution ='h')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.fillcontinents(color='#04BAE3', lake_color='#FFFFFF')
m.drawmapboundary(fill_color='#FFFFFF')


# Define Stream Listener to detect tweets. 
class listener(StreamListener):
    x = []
    y = []

    temp = [] 



    def on_status(self, status):
        if status.coordinates:
            print status.text
            print status.coordinates
            print("\n")
            coords  = status.coordinates
            latitude = coords['coordinates'][0]
            longitude = coords['coordinates'][1]
            xt,yt = m(latitude, longitude)
            self.x.append(xt)
            self.y.append(yt)
            m.plot(self.x, self.y, 'ro', markersize=5, alpha=.5)
            self.temp.extend([status.created_at, (status.text).encode('ascii', 'ignore'), status.coordinates['coordinates']])

            with open('streamlocationresults.csv', 'w') as f:
                f.write('Date,Text,Coordinates')
                writer = csv.writer(f)
                writer.writerow([self.temp])
            f.close()

        

Plotter = listener()
try:
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    twitterStream = Stream(auth, Plotter)
    twitterStream.filter(locations=[-92.29,40.64,-75.12,49.34])
    Plotter.plotAll()
except KeyboardInterrupt, e:
    plt.show()
