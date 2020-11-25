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
