#---------------------------------------------------------------------------------------------------------------------
#
#       GENERATE LIST OF IMAGE URL FOR TOP100GAMES
#       RETURNS DIRECTORY WITH FOLDERS FOR EACH GAME CONTAING A CSV OF IMAGE URLS AND A FOLDER OF DOWNLOADED IMAGES
#
#---------------------------------------------------------------------------------------------------------------------

"""
- hould be run with os argumetns: Num_games Num_scrolls Num_down. 
Otherwise provide these integers as a list.
- If Top100Games.csv does not exist Top100Games.py is called to create it.
- If they don't exist '/rawimages' is created and 'rawimages/game_name' directories are created 
for each game. 
- In 'rawimages/game_folder' a csv containing the URLs of images from the games steam community is created/updated.
- In 'rawimages/game_folder' '/downloads' is created.
- If the games steam community page is found Num_scrolls*Num_down images are saved in the downloads folder.abs
If not then the game's URL dataframe is updated with COMMUNITY NOT FOUND and the program continues 
 """



import os
from lxml import html
from lxml import etree
import requests
import pandas as pd
import Top100Games
import sys

def main(os_in = True, Nums = [5,2,10]):
    """ OS argumetns: Num_games Num_scrolls Num_down
    If os_in = False
    Nums: Default is set low for testing purposes.
    """
    # Set Parameters

    if os_in:
        Num_scrolls = int(sys.argv[2])    # Number of scrolls to call
        Num_games = int(sys.argv[1])    # Number of Games to use. Ordered by most popular)
        Num_down = int(sys.argv[3])    # Number of Games to Download
        #download = True   # Decides if images are downloaded. If False only URLs are updated
    
    else:
        Num_games,Num_scrolls,Num_down = Nums
    
    print('Games, Scrolls, Down')
    print(Num_games,Num_scrolls,Num_down)
    # Get the top Num_games info 

    if not os.path.isfile('Top100Games.csv'):
        Top100Games.main()
    
    Game_df = pd.read_csv('Top100Games.csv', nrows = Num_games)

    # Make a folder to hold all the game images.

    # Check if the folder is already there
    if not os.path.exists('rawimages'):
        os.makedirs('rawimages')

    if not os.path.exists('Top100Games.csv'):
        print('Creating Top 100 List...')
        Top100Games.main()

    for index,row in Game_df.iterrows():
        appID = int(row['STEAM ID'])
        name = row['GAME']

        print('Finding ', name)

        appID_str = str(appID)
        Num_scrolls_str = str(Num_scrolls)
        
        # Make a folder for each game in the rawimages folder
        # Folder name is appID to avoid nonsense names

        fold_name = str(appID)
        image_folder = 'rawimages/'+fold_name
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        
        # Loop through the number of scrolls

        for scroll in range(Num_scrolls):
            
            # Make the games url
            g_url = 'http://steamcommunity.com/app/'+ appID_str +'/homecontent/?screenshotspage='+str(scroll)+'&numperpage=100&browsefilter=mostrecent&browsefilter=mostrecent&l=english&appHubSubSection=2&filterLanguage=default&searchText=&forceanon=1'
            
            # NOT ALL PAGES HAVE A COMMUNITY
            # See if the page exists:
            try:
                # Request the page
                g_page = requests.get(g_url)

                print('Scroll %d ' % scroll )

                # Get the page and make the tree
                g_page = requests.get(g_url) 
                g_tree = html.fromstring(g_page.content)

                #Scrape for the sources of the images displayed
                g_img_urls = g_tree.xpath('//img[@class = "apphub_CardContentPreviewImage"]/@src')
                print('Found %d images to scrape' % len(g_img_urls))
           
                # Make a download folder inside the game folder

                # Changed to not add the unecessary downloads folder
                #new_folder = image_folder +'/downloads/'
                new_folder = image_folder
                
                # Check if it exists
                if not os.path.isdir(new_folder):
                    os.makedirs(new_folder)
                
                # Find the number of elements in the folder
                # index starts after that one.
                img_label = len(os.listdir(new_folder))

                go_to = min([len(g_img_urls),Num_down])

                for ii in range(go_to):
                    # Get the row data and then the image from its page
                    row_url = g_img_urls[ii]
                    img_data = requests.get(row_url).content

                    # Image name to save as appID_(Download number).jpg
                    image_name = appID_str+'_'+ str(ii+img_label)
                    
                    print('Downloading image '+str(ii))

                    # Write the image into its folder
                    with open(new_folder+'/'+ image_name +".jpg", 'wb') as handler:
                        handler.write(img_data)

    # IF the community does not exist
            except:
                print(name + ' community not found')

if __name__ == '__main__':
    main()
