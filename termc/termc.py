#!/bin/python3

# THIS IS A POSIX SCRIPT, SO DON'T RUN IT IN A WINDOWS/NT SYSTEM!!!
# ████████╗███████╗██████╗ ███╗   ███╗ ██████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
#    ██║   █████╗  ██████╔╝██╔████╔██║██║
#    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║
#    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╗
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝
# “MANKIND IS DEAD. BLOOD IS FUEL. HELL IS FULL.” - UltraKill

import os, time, readline, signal, urllib.request
from InquirerPy import inquirer
from yaspin import yaspin
from yaspin.spinners import Spinners
from json import loads

def UserAgent():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion')]
    urllib.request.install_opener(opener)

@yaspin(Spinners.growHorizontal, "[ Getting Versions ]")
def GetMohistVer():
    UserAgent()
    versionsRaw = urllib.request.urlopen("https://mohistmc.com/api/v2/projects/mohist").read()
    versions = loads(versionsRaw)["versions"]
    urllib.request.urlcleanup()
    return list(reversed(versions))

@yaspin(Spinners.growHorizontal, "[ Getting Available Builds ]")
def GetMohistBuild(ver):
    UserAgent()
    buildRaw = urllib.request.urlopen(f"https://mohistmc.com/api/v2/projects/mohist/{ver}/builds").read()
    builds = loads(buildRaw)
    buildsDict = {}
    for buildsList in list(reversed(builds["builds"])):
        buildsDict[buildsList["number"]] = buildsList["url"]
    urllib.request.urlcleanup()
    return buildsDict

@yaspin(Spinners.growHorizontal, "[ Getting Versions ]")
def GetVanilla():
    versions = loads(urllib.request.urlopen("https://launchermeta.mojang.com/mc/game/version_manifest.json").read())["versions"]
    # I don't set the url to a variable because the minecraft servers are very slow
    versionsDict = {}

    for versionInfo in filter(lambda x: x["type"] == "release", versions):
        url = loads(urllib.request.urlopen(versionInfo["url"]).read())["downloads"]["server"]["url"]
        release = versionInfo["id"]
        versionsDict[release] = url
        if release == "1.2.5": # The servers are good until this versions
            break

    return versionsDict

@yaspin(Spinners.growHorizontal, "[ Getting Versions ]")
def GetFabricVer():
    versionsRaw = urllib.request.urlopen("https://meta.fabricmc.net/v2/versions").read()
    versions = loads(versionsRaw)["game"]
    listVer = []

    for versionInfo in filter(lambda x: x["stable"] == True, versions):
        listVer.append(versionInfo["version"])

    return listVer

@yaspin(Spinners.growHorizontal, "[ Getting Available Loaders ]")
def GetFabricLoader(ver):
    loaderRaw = urllib.request.urlopen(f"https://meta.fabricmc.net/v2/versions/loader/{ver}").read()
    loaders = loads(loaderRaw)
    loadersList = []
    for loaderVerRaw in loaders:
        loaderVer = loaderVerRaw["loader"]["version"]
        loadersList.append(loaderVer)
        if loaderVer == "0.12.0":
            break
    return loadersList

@yaspin(Spinners.growHorizontal, "[ Getting Versions ]")
def GetPaperVer():
    versionsRaw = urllib.request.urlopen("https://api.papermc.io/v2/projects/paper/").read()
    versions = loads(versionsRaw)["versions"]
    listVer = []

    for versionInfo in versions:
        if versionInfo != "1.13-pre7":
            listVer.append(versionInfo)
    return list(reversed(listVer))

@yaspin(Spinners.growHorizontal, "[ Getting Available Builds ]")
def GetPaperBuild(ver):
    buildRaw = urllib.request.urlopen(f"https://api.papermc.io/v2/projects/paper/versions/{ver}/builds/").read()
    builds = loads(buildRaw)["builds"]
    buildsList = []
    for buildVerRaw in list(reversed(builds)):
        buildsList.append(buildVerRaw["build"])
    return buildsList

@yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
def GetBTAVer():
    versionsRaw = urllib.request.urlopen("https://api.github.com/repos/Better-than-Adventure/bta-download-repo/tags").read()
    versions = loads(versionsRaw)
    verList = []

    for versionInfo in versions:
        verList.append(versionInfo['name'])
        if versionInfo['name'] == "v1.7.6-prerelease-2c":
            break

    verDict = {}

    for releases in verList:
         releasesRaw = urllib.request.urlopen(f"https://api.github.com/repos/Better-than-Adventure/bta-download-repo/releases/tags/{releases}").read()
         releasesList = loads(releasesRaw)
         for realeaseInfo in releasesList["assets"]:
             if "server" in realeaseInfo["name"]:
                 verDict[releases] = f"https://github.com/Better-than-Adventure/bta-download-repo/releases/download/{releases}/{realeaseInfo['name']}"

    return(verDict)

def Ram():
    ram = os.popen("free -h | awk '/^Mem:/{print $2}'").readlines()[0].strip()[:-2]
    ramAllocation = []
    for ramSymbol in range(1, round(float(ram))+1):
        ramAllocation.append(f"{ramSymbol}G")

    RamSelection = inquirer.select(
        message="How many GB of ram you'll use?",
        choices=ramAllocation,
    ).execute()

    return RamSelection

def Folder():
    HOME = os.environ["HOME"]

    if not os.path.isdir(f"{HOME}/MinecraftServers"):
        os.mkdir(f"{HOME}/MinecraftServers")

    result = inquirer.text(
            message="Name:",
            validate=lambda result: len(result) > 0 and not "/" in result and not "\\" in result and not " " in result and not os.path.isdir(f"{HOME}/MinecraftServers/{result}/"),
            invalid_message="Input cannot be empty and can't contain spaces, '/' & '\\', and can't be the same!",
    ).execute()

    os.mkdir(f"{HOME}/MinecraftServers/{result}")

    return f"{HOME}/MinecraftServers/{result}/"

def CreateMethod():
    FOLDER = Folder()
    RAM = Ram()
    def CreateFolder(paper=False, jar=""):
        with open(FOLDER + "eula.txt", "w") as file:
            file.write("eula=true")

        with open(FOLDER + "run.sh", "w") as file:
            if paper:
                file.write(f"java -Xms{RAM} -Xmx{RAM} -DPaper.IgnoreJavaVersion=true -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar {FOLDER}{jar}")
            else:
                file.write(f"java -Xms{RAM} -Xmx{RAM} -jar {FOLDER}{jar}")

    Server = inquirer.select(
        message="What server type you'll use?",
        choices=["Fabric", "Paper", "Vanilla", "Mohist", "BTA (Better Than Adventure)"],
    ).execute()

    match Server:
        case "BTA (Better Than Adventure)":

            Versions = GetBTAVer()
            Bersion = inquirer.select(message="What version you want?", choices=list(Versions.keys())).execute()

            with yaspin(text=f"[ Downloading Better Than Adventure {Bersion} ]") as sp:
                urllib.request.urlretrieve(Versions[Bersion], FOLDER + "bta.jar")

            CreateFolder(jar="bta.jar")

        case "Vanilla":

            Versions = GetVanilla()
            Version = inquirer.select(message="What version you want?", choices=list(Versions.keys())).execute()

            with yaspin(text=f"[ Downloading Minecraft {Version} ]") as sp:
                urllib.request.urlretrieve(Versions[Version], FOLDER + "server.jar")

            CreateFolder(jar="server.jar")

        case "Fabric":

            Versions = GetFabricVer()
            Fersion = inquirer.select(message="What version you want?", choices=Versions).execute()

            Loader = GetFabricLoader(Fersion)

            Foader = inquirer.select(message="What loader version you'll use??", choices=Loader).execute()

            with yaspin(text=f"[ Downloading Minecraft {Fersion} ]") as sp:
                urllib.request.urlretrieve(f"https://meta.fabricmc.net/v2/versions/loader/{Fersion}/{Foader}/1.0.0/server/jar", FOLDER + "fabric.jar")

            CreateFolder(jar="fabric.jar")

        case "Paper":

            Versions = GetPaperVer()
            Persion = inquirer.select(message="What version you want?", choices=Versions).execute()
            Builds = GetPaperBuild(Persion)
            Build = inquirer.select(message="What build version you'll use?", choices=Builds).execute()

            with yaspin(text=f"[ Downloading Minecraft {Persion} ]") as sp:
                DownloadRaw = urllib.request.urlopen(f"https://api.papermc.io/v2/projects/paper/versions/{Persion}/builds/{Build}/").read()
                Download = loads(DownloadRaw)["downloads"]["application"]["name"]
                urllib.request.urlretrieve(f"https://api.papermc.io/v2/projects/paper/versions/{Persion}/builds/{Build}/downloads/{Download}", FOLDER + "paper.jar")

            CreateFolder(paper=True, jar="paper.jar")

        case "Mohist":

            Versions = GetMohistVer()
            Mersion = inquirer.select(message="What version you want?",choices=Versions).execute()

            Builds = GetMohistBuild(Mersion)

            Build = inquirer.select(message="What build version you'll use?", choices=list(Builds.keys())).execute()

            with yaspin(text=f"[ Downloading Minecraft {Mersion} ]") as sp:
                UserAgent()
                urllib.request.urlretrieve(Builds[Build], FOLDER + "mohist.jar")
                urllib.request.urlcleanup()

            CreateFolder(jar="mohist.jar")

def StartMethod():
    HOME = os.environ["HOME"]
    servers = os.listdir(f"{HOME}/MinecraftServers")
    servers.append("Exit")
    Server = inquirer.select(message="Select a server to run", choices=list(servers)).execute()

    if Server != "Exit":
        os.chdir(f"{HOME}/MinecraftServers/{Server}")
        os.system("bash run.sh")

def RemoveMethod():
    while True:
        HOME = os.environ["HOME"]
        servers = os.listdir(f"{HOME}/MinecraftServers")
        servers.append("Exit")

        Server = inquirer.select(message="Select a server to remove", choices=list(servers)).execute()

        os.system(f"rm -rf '{HOME}/MinecraftServers/{Server}'")

        if Server == "Exit": break

def Method():
    MethodSelection = inquirer.select(message="What do you want to do?", choices=["Create", "Start", "Remove", "Exit"]).execute()

    match MethodSelection:
        case "Create":
            CreateMethod()
            Method()
        case "Start":
            StartMethod()
            Method()
        case "Remove":
            RemoveMethod()
            Method()
        case "Exit":
            quit()
