import pandas as pd
import sys
sys.path.insert(0, "scraper/")
from player_data_driver import PlayerData


players_data = pd.ExcelFile('data/world_cup_2022_data/players_2022.xlsx')
new_data = pd.DataFrame()

non_2022_players: int = 0
for nation in players_data.sheet_names:
    print(nation)
    sheet_df = pd.read_excel(players_data, nation)
    # print(temp_df)
    nation_df = pd.DataFrame()
    for link in sheet_df["so_fifa_url"]:
        if isinstance(link, str):
            print(link)
            if link.find("202200") != -1:
                try:
                    player = PlayerData(link)
                    player_df = player.get_player_data()
                    nation_df = nation_df.append(player_df, ignore_index=True)
                except:
                    non_2022_players += 1
            else:
                # print(link)
                # raise ValueError("Link is not a 2022 player")
                non_2022_players += 1
        else:
            non_2022_players += 1
    print(nation_df)
    print()

    print(non_2022_players)


