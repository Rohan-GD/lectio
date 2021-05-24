![BFH Banner](https://trello-attachments.s3.amazonaws.com/542e9c6316504d5797afbfb9/542e9c6316504d5797afbfc1/39dee8d993841943b5723510ce663233/Frame_19.png)
# Lectio bot
This is a twitter bot account (@lectiobot).Follow this account on twitter, then go to any thread in twitter 
and tweet a comment tagging this bot.     In a few moments, the bot will send you a dm with the contents from
the thread.
## Team members
1. Sidharth R [https://github.com/Raf5017]
2. S Sandeep [https://github.com/Sandeep-2060]
3. Rohan George D [https://github.com/Rohan-GD]
## Team ID
BFH/rec7Ia3d8sff3ZODq/2021
## Link to product walkthrough
[link to video]
## How it Works ?
1. First follow the account @lectiobot ( [https://twitter.com/lectiobot] )
2. Go to any recent thread on twitter 
3. Tag the bot and type : "@lectiobot unroll"
4. After a few moments, the bot will send you a dm with the thread
## Libraries used
Python - 3.8.5
tweepy - 3.10.0
dotenv - 0.17.1
## How to configure

# Setup and Installation
Make sure you have the latest python installed
```
git clone <repo url>

```
Inside the project directory, install the modules used
```
pip install tweepy
```
```
pip install python-dotenv
```
Now before proceeding further you will have to make a new app at [https://developer.twitter.com/apps]
If you do not have a twitter dev account, apply for the same and then make a new app
1. Sign in with your Twitter account
2. Create a new app account
3. Modify the settings for that app account to allow read & write
4. Generate new consumer key and access token with those permissions

Following these steps will create 4 tokens that you will need to place in the .env_sample file.
Then rename the file as .env

## How to Run
Now in the terminal run
```
python main.py
```
Now the bot is active
