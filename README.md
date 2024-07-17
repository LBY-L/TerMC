```
 ████████╗███████╗██████╗ ███╗   ███╗ ██████╗
 ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
    ██║   █████╗  ██████╔╝██╔████╔██║██║
    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║
    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╗
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝
```
### A simple script to download and execute Minecraft servers 🎇
## Script dependences

> Termux:
> ```bash
> pkg install python3 python-pip openjdk-17
> ```
> IMPORTANT: In the case of Termux, there isn't Openjdk 21 so the 1.21, CAN'T RUN

> Fedora/CentOS/OpenSUSE:
> ```bash
> sudo dnf install python3 python3-pip java-21-openjdk-headless
> ```

> Debian/Ubuntu:
> ```bash
> sudo apt install python3 python3-pip openjdk-21-jre-headless bash
> ```

> Arch/Manjaro:
> ```bash
> sudo pacman -S python python-pip jre21-openjdk-headless bash
> ```

## Install
```bash
pip3 install git+https://github.com/LBY-L/TerMC.git
```

## Run
```bash
python3 -m termc
```

## Portable Run
> Bash/Zsh
> ```bash
> python3 -c $("https://raw.githubusercontent.com/LBY-L/TerMC/main/termc/termc.py")
> ```

> Fish
> ```bash
> python3 -c ("https://raw.githubusercontent.com/LBY-L/TerMC/main/termc/termc.py")
> ```
