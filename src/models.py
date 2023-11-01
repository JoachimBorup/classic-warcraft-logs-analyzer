import argparse
from dataclasses import dataclass
from typing import List, Optional

from src.constants import ENCOUNTER


@dataclass
class ReportRequest:
    code: str
    name: Optional[str]
    encounter_id: Optional[int]
    fight_ids: List[int]
    kill_type: str

    def __init__(self, args: argparse.Namespace):
        self.code = args.report
        self.fight_ids = args.fights
        self.kill_type = args.type.capitalize()

        if args.name is not None:
            self.name = args.name
            self.encounter_id = ENCOUNTER.get_id(args.name)
        elif args.encounter is not None:
            self.encounter_id = args.encounter
            self.name = ENCOUNTER.get_name(args.encounter)
        else:
            self.name = None
            self.encounter_id = None


@dataclass
class DeathEvent:
    name: str
    time: int
    ability_name: str

    def __init__(self, json):
        self.name = json['name']
        self.time = json['deathTime']
        self.ability_name = json['ability']['name']


@dataclass
class Fight:
    id: int
    name: str
    encounter_id: int
    start_time: int
    end_time: int
    kill: Optional[bool]
    difficulty: Optional[int]
    boss_percentage: Optional[float]
    average_item_level: Optional[float]
    death_events: List[DeathEvent]

    def __init__(self, json, death_events):
        self.id = json['id']
        self.name = json['name']
        self.encounter_id = json['encounterID']
        self.start_time = json['startTime']
        self.end_time = json['endTime']
        self.kill = json['kill']
        self.difficulty = json['difficulty']
        self.boss_percentage = json['bossPercentage']
        self.average_item_level = json['averageItemLevel']
        self.death_events = death_events


@dataclass
class Report:
    fights: List[Fight]
