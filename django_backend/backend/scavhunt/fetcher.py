import scavhunt.local_schema as sc

class Fetcher:

    def __init__(self):
        raise NotImplementedError

    def get_player(self, id: str) -> sc.Player:
        raise NotImplementedError

    def get_all_players(self) -> list[sc.Player]:
        raise NotImplementedError

    def get_question(self, id: str) -> sc.Question:
        raise NotImplementedError

    def get_all_questions(self) -> list[sc.Question]:
        raise NotImplementedError

    def get_team(self, id: str) -> sc.Team:
        raise NotImplementedError

    def get_all_teams(self) -> list[sc.Team]:
        raise NotImplementedError

    def get_card(self, id:  str) -> sc.Card:
        raise NotImplementedError

    def get_all_cards(self) -> list[sc.Card]:
        raise NotImplementedError
    
    def favorite_question(self, team_id, card_id):
        pass

    def unfavorite_question(self, team_id, card_id):
        pass
