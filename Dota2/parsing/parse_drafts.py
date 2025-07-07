import pickle
import json

from MatchIterator import MatchIterator

def count_comps():
	drafts = []

	folder = "E:\\output_folder"
	#folder = "/run/media/leo/Volume/output_folder"
	match_iterator = MatchIterator(folder)
	total = len(match_iterator)

	possible_modes = dict()

	faulty_matches = 0
	unparsed_matches = 0
	short_matches = 0

	for i, match in enumerate(match_iterator):
		if not match:
			print(f"Game NOT OD PARSED {i:5} of {total} ({(i/total)*100:3.2f}% - {len(match_iterator)} left)")
			unparsed_matches += 1
			continue
		print(f"Game {match.match_id} {i:5} of {total} ({(i/total)*100:3.2f}% - {len(match_iterator)} left)")
		
		elo = 'high_elo' if match.high_elo else 'low_elo'
		if (elo,match.lobby_type, match.game_mode) in possible_modes:
			possible_modes[(elo,match.lobby_type, match.game_mode)] += 1
		else:
			possible_modes[(elo,match.lobby_type, match.game_mode)] = 1
		
		if not match.draft:
			faulty_matches += 1
			continue

		if match.duration < 600:
			short_matches += 1

		draft = {
			'match_id':match.match_id,
			'patch':match.patch,
			'radiant_win':match.radiant_win,
			'duration':match.duration,
			'high_elo':match.high_elo,
			'lobby_type':match.lobby_type,
			'game_mode':match.game_mode,
			'leavers':match.leavers,
			'draft':match.draft,
			'team_comp':match.team_comp,
		}
		drafts.append(draft)

	with open('all_drafts.json', 'w') as file:
		json.dump(drafts, file)
	print(f"Faulty Drafts {faulty_matches}")
	print(f"Unparsed Matches {unparsed_matches}")
	print(f"Matches under 10 min {short_matches}")
	print(possible_modes)

def main():
	#Total count: 15291
	#es gibt 38 Comps die 2 Mal gespielt worden, sonst nur einzigartige
	count_comps()
	#with open('team_comp_counter.pickle', 'rb') as file:
	#	team_comp_counter = pickle.load(file)
	

if __name__ == "__main__":
	main()

"""
{('low_elo', 'lobby_type_ranked', 'game_mode_all_draft'): 6002, 
('low_elo', 'lobby_type_normal', 'game_mode_all_draft'): 820, 
('low_elo', 'lobby_type_normal', 'game_mode_single_draft'): 258, 
('low_elo', 'lobby_type_ranked', 'game_mode_random_draft'): 84, 
('high_elo', 'lobby_type_normal', 'game_mode_all_draft'): 680, 
('high_elo', 'lobby_type_practice', 'game_mode_captains_mode'): 2733, 
('high_elo', 'lobby_type_ranked', 'game_mode_all_draft'): 11025, 
('high_elo', 'lobby_type_normal', 'game_mode_single_draft'): 174, 
('high_elo', 'lobby_type_ranked', 'game_mode_random_draft'): 170, 
('high_elo', 'lobby_type_practice', 'game_mode_all_pick'): 30, 
('low_elo', 'lobby_type_normal', 'game_mode_random_draft'): 3, 
('high_elo', 'lobby_type_battle_cup', 'game_mode_captains_mode'): 34, 
('high_elo', 'lobby_type_practice', 'game_mode_random_draft'): 2, 
('high_elo', 'lobby_type_normal', 'game_mode_random_draft'): 5, 
('high_elo', 'lobby_type_practice', 'game_mode_single_draft'): 1, 
('high_elo', 'lobby_type_practice', 'game_mode_all_draft'): 1}
"""