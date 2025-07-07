import requests
import time
import datetime
from itertools import chain

from dota2match import Dota2Match

class MatchNotParsedException(Exception):
    pass

class DailyRateLimitExhaustedException(Exception):
    pass

class OpendotaClient:
    def __init__(self, timeout=5, proxies=[]):
        requests.packages.urllib3.util.connection.HAS_IPV6 = False #opendota needs ipv4, times out for ipv6
        self.req_timeout = timeout
        self.proxies = proxies

    def get_json_request_with_retry(self, url, counter=0) -> dict:
        try:
            response = requests.get(url, timeout=self.req_timeout)
        except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
            time.sleep(5)
            if counter > 2:
                print('Internet connection seems to be lost, press ENTER to retry')
                input()
            return self.get_json_request_with_retry(url, counter + 1)
        else:
            if int(response.headers["X-Rate-Limit-Remaining-Minute"]) <= 1:
                current_second = datetime.datetime.now().second
                remaining_seconds = 60 - current_second
                time.sleep(remaining_seconds + 1)
            if int(response.headers["X-Rate-Limit-Remaining-Day"]) <= 10:
                raise DailyRateLimitExhaustedException
            if response.status_code == 500:
                return self.get_json_request_with_retry(url, counter + 1)
            if response.status_code != 200:
                #unknown error
                print(response, response.text)
                input()
            return response.json()

    def get_pro_matches(self) -> list[Dota2Match]:
        response = self.get_json_request_with_retry('https://api.opendota.com/api/proMatches')
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_public_matches(self, min_rank = None, max_rank = None) -> list[Dota2Match]:
        min_rank = min_rank if min_rank else 0
        max_rank_param = f"&max_rank={max_rank}" if max_rank else ""
        response = self.get_json_request_with_retry(f"https://api.opendota.com/api/publicMatches?min_rank={min_rank}{max_rank_param}")
        matches = [Dota2Match(m['match_id'], m['start_time']) for m in response]
        return matches

    def get_high_elo_matches(self) -> list[Dota2Match]:
        pro_matches = self.get_pro_matches()
        #min_rank = 60, equals a minimum rank of Ancient https://docs.opendota.com/#tag/public-matches
        high_elo_matches = self.get_public_matches(min_rank=60)
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
        except requests.exceptions.RequestException:
            pass

if __name__ == '__main__':
    Client = OpendotaClient()
    print(Client.get_pro_matches())
