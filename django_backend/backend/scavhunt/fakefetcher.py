from scavhunt.fetcher import Fetcher
import scavhunt.local_schema as sc

mario = [sc.Player("1", "Mario"), sc.Player("2", "Luigi"), sc.Player("3", "Peach"), sc.Player("4", "Daisy")]
stuck = [sc.Player("5", "John"), sc.Player("6", "Rose"), sc.Player("7", "Dave"), sc.Player("8", "Jade"), 
         sc.Player("10", "Jake"), sc.Player("11", "Dirk"), sc.Player("12", "Roxy"), sc.Player("13", "Jane")]
sonic = [sc.Player("14", "Sonic"), sc.Player("15", "Amy"), sc.Player("16", "Shadow")]

questions = [sc.Question("qa", "Title", "Description", 10, "Standard", False), 
             sc.Question("qb", "Where am I?", "I will tell you the exact place I am.", 250, "Desperation", False), 
             sc.Question("qc", "Am I at a restaurant", "I love eating.", 45, "Locations", False),
             sc.Question("qd", "What is the rating of this place?", "This is the rating based on Google Maps", 150, "About the Place", False),
             sc.Question("qe", "Is this show in the sopranos", "WOKE UP THIS MORNING GOT MYSELF A GUN", 400, "Movies", True),
             sc.Question("qf", "How far is this location to you?", "This is a weird experience", 50, "Asking", True)]

fries = sc.Card("ca", "Dip fries into anything", "Dip fries into anything besides ketchup", 5)
rig = sc.Card("cb", "Deffinitely not Rigged", "Win a carnival game", 90)
ddr = sc.Card("cc", "Get a B or higher on any DDR song", "Song must be a 7 or higher, ten points per every difficult above", 80)
constitution = sc.Card("cd", "Sign a constitution", "Find the house of an American Founding Father", 70)
wonderville = sc.Card("ce", "Join in a game of Typing Party and Killer Queen", "Play a round of both of these games", 80)
pizza = sc.Card("cf", "Find a pizza rat", "Find a pizza rat. Can be real, can be fake. Cannot be an image on your phone. You are allowed to give pizza to a rat", 70)
cannoli = sc.Card("cg", "Cannoli, Cannoli, Get me the Foruoli", "Get a cannoli at what is called the Real Little Guy", 70)
cards = [fries, rig, ddr, constitution, wonderville, pizza, cannoli]

ninty = sc.Team("ta", mario, "Nintendo", 150, [fries, rig, ddr], [pizza, ddr], [questions[0], questions[2], questions[4]])
home = sc.Team("tb", stuck, "Alpha and Beta", 10, [cannoli, wonderville, constitution], [fries, rig], [questions[0], questions[1], questions[0]])
rolling = sc.Team("tc", sonic, "Sonic Heros", 580, [fries, rig, ddr, constitution, wonderville, pizza, cannoli], [constitution, wonderville], [questions[3], questions[5]])


class FakeFetcher(Fetcher):

    def __init__(self):
        pass

    def get_player(self, id: str):
        players = mario + stuck + sonic
        for player in players:
            print(player)
            if player.id == id:
                return player
        return None

    def get_all_players(self):
        return mario + stuck + sonic

    def get_question(self, id: str):
        questions = self.get_all_questions()
        for question in questions:
            if question.id == id:
                return question
        return None

    def get_all_questions(self):
        return questions

    def get_team(self, id: str):
        teams = self.get_all_teams()
        for team in teams:
            if team.id == id:
                return team
        return None

    def get_all_teams(self):
        return [ninty, home, rolling]

    def get_card(self):
        pass

    def get_all_cards(self) -> list[sc.Card]:
        return cards
    
print(FakeFetcher().get_all_cards())