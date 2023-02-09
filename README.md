# Valorant Scoreboard Bot - pain
# Inspiration

We were interested in the world of image processing and how we could employ it to improve our daily lives, so we built a Valorant discord bot that employs the technology to promote healthy competition within users in a server. 

## What it does

Takes a Valorant leaderboard screenshot and the users in-game user ID as input and saves the user's Kill/Death and Assist ratio. On prompt, can also show the generated leaderboard of past screenshots, including the Top 10 players' KDA and their respective user IDs.

## How we built it

First, we had to develop an image processing class function using pytesseract and pillow dependencies. Then we used a discord.py dependency to input respective commands for the user on discord to implement. Finally, using mainly the pickle model, we saved the users game UID and KDA. 

## Challenges we ran into

Processing the image involved scanning for specific fields associated with a username and Valorant scoreboards have formatting issues to get through which added to the difficulty.

## Accomplishments that we're proud of
For our first hackathon we managed to pull through and complete the main project in 6 hours.

## What we learned

We learnt loads of new python libraries and the way the entire discord API is setup in the backend.

## How to run

Install dependencies like tesseract, discord.py, pillow, pickle
Add your own discord token in a file called token.txt (included)
Bot has 4 commands:
.save = Saves the provided image, processes it and then reads the stats to store them
.saveusername = must be done first to give the bot the in-game username for it to find it while image processing
.updateusername = updates the in-game username
.showleaderboard = shows the leaderboard of highest KDA within the server with ranking included
