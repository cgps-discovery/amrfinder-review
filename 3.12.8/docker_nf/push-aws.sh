python docker/deploy.py build --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery  --docker-image-version 2.1.0
python docker/deploy.py test --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-image-version 2.1.0
python docker/deploy.py build --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --push --docker-image-version 2.1.0
python docker/deploy.py build --push --docker-image-version 2.1.0
