import argparse
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ReportRequest:
    code: str
    encounter: Optional[str]
    fights: List[str]

    def __init__(self, args: argparse.Namespace):
        self.code = args.report
        self.encounter = args.encounter
        self.fights = args.fights


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
