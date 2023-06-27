#!/usr/bin/env bash

set -e

CRIT="\e[31m"
SUCCESS="\e[32m"
WARN="\e[33m"
RESETCOLOR="\e[0m"
INFO="\e[37m"

printer() {
    level=$1
    printf "${!level}$2${RESETCOLOR}\n"
}

EMAIL=david.cheal@gmail.com #default
NAME="David Cheal"          #default

LINUX_APP_FOLDER=~/apps

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
    printer CRIT "OS doesnt match anything this script can help with."
    exit 1
fi

read -p "What is your email address?: " -r
if [[ ! -z $REPLY ]]; then
    EMAIL=$REPLY
fi

read -p "What is your name?: " -r
if [[ ! -z $REPLY ]]; then
    NAME=$REPLY
fi

printer CRIT "This will install a lot of apps. NO effort ias made to preserve existing versions and configs"

read -p "Are you sure you want to continue? Press y or n" -n 1 -r -s
printf "\n"

if [[ $REPLY =~ ^[Nn]$ ]]; then
    printer SUCCESS "\nInstall cancelled"
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
    if [[ $OS == 'linux' ]]; then
        printer INFO "Running apt update/upgrade"
        sudo apt-get update
        sudo apt-get dist-upgrade -y
        touch phase1
        # TODO: Reboot should not be requird, needs to be validated
        # sudo shutdown -r +1
    fi
else
    printer SUCCESS "Phase 1 already complete. Skipping"
fi

if [[ ! -f phase2 ]]; then
    printer INFO "Upgrading Ubuntu"
    # if [[ $OS == 'linux' ]]; then
    #     printer INFO "Doing release upgrade"
    #     # sudo do-release-upgrade -q DistUpgradeViewNonInteractive 2>/dev/null || true
    # fi
    touch phase2
else
    printer SUCCESS "Phase 2 already complete. Skipping"
fi
if [[ ! -f phase3 ]]; then
    printer INFO "Installing applications"
    # Linux Only
    if [[ $OS == 'linux' ]]; then
        # Distro based apps
        ## Remove guff
        sudo apt-get remove thunderbird -y
        sudo apt-get remove --purge libreoffice* -y
        # Update pat sources for MS apps	
        sudo apt-get install -y gpg
        wget -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o microsoft.asc.gpg
        sudo mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/
        wget https://packages.microsoft.com/config/ubuntu/20.04/prod.list
        sudo mv prod.list /etc/apt/sources.list.d/microsoft-prod.list
        sudo chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg
        sudo chown root:root /etc/apt/sources.list.d/microsoft-prod.list
        sudo apt-get update
        #apt install
        sudo apt-get install net-tools git nmap curl rar \
            p7zip-full p7zip-rar vlc terminator libfuse2 \
            openvpn kompare krusader trash-cli krename \
            qbittorrent filezilla libreoffice-calc \
            krename kompare ruby-full python3-pip \
            dmidecode firefox php-fpm nginx default-jre default-jdk \
            golang-go dotnet-sdk-7.0 aspnetcore-runtime-7.0 -y
        sudo apt remove unattended-upgrades -y
        sudo apt-get autoremove -y
        export BOX=$(sudo dmidecode -s system-manufacturer)
        if [[ $BOX =~ VMware ]]; then # Install vmware tool if on a vmware host
            sudo apt-get install open-vm-tools-desktop open-vm-tools
        fi
        ## SNAPs
        if [[ ! $(which ffmpeg) ]]; then sudo snap install ffmpeg; fi
        if [[ ! $(which ffmpeg) ]]; then sudo snap install postman; fi
        ## KDENlive video editor

        if [[ ! -f $LINUX_APP_FOLDER/kdenlive ]]; then
            printer INFO "Installing KDENlive"
            wget -O $LINUX_APP_FOLDER/kdenlive https://download.kde.org/stable/kdenlive/22.12/linux/kdenlive-22.12.3-x86_64.AppImage --show-progress
            chmod +x $LINUX_APP_FOLDER/kdenlive
        fi
    fi

    # MacOS Only
    if [[ $OS == 'macos' ]]; then
        ## Install xcode
        # if [[ ! $(which xcode) ]]; then
        #     printer INFO "Installing xCode, this will take a long time!"
        #     xcode-select --install
        # fi
        ## Install Homebrew
        printer INFO "Installing Homebrew"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        brew update
        ## Install brew apps
        printer INFO "Installing Brew apps"
        brew install curl php vlc filezilla ruby python postman \
            openvpn-connect zip sevenzip rar wget nginx xtorrent \
            java go
        brew install --cask firefox
    fi

    # MacOS and Ubuntu
    ## Anaconda
    if [[ ! $(which anaconda) ]]; then
        printer INFO "Installing Anaconda"
        if [[ $OS == 'linux' ]]; then
            if [[ -d /home/developer/anaconda3 ]]; then
                sudo rm /home/developer/anaconda3 -R
            fi
            wget -O $TMP/anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh --show-progress
        else
            if [[ -d /home/developer/anaconda3 ]]; then
                rm -R /home/developer/anaconda3
            fi
            wget -O $TMP/anaconda.sh https://repo.anaconda.com/archive/Anaconda3-2023.03-1-MacOSX-x86_64.sh --show-progress
        fi
        bash $TMP/anaconda.sh -bf
        echo 'export PATH="$HOME/anaconda3/bin:$PATH"' >>~/.bashrc
	export PATH="$HOME/anaconda3/bin:$PATH"
    fi

    ## AWS CLI
    if [[ ! $(which aws) ]]; then
        printer INFO "Installing AWS CLI"
        if [[ $OS == 'linux' ]]; then
            wget -O $TMP/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" --show-progress
            unzip $TMP/awscliv2.zip -d $TMP
            sudo bash $TMP/aws/install
        else
            pip3 install awscli --upgrade --user
        fi
    fi

    ## Authy
    if [[ ! $(which authy) ]]; then
        printer INFO "Installing Authy"
        if [[ $OS == 'linux' ]]; then
            sudo snap install authy
        else
            pip3 install awscli --upgrade --user
        fi
    fi

    ## VSCode
    if [[ ! $(which code) ]]; then
        printer INFO "Installing VSCode"
        if [[ $OS == 'linux' ]]; then
            sudo snap install --classic code
        else
            brew install --cask visual-studio-code
        fi

        ## VSCode Extensions
        code --install-extension amazonwebservices.aws-toolkit-vscode
        code --install-extension Codeium.codeium
        code --install-extension cshum.convert-newline-list-to-array
        code --install-extension dbaeumer.vscode-eslint
        code --install-extension eamodio.gitlens
        code --install-extension esbenp.prettier-vscode
        code --install-extension janisdd.vscode-edit-csv
        code --install-extension jmviz.quote-list
        code --install-extension mechatroner.rainbow-csv
        code --install-extension ms-azuretools.vscode-docker
        code --install-extension ms-python.python
        code --install-extension ms-python.vscode-pylance
        code --install-extension petli-full.json-to-yaml-and-more
        code --install-extension shd101wyy.markdown-preview-enhanced
        code --install-extension streetsidesoftware.code-spell-checker
        code --install-extension Tyriar.sort-lines
        code --install-extension wmaurer.change-case
        code --install-extension foxundermoon.shell-format
    fi

    ## Node Version Manager, npm and Node
    if [[ ! $(which node) ]]; then
        printer INFO "Install Node Version Manager and NPM LTS"
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
        nvm install --lts
        ## Global NPM Packages
        npm install -g npm-check-updates create-react-app express-generator
    fi

    ## Docker
    if [[ ! $(which docker) ]]; then
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
    fi

    ## Chrome
    if [[ $OS == 'linux' ]]; then
        if [[ ! $(which google-chrome) ]]; then
            printer INFO "Installing Chrome"
            wget -O $TMP/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb --show-progress
            sudo dpkg --install $TMP/chrome.deb
        fi
    else
        printer INFO "Installing Chrome"
        wget -O https://dl.google.com/dl/chrome/mac/universal/stable/gcea/googlechrome.dmg --show-progress
        hdiutil attach $TMP/chrome.dmg -nobrowse
        cp -pPR /Volumes/Google Chrome/Google Chrome.app /Applications/
        GoogleChromeDMG="$(hdiutil info | grep "/Volumes/Google Chrome" | awk '{ print $1 }')"
        hdiutil detach $GoogleChromeDMG
    fi

    ## Tor
    if [[ $OS == 'linux' ]]; then
        if [[ ! -f $LINUX_APP_FOLDER/tor/tor ]]; then
            wget -O $TMP/tor.tar.xz https://www.torproject.org/dist/torbrowser/12.5/tor-browser-linux64-12.5_ALL.tar.xz --show-progress
            tar -xf $TMP/tor.tar.xz -C $LINUX_APP_FOLDER
        fi
    else
        brew install tor
    fi

    # Creating SSH keys for use with git
    if [[ ! -f ~/.ssh/$EMAIL ]]; then
        printer INFO "Generating ssh keypair for use with git"
        ssh-keygen -t rsa -N '' -f ~/.ssh/$EMAIL <<<y
    fi

    # Config Apps
    ## Config Git
    printer INFO "Updatng app configs."
    git config --global --replace-all user.email "$EMAIL"
    git config --global --replace-all user.name "$NAME"

    ## Templates
    cp assets/templates/* ~/Templates -r
    ## Terminator
    if [[ $OS == 'linux' ]]; then
        if [[ ! -d ~/.config/terminator ]]; then
            mkdir ~/.config/terminator
            cp assets/terminator ~/.config/terminator/config/terminator-config
        fi
        # Backup
        cp ~/.profile ~/.profile.old
        cp assets/bashrc ~/.bashrc.old
        # Copy
        cp assets/profile ~/.profile
        cp assets/bashrc ~/.bashrc
        cp assets/vscode ~/.config/Code/User/settings.json
    fi

    ## Set shell prompt
    if [[ $OS == 'linux' ]]; then
        echo "export PS1='\[\033[1;32m\]$(whoami)@\[\033[1;34m\]$(hostname):\[\033[33m\]$(pwd)\[\033[0;37m\]\[\e[91m\]$(parse_git_branch)\[\e[00m\]\n'" >>~/.bashrc
    else
        echo "export PS1='\[\033[1;32m\]$(whoami)@\[\033[1;34m\]$(hostname):\[\033[33m\]$(pwd)\[\033[0;37m\]\[\e[91m\]$(parse_git_branch)\[\e[00m\]\n'" >>~/.bashrc
    fi

    # Clean up
    #rm $TMP -r
    touch phase3
	source ~/.bashrc
    printer SUCCESS "DevBox build complete."
else
    printer SUCCESS "Phase 3 already complete."
fi
printer INFO "Node:"
node --version
printer INFO "npm:"
npm --version
printer INFO "Java:"
java --version
printer INFO "Python:"
python3 --version
printer INFO "PHP:"
php --version
printer INFO ".Net"
dotnet --version
printer INFO "AWS CLI"
aws --version
