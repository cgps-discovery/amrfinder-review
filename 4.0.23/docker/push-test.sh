#!/bin/bash
file="VERSION"     #the file where you keep your string name
read -d $'\x04' ver < "$file" #the content of $file is redirected to stdin from where it is read out into the $name variable
echo $ver          
DOCKER_DIR="4.0.23/docker"
cp curated_mechanisms.json "$DOCKER_DIR"/
python3 "$DOCKER_DIR"/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir "$DOCKER_DIR" --image-target base build
python3 "$DOCKER_DIR"/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir "$DOCKER_DIR" --image-target runtime build --push
python3 "$DOCKER_DIR"/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir "$DOCKER_DIR" --image-target nextflow build --push