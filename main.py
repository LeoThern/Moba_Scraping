import requests
import shutil
import json
import time
import os

from dota2match import Dota2Match
from opendota_client import OpendotaClient

OUTPUT_FOLDER = './output_folder/'

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
        local_match_ids = [int(filename.split('_')[0]) for filename in os.listdir(OUTPUT_FOLDER)]
        matches = [match for match in matches if not match.id in local_match_ids]
        print(f"Removed {total_len-len(matches)} local duplicates")
        print(f"Downloading remaining {len(matches)} replays")

        for i,match in enumerate(matches):
            print(i)
            od_client.fill_match_info(match)
            if match.is_older_than_a_week():
                continue
            download_match(match.replay_url, OUTPUT_FOLDER)

        time.sleep(10)

if __name__ == '__main__':
    main()
