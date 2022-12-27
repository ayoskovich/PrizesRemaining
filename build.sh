aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 324332189278.dkr.ecr.us-east-1.amazonaws.com
docker build -t lotto .
docker tag lotto:latest 324332189278.dkr.ecr.us-east-1.amazonaws.com/lotto:latest
docker push 324332189278.dkr.ecr.us-east-1.amazonaws.com/lotto:latest