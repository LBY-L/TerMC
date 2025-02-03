<p align="center"><a href="https://github.com/LBY-L/TerMC"><img src="https://github.com/user-attachments/assets/a90c8c78-f223-4922-90f8-c6cb5b049722" alt="Logo" height="450"/></a></p>

<h3 align="center">A simple script to download and execute Minecraft servers 🎇</h3>


## Script dependences

> Termux:
> ```bash
> pkg install python3 python-pip openjdk-17
> ```
> IMPORTANT: In the case of Termux, there isn't an Openjdk 21 package so the 1.21,CAN'T RUN

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
> sudo pacman -S python python-pip jre21-openjdk-headless
> ```

## Install
Is higly recommended to use `pipx` insted of `pip`, but you can use it anyway
```bash
pipx install git+https://github.com/LBY-L/TerMC.git --force
```

## Run
Remember to set in your path `~/.local/bin`, to be able to use TerMC
```bash
termc
```
