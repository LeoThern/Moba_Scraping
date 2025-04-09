from riotwatcher import LolWatcher, ApiError
import datetime
import json
import os
import random
import time

OUTPUT_FOLDER = './output_folder_low_elo/'
riot_api_key = ""

class Custom_LolWatcher:
    def __init__(self, riot_api_key):
        self.lol_watcher = LolWatcher(riot_api_key)
        self.region = 'euw1'
        self.queue = 'RANKED_SOLO_5x5'

    def get_low_elo_players(self, sample_size=1000):
        tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']
        divisions = ['I', 'II', 'III', 'IV']
        all_entries = []

        # Collect players from all low elo tiers
        for tier in tiers:
            for division in divisions:
                print(f"Getting {tier}, {division}")
                page = 1
                while True:
                    try:
                        entries = self.lol_watcher.league.entries(
                            region=self.region,
                            queue=self.queue,
                            tier=tier,
                            division=division,
                            page=page
                        )
                        all_entries.extend(entries)
                        if not entries or page >= 5:
                            break
                        page += 1
                    except ApiError as e:
                        if e.response.status_code == 429:
                            retry_after = int(e.response.headers.get('Retry-After', 1))
                            time.sleep(retry_after)
                        else:
                            raise

        # Convert to PUUIDs
        puuids = [entry['puuid'] for entry in all_entries]

        random.shuffle(puuids)
        sampled_puuids = puuids[:sample_size]

        return sampled_puuids

    def get_last_100_soloqueue_ranked_games(self, puuid):
        return self.lol_watcher.match.matchlist_by_puuid(
            region=self.region,
            puuid=puuid,
            count=100,
            queue=420,
            type='ranked'
        )

    def get_match_data(self, match_id):
        return self.lol_watcher.match.by_id(
            region=self.region,
            match_id=match_id
        )

def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    LoLAPI = Custom_LolWatcher(riot_api_key)

    print("Fetching low elo players...")
    player_puuids = LoLAPI.get_low_elo_players()
    print(f"Found {len(player_puuids)} players")

    all_matches = set()

    # Collect matches from sampled players
    for i, puuid in enumerate(player_puuids):
        print(f"Processing player {i+1}/{len(player_puuids)}")
        try:
            matches = LoLAPI.get_last_100_soloqueue_ranked_games(puuid)
            all_matches.update(matches)
        except ApiError as e:
            print(f"Error getting matches: {e}")
            continue

    # Download and save matches
    total_count = len(all_matches)
    for i, match_id in enumerate(all_matches):
        print(f"Downloading match {i+1}/{total_count}")
        try:
            match_data = LoLAPI.get_match_data(match_id)
            date = datetime.datetime.fromtimestamp(match_data['info']['gameCreation'] / 1000)
            date_folder = date.strftime("%d_%m_%Y/")
            folder_path = os.path.join(OUTPUT_FOLDER, date_folder)
            os.makedirs(folder_path, exist_ok=True)
            
            with open(os.path.join(folder_path, f"{match_id}.json"), 'w') as out_file:
                json.dump(match_data, out_file, indent=4)
        except ApiError as e:
            print(f"Error downloading match {match_id}: {e}")

if __name__ == '__main__':
    main()