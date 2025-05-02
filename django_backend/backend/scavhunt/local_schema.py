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

class Category(Enum):
    NO_CATEGORY = 1


class Question():

    def __init__(self,
                 title: str,
                 description: str,
                 cost: int,
                 category: Category,
                 additional_info: bool):
        self.tile = title
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
                 favorite_cards: list[Card]):
        self.id = id
        self.players = players
        self.name = name
        self.points = points
        self.completed_cards = completed_cards
        self.favorite_cards = favorite_cards
