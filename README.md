# Discord Blackjack Bot
 This is a discord Blackjack bot that connects to a discord server with a suite of user commands. This bot is designed to be deployed on heroku and it uses a mongodb atlas backend to store user game state data.
 
![til](https://media.giphy.com/media/Hjx4WONVX1ferlJZsG/giphy.gif)

## How to install

From the repository's main directory:

``` bash
$ pip3 install -r requirements.txt
```

## Setup

Next, setup a `.env` file in the main directory:

``` bash
_TOKEN=<Discord Token>
_USERNAME=<MongoDB Atlas Username>
_PASSWORD=<MongoDB Atlas Password>
_DATABASE=<MongoDatabase.MongoCollection>
_CLUSTER=<cluster#>
```

If you don't have an account, follow the steps at <https://docs.atlas.mongodb.com/getting-started/> to setup and deploy a cluster.

## Run locally

This bot can be run locally off a personal computer or server:

``` bash
$ python bot.py
```

Alternatively, it can be deployed on heroku's cloud platform using the Procfile included.

## How to play

The following commands are support by the Blackjack bot:

``` bash
dealer play
dealer hit
dealer stay
```

`play` starts the game with the dealer drawing two cards for themself and the player. The dealer will hide one of their cards until it is time to reveal the cards. The player can then decide to `hit` inorder to draw another card or `stand` and allow the dealer to reveal their cards. If the player's point score of their hand exceeds 21 they bust, if they get 21 it's a Blackjack and they win, or if its below 21 and the player `stand`s the dealer will reveal their cards. The dealer will try to win in the same way attempting to `hit` until their score is higher than the player or they bust. 
