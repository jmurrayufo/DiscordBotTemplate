
# .creds file should look like this 
# export CLIENT_TOKEN="LOTS OF NUMBERS THAT MAKE A TOKEN GO HERE"

source ~/.ssh/stats_bot.dev.creds
pipenv run python ./Bot.py --env dev "$@"
