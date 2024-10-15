from dataclasses import dataclass
from datetime import datetime

@dataclass
class Dota2Match:
    """Keep info about a specific Dota2 Match"""
    id: str
    start_time: int = -1
    replay_url: str = ''

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def is_older_than_a_week(self):
        assert self.start_time > 0, "Match start_time is missing"
        age = datetime.now() - datetime.fromtimestamp(self.start_time)
        if age.days > 7:
            return True
        return False
