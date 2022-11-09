# Quickstart 

Install Telethon ( telethon is at 1.25.4 at the moment of writing. )

```py

python3 -m pip install telethon

```


Make a .env file on the project root with the following fields 

```py
# get these from my.telegram.org
API_ID=00000000
API_HASH="EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
# get this using string gen utilities 
SESH="" 
# if you want to use a different database provider than sqlite 
DB_URL="db.db"

```

Start the bot with 

```py

python3 -m ubi

```
