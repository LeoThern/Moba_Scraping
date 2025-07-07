import json
import os
from dataclasses import dataclass

OUTPUT_FOLDER = './output_folder/' # output of scraper, i.e. input

@dataclass
class Match():
    match_id: str
    date: int
    duration: int
    blueside_win: bool
    team_comp: dict[str, tuple[int]]
    bans: list[dict]

def parse_team_comp(match_data_json):
    blueside, redside = {}, {}
    for player in match_data_json["info"]["participants"]:
        if player["teamId"] == 100:
            blueside[player["championId"]] = player['teamPosition']
        else:
            redside[player["championId"]] = player['teamPosition']
    team_comp = {"blueside": blueside, "redside": redside}
    return team_comp

def parse_draft(match_data_json):
    bans = {}
    bans['blueside'] = match_data_json['info']['teams'][0]['bans']
    bans['redside'] = match_data_json['info']['teams'][1]['bans']
    return bans

def main():
    all_data = []

    i = 0

    for folder in os.listdir(OUTPUT_FOLDER):
        for file in os.listdir(os.path.join(OUTPUT_FOLDER, folder)):
            i += 1
            print(f"Parsing Match {i}")
            match_data_json = json.load(open(os.path.join(OUTPUT_FOLDER, folder, file), "r"))
            match_id = file.split('.')[0]
            date = match_data_json['info']['gameCreation']
            duration = match_data_json['info']['gameDuration']
            blueside_win = match_data_json['info']['teams'][0]['win']
            if match_data_json['info']['teams'][0]['teamId'] != 100:
                raise Exception('blueside not first team')
            match = {'match_id':match_id,
                     'start_date':date,
                     'duration':duration,
                     'blueside_win':blueside_win,
                     'team_comp': parse_team_comp(match_data_json),
                     'bans': parse_draft(match_data_json)}
            all_data.append(match)

    with open("all_lol_matches.json",'w') as file:
        json.dump(all_data, file)


if __name__ == '__main__':
    main()