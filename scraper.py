import requests as r
import json
import time


def get_ids() -> list[str]:
    pass

def download_match(id:str, path:str):
    pass

def main():
    while True:
        ids = get_ids()
        for id in ids:
            download_match(id, './output_folder/')
        time.sleep(60*60)

if __name__ == '__main__':
    main()
