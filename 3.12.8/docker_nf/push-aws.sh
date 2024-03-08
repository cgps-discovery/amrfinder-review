#!/bin/bash
file="VERSION"     #the file where you keep your string name
read -d $'\x04' ver < "$file" #the content of $file is redirected to stdin from where it is read out into the $name variable
echo $ver    
cp curated_mechanisms.json 3.12.8/docker_nf/
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-dir 3.12.8/docker_nf --image-target base build 
# python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-1.0.1 --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery  --docker-dir 3.12.8/docker_nf --image-target base test
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-dir 3.12.8/docker_nf  --image-target base build --push
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-dir 3.12.8/docker_nf  --image-target aws build --push
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo 902121496535.dkr.ecr.us-east-2.amazonaws.com/cgps-discovery --docker-dir 3.12.8/docker_nf  --image-target runtime build --push