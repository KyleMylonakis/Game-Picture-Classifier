import pandas as pd
import os
import game_name_scraper
import image_scraper_steam

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
        os.makedirs(download_path)


# Open games list as a pandas dataframe
games_df = pd.read_csv('top_100_games.csv')
#print(games_df.head())

pics_per_game = 10

all_games_url = []
#print(games_df.at[1,'App ID'])

for ii in range(0,games_df.shape[0]):
    #print(ii)
    game_id = str(games_df.at[ii,'App ID'])
    game_image_df = pd.DataFrame({'URLs':image_scraper_steam.scrape(game_id, pics_per_game)})
    games_df.to_csv(download_path + games_df.at[ii,'Game Names'].replace(" ", "_")+'.csv')
    print('Sucessfuly scraped game ID: ', game_id )

#print(len(all_games_url))
