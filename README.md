# social-watchdog

[Telegram bot](https://t.me/reddit_watchdog_bot) which notifies you about new keyword mentions on social networks. Currently supports Reddit and Twitter.

It consists of 2 services:
* search-service
  * responsible for performing search queries based on Watchables on social networks and sending new occurences to MQ
* telegram-bot
  * responsible for receiving commands from user and processing them
  * also responsible for receiving new keyword updates and sending them to corresponding user 

Those services uses MongoDB storage and they communicate through MQ (redis).

## Bot commands
* /list - lists all watchables for user
* /add {type} {query}
  * type: strict/default
    * default - loosely match lemmas of give search phrase (match them  in any other)
    * strict - strictly match lemmas sequence of given search phrase
  * query: phrase you want to look for. Can be single keyword.
* /remove {id} - removes Watchable for user
  * id: UUID that can be received from /list command