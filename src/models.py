import argparse
from dataclasses import dataclass
from typing import List, Optional

from src.constants import ENCOUNTER


@dataclass
class ReportRequest:
    code: str
    name: Optional[str]
    encounter: Optional[int]
    fights: List[str]
    type: str

    def __init__(self, args: argparse.Namespace):
        self.code = args.report
        self.fights = args.fights
        self.type = args.type

        if args.name is not None:
            self.name = args.name
            self.encounter = ENCOUNTER.get_id(args.name)
        elif args.encounter is not None:
            self.encounter = args.encounter
            self.name = ENCOUNTER.get_name(args.encounter)
        else:
            self.name = None
            self.encounter = None


@dataclass
class Fight:
    name: str
    encounter_id: int
    kill: Optional[bool]
    difficulty: Optional[int]
    boss_percentage: Optional[float]
    average_item_level: Optional[float]


@dataclass
class Report:
    fights: List[Fight]
