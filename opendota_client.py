import requests
from dota2match import Dota2Match
from itertools import chain

class OpendotaClient:

    def get_pro_matches(self) -> list[Dota2Match]:
        response = requests.get('https://api.opendota.com/api/proMatches', timeout=5).json()
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_high_elo_public_matches(self, min_rank = 60) -> list[Dota2Match]:
        #min_rank = 60, equals a minimum rank of Ancient https://docs.opendota.com/#tag/public-matches
        response = requests.get(f"https://api.opendota.com/api/publicMatches?min_rank={min_rank}",timeout=5).json()
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_all_matches(self) -> list[Dota2Match]:
        pro_matches = self.get_pro_matches()
        high_elo_matches = self.get_high_elo_public_matches()
        return list(chain(pro_matches, high_elo_matches))

    def fill_match_info(self, match:Dota2Match) -> None:
        #TODO handle possibly missing replay_url
        url = f"https://api.opendota.com/api/matches/{match.id}"
        response = requests.get(url, timeout=5).json()
        match.start_time = response['start_time']
        match.replay_url = response['replay_url']


if __name__ == '__main__':
    Client = OpendotaClient()
    print(Client.get_pro_matches())
