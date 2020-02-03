# tg-bot
`TELEGRAM_API_TOKEN` — Bots API token. In order to get API token, you'd need to find @BotFather user on telegram (Also a bot) and follow instructions from welcome message.
`TELEGRAM_ACCESS_ID` — Only messages from this user id would be accepted. In order to find out your Telegram userID  
Find @userinfobot and start conversation with it.

`vspolam/python3.7-base` is an image provided by Surendra Polam (`@suru33` on TG) with sqlite already installed 

At the start point db populates with predefined budget group and services inside/outside budget

In order to start app, run `docker-compose up --build` from the directory with `docker-compose.yml`
