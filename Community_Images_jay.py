import os
from lxml import html
from lxml import etree
import requests
import pandas as pd



# Get the last updated top 100 games on steam list
Game_df = pd.read_csv('/home/jay/Desktop/Codes/WebScrapping/Top100Games.csv')


#print( Game_df.head())

front_page = 'http://steamcommunity.com/app/'
back_page = '/screenshots/?p=1&browsefilter=mostrecent'
image_page = requests.get('http://steamcommunity.com/app/570/screenshots/?p=1&browsefilter=mostrecent')


#Create a list of the url for the games in the dataframe

Game_df['URLs'] = Game_df['Steam ID'].apply( lambda x:  front_page + str(int(x)) + back_page)

print( Game_df['URLs'].head())

#Game_df.to_csv('TestImages')

image_tree = html.fromstring(image_page.content)



Urls = image_tree.xpath('//img[@class = "apphub_CardContentPreviewImage"]/@src')

#
#
#
#
test_page1 = requests.get('http://steamcommunity.com/app/433340/homecontent/?userreviewsoffset=0&p=2&workshopitemspage=2&readytouseitemspage=2&mtxitemspage=2&itemspage=2&screenshotspage=2&videospage=2&artpage=2&allguidepage=2&webguidepage=2&integratedguidepage=2&discussionspage=2&numperpage=99&browsefilter=mostrecent&browsefilter=mostrecent&l=english&appHubSubSection=2&filterLanguage=default&searchText=&forceanon=1')
#test_page2 = requests.get('http://steamcommunity.com/app/433340/homecontent/?userreviewsoffset=0&p=3&workshopitemspage=3&readytouseitemspage=3&mtxitemspage=3&itemspage=3&screenshotspage=3&videospage=3&artpage=3&allguidepage=3&webguidepage=3&integratedguidepage=3&discussionspage=3&numperpage=10&browsefilter=mostrecent&browsefilter=mostrecent&appid=433340&appHubSubSection=2&appHubSubSection=2&l=english&filterLanguage=default&searchText=&forceanon=1')


tree1 = html.fromstring(test_page1.content)
#tree2 = html.fromstring(test_page2.content)


Urls1 = tree1.xpath('//img[@class = "apphub_CardContentPreviewImage"]/@src')
#Urls2 = tree2.xpath('//img[@class = "apphub_CardContentPreviewImage"]/@src')

print(len(Urls1))
#for x in Urls1:
#    if x in Urls2:
#        print( ':(')
#    else:
#        print('New') 


#
# 
#



testRLS = pd.DataFrame({'One': Urls1})
testRLS['Good'] = testRLS.duplicated(keep= False)
testRLS.to_csv('testRL')

#print(len(Urls1), len(Urls2))

#img_data = requests.get(Urls[0]).content
#with open('image_name.jpg', 'wb') as handler:
    #handler.write(img_data)


