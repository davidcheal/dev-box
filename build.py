#!/usr/bin/env python3

import os
import platform
import subprocess
from getpass import getpass
import sys
import re

CRIT = "\033[31m"
SUCCESS = "\033[32m"
WARN = "\033[33m"
RESET = "\033[0m"
INFO = "\033[37m"

# DEfaults
EMAIL = "david.cheal@gmail.com"  # default
NAME = "David Cheal"  # default
BOX_TYPE = "devbox"  # default
LINUX_APP_FOLDER = os.path.expanduser("~/apps")
VMWARE = False

LINUX_APT = "sudo apt-get install -y"
MACOS_BREW = "brew install -y",

BASE_LINUX_APPS = [
    {"name":"Curl", "package_name":"curl", "options":None},
    {"name":"DMI Decode", "package_name":"dmidecode", "options":None},
    {"name":"Firefox", "package_name":"firefox", "options":None},
    {"name":"GPG", "package_name":"gpg", "options":None},
    {"name":"jq", "package_name":"jq", "options":None},
    {"name":"Kompare", "package_name":"kompare", "options":None},
    {"name":"KRename", "package_name":"krename", "options":None},
    {"name":"Krusader", "package_name":"krusader", "options":None},
    {"name":"librefuse2", "package_name":"librefuse2", "options":None},
    {"name":"jq", "package_name":"jq", "options":None},
    {"name":"libreoffice-calc", "package_name":"libreoffice-calc", "options":None},
    {"name":"Network Tools", "package_name":"net-tools", "options":None},
   
    # "libreoffice-calc",
    # "net-tools",
    # "p7zip-full",
    # "p7zip-rar",
    # "python3-pip",
    # "qbittorrent",
    # "rar",
    # "terminator",
    # "trash-cli",
    # "vlc",
]

CROSS_PLATFORM = [
    {
        "name": "ffmpeg",
        "package_name": "ffmpeg",
        
    },
    {
        "name": "aws cli",
        "package_name": "aws",
        "linux": "sudo apt-get install -y",
        "macos": "brew install -y",
    }
]

DEV_LINUX_APP = [
    "aspnetcore-runtime-7.0",
    "default-jdk",
    "default-jre",
    "dotnet-sdk-7.0",
    "filezilla",
    "golang-go",
    "nginx",
    "nmap",
    "openvpn",
    "php-fpm",
    "ruby-full",
]

BREW_APPS = [
    "curl",
    "php",
    "vlc",
    "ruby",
    "python",
    "postman",
    "openvpn-connect",
    "zip",
    "sevenzip",
    "rar" "wget" "nginx" "xtorrent" "java",
    "go",
]

def printer(color, text):
    print(f"{color}{text}{RESET}")


# Detect VMWARE
DMI_CODE = subprocess.check_call("sudo dmidecode -s system-manufacturer", shell=True)
if re.match("VMware", DMI_CODE):
    VMWARE = True



# Detect Ubuntu or MacOs
if "linux" in platform.system().lower():
    OS = "linux"
    PROJECT_DIR = os.path.expanduser("~/projects")
    TMP = "/tmp/build"
elif "darwin" in platform.system().lower():
    OS = "macos"
    PROJECT_DIR = os.path.expanduser("~/projects")
    TMP = "/tmp/build"
else:
    printer(CRIT, "OS doesn't match anything this script can help with.")
    sys.exit(1)

def install_linux_packages(packages):
    try:
        APPS = " ".join(map(str, packages))
        for APP in APPS:
            INSTALLED = True if subprocess.call("which " + APP.package_name, shell=True) else False
            if not INSTALLED:
                subprocess.call(APP[OS] + " " + APP.package_name, shell=True)
                # subprocess.check_call("sudo apt-get install -y " + apps, shell=True)
                printer(SUCCESS, f"{packages} installation successful")
    except subprocess.CalledProcessError:
        printer(CRIT, f"{packages} installation failed")
        sys.exit(1)

def install_python_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"{SUCCESS}{package_name} installation successful.")
    except subprocess.CalledProcessError:
        print(f"{CRIT}Error occurred during {package_name} installation.")
        sys.exit(1)

BOX_TYPE = input(f"What box type?: minimal or [{BOX_TYPE}] ") or BOX_TYPE
EMAIL = input(f"What is your email address?: [{EMAIL}]") or EMAIL
NAME = input(f"What is your name?: [{NAME}]") or NAME

# Install OS specific apps
if OS == "linux":
    COMMANDS = [
        "sudo apt-get update",
        "wget -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o microsoft.asc.gpg",
        "sudo mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/",
        "wget https://packages.microsoft.com/config/ubuntu/20.04/prod.list",
        "sudo mv prod.list /etc/apt/sources.list.d/microsoft-prod.list",
        "sudo chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg",
        "sudo chown root:root /etc/apt/sources.list.d/microsoft-prod.list",
        "sudo apt-get remove thunderbird -y",
        "sudo apt-get remove --purge libreoffice* -y",
        "sudo apt remove unattended-upgrades -y",
        "sudo apt-get autoremove -y",
        "sudo apt-get upgrade -y",
    ]
    # Install vmware tools on VM Guests
    if VMWARE:
        subprocess.check_call(
            "sudo apt-get install open-vm-tools-desktop open-vm-tools -y", shell=True
        )
    # Make project folders
    subprocess.check_call("sudo mkdir -p " + LINUX_APP_FOLDER, shell=True)
    subprocess.check_call("sudo chown -R $USER:$USER " + LINUX_APP_FOLDER, shell=True)
    # Snaps
    subprocess.check_call("sudo snap install ffmpeg", shell=True)
    subprocess.check_call("sudo snap install postman", shell=True)
if OS == "macos":
    subprocess.check_call(
        'NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
        shell=True,
    )
    subprocess.check_call("brew update", shell=True)

    subprocess.check_call("brew install " + " ".join(map(str, BREW_APPS)), shell=True)
    subprocess.check_call("brew install --cask firefox", shell=True)


for app in CROSS_PLATFORM:
    INSTALLED = True if subprocess.call("which " + app.package_name, shell=True) else False
    if not INSTALLED:
        subprocess.call(app[OS] + " " + app.package_name, shell=True)
