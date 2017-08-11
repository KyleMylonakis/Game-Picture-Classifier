###############################################################
# Script to automate the URL database generation
# Takes as input the number of games to be in the database
# and the max number of images per game as command line
# arguments.
###############################################################


import pandas as pd
import os
import game_name_scraper
import image_scraper_steam
import sys 

os.environ["PATH"] += os.pathsep + os.getcwd()


# Detect whether games list exists or needs to be created
# in the current directory
print("Does list of games exist?")
if not os.path.exists("top_100_games.csv"):
    print("No. Creating File")
    game_name_scraper.main()
else:
    print("CSV Already Exists")

# Create folder to house csv files of urls
download_path ='game_urls/'
if not os.path.exists(download_path):
        print("Folder for URLs does not exist: Creating folder")
        os.makedirs(download_path)
        print("Folder created")
else:
    print("Folder for URLs exists. No need to create folder")



# Open games list as a pandas dataframe
games_df = pd.read_csv('top_100_games.csv')
#print(games_df.head())

pics_per_game = int(sys.argv[2])

#
number_of_games = int(sys.argv[1])
if number_of_games > games_df.shape[0]:
    print("Too many games requested. Defaulting to the top 5 games.")
    number_of_games = 5

for ii in range(0,number_of_games):
    #print(ii)
    game_id = str(games_df.at[ii,'App ID'])
    game_image_df = pd.DataFrame({'URLs':image_scraper_steam.scrape(game_id, pics_per_game)})
    game_image_df.to_csv(download_path + games_df.at[ii,'Game Names'].replace(" ", "_")+'.csv')
    print('Sucessfuly scraped game ID: ', game_id )

print("Database generated.")
#print(len(all_games_url))
