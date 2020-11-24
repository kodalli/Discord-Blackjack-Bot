import random
from main.mongo_handler import Mongo
import discord
from discord.ext import commands
import os
import time
import cv2

MAX_MESSAGE_LENGTH = 256


class Card:
    def __init__(self, suit=None, rank=None, value=None):
        """
        Card object holds suit, rank, and value properties
        :param suit: Suit of the Card such as Spades and Clubs, type str
        :param rank: Representing rank of the Card such as  A for Ace, K for King, type str
        :param value: Score Value for the Card such as 10 for King, type int
        """
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        """
        :return: String with each card field and value
        """
        return f"Suit : {self.suit}, Rank : {self.rank}"

    @property
    def bson(self):
        """
        :return: bson friendly string property with suit char and rank char, ex: King of Hearts is 'KH'
        """
        return f"{self.rank}{self.suit[0]}"

    def decode_bson(self, card: str):
        """
        Converts bson friendly string back into Card
        :param card: bson string with suit char and rank char, ex: King of Hearts is 'KH'
        :return: Card
        """
        self.rank = card[:-1]
        self.suit = {'H': 'Hearts', 'D': 'Diamonds', 'S': 'Spades', 'C': 'Clubs'}[card[-1]]
        self.value = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                      "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}[self.rank]
        return self


class Hand:
    def __init__(self, hand=None) -> None:
        if hand is None:
            hand = []
        self.hand = hand  # hand is a list of card objects

    def __str__(self) -> str:
        """
        :return: String with each card in the hand and the score at the end
        """
        s = ""
        for card in self.hand:
            s += f"{card} "
        return s + f"score : {self.score}"

    @property
    def score(self) -> int:
        """
        Sums all card values in the hand and accounts for ace cards if over 21
        :return: int score of the cards
        """
        values = [card.value for card in self.hand]
        score, aces = sum(values), values.count(11)
        for _ in range(aces):
            if score <= 21:
                break
            else:
                score -= 10
        return score

    def append(self, card: Card) -> None:
        """
        Appends card to hand
        :param card: card object, type Card
        :return: None
        """
        self.hand.append(card)

    def hit(self, deck: list) -> list:
        """
        Updates deck after both dealer and player remove cards for their hands
        :param deck: list of cards
        :return: list with updated deck of cards removed from deck to fill hand, or False if 21 or bust
        """
        if self.score < 21:
            card = random.choice(deck)
            self.append(card)
            deck.remove(card)
        return deck


def make_deck() -> list:
    """
    Creates list of cards akin to standard deck of 52
    :return: list of card objects, type list
    """
    # The type of suit
    suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
    # The type of card
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    # The card value
    card_values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
                   "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
    # The deck of 52 cards
    deck = [Card(suit, rank, card_values[rank])
            for suit in suits for rank in ranks]
    return deck


def push_mongo(member_id: int, player: Hand = None, dealer: Hand = None, deck: list = None,
               is_playing: bool = None) -> None:
    """
    Encodes data into bson friendly format and pushes to MongoDB Atlas
    :param member_id: discord member id, type int
    :param player: current player cards, type Hand
    :param dealer: current dealer cards, type Hand
    :param deck: current deck of cards, type list of Cards
    :param is_playing: if player is in game, type bool
    :return: None
    """
    player_state = Mongo(member_id)
    if player:
        player_state.player_cards = [card.bson for card in player.hand]
    if dealer:
        player_state.dealer_cards = [card.bson for card in dealer.hand]
    if deck:
        player_state.deck = [card.bson for card in deck]
    if is_playing is not None:
        player_state.is_playing = is_playing


def reset_game(member_id) -> None:
    """
    Resets game for player and sets player default values
    :param member_id: discord member id, type int
    :return: None
    """
    push_mongo(member_id, Hand(), Hand(), make_deck(), False)


def write_hand_to_file(hand: Hand, hidden: bool = False) -> str:
    """
    Creates image file of hand and writes the image to storage
    :param hand: hand object, type Hand
    :param hidden: one card will be hidden in image, type bool
    :return: filename of image, type str
    """
    path = os.path.join(os.getcwd(), "deck_of_cards")
    card_images = []
    for card in hand.hand:
        img = cv2.imread(os.path.join(
            path, f"{card.rank}{card.suit[0]}.png"))
        img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        card_images.append(img)
    if hidden:
        img = cv2.imread(os.path.join(
            path, "Hidden.png"))
        img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        card_images[-1] = img

    filename = 'temp.png'
    if os.path.exists('temp.png'):
        os.remove("temp.png")
        time.sleep(0.1)

    result = cv2.hconcat(card_images)
    cv2.imwrite(filename, result)

    return filename


async def print_cards(ctx, player: Hand, dealer: Hand, hidden: bool = False) -> None:
    """
    Sends discord message with player and dealer cards and scores
    :param ctx: discord context, includes channel and server to send message to
    :param player: player hand object, type Hand
    :param dealer: dealer hand object, type Hand
    :param hidden: dealer second card is hidden prior to reveal when True, type bool
    :return: None
    """
    await send_embed(ctx, f"Dealer score: {dealer.score}\nDealer cards:")
    await ctx.send(file=discord.File(write_hand_to_file(dealer, hidden)))

    await ctx.send(file=discord.File(write_hand_to_file(player)))
    await send_embed(ctx, f"{ctx.message.author.nick} score: {player.score}\n{ctx.message.author.nick} cards:")


async def send_embed(ctx, message: str) -> None:
    """
    Wraps text into discord embed then sends message
    :param ctx: discord context, includes channel and server to send message to
    :param message: text message to send, type str
    :return: None
    """
    await ctx.send(embed=discord.Embed(title=message[:MAX_MESSAGE_LENGTH], description="\u200b"))


class BlackJack(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['play'])
    async def start_game(self, ctx):
        """
        Begin Blackjack game
        :param ctx: discord member object
        """
        # Check if already playing
        player_state = Mongo(ctx.message.author.id)

        if player_state.is_playing:
            player_state.is_playing = False
            reset_game(ctx.message.author.id)
        else:
            player_state.is_playing = True

        deck = make_deck()
        player = Hand()
        dealer = Hand()

        # Randomly deal cards to both player and dealer
        for _ in range(2):
            deck = player.hit(deck)
            deck = dealer.hit(deck)

        push_mongo(ctx.message.author.id, player, dealer, deck)

        if player.score == 21:
            reset_game(ctx.message.author.id)
            await send_embed(ctx, "You Hit A Blackjack! You Win!")

        # Print cards, one of the dealer cards are hidden until the player stands
        await print_cards(ctx, player, dealer, hidden=True)
        await send_embed(ctx, "Enter 'dealer hit' or 'dealer stand':")

    @commands.command(aliases=['hit'])
    async def draw_card(self, ctx) -> None:
        """
        Draws card from deck for player then updates both player and dealer hand. Sends discord message with
        player and dealer hands and requests player to continue game if possible.
        :param ctx: discord member object
        :return: None
        """
        # Retrieve player data from MongoDB
        player_state = Mongo(ctx.message.author.id)
        if not player_state.is_playing:
            await send_embed(ctx, "You must start a game with 'dealer play' to use the hit command")
            return

        deck = [Card().decode_bson(card) for card in player_state.deck]
        dealer = Hand([Card().decode_bson(card) for card in player_state.dealer_cards])
        player = Hand([Card().decode_bson(card) for card in player_state.player_cards])
        deck = player.hit(deck)

        # Print cards, one of the dealer cards are hidden until the player stands
        await print_cards(ctx, player, dealer, hidden=True)

        if player.score == 21:
            reset_game(ctx.message.author.id)
            await send_embed(ctx, "You Hit A Blackjack! You Win!")
        elif player.score > 21:
            reset_game(ctx.message.author.id)
            await send_embed(ctx, "Oh No! You Busted...You Lose")
        else:
            # Update player data with new hand
            push_mongo(ctx.message.author.id, player=player, deck=deck)
            await send_embed(ctx, "Enter 'dealer hit' or 'dealer stand':")

    @commands.command(aliases=['stay', 'stand'])
    async def end_turn(self, ctx) -> None:
        """
        Player is done drawing cards and now the dealer will reveal their cards to the player. Sends discord
        message with game results.
        :param ctx: discord member object
        :return: None
        """
        # Retrieve player data from MongoDB
        player_state = Mongo(ctx.message.author.id)
        if not player_state.is_playing:
            await send_embed(ctx, "You must start a game with 'dealer play' to use the stand command")
            return

        deck = [Card().decode_bson(card) for card in player_state.deck]
        player = Hand([Card().decode_bson(card) for card in player_state.player_cards])
        dealer = Hand([Card().decode_bson(card) for card in player_state.dealer_cards])

        await send_embed(ctx, "Dealer Is Revealing The Cards...")
        await print_cards(ctx, player, dealer)

        while dealer.score < 21 and dealer.score < player.score:
            deck = dealer.hit(deck)
            await print_cards(ctx, player, dealer)

        if dealer.score == 21:
            await send_embed(ctx, "Dealer Hit A Blackjack! Dealer Wins!")
        elif dealer.score > 21:
            await send_embed(ctx, "Dealer Busted! You Win!")
        elif dealer.score == player.score:
            await send_embed(ctx, "Tie Game!")
        else:  # dealer.score > player.score
            await send_embed(ctx, "Dealer Has A Higher Score. Dealer Wins!")

        reset_game(ctx.message.author.id)
