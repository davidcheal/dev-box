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


def printer(color, text):
    print(f"{color}{text}{RESET}")


# Defaults
EMAIL = "david.cheal@gmail.com"  # default
NAME = "David Cheal"  # default
BOX_TYPE = "devbox"  # default
VMWARE = False
LINUX_APP_FOLDER = os.path.expanduser("~/apps")
HOME = os.path.expanduser("~/")
PROJECT_DIR = os.path.expanduser("~/projects")

LINUX_COMMANDS = [
    "sudo apt-get update",
    "wget -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o microsoft.asc.gpg",
    "sudo mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/",
    "wget https://packages.microsoft.com/config/ubuntu/20.04/prod.list",
    "sudo mv prod.list /etc/apt/sources.list.d/microsoft-prod.list",
    "curl -fsSL https://packages.openvpn.net/packages-repo.gpg | sudo tee /etc/apt/keyrings/openvpn.asc",
    "echo deb [signed-by=/etc/apt/keyrings/openvpn.asc] https://packages.openvpn.net/openvpn3/debian jammy main | sudo tee /etc/apt/sources.list.d/openvpn-packages.list",
    "sudo apt-get update",
    "sudo chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg",
    "sudo chown root:root /etc/apt/sources.list.d/microsoft-prod.list",
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
        "which": "",
    },
    {
        "name": "Firefox",
        "package_name": "firefox",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "GPG",
        "package_name": "gpg",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "JQ",
        "package_name": "jq",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Kompare",
        "package_name": "kompare",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "K Rename",
        "package_name": "krename",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Krusader",
        "package_name": "krusader",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Libre Office Calc",
        "package_name": "libreoffice-calc",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Network Tools",
        "package_name": "net-tools",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "P7 Zip",
        "package_name": "p7zip-full",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "P7 RAR",
        "package_name": "p7zip-rar",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Python 3 PIP",
        "package_name": "python3-pip",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Qbittorrent",
        "package_name": "qbittorrent",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Rar",
        "package_name": "rar",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Terminator",
        "package_name": "terminator",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Trash CLI",
        "package_name": "trash-cli",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "VLC Player",
        "package_name": "vlc",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "FF Mpeg",
        "package_name": "ffmpeg",
        "options": None,
        "installer": "apt",
        "which": "",
    },
]

LINUX_DEV_APPS = [
    {
        "name": ".Net Core Runtime",
        "package_name": "aspnetcore-runtime-7.0",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": ".Net Core SDK",
        "package_name": "dotnet-sdk-7.0",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Java JDK",
        "package_name": "default-jdk",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Java JRE",
        "package_name": "default-jre",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "FileZilla",
        "package_name": "filezilla",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "GoLang",
        "package_name": "golang-go",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "GoLang",
        "package_name": "golang-go",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "NGINX",
        "package_name": "nginx",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "NMap",
        "package_name": "nmap",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Open VPN",
        "package_name": "openvpn3",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "PHP FPM",
        "package_name": "php-fpm",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Ruby",
        "package_name": "ruby-full",
        "options": None,
        "installer": "apt",
        "which": "",
    },
    {
        "name": "Postman",
        "package_name": "postman",
        "options": None,
        "installer": "snap",
        "which": "",
    },
    {
        "name": "VSCode",
        "package_name": "--classic code",
        "options": None,
        "installer": "snap",
        "which": "",
    },
]

# Detect VMWARE
DMI_CODE = subprocess.check_output("sudo dmidecode -s system-manufacturer", shell=True)

if re.match("VMware", str(DMI_CODE, encoding="utf-8")):
    VMWARE = True
# Detect Ubuntu or MacOs
if "linux" in platform.system().lower():
    OS = "linux"
    TMP = "/tmp/build"
elif "darwin" in platform.system().lower():
    OS = "macos"
    TMP = "/tmp/build"
else:
    printer(CRIT, "OS doesn't match anything this script can help with.")
    sys.exit(1)


def linux_commands(commands):
    for command in commands:
        try:
            subprocess.check_call(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True
            )
            printer(SUCCESS, command + " successful")
        except subprocess.CalledProcessError:
            printer(CRIT, command + " failed")
            sys.exit(1)


def install_linux_packages(packages):
    try:
        for APP in packages:
            installed = False
            if subprocess.call(f"which {APP['package_name']}", shell=True) == 0:
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
                        f"snap install -y {APP['package_name']}, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True"
                    )
                printer(SUCCESS, f"{APP['name']} installation successful")
            else:
                printer(INFO, APP["name"] + "already installed")
    except subprocess.CalledProcessError:
        printer(CRIT, f"{APP['name']} installation failed")
        sys.exit(1)


def linux_configure():
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

linux_commands(LINUX_COMMANDS)
linux_configure()
install_linux_packages(LINUX_BASE_APPS)
install_linux_packages(LINUX_DEV_APPS)
