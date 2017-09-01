###############################################################
# Script to automate the image database generation
# Takes as input the number of games to be in the database
# and the max number of images per game as command line
# arguments.
###############################################################

import os
import game_name_scraper
#import image_scraper_steam
import sys 
#import generate_database
import requests
import pandas as pd

os.environ["PATH"] += os.pathsep + os.getcwd()

def main():

    print("Does list of games exist?")
    if not os.path.exists("top_100_games.csv"):
        print("No. Creating File")
        game_name_scraper.main()
    else:
        print("CSV Already Exists")

    # Create folder to house csv files of urls
    url_path ='game_urls/'
    if not os.path.exists(url_path):
        print("Folder for URLs does not exist: Please run generate_database.py first")
    else:
        print("Folder for URLs exists. Proceeding")

    download_path ='game_images/'
    if not os.path.exists(url_path):
        print("Image Database Directory Successfuly created")
            




    # Open games list as a pandas dataframe
    games_df = pd.read_csv('top_100_games.csv')
    #print(games_df.head())

    pics_per_game = int(sys.argv[2])
    if not pics_per_game > 0:
        print("Invalid input: Defaulting to 100 pictures") 
        pics_per_game = 100

    #
    number_of_games = int(sys.argv[1])
    if number_of_games > games_df.shape[0]:
        print("Too many games requested. Defaulting to the top 5 games.")
        number_of_games = 5

    for ii in range(0,number_of_games):
        #print(ii)
        game_df = pd.read_csv(url_path + games_df.at[ii,'Game Names'].replace(" ", "_").replace(":", "-")+'/' + games_df.at[ii,'Game Names'].replace(" ", "_").replace(":", "-")+'.csv')
        #print(game_df.head())
        num_pics = 0
        for url in game_df['URLs']:
            if not os.path.exists(download_path +'/raw_images/' + games_df.at[ii,'Game Names'].replace(" ", "_").replace(":", "-")):
                print('Creating Raw Image Folder')
                os.makedirs(download_path +'/raw_images/' + games_df.at[ii,'Game Names'].replace(" ", "_").replace(":", "-"))
            if num_pics < pics_per_game:
                img_url = url
                img = requests.get(img_url).content
                with open(download_path +'/raw_images/' + games_df.at[ii,'Game Names'].replace(" ", "_").replace(":", "-") +'/' +str(num_pics), 'wb' ) as handler:
                    handler.write(img)
                num_pics +=1
                print("Downloaded image " + str(num_pics) + " of " + str(pics_per_game) + " for " + games_df.at[ii,'Game Names'])
            else:
                break
        print("All requested " + games_df.at[ii,'Game Names'] + " images downloaded")


    print("Database generated.")
    #print(len(all_games_url))

if __name__ == '__main__':
    main()