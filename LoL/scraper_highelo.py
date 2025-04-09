from riotwatcher import LolWatcher
import datetime
import json
import os

OUTPUT_FOLDER = './output_folder/'
riot_api_key = ""

class Custom_LolWatcher:
    def __init__(self, riot_api_key):
        self.lol_watcher = LolWatcher(riot_api_key)

    def get_top1000_players(self):
        challengers = self.lol_watcher.league.challenger_by_queue(region='euw1', queue='RANKED_SOLO_5x5')['entries']
        grand_masters = self.lol_watcher.league.grandmaster_by_queue(region='euw1', queue='RANKED_SOLO_5x5')['entries']
        return challengers + grand_masters

    def get_last_100_soloqueue_ranked_games(self, puuid):
        matches = self.lol_watcher.match.matchlist_by_puuid(region='euw1', 
                                                            puuid=puuid, 
                                                            count=100,
                                                            queue=420, #https://static.developer.riotgames.com/docs/lol/queues.json
                                                            type='ranked',)
        return matches

    def get_match_data(self, match_id):
        return self.lol_watcher.match.by_id(region='euw1', match_id=match_id)


def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    LoLAPI = Custom_LolWatcher(riot_api_key)

    top_1000 = LoLAPI.get_top1000_players()

    all_matches = set()

    for i, player in enumerate(top_1000):
        print(f"Getting Matches for Player {i+1} of 1000")
        matches = LoLAPI.get_last_100_soloqueue_ranked_games(puuid=player['puuid'])
        all_matches.update(matches)

    total_count = len(all_matches)

    for i, match_id in enumerate(all_matches):
        print(f"Downloading match {i+1} of {total_count}")
        match_data = LoLAPI.get_match_data(match_id=match_id)
        date = datetime.datetime.fromtimestamp(match_data['info']['gameCreation'] / 1000) #lol uses milisecond timestamps
        date_folder = date.strftime("%d_%m_%Y/")
        folder_path = os.path.join(OUTPUT_FOLDER, date_folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(os.path.join(folder_path, f"{match_id}.json"), 'w') as out_file:
            json.dump(match_data, out_file, indent=4)


if __name__ == '__main__':
    main()