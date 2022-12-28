# Prizes Remaining

Code that archives and analyes data on the Michigan Lottery.

# Motivation

    1. Creatively nurture Nolan's gambling addiction
    2. Analyze data collected to make decisions about what games are advantageous for players
    3. Supplement data from existing websites that already do #2
    4. Make cool graphs

# Roadmap

    1. Script that merely pulls a single game's statistics from the michiganlottery.com
    2. Script that pulls all the active scratch off games and stores
    3. Process that does #1 for all games returned by #2 but every day (or several times a day? - every time they update, really)
    4. A plan for how to display data - Some ideas include,
        - time based "burn" chart of a ticket's prize denominations
        - initial odds of each denomination compared to current odds
        - estimated tickets remaining
    5. Process that continually monitors all active games offered and notifies us of new games.
    6. Tooling that monitors competitors websites for the same information we collect 

# Developer Notes

## Online data sources

1. [Prizes remaining](https://www.michiganlottery.com/resources/instant-games-prizes-remaining)
2. [Search the map](https://www.michiganlottery.com/resources/find-a-retailer/453-instore-instant-tinsel-town)
3. [Odds / price / game number](https://www.michiganlottery.com/games/453-instore-instant-tinsel-town)
    - Click on image in #1
4. External sites
    - [Scratchoff-odds](https://scratchoff-odds.com/)
    - [Scratchoffodds](https://www.scratchoffodds.com/)

## Docker

Remove all stopped containers

```
docker rm $(docker ps --filter status=exited -q)
```

Use the `--rm` to delete the container after it exits.

```
docker build -t scrape .
docker run --rm scrape
```

Use this to keep the container running and start a shell inside.
```
docker run -it --entrypoint=/bin/bash scrape
```

Note that after pushing a new image to the AWS ECR the task in AWS ECS will automatically use the latest image.

## WSL 2 Environment

To get started developing in WSL2, do the following

`sudo apt install python3.8`

Then, run,

`pip install -r requirements.txt`

Note: `pip` should be installed with `python`, but if it isn't give "pip install" a Google.

TODO: X server, Windows X server setup in Windows Defender, etc.

https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/
https://stackoverflow.com/questions/61110603/how-to-set-up-working-x11-forwarding-on-wsl2
https://github.com/cascadium/wsl-windows-toolbar-launcher#firewall-rules


## AWS ECS

- https://stackoverflow.com/questions/35924158/docker-run-program-arguments-in-aws-ecs
    - The scraping script gets this weird error, which I think is due to an inadequate amount of disk space or something.