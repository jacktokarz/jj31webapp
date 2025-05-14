
class Player():
    
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    def __str__(self):
        return "Player\n  Id: " + self.id + "\n  Name: " + self.name

class Card():

    def __init__(self,
                 id: str,
                 title: str,
                 description: str,
                 value: int):
        self.id = id
        self.title = title
        self.description = description
        self.value = value
    
    def __str__(self):
        return "Card\n  Id: " + self.id + "\n  Title: " + self.title + "\n  Description: " + self.description + "\n  Points: " + str(self.value)


class Question():

    def __init__(self,
                 id: str,
                 title: str,
                 description: str,
                 cost: int,
                 category: str,
                 additional_info: bool):
        self.id = id
        self.title = title
        self.description = description
        self.cost = cost
        self.category = category
        self.additional_info = additional_info
    
    def __str__(self):
        return "Question\n  Id: " + self.id + "\n  Title:  " + self.title + "\n  Description: " + self.description + "\n  Cost: " + str(self.cost) + "\n  Category: " + self.category + "\n  Additional Info: " + str(self.additional_info)

class Team():

    def __init__(self, 
                 id: str, 
                 players: list[Player], 
                 name: str, 
                 points: int,
                 completed_cards: list[Card],
                 favorite_cards: list[Card],
                 asked_questions: list[Question]):
        self.id = id
        self.players = players
        self.name = name
        self.points = points
        self.completed_cards = completed_cards
        self.favorite_cards = favorite_cards
        self.asked_questions = asked_questions
    
    def __str__(self):
        string = "Team!\n  Id: " + self.id + "\n  Name: " + self.name + "\n  Points: " + str(self.points)
        string = string + "\n------\n  Players: \n"
        for player in self.players:
            string = string + str(player) + "\n"
        string = string + "\n--------\n Completed Cards\n"
        for comp in self.completed_cards:
            string = string + str(comp) + "\n-"
        string = string + "\n--------\n Favorite Cards\n"
        for fav in self.favorite_cards:
            string = string + str(fav) + "\n"
        string = string + "\n--------\n Asked Questions\n"
        for quest in self.asked_questions:
            string = string + str(quest) + "\n"
        return string
        
