#!/bin/bash
DOCKER_DIR="4.0.23/docker"
file="VERSION"     # the file where you keep your string name
read -d $'\x04' ver < "$file" # the content of $file is redirected to stdin from where it is read out into the $name variable
echo "$ver"
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery
cp curated_mechanisms.json "$DOCKER_DIR"/
python3 "$DOCKER_DIR"/deploy.py build --docker-image-version amrfinder-$ver --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-dir "$DOCKER_DIR" --image-target base --push
python3 "$DOCKER_DIR"/deploy.py build --docker-image-version amrfinder-$ver --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-dir "$DOCKER_DIR" --image-target runtime --push