##################################################################
# This program will take as input a Steam app_id and a postive
# integer and generate a database of urls of screenshots of images
# from the game off the Steam community forums
##################################################################

import os
from lxml import html
from lxml import etree
import requests
import pandas as pd
import sys

os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "raw_image_data/"

def main():
    # for testing purposes only
    scrape(243750,10)
def scrape(steam_app_id,num_requested):
    # Command line arguments
    #steam_app_id = str(sys.argv[1])
    #num_requested = int(sys.argv[2])
    steam_app_id = str(steam_app_id)
    #num_requested = int(num_requested)
    num_requested = 1750

    pages_to_load = int(num_requested/100) + 1

    url_list = []
    num_urls = 0

    for current_page_number in range(1,pages_to_load+1):
        try:
            current_page_number = str(current_page_number)
            current_page = 'https://steamcommunity.com/app/'+steam_app_id+'/homecontent/?userreviewsoffset=0&'
            current_page+= 'p='+current_page_number+'2&workshopitemspage='+current_page_number+'&readytouseitemspage='+current_page_number+'&mtxitemspage='+current_page_number+'&itemspage='+current_page_number
            current_page+= '&screenshotspage='+current_page_number+'&artpage='+current_page_number+'&allguidepage='+current_page_number+'&webguidepage='+current_page_number+'&integratedguidepage='+current_page_number+'&discussionspage='+current_page_number
            current_page+= '&numperpage=1000&browsefilter=trend&browsefilter=trend&l=english&appHubSubSection='+current_page_number+'&filterLanguage=default&searchText=&forceanon=1'
            #current_page = requests.get('http://steamcommunity.com/app/'+ steam_app_id +'/homecontent/?screenshotspage='+str(current_page_number)+'&numperpage=100&browsefilter=mostrecent&browsefilter=mostrecent&l=english&appHubSubSection=2&filterLanguage=default&searchText=&forceanon=1')
            print("Tick")
            current_page = requests.get(current_page)
            print("Tock")
            current_page_tree = html.fromstring(current_page.content)
            image_urls = current_page_tree.xpath('//img[@class = "apphub_CardContentPreviewImage"]/@src')
            #print(len(image_urls))
            current_page_number = int(current_page_number)
            if (current_page_number != pages_to_load):
                for url in image_urls:
                    url_list.append(url)
            else:
                for iii in range(0,num_requested % 100):
                    url_list.append(image_urls[iii])
        except etree.XMLSyntaxError:
            pass
    url_list = set(url_list)
    url_list = list(url_list)
    print("Images found " + str(len(url_list)))
    return(url_list)
    
if __name__ == "__main__":
    # For testing purposes only
    main()
