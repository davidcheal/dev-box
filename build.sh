#!/usr/bin/env bash

FAIL="\e[31m"
SUCCESS="\e[32m"
WARN="\e[33m"
RESETCOLOR="\e[0m"
INFO="\e[37m"

printer () {
 level=$1
 printf "${!level}$2${RESETCOLOR}\n"
}

# Update Ubunutu and install apt software
sudo apt-get update
printer INFO "Running Ubuntu upgrade"
sudo apt-get upgrade -y
printer INFO "Installing apt applications"
sudo apt-get install net-tools php-fpm git nmap curl rar p7zip-full p7zip-rar vlc ffpmeg terminator libfuse2 -y
printer INFO "Removing guff"
sudo apt remove unattended-upgrades -y
sudo apt-get autoremove -y
# Install apps
## VSCode
printer INFO "Installing VSCode"
sudo snap install --classic code
## Node Version Manager
printer INFO "Install Node Version Manager and NPM LTS"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  
nvm install --lts
## Docker
printer INFO "Installing Docker"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y
sudo apt-cache policy docker-ce
sudo apt install docker-ce