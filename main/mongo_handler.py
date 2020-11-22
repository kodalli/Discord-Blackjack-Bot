import os
import pymongo
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)


class Mongo:
    username = os.getenv('_USERNAME')
    password = os.getenv('_PASSWORD')
    cluster = os.getenv('_CLUSTER')
    dbname = os.getenv('_DATABASE')
    mongo_cluster = pymongo.MongoClient(
        f"mongodb+srv://{username}:{password}@{cluster}.02kve.mongodb.net/{dbname}?retryWrites=true&w=majority")
    collection = mongo_cluster.Discord_Database.Blackjack_Collection

    def __init__(self, member_id) -> None:
        """
        Creates an instance of a connection to a player's game state data
        :param member_id: discord member identification
        :type member_id: int
        """

        self.id = member_id
        # Create player and push to MongoDB Atlas
        if not self.collection.find_one({"_id": self.id}):
            post = {"_id": self.id, "score": 1, "player_cards": [],
                    "dealer_cards": [], "is_playing": False, "deck": []}
            self.collection.insert_one(post)

    @property
    def is_playing(self) -> bool:
        """
        Player in game status that is retrieved from MongoDB Atlas
        :return: bool
        """
        return self.collection.find_one({"_id": self.id})["is_playing"]

    @is_playing.setter
    def is_playing(self, is_playing: bool) -> None:
        """
        Change player in game status and push to MongoDB Atlas
        :param is_playing: player in game status, type bool
        :return: None
        """
        self.collection.update_one({"_id": self.id}, {"$set": {"is_playing": is_playing}})

    @property
    def score(self) -> int:
        """
        Player score retrieved from MongoDB Atlas, wins increase score and losses decrease score
        :return: int
        """
        return self.collection.find_one({"_id": self.id})["score"]

    @score.setter
    def score(self, score: int) -> None:
        """
        Change player score and push to MongoDB Atlas
        :param score: player score from wins and losses, type int
        :return: None
        """
        self.collection.update_one({"_id": self.id}, {"$set": {"score": score}})

    @property
    def player_cards(self) -> list:
        """
        Player hand of cards retrieved from MongoDB Atlas
        :return: list of strings with card names, ex: 'AS' is Ace of Spades, '3H' is 3 of Hearts etc.
        """
        return self.collection.find_one({"_id": self.id})["player_cards"]

    @player_cards.setter
    def player_cards(self, player_cards: list) -> None:
        """
        Change player hand of cards and push to MongoDB Atlas
        :param player_cards: list of strings with card names, ex: 'AS' is Ace of Spades, '3H' is 3 of Hearts etc.
        :return: None
        """
        self.collection.update_one({"_id": self.id}, {"$set": {"player_cards": player_cards}})

    @property
    def dealer_cards(self) -> list:
        """
        Dealer hand of cards retrieved from MongoDB Atlas
        :return: list of strings with card names, ex: 'AS' is Ace of Spades, '3H' is 3 of Hearts etc.
        """
        return self.collection.find_one({"_id": self.id})["dealer_cards"]

    @dealer_cards.setter
    def dealer_cards(self, dealer_cards: list) -> None:
        """
        Change dealer hand of cards and push to MongoDB Atlas
        :param dealer_cards: list of strings with card names, ex: 'AS' is Ace of Spades, '3H' is 3 of Hearts etc.
        :return: None
        """
        self.collection.update_one({"_id": self.id}, {"$set": {"dealer_cards": dealer_cards}})

    @property
    def deck(self) -> list:
        """
        Deck of cards retrieved from MongoDB
        :return: list of strings with card names, ex: 'AS' is Ace of Spades, '3H' is 3 of Hearts etc.
        """
        return self.collection.find_one({"_id": self.id})["deck"]

    @deck.setter
    def deck(self, deck: list) -> None:
        """
        Change deck of cards and push to MongoDB
        :param deck: list of strings with card names, ex: 'AS' is Ace of Spades, '3H' is 3 of Hearts etc.
        :return: None
        """
        self.collection.update_one({"_id": self.id}, {"$set": {"deck": deck}})
