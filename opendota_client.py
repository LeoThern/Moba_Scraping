import requests
from dota2match import Dota2Match

class OpendotaClient:
    def __init__(self):
        pass

    def get_pro_matches(self):
        response = requests.get('https://api.opendota.com/api/proMatches').json()
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_high_elo_public_matches(self):
        min_rank = 60 #min rank of Ancient
        response = requests.get(f"https://api.opendota.com/api/publicMatches?min_rank={min_rank}").json()
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

if __name__ == '__main__':
    Client = OpendotaClient()
    print(Client.get_high_elo_public_matches())
