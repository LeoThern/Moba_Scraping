import requests
from dota2match import Dota2Match
from itertools import chain

class IncompleteDataException(Exception):
    pass

class OpendotaClient:
    def __init__(self, timeout=5):
        self.req_timeout = timeout #python/urllib requests sometimes load infinitely without timeout, after latest update??

    def get_json_request_with_retry(self, url, counter=0) -> dict:
        try:
            response = requests.get(url, timeout=self.req_timeout).json()
            return response
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
        try:
            match.start_time = response['start_time']
            match.replay_url = response['replay_url']
        except KeyError:
            raise IncompleteDataException
        else:
            return response

if __name__ == '__main__':
    Client = OpendotaClient()
    print(Client.get_pro_matches())
