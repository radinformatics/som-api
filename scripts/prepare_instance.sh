#!/bin/sh

# Prepare Google Cloud/ etc to run Docker

sudo apt-get update > /dev/null
sudo apt-get -y install git build-essential nginx

# Needed module for system python
sudo apt-get install -y python-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo /usr/bin/python get-pip.py
rm get-pip.py
sudo pip install ipaddress
sudo pip install oauth2client

# Add docker key server
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

# Install Docker!
sudo apt-get update \
   && sudo apt-get install apt-transport-https ca-certificates \
   && sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee --append /etc/apt/sources.list.d/docker.list

sudo apt-get update && apt-cache policy docker-engine
sudo apt-get update
sudo apt-get -y install linux-image-extra-$(uname -r) linux-image-extra-virtual &&
sudo apt-get -y install docker-engine &&
sudo service docker start
#sudo docker run hello-world
sudo usermod -aG docker $USER

# Docker-compose
sudo apt -y install docker-compose

# Install Singularity
sudo apt-get -y install libtool \
                       autotools-dev \
                       automake \
                       autoconf \
                       git

cd /tmp
git clone https://github.com/singularityware/singularity
cd singularity
git checkout -b development
git pull origin development
./autogen.sh
./configure --prefix=/usr/local
make
sudo make install

# Note that you will need to log in and out for changes to take effect
sudo service nginx stop

if [ ! -d $HOME/som-api ]
then
  cd $HOME
  git clone https://www.github.com/radinformatics/som-api
  cd som-api
  docker build -t vanessa/som-api .
  # you need to add .env file here
  docker-compose up -d
fi
