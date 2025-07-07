# Dota2 and LoL ML Experiments

This project was developed as part of my Bachelor's thesis. It focuses on the automated collection, parsing, and machine learning analysis of draft data from matches in two major MOBA games: Dota 2 and League of Legends (LoL).

## Overview
- **Scraping Dota 2 matches** from [OpenDota](https://www.opendota.com/) using custom Python scripts.
- **Scraping LoL matches** from the Riot API, targeting high and low elo games.
- **Parsing draft data** for both games, extracting picks, bans, and related metadata.
- **Testing clustering algorithms** on draft data to identify patterns and strategies.
- **Applying logistic regression models** with various features to predict match winners.

## Directory & File Structure

### Dota2/
- **opendota_scraping/**
  - `main.py`: Main entry point for scraping Dota 2 matches from OpenDota.
  - `opendota_client.py`: Handle requests to OpenDota REST API.
  - `dota2match.py`: Data structures for Dota 2 match data.
- **parsing/**
  - `parse_drafts.py`: Parses draft data from scraped Dota 2 matches using MatchIterator.
  - `MatchIterator.py`: Iterates and loads match data.
  - `curl_opendota_parser.py`: Client for local OpenDota Parser for advanced parsing.
- `requirements.txt`: Python dependencies for Dota 2 scraping and parsing.

### LoL/
- `scraper_highelo.py`: Scrapes high elo LoL matches from the Riot API.
- `scraper_lowelo.py`: Scrapes low elo LoL matches from the Riot API.
- `parser.py`: Parses draft and match data from LoL API responses.
- `requirements.txt`: Python dependencies for LoL scraping and parsing.

### Analysis/
- `DraftAnalysis_Bachelor.ipynb`: Main analysis notebook for draft data, clustering, and modeling.
- `Experiments.ipynb`: Condensed notebook of just the experiments and results present in my thesis.
- `joined_all_matches.json`, `all_lol_matches_highelo.json`, `all_low_lol_matches.json`: Raw match data for Dota2 and LoL.
- `champion.json`, `lol_classes.json`, `opendota_heroes.json`: Metadata for champions/heroes and classes.

## Research Goals
- Explore and compare drafting strategies in Dota 2 and LoL.
- Test clustering and visualization algorithms to group similar drafts or strategies.
- Build and evaluate logistic regression models to predict match outcomes based on draft features.

# Results
- The meta exists.
- Dota2 is a lot less balanced than LoL.
---
For more details, see the code and notebooks in each directory.
