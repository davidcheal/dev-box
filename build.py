#!/usr/bin/env python3

import os
import platform
import re
import shutil
import subprocess
import sys

CRIT = "\033[31m"
SUCCESS = "\033[32m"
WARN = "\033[33m"
RESET = "\033[0m"
INFO = "\033[37m"
OS_NAME = "unknown"


def printer(color, text):
    print(f"{color}{text}{RESET}")


if "Linux" in platform.system():
    OS_NAME = "Linux"
elif "Darwin" in platform.system():
    OS_NAME = "Mac"
else:
    printer(CRIT, f"{OS_NAME} doesn't match any OS this script can help with.")
    sys.exit(1)

# Defaults
EMAIL = "david.cheal@gmail.com"  # default
NAME = "David Cheal"  # default
BOX_TYPE = "devbox"  # default
VMWARE = False
LINUX_APP_FOLDER = os.path.expanduser("~/apps")
HOME = os.path.expanduser("~/")
PROJECT_DIR = os.path.expanduser("~/projects")


def create_build_loc():
    if OS_NAME == "Linux":
        if not os.path.exists("/tmp/build"):
            os.mkdir("/tmp/build")


LINUX_COMMANDS = [
    "sudo apt-get update",
    "wget -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o microsoft.asc.gpg",
    "sudo mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/",
    "wget https://packages.microsoft.com/config/ubuntu/20.04/prod.list",
    "sudo mv prod.list /etc/apt/sources.list.d/microsoft-prod.list",
    "sudo chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg",
    "sudo chown root:root /etc/apt/sources.list.d/microsoft-prod.list",
    "curl -fsSL https://packages.openvpn.net/packages-repo.gpg | sudo tee /etc/apt/keyrings/openvpn.asc",
    "echo deb [signed-by=/etc/apt/keyrings/openvpn.asc] https://packages.openvpn.net/openvpn3/debian jammy main | sudo tee /etc/apt/sources.list.d/openvpn-packages.list",
    "sudo apt-get update",
    "sudo apt-get remove thunderbird -y",
    "sudo apt-get remove --purge libreoffice* -y",
    "sudo apt-get upgrade -y",
    "sudo apt remove unattended-upgrades -y",
    "sudo apt-get autoremove -y",
]

LINUX_BASE_APPS = [
    {
        "name": "Curl",
        "package_name": "curl",
        "options": None,
        "installer": "apt",
        "which": "curl",
    },
    {
        "name": "DMI Decode",
        "package_name": "dmidecode",
        "options": None,
        "installer": "apt",
        "which": "dmidecode",
    },
    {
        "name": "Firefox",
        "package_name": "firefox",
        "options": None,
        "installer": "apt",
        "which": "firefox",
    },
    {
        "name": "GPG",
        "package_name": "gpg",
        "options": None,
        "installer": "apt",
        "which": "gpg",
    },
    {
        "name": "JQ",
        "package_name": "jq",
        "options": None,
        "installer": "apt",
        "which": "jq",
    },
    {
        "name": "Kompare",
        "package_name": "kompare",
        "options": None,
        "installer": "apt",
        "which": "kompare",
    },
    {
        "name": "K Rename",
        "package_name": "krename",
        "options": None,
        "installer": "apt",
        "which": "krename",
    },
    {
        "name": "Krusader",
        "package_name": "krusader",
        "options": None,
        "installer": "apt",
        "which": "krusader",
    },
    {
        "name": "Libre Office Calc",
        "package_name": "libreoffice-calc",
        "options": None,
        "installer": "apt",
        "which": "libreoffice --calc",
    },
    {
        "name": "Network Tools",
        "package_name": "net-tools",
        "options": None,
        "installer": "apt",
        "which": False,
    },
    {
        "name": "P7 Zip",
        "package_name": "p7zip-full",
        "options": None,
        "installer": "apt",
        "which": "p7zip",
    },
    {
        "name": "P7 RAR",
        "package_name": "p7zip-rar",
        "options": None,
        "installer": "apt",
        "which": "p7zip",
    },
    {
        "name": "Python 3 PIP",
        "package_name": "python3-pip",
        "options": None,
        "installer": "apt",
        "which": "pip",
    },
    {
        "name": "Qbittorrent",
        "package_name": "qbittorrent",
        "options": None,
        "installer": "apt",
        "which": "qbittorrent",
    },
    {
        "name": "Rar",
        "package_name": "rar",
        "options": None,
        "installer": "apt",
        "which": "rar",
    },
    {
        "name": "Terminator",
        "package_name": "terminator",
        "options": None,
        "installer": "apt",
        "which": "terminator",
    },
    {
        "name": "Trash CLI",
        "package_name": "trash-cli",
        "options": None,
        "installer": "apt",
        "which": "trash",
    },
    {
        "name": "VLC Player",
        "package_name": "vlc",
        "options": None,
        "installer": "apt",
        "which": "vlc",
    },
    {
        "name": "FF Mpeg",
        "package_name": "ffmpeg",
        "options": None,
        "installer": "apt",
        "which": "ffmpeg",
    },
]

LINUX_DEV_APPS = [
    {
        "name": ".Net Core Runtime",
        "package_name": "aspnetcore-runtime-7.0",
        "options": None,
        "installer": "apt",
        "which": "dotnet",
    },
    {
        "name": ".Net Core SDK",
        "package_name": "dotnet-sdk-7.0",
        "options": None,
        "installer": "apt",
        "which": "dotnet",
    },
    {
        "name": "Java JDK",
        "package_name": "default-jdk",
        "options": None,
        "installer": "apt",
        "which": "javac",
    },
    {
        "name": "Java JRE",
        "package_name": "default-jre",
        "options": None,
        "installer": "apt",
        "which": "java",
    },
    {
        "name": "FileZilla",
        "package_name": "filezilla",
        "options": None,
        "installer": "apt",
        "which": "filezilla",
    },
    {
        "name": "GoLang",
        "package_name": "golang-go",
        "options": None,
        "installer": "apt",
        "which": "go",
    },
    {
        "name": "NGINX",
        "package_name": "nginx",
        "options": None,
        "installer": "apt",
        "which": "nginx",
    },
    {
        "name": "NMap",
        "package_name": "nmap",
        "options": None,
        "installer": "apt",
        "which": "nmap",
    },
    {
        "name": "Open VPN",
        "package_name": "openvpn3",
        "options": None,
        "installer": "apt",
        "which": "openvpn3",
    },
    {
        "name": "PHP FPM",
        "package_name": "php-fpm",
        "options": None,
        "installer": "apt",
        "which": "php",
    },
    {
        "name": "Ruby",
        "package_name": "ruby-full",
        "options": None,
        "installer": "apt",
        "which": "ruby",
    },
    {
        "name": "Postman",
        "package_name": "postman",
        "options": None,
        "installer": "snap",
        "which": "postman",
    },
    {
        "name": "VSCode",
        "package_name": "code",
        "options": "--classic",
        "installer": "snap",
        "which": "code",
    },
]

# Detect VMWARE
DMI_CODE = subprocess.check_output("sudo dmidecode -s system-manufacturer", shell=True)

if re.match("VMware", str(DMI_CODE, encoding="utf-8")):
    VMWARE = True


# Detect Ubuntu or MacOs


def install_chrome():
    if OS_NAME == "Linux":
        if (
                subprocess.call(
                    "which chrome",
                    shell=True,
                )
                == 1
        ):
            return
        subprocess.check_call(
            "wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/build/chrome.deb",
            shell=True,
        )
        subprocess.check_call(
            "sudo dpkg -i /tmp/build/chrome.deb",
            shell=True,
        )


def install_node():
    if OS_NAME == "Linux":
        if subprocess.call("which node", shell=True) == 0:
            subprocess.check_call(
                " curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash",
                shell=True,
            )
            subprocess.check_call("nvm install --lts", shell=True)
            subprocess.check_call(
                "npm install -g npm-check-updates vite express-generator",
                shell=True,
            )
            printer(SUCCESS, "Node installation successful. Reboot before sue")
        else:
            printer(INFO, "Node Already installed")


def linux_commands(commands):
    if OS_NAME != "Linux":
        return
    for command in commands:
        try:
            subprocess.check_call(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True
            )
            printer(SUCCESS, command + " successful")
        except subprocess.CalledProcessError as e:
            printer(
                CRIT,
                f"'{command}' failed with Code: {e.returncode} message: {e.output}",
            )
            sys.exit(1)


def install_linux_packages(packages):
    if OS_NAME != "Linux":
        return
    for APP in packages:
        try:
            installed = False
            if subprocess.call(f"which {APP['which']}", shell=True) == 0:
                installed = True
            if not installed:
                printer(INFO, f"Installing {APP['name']}")
                if APP["installer"] == "apt":
                    subprocess.check_call(
                        "sudo apt-get install -y " + APP["package_name"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT,
                        shell=True,
                    )
                else:
                    subprocess.check_call(
                        f"snap install {APP['package_name']} {APP['options']}, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True"
                    )
                printer(SUCCESS, f"{APP['name']} installation successful")
            else:
                printer(INFO, APP["name"] + " already installed")
        except subprocess.CalledProcessError:
            printer(CRIT, f"{APP['name']} installation failed")
            sys.exit(1)


def linux_configure():
    if OS_NAME != "Linux":
        return
    if not os.path.exists(os.path.expanduser(f"{HOME}.config/terminator")):
        os.mkdir(os.path.expanduser(f"{HOME}.config/terminator"))
        shutil.copyfile(
            "./assets/terminator", f"{HOME}.config/terminator/config/terminator-config"
        )
    if not os.path.isfile(os.path.expanduser(f"{HOME}.ssh/known_hosts")):
        subprocess.check_call(
            f"ssh-keygen -t rsa -N '' -f {HOME}.ssh/{EMAIL} <<<y",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            shell=True,
        )
    shutil.copyfile(f"{HOME}.profile", f"{HOME}.profile.old")
    shutil.copyfile("./assets/bashrc", f"{HOME}.bashrc.old")
    shutil.copyfile("./assets/profile", f"{HOME}.profile")
    shutil.copyfile("./assets/bashrc", f"{HOME}.bashrc")
    subprocess.check_call(
        f"git config --global --replace-all user.email {EMAIL}",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=True,
    )
    subprocess.check_call(
        f"git config --global --replace-all user.name {NAME}",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        shell=True,
    )


# Get user input
BOX_TYPE = input(f"What box type?: minimal or [{BOX_TYPE}] ") or BOX_TYPE
EMAIL = input(f"What is your email address?: [{EMAIL}]") or EMAIL
NAME = input(f"What is your name?: [{NAME}]") or NAME

create_build_loc()
linux_commands(LINUX_COMMANDS)
linux_configure()
install_chrome()
install_linux_packages(LINUX_BASE_APPS)
install_linux_packages(LINUX_DEV_APPS)
