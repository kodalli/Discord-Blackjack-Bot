import random
import asyncio


class Card:
    def __init__(self, suit, rank, value):
        # Suit of the Card such as Spades and Clubs
        self.suit = suit
        # Representing rank of the Card such as  A for Ace, K for King
        self.rank = rank
        # Score Value for the Card such as 10 for King
        self.value = value

    def __str__(self):
        return f"Suit : {self.suit}, Rank : {self.rank}, Value : {self.value}"


class Hand:
    def __init__(self):
        self.hand = []

    @property
    def score(self):
        score = 0
        aces = 0
        for card in self.hand:
            score += card.value
            if card.rank == 'A':
                aces += 1
        for _ in range(aces):
            if score <= 21:
                break
            else:
                score -= 10
        return score

    def append(self, card: Card):
        self.hand.append(card)

    def __str__(self):
        s = ""
        for card in self.hand:
            s += str(card) + " "
        return s + f"score : {self.score}"

    def hit(self, deck):
        if self.score < 21:
            card = random.choice(deck)
            self.append(card)
            deck.remove(card)
            return deck
        return False


def print_cards(hand, hidden=False):
    print(hand)


def start_game():
    deck = make_deck()
    player = Hand()
    dealer = Hand()

    # Randomly deal cards to both player and dealer
    for _ in range(2):
        deck = player.hit(deck)
        deck = dealer.hit(deck)

    # print cards, one of the dealer cards are hidden until the player stands
    print_cards(dealer, True)
    print_cards(player)

    player_choice = input("Enter hit or stand: ")
    if(player_choice == 'hit'):
        deck = player.hit(deck)
    while(player_choice != 'stand' and player.score < 21):
        print_cards(dealer, True)
        print_cards(player)
        player_choice = input("Enter hit or stand: ")
        if(player_choice == 'hit'):
            deck = player.hit(deck)
    while(dealer.score < 18):
        deck = dealer.hit(deck)
        print_cards(dealer, True)
        print_cards(player)


def make_deck():
    # The type of suit
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    # The type of card
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    # The card value
    card_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                   "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    # The deck of cards
    deck = [Card(suit, rank, card_values[rank])
            for suit in suits for rank in ranks]
    return deck


if __name__ == "__main__":
    start_game()
