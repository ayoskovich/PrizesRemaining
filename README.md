# Prizes Remaining
Code that archives data on the michigan powerball.

## Helpful docker commands

Remove all stopped containers
```
docker rm $(docker ps --filter status=exited -q)
```

Use the `--rm` to delete the container after it exits.
```
docker build -t scrape .
docker run --rm scrape
```