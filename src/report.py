import time
from collections import Counter, defaultdict

from src import graphql
from src.models import Fight, Report, ReportRequest


def analyze(request: ReportRequest):
    analyzer = ReportAnalyzer(request)
    analyzer.analyze()


def get_report(request: ReportRequest) -> Report:
    print(f"Retrieving report {request.code} from Warcraft Logs...")
    start_time = time.time()
    report = graphql.get_report(request)
    print(f"Retrieved report {request.code} after {time.time() - start_time:.2f} seconds!\n")
    return report


class ReportAnalyzer:
    def __init__(self, request: ReportRequest):
        self.request = request
        self.report = get_report(request)

    def analyze(self):
        fights = self.report.fights
        if len(fights) == 0:
            print("No fights found matching the given criteria.")
            return

        print(f"Report consists of {len(fights)} fights:")
        for fight in fights:
            mode = "Heroic" if fight.difficulty == 4 else "Normal"
            if fight.kill:
                print(f"Killed {fight.name} ({mode}):")
            else:
                print(f"Wiped on {fight.name} ({mode}) at {fight.boss_percentage}%:")

            self.analyze_fight(fight)

    def analyze_fight(self, fight: Fight):
        if fight.name == 'Lady Deathwhisper':
            self.analyze_lady_deathwhisper(fight)
        self.analyze_deaths(fight)

    def analyze_lady_deathwhisper(self, fight: Fight):
        vengeful_shade_actor_id = self.report.actor_ids['Vengeful Shade']
        vengeful_shade_events = graphql.get_actor_events(self.request, vengeful_shade_actor_id, fight)
        vengeful_shade_casts = [event for event in vengeful_shade_events if event['type'] == 'cast']
        if len(vengeful_shade_casts) == 0:
            return

        common_target_ids = Counter(cast['targetID'] for cast in vengeful_shade_casts).most_common()
        damage_caused = defaultdict(int)
        deaths_caused = defaultdict(int)
        current_target_id = None

        # Compute damage dealt by each explosion
        for event in vengeful_shade_events:
            if event['type'] == 'cast':
                current_target_id = event['targetID']
            elif event['type'] == 'damage':
                damage_caused[current_target_id] += event['amount']

        # Compute deaths caused by each explosion
        for i, cast in enumerate(vengeful_shade_casts):
            start_time = cast['timestamp']
            end_time = vengeful_shade_casts[i + 1]['timestamp'] if i + 1 < len(vengeful_shade_casts) else fight.end_time
            deaths_caused[cast['targetID']] += len([death for death in fight.deaths_between(start_time, end_time)
                                                    if death.ability_name == 'Vengeful Blast'])

        print('- Vengeful Shade explosions:')
        for target_id, count in common_target_ids:
            deaths = deaths_caused[target_id]
            print(f"  - {self.report.actors[target_id]}: hit {count} time{'' if count == 1 else 's'}, "
                  f"causing {damage_caused[target_id]} damage and {deaths} death{'' if deaths == 1 else 's'}")

    @staticmethod
    def analyze_deaths(fight: Fight):
        death_events = fight.death_events
        if len(death_events) == 0:
            print('- No deaths')
            return

        ignored_abilities = {'Divine Intervention'}
        death_events = [death for death in death_events if death.ability_name not in ignored_abilities]
        common_deaths = Counter(death.ability_name for death in death_events).most_common(3)

        print('- All deaths:')
        for death in death_events:
            minutes, seconds = divmod(death.time / 1000, 60)
            print(f'  - {death.name} died to {death.ability_name} at {minutes:.0f}:{seconds:02.0f}')

        print(f'- Most common deaths:')
        for ability_name, count in common_deaths:
            print(f'  - {ability_name}: {count}')
