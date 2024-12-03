```
 ████    ████   ████████╗███████╗██████╗ ███╗   ███╗ ██████╗ 
 ████    ████   ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
     ████          ██║   █████╗  ██████╔╝██╔████╔██║██║
   ████████        ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║
   ████████        ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╗
   ██    ██        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝
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
Is higly recommended to use `pipx` insted of `pip`, but you can use it anyway
```bash
pipx install git+https://github.com/LBY-L/TerMC.git
```

## Run
Remember to set in your path `~/.local/bin`, to be able to use TerMC
```bash
termc
```
