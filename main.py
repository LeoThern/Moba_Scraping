import datetime
import requests
import shutil
import json
import time
import os

from dota2match import Dota2Match
from opendota_client import OpendotaClient
from opendota_client import IncompleteDataException

OUTPUT_FOLDER = './output_folder/'

def get_local_ids_last_week() -> set:
    def last_seven_days():
        today = datetime.date.today()
        for i in range(7):
            date = today - datetime.timedelta(days=i)
            yield date.strftime('%d_%m_%Y/')

    ids = []
    for day in last_seven_days():
        folder = os.path.join(OUTPUT_FOLDER, day)
        if os.path.exists(folder):
            ids.extend([int(file.split('.')[0]) for file in os.listdir(folder) if '.json' in file])
    return set(ids)

def download_match(url:str, out_path:str):
    out_file = os.path.join(out_path, url.split('/')[-1])
    with requests.get(url, stream=True, allow_redirects=True) as r:
        with open(file=out_file, mode='wb') as f:
            shutil.copyfileobj(r.raw, f)


def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    od_client = OpendotaClient()
    while True:
        matches = od_client.get_all_matches()

        print(f"Found {len(matches)} matches on OpenDota")
        total_len = len(matches)
        local_match_ids = get_local_ids_last_week()
        matches = [match for match in matches if not match.id in local_match_ids]
        print(f"Removed {total_len-len(matches)} local duplicates")
        print(f"Downloading remaining {len(matches)} replays")

        for i, match in enumerate(matches):
            print(i)
            try:
                full_info = od_client.fill_match_info(match)
            except IncompleteDataException:
                print(f"OpenDota provides no replay_url for {match.id}")
                continue
            if match.is_older_than_a_week():
                print(f"Match {match.id} is older than a week, replay not available anymore")
                continue

            date = datetime.datetime.fromtimestamp(match.start_time)
            date_folder = date.strftime("%d_%m_%Y/")
            folder_path = os.path.join(OUTPUT_FOLDER, date_folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            download_match(match.replay_url, folder_path)
            with open(os.path.join(folder_path, f"{match.id}.json"), 'w') as out_file:
                json.dump(full_info, out_file, indent=4)

        time.sleep(60*60)

if __name__ == '__main__':
    main()
