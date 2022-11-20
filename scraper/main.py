import pandas as pd
import sys
import logging
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, "scraper/")
from player_data_driver import PlayerData

FORMAT = '%(asctime)s --> %(message)s'
logging.basicConfig(filename = 'scraping_logs.log', level = logging.DEBUG, format=FORMAT)

players_data = pd.ExcelFile('data/world_cup_2022_data/players_2022.xlsx')
players2022_worldCup_df = pd.DataFrame()

non_2022_players: int = 0
for nation in players_data.sheet_names:
    print(nation)
    sheet_df = pd.read_excel(players_data, nation)
    nation_df = pd.DataFrame()
    for link in sheet_df["so_fifa_url"]:
        if not isinstance(link,str):
            continue
        if link.find("202200") == -1:
            splitted_link = link.split("/")
            link = splitted_link[0] + '//' + splitted_link[2] + '/' + splitted_link[3]  + '/' + splitted_link[4] + '/' + splitted_link[5] + '/' + "202200"
        
        print(link)
        player = PlayerData(link)
        player_df = player.get_player_data()
        nation_df = nation_df.append(player_df, ignore_index=True)

        logging.info(f"Link ✅: {link}")
    
    logging.info(f"INFO: Players scraped for {nation}: {nation_df.shape[0]}")
   
    players2022_worldCup_df = players2022_worldCup_df.append(nation_df, ignore_index=True)
   
    logging.info(f"INFO: Current total players scraped: {players2022_worldCup_df.shape[0]}...")

logging.info(f"Players_df ✅: Done scraping => Total players scraped: {players2022_worldCup_df.shape[0]}")

print(players2022_worldCup_df)
players2022_worldCup_df.to_excel("data/world_cup_2022_data/players_worldcup_2022.xlsx", index=False)
players2022_worldCup_df.to_csv("data/world_cup_2022_data/players_worldcup_2022.csv", index=False)

logging.info(f"Export excel & csv ✅: Players data exported")