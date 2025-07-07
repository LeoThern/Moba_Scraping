import os
import json
from datetime import datetime
from dataclasses import dataclass

game_modes = {0: 'game_mode_unknown', 1: 'game_mode_all_pick', 2: 'game_mode_captains_mode', 3: 'game_mode_random_draft', 4: 'game_mode_single_draft', 5: 'game_mode_all_random', 6: 'game_mode_intro', 7: 'game_mode_diretide', 8: 'game_mode_reverse_captains_mode', 9: 'game_mode_greeviling', 10: 'game_mode_tutorial', 11: 'game_mode_mid_only', 12: 'game_mode_least_played', 13: 'game_mode_limited_heroes', 14: 'game_mode_compendium_matchmaking', 15: 'game_mode_custom', 16: 'game_mode_captains_draft', 17: 'game_mode_balanced_draft', 18: 'game_mode_ability_draft', 19: 'game_mode_event', 20: 'game_mode_all_random_death_match', 21: 'game_mode_1v1_mid', 22: 'game_mode_all_draft', 23: 'game_mode_turbo', 24: 'game_mode_mutation', 25: 'game_mode_coaches_challenge'}
lobby_types = {0: 'lobby_type_normal', 1: 'lobby_type_practice', 2: 'lobby_type_tournament', 3: 'lobby_type_tutorial', 4: 'lobby_type_coop_bots', 5: 'lobby_type_ranked_team_mm', 6: 'lobby_type_ranked_solo_mm', 7: 'lobby_type_ranked', 8: 'lobby_type_1v1_mid', 9: 'lobby_type_battle_cup', 10: 'lobby_type_local_bots', 11: 'lobby_type_spectator', 12: 'lobby_type_event', 13: 'lobby_type_gauntlet', 14: 'lobby_type_new_player', 15: 'lobby_type_featured'}

@dataclass
class Match():
	match_id: str
	path: str
	radiant_win: bool
	team_comp: dict[str, tuple[int]]
	draft: list[dict]
	high_elo: bool
	avg_elo: str
	game_mode: str
	lobby_type: str

def parse_team_comp(match_data_json):
	radiant, dire = set(), set()
	for player in match_data_json["players"]:
		if player["isRadiant"]:
			radiant.add(player["hero_id"])
		else:
			dire.add(player["hero_id"])
	team_comp = {"radiant": tuple(radiant), "dire": tuple(dire)}
	return team_comp

def parse_draft(match_data_json):
	draft = []
	try:
		picks_bans = match_data_json["picks_bans"]
	except KeyError:
		return None
	for pick_ban in picks_bans:
		team = "radiant" if pick_ban["team"] == 0 else "dire"
		draft_type = "pick" if pick_ban["is_pick"] else "ban"
		draft.append((f"{team}_{draft_type}",pick_ban["hero_id"]))
	return draft

def clean_draft(draft, team_comp):
	#remove bans and faulty picks from draft
	clean_draft = []
	for item in draft:
		action = item[0]
		hero_id = item[1]
		if "radiant" in action:
			if hero_id in team_comp['radiant']:
				clean_draft.append(item)
		else:
			if hero_id in team_comp['dire']:
				clean_draft.append(item)
	return clean_draft

def parse_avg_elo(match_data_json):
	if match_data_json["leagueid"] > 0:
		return 100
	elos = []
	for player in match_data_json["players"]:
		if rank := player["rank_tier"]:
			elos.append(rank)
	if not elos:
		return 0
	avg_elo = sum(elos) / len(elos)
	return avg_elo

class MatchIterator:
	def __init__(self, path, start_day=None, end_day=None): 
		self.base_path = path
		self.available_days = list(os.listdir(self.base_path))
		self.available_matches = []

		# Convert input dates to datetime objects for comparison if provided
		start_date = datetime.strptime(start_day, "%d.%m.%Y") if start_day else None
		end_date = datetime.strptime(end_day, "%d.%m.%Y") if end_day else None

		join = lambda *paths: os.path.join(*paths)
		for day in self.available_days:
			day_date = datetime.strptime(day, "%d_%m_%Y")  # Convert folder name to date

			# Check if the day is within the optional start_day and end_day filters
			if (not start_date or day_date >= start_date) and (not end_date or day_date <= end_date):
				for match in os.listdir(join(self.base_path, day)):
					if match.endswith(".json"):
						self.available_matches.append(join(self.base_path, day, match))

	def __iter__(self):
		return self

	def __next__(self):
		if not self.available_matches:
			raise StopIteration
		
		match_path = self.available_matches.pop(0)
		try:
			match_data_json = json.load(open(match_path, "r"))
		except json.decoder.JSONDecodeError as e:
			raise Exception(f"while parsing {match_path} :\n{e}")
		else:
			match_id = match_data_json["match_id"]
			radiant_win = match_data_json['radiant_win']
			team_comp = parse_team_comp(match_data_json)
			draft = parse_draft(match_data_json)
			if draft:
				draft = clean_draft(draft, team_comp)
			avg_elo = parse_avg_elo(match_data_json)
			high_elo = False
			if avg_elo >= 60:
				high_elo = True
			if avg_elo == 100:
				high_elo = True
				avg_elo = "professional_league"
			avg_elo = str(avg_elo)
			game_mode = game_modes[match_data_json['game_mode']]
			lobby_type = lobby_types[match_data_json['lobby_type']]
			return Match(match_id, match_path, radiant_win, team_comp, draft, high_elo, avg_elo, game_mode, lobby_type)

	def __len__(self):
		return len(self.available_matches)


def main():
	folder = "E:\\output_folder"
	for match in MatchIterator(folder):
		print(match)

if __name__ == "__main__":
	main()
