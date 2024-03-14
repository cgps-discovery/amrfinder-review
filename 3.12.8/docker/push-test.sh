#!/bin/bash
file="VERSION"     #the file where you keep your string name
read -d $'\x04' ver < "$file" #the content of $file is redirected to stdin from where it is read out into the $name variable
echo $ver          
cp curated_mechanisms.json 3.12.8/docker_nf/
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir 3.12.8/docker_nf --image-target base build 
# python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder  --docker-dir 3.12.8/docker_nf --image-target base test
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir 3.12.8/docker_nf  --image-target base build --push
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir 3.12.8/docker_nf  --image-target runtime build --push
python 3.12.8/docker_nf/deploy.py --docker-image-version amrfinder-$ver --docker-repo happykhan/amrfinder --docker-dir 3.12.8/docker_nf  --image-target nextflow build --push