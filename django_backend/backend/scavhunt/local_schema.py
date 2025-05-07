from enum import Enum

class Player():
    
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

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
