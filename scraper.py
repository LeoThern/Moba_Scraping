import requests
import shutil
import json
import time
import os


def get_ids() -> list[str]:
    pass

def get_match_info(id:str) -> dict:
    url = f"https://api.opendota.com/api/matches/{id}"
    response = requests.get(url).json()
    info = {
        'id':id,
        'start_time':response['start_time'],
        'replay_url':response['replay_url']
    }
    return info

def download_match(url:str, out_path:str):
    out_file = os.path.join(out_path, url.split('/')[-1])
    with requests.get(url, stream=True, allow_redirects=True) as r:
        with open(file=out_file, mode='wb') as f:
            shutil.copyfileobj(r.raw, f)


def main():
    while True:
        ids = get_ids()
        for id in ids:
            info = get_match_info(id)
            download_match(info['replay_url'], './output_folder/')
        time.sleep(60*60)

if __name__ == '__main__':
    main()
