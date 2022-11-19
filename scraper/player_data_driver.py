from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


target_values = {"overall_ranking": 0, "potential": 1, "ID": 4 ,"position": 6, "attacking": 7, "skill": 8, "movement": 9, "power": 10, "mentality": 11, "defending": 12, "goalkeeping": 13}
keys_list = list(target_values.keys())
values_list = list(target_values.values())


class PlayerData:
    def __init__(self, player_url):
        self.player_url: str = player_url
        self.player_dict: dict = {}

    def _scrap_player_data(self) -> dict:
        page = requests.get(self.player_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        name: str = soup.find('div', class_='info').h1.text
        self.player_dict["long_name"] = name

        meta_data = soup.find_all('div', class_='meta ellipsis')
        height_expression = re.compile(r'\d+cm')
        height = height_expression.findall(meta_data[0].text)
        height = height[0][:-2]
        self.player_dict["height_cm"] = height

        weight_expresoion = re.compile(r'\d+kg')
        weight = weight_expresoion.findall(meta_data[0].text)
        weight = weight[0][:-2]
        self.player_dict["weight_kg"] = weight

        age_expression = re.compile(r'\d+')
        age = age_expression.findall(meta_data[0].text)
        self.player_dict["age"] = age[0]

        for i, block in enumerate(soup.find_all('div', class_='block-quarter')):
            if i == 0:
                overall_ranking = block.find_all('span', class_='bp3-tag')
                self.player_dict["overall"] = overall_ranking[0].text

            if i == 1:
                potential = block.find_all('span', class_='bp3-tag')
                self.player_dict["potential"] = potential[0].text

            if i == 4:
                ID = block.find_all('li', class_='ellipsis')
                ID = ID[7].text[2:]
                self.player_dict["sofifa_id"] = ID


            if i == 6:
                position = block.find_all('span', class_='pos')
                self.player_dict["nation_position"] = position[0].text
                nationality = block.find_all('a')
                self.player_dict["nationality_name"] = nationality[0].text

            attacking_list: list = []
            if i == 7:
                attacking = block.find_all('span', class_='bp3-tag')
                for i in attacking:
                    attacking_list.append(int(i.text))
                self.player_dict["attacking_crossing"] = attacking_list[0]
                self.player_dict["attacking_finishing"] = attacking_list[1]
                self.player_dict['attacking_heading_accuracy'] = attacking_list[2]
                self.player_dict["attacking_short_passing"] = attacking_list[3]
                self.player_dict["attacking_volleys"] = attacking_list[4]

            skill_list: list = []
            if i == 8:
                skill = block.find_all('span', class_='bp3-tag')
                for i in skill:
                    skill_list.append(int(i.text))
                self.player_dict["skill_dribbling"] = skill_list[0]
                self.player_dict["skill_curve"] = skill_list[1]
                self.player_dict['skill_fk_accuracy'] = skill_list[2]
                self.player_dict["skill_long_passing"] = skill_list[3]
                self.player_dict["skill_ball_control"] = skill_list[4]

            movement_list: list = []
            if i == 9:
                movement = block.find_all('span', class_='bp3-tag')
                for i in movement:
                    movement_list.append(int(i.text))
                self.player_dict["movement_acceleration"] = movement_list[0]
                self.player_dict["movement_sprint_speed"] = movement_list[1]
                self.player_dict['movement_agility'] = movement_list[2]
                self.player_dict["movement_reactions"] = movement_list[3]
                self.player_dict["movement_balance"] = movement_list[4]

            power_list: list = []
            if i == 10:
                power = block.find_all('span', class_='bp3-tag')
                for i in power:
                    power_list.append(int(i.text))
                self.player_dict["power_shot_power"] = power_list[0]
                self.player_dict["power_jumping"] = power_list[1]
                self.player_dict['power_stamina'] = power_list[2]
                self.player_dict["power_strength"] = power_list[3]
                self.player_dict["power_long_shots"] = power_list[4]

            mentality_list: list = []
            if i == 11:
                mentality = block.find_all('span', class_='bp3-tag')
                for i in mentality:
                    mentality_list.append(int(i.text))
                self.player_dict["mentality_aggression"] = mentality_list[0]
                self.player_dict["mentality_interceptions"] = mentality_list[1]
                self.player_dict['mentality_positioning'] = mentality_list[2]
                self.player_dict["mentality_vision"] = mentality_list[3]
                self.player_dict["mentality_penalties"] = mentality_list[4]

            defending_list: list = []
            if i == 12:
                defending = block.find_all('span', class_='bp3-tag')
                for i in defending:
                    defending_list.append(int(i.text))
                self.player_dict["defending_marking_awareness"] = defending_list[0]
                self.player_dict["defending_standing_tackle"] = defending_list[1]
                self.player_dict['defending_sliding_tackle'] = defending_list[2]

            goalkeeping_list: list = []
            if i == 13:
                goalkeeping = block.find_all('span', class_='bp3-tag')
                for i in goalkeeping:
                    goalkeeping_list.append(int(i.text))
                self.player_dict["goalkeeping_diving"] = goalkeeping_list[0]
                self.player_dict["goalkeeping_handling"] = goalkeeping_list[1]
                self.player_dict["goalkeeping_kicking"] = goalkeeping_list[2]
                self.player_dict["goalkeeping_positioning"] = goalkeeping_list[3]
                self.player_dict["goalkeeping_reflexes"] = goalkeeping_list[4]


    def get_player_data(self) -> pd.DataFrame:
        self._scrap_player_data()
        data_frame = pd.DataFrame(self.player_dict, index=[0])

        return data_frame
        