##################################################################
# This program generates a csv file named "top_100_games.csv"
# containing a Pandas dataframe of the top 100 most played games
# on steam.
###################################################################

from lxml import html
import requests
import pandas as pd

def main():

    page = requests.get('http://store.steampowered.com/stats/')
    tree = html.fromstring(page.content)

    #This will create a list of games:
    games = tree.xpath('//a[@class="gameLink"]/text()')
    app_id = tree.xpath('//a[@class="gameLink"]/@href')

    game_id = []

    count = 0
    for hyperlink in app_id:
        #print(games[count])
        count +=1
        num_slashes = 0
        steam_id = ''
        for i in range(0,len(hyperlink)):
            if hyperlink[i] == '/':
                num_slashes += 1
                i+=1
            elif num_slashes == 4:
                while (hyperlink[i] != '/') and (i < len(hyperlink)-1):
                    steam_id += hyperlink[i]
                    i+=1
                    if i == (len(hyperlink) - 1):
                        steam_id += hyperlink[i]
                        break
                num_slashes +=1
                game_id.append(steam_id)
                #print(hyperlink)
                break
            else:
                i+=1
    #print(game_id)
            
    #Save the list of games 
    games_df = pd.DataFrame({'Game Names': games, 'App ID': game_id})
    #print(games_df.head())
    games_df.to_csv('top_100_games.csv')
    print("List created")

    #print(games_df)

if __name__ == "__main__":
    main()