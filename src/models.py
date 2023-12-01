import argparse
from dataclasses import dataclass
from typing import Optional

from src.constants import ENCOUNTER


@dataclass
class ReportRequest:
    code: str
    name: Optional[str]
    encounter_id: Optional[int]
    fight_ids: list[int]
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

    def is_between(self, start_time, end_time) -> bool:
        return start_time <= self.time <= end_time


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
    death_events: list[DeathEvent]

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

    def deaths_between(self, start_time, end_time) -> list[DeathEvent]:
        start_time -= self.start_time
        end_time -= self.start_time
        return [death for death in self.death_events if death.is_between(start_time, end_time)]


@dataclass
class Report:
    fights: list[Fight]
    actors: dict[int, str]
    actor_ids: dict[str, int]

    def __init__(self, fights, actors):
        self.fights = fights
        self.actors = actors
        self.actor_ids = {actor: id for id, actor in actors.items()}
