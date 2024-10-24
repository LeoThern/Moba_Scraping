import requests
import time
from itertools import chain

from dota2match import Dota2Match

class MatchNotParsedException(Exception):
    pass

class OpendotaClient:
    def __init__(self, timeout=5, proxies=[]):
        self.req_timeout = timeout #python/urllib requests sometimes load infinitely without timeout, after latest update??
        self.proxies = proxies

    def get_json_request_with_retry(self, url, counter=0) -> dict:
        try:
            response = requests.get(url, timeout=self.req_timeout)
            if response.status_code != 200:
                #free uses expired?
                print(response, response.text)
                input()
            return response.json()
        except requests.exceptions.Timeout:
            if counter > 2:
                print('Internet connection seems to be lost, press ENTER to retry')
                input()
            return self.get_json_request_with_retry(url, counter + 1)

    def get_pro_matches(self) -> list[Dota2Match]:
        response = self.get_json_request_with_retry('https://api.opendota.com/api/proMatches')
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_high_elo_public_matches(self, min_rank = 60) -> list[Dota2Match]:
        #min_rank = 60, equals a minimum rank of Ancient https://docs.opendota.com/#tag/public-matches
        response = self.get_json_request_with_retry(f"https://api.opendota.com/api/publicMatches?min_rank={min_rank}")
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_all_matches(self) -> list[Dota2Match]:
        pro_matches = self.get_pro_matches()
        high_elo_matches = self.get_high_elo_public_matches()
        return list(chain(pro_matches, high_elo_matches))

    def fill_match_info(self, match:Dota2Match) -> dict:
        response = self.get_json_request_with_retry(f"https://api.opendota.com/api/matches/{match.id}")
        match.start_time = response['start_time']
        try:
            match.replay_url = response['replay_url']
        except KeyError:
            self.request_parse(match.id)
            raise MatchNotParsedException
        else:
            return response

    def request_parse(self, match_id:int) -> None:
        try:
            requests.post(url=f"https://api.opendota.com/api/request/{match_id}",timeout=self.req_timeout)
        except requests.exceptions.Timeout:
            pass

if __name__ == '__main__':
    Client = OpendotaClient()
    print(Client.get_pro_matches())
