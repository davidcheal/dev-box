#!/usr/bin/env bash

set -e

FAIL="\e[31m"
SUCCESS="\e[32m"
WARN="\e[33m"
RESETCOLOR="\e[0m"
INFO="\e[37m"

EMAIL=david.cheal@gmail.com
NAME="David Cheal"

LINUX_APP_FOLDER=~/apps

printer() {
    level=$1
    printf "${!level}$2${RESETCOLOR}\n"
}

# Detect Ubuntu or MacOs
if [[ $OSTYPE =~ ^linux ]]; then
    export OS=linux
    export PROJECT_DIR=~/projects
    export TMP=/tmp/build
elif [[ $OSTYPE =~ ^darwin ]]; then
    export OS=macos
    export PROJECT_DIR=~/projects
    export TMP=/tmp/build
else
    printer ERROR "OS doesnt match anything this script can help with."
    exit 1
fi

printer ERROR "This will install a lot of apps and makes not effort to not overwrite existing versions and configs"
read -p "Are you sure? y/n" -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    printer INFO "\nInstall cancelled"
    exit 0
fi

# Create base folders
[ ! -d $PROJECT_DIR ] && mkdir $PROJECT_DIR
[ ! -d $TMP ] && mkdir $TMP

# Setup Linux
if [[ $OS == 'linux' ]]; then
    [ ! -d $LINUX_APP_FOLDER ] && mkdir $LINUX_APP_FOLDER
fi

printer INFO "Starting build"

if [[ ! -f phase1 ]]; then
    printer INFO "Running upgrade"
    sudo apt-get update
    sudo apt-get dist-upgrade -y
    touch phase1
    # TODO: Reboot should not be requird, needs to be validated
    # sudo shutdown -r +1
else
    printer INFO "Phase 1 already complete. Skipping"
fi

if [[ ! -f phase2 ]]; then
    # if [[ $OS == 'linux' ]]; then
    #     printer INFO "Doing release upgrade"
    #     # sudo do-release-upgrade -q DistUpgradeViewNonInteractive 2>/dev/null || true
    # fi
    touch phase2
else
    printer INFO "Phase 2 already complete. Skipping"
fi

if [[ ! -f phase3 ]]; then
    printer INFO "Installing apt applications"

    # Linux Only
    if [[ $OS == 'linux' ]]; then
        # Distro based apps
        ## APT
        sudo apt-get install net-tools git nmap curl rar \
            p7zip-full p7zip-rar vlc terminator libfuse2 \
            openvpn kompare krusader trash-cli krename \
            qbittorrent filezilla libreoffice-calc \
            krename kompare ruby-full python3-pip \
            dmidecode firefox php-fpm nginx -y
        sudo apt remove unattended-upgrades -y
        sudo apt-get autoremove -y
        export BOX=$(sudo dmidecode -s system-manufacturer)
        if [[ $BOX =~ VMware ]]; then
            sudo apt-get install open-vm-tools-desktop open-vm-tools
        fi
        ## SNAPs
        sudo snap install ffmpeg
        sudo snap install postman
        ## KDENlive video editor
        printer INFO "Installing KDENlive"
        wget -O $LINUX_APP_FOLDER/kdenlive https://download.kde.org/stable/kdenlive/22.12/linux/kdenlive-22.12.3-x86_64.AppImage --show-progress
        chmod +x $LINUX_APP_FOLDER/kdenlive
    fi

    # MacOS Only
    if [[ $OS == 'macos' ]]; then
        ## Install xcode
        printer INFO "Installing xCode"
        xcode-select --install
        ## Install Homebrew
        printer INFO "Installing Homebrew"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        brew update
        ## Install brew apps
        printer INFO "Installing Brew apps"
        brew install curl php vlc filezilla ruby python postman openvpn-connect zip sevenzip rar wget nginx xtorrent
    fi

    # MacOS and Ubuntu
    ## Anaconda
    printer INFO "Installing Anaconda"
    if [[ $OS == 'linux' ]]; then
        wget -O $TMP/anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh --show-progress
        bash $TMP/anaconda.sh
    else
        wget -O $TMP/anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh --show-progress
        bash $TMP/anaconda.sh
    fi
    bash $TMP/anaconda.sh -bf

    ## AWS CLI
    printer INFO "Installing AWS CLI"
    if [[ $OS == 'linux' ]]; then
        wget -O $TMP/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" --show-progress
        unzip awscliv2.zip temp/
        sudo .$TMP/aws/install
        aws -v
    else
        pip3 install awscli --upgrade --user
        aws -v
    fi

    ## VSCode
    printer INFO "Installing VSCode"
    if [[ $OS == 'linux' ]]; then
        sudo snap install --classic code
    else
        brew install --cask visual-studio-code
    fi

    ## VSCode Extensions
    vscode --install-extension amazonwebservices.aws-toolkit-vscode
    vscode --install-extension Codeium.codeium
    vscode --install-extension cshum.convert-newline-list-to-array
    vscode --install-extension dbaeumer.vscode-eslint
    vscode --install-extension eamodio.gitlens
    vscode --install-extension esbenp.prettier-vscode
    vscode --install-extension janisdd.vscode-edit-csv
    vscode --install-extension jmviz.quote-list
    vscode --install-extension mechatroner.rainbow-csv
    vscode --install-extension ms-azuretools.vscode-docker
    vscode --install-extension ms-python.python
    vscode --install-extension ms-python.vscode-pylance
    vscode --install-extension petli-full.json-to-yaml-and-more
    vscode --install-extension shd101wyy.markdown-preview-enhanced
    vscode --install-extension streetsidesoftware.code-spell-checker
    vscode --install-extension Tyriar.sort-lines
    vscode --install-extension wmaurer.change-case

    ## Node Version Manager, npm and Node
    printer INFO "Install Node Version Manager and NPM LTS"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
    nvm install --lts

    ## Global NPM Packages
    npm install -g npm-check-updates create-react-app express-generator
    node -v
    npm -v

    ## Docker
    printer INFO "Installing Docker"
    if [[ $OS == 'linux' ]]; then
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y
        sudo apt-cache policy docker-ce
        sudo apt-get update
        sudo apt install docker-ce -y
    else
        brew install docker
    fi

    ## Chrome
    if [[ $OS == 'linux' ]]; then
        wget -O $TMP/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb --show-progress
        sudo dpkg --install $TMKP/chrome.deb
    else
        wget -O https://dl.google.com/dl/chrome/mac/universal/stable/gcea/googlechrome.dmg --show-progress
        hdiutil attach $TMP/chrome.dmg -nobrowse
        cp -pPR /Volumes/Google Chrome/Google Chrome.app /Applications/
        GoogleChromeDMG="$(hdiutil info | grep "/Volumes/Google Chrome" | awk '{ print $1 }')"
        hdiutil detach $GoogleChromeDMG
    fi

    ## Tor
    if [[ $OS == 'linux' ]]; then
        wget -O $TMP/tor.tar.xz https://www.torproject.org/dist/torbrowser/12.0.5/tor-browser-linux64-12.0.5_ALL.tar.xz --show-progress
        tar -xf $TMP/tor.tar.xz -C $LINUX_APP_FOLDER
    else
        brew install tor
    fi

    # Config Apps
    ## Config Git
    git config --global user.email $EMAIL
    git config --global user.name $NAME

    ## Terminator
    if [[ $OS == 'linux' ]]; then
        mkdir ~/.config/terminator
        cp assets/terminator-config ~/.config/terminator/config
    fi

    ## Profile
    cp ~/.profile ~/.profile.old
    cp assets/bashrc ~/.bashrc.old
    cp assets/profile ~/.profile
    cp assets/bashrc ~/.bashrc

    ## Set shell prompt
    if [[ $OS == 'linux' ]]; then
        echo "export PS1='\[\033[1;32m\]$(whoami)@\[\033[1;34m\]$(hostname):\[\033[33m\]$(pwd)\[\033[0;37m\]\[\e[91m\]$(parse_git_branch)\[\e[00m\]\n'" >>~/.bashrc
    else
        echo "export PS1='\[\033[1;32m\]$(whoami)@\[\033[1;34m\]$(hostname):\[\033[33m\]$(pwd)\[\033[0;37m\]\[\e[91m\]$(parse_git_branch)\[\e[00m\]\n'" >>~/.bashrc
    fi

    # Clean up
    rm $TMP -r
    touch phase3
else
    printer INFO "Skipping apt applications"
fi
