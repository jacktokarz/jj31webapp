import scavhunt.local_schema as ls
import random as rnd
from prettytable import PrettyTable
# import discordsender as ds
import scavhunt.discordsender as ds

class Leaderboard():

    def __init__(self, timeline: list[ls.Timeline], teams: list[ls.Team]):
        self.team_points = {}
        self.timeline = timeline
        self.teams = teams
    
    def calculate_points(self, timeline: list[ls.Timeline], teams: list[ls.Team]):
        self.timeline = timeline
        self.teams = teams
        changes = {}
        for team in self.teams:
            new_points = 0
            old_points = team.points
            for card in team.completed_cards:
                new_points = new_points + card.value
            for a_time in self.timeline:
                if a_time.team.id == team.id:
                    new_points = new_points + a_time.get_total_points()
            if new_points != old_points:
                changes[team.id] = {"name": team.name, "new_points": new_points, "old_points": old_points}
            self.team_points[team.id] = {"name": team.name, "points": new_points}
        all_changes = self.send_points(changes)
        if len(changes) > 0:
            ds.DiscordSender().update_leaderboard(all_changes[0])
        return all_changes

    def send_points(self, changes = {}):
        header = rnd.choice(["Eyyyyoooo, a new update is here!", "Hi hi! Time for an update!", "Omg someone has DONE something", "People keep on doing things!", 
                             "You happy to see me! I'm happy to see you too!", "Oh wow this game is intense!", 
                             "CALL YOUR BETS! Something changed!", "Hi :3 Its your Party Bot. I love you", "Did you feel that ping? It's update time", 
                             "Everyone! Come watch the updates", "Oh wow is that an update?!"])

        sorted_tuple = []
        for k , v in self.team_points.items():
            sorted_tuple.append((k, v["points"]))
        final_tuple = sorted(sorted_tuple, key=lambda p: p[1], reverse=True)

        table = PrettyTable()
        table.field_names = ["Team Name", "Points", "Difference"]
        for k, v  in final_tuple:
            changed_value = 0
            if k in changes:
                changed_value = changes[k]['new_points'] - changes[k]['old_points']
            table.add_row([self.team_points[k]["name"], v, changed_value])
        
        output = f"""## {header} 
Here's where the leaderboard stands
```
{table.get_string()}
```
        """
        return output, changes

