#!/bin/python3

# THIS IS A HAS POSIX IN, SO DON'T RUN IT IN A WINDOWS/NT SYSTEM!!!
# ████████╗███████╗██████╗ ███╗   ███╗ ██████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
#    ██║   █████╗  ██████╔╝██╔████╔██║██║
#    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║
#    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╗
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝
# “MANKIND IS DEAD. BLOOD IS FUEL. HELL IS FULL.” - UltraKill

import os, readline, urllib.request, shutil
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from psutil import virtual_memory as RamMemory
from yaspin import yaspin
from yaspin.spinners import Spinners
from json import loads

def UserAgent():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion')]
    urllib.request.install_opener(opener)

@yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
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

@yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
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

@yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
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

@yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
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
    ramAllocation = []
    for ramSymbol in range(1, (RamMemory().total//1000000000)-1):
        ramAllocation.append(f"{ramSymbol}G")

    RamSelection = inquirer.select(
        message="How many GB of ram you'll use?",
        choices=ramAllocation,
    ).execute()

    return RamSelection

def Folder():
    HOME = os.environ["HOME"]

    def GValidator(result):
        if len(result) == 0:
            return False
        if "/" in result or "\\" in result or " " in result or "|" in result:
            return False
        if os.path.isdir(f"{HOME}/MinecraftServers/{result}/"):
            return False
        return True

    result = inquirer.text(
            message="Name:",
            validate=GValidator,
            invalid_message="Input cannot be empty and can't contain spaces, \
            or '/' & '\\', '|' and can't be the same!"
    ).execute()

    return f"{HOME}/MinecraftServers/{result}/"

def SetupFolder(paper=False, jar="", Ram="", Folder=""):
    HOME = os.environ["HOME"]

    if not os.path.isdir(f"{HOME}/MinecraftServers"):
        os.mkdir(f"{HOME}/MinecraftServers")

    os.mkdir(Folder)

    AcceptEula = inquirer.confirm(
        message="Do you want to accept the Minecraft EULA?",
        default=True
    ).execute()

    if AcceptEula:
        with open(Folder + "eula.txt", "w") as file:
            file.write("eula=true")

    with open(Folder + "run.sh", "w") as file:
        if paper:
            file.write(f"java -Xms{Ram} -Xmx{Ram} -DPaper.IgnoreJavaVersion=true \
-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \
-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC \
-XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 \
-XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 \
-XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 \
-XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 \
-XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 \
-Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true \
-jar {jar} nogui")
        else:
            file.write(f"java -Xms{Ram} -Xmx{Ram} -jar {jar} nogui")

def BTA(RamAllocation="", FolderPath=""):
    Versions = GetBTAVer()
    Bersion = inquirer.select(message="What version you want?",
                            choices=list(Versions.keys())).execute()

    SetupFolder(jar="bta.jar", Ram=RamAllocation, Folder=FolderPath)

    with yaspin(text=f"[ Downloading Better Than Adventure {Bersion} ]") as sp:
        urllib.request.urlretrieve(Versions[Bersion], FolderPath + "bta.jar")

def Vanilla(RamAllocation="", FolderPath=""):
    Versions = GetVanilla()
    Version = inquirer.select(message="What version you want?",
                            choices=list(Versions.keys())).execute()

    SetupFolder(jar="server.jar", Ram=RamAllocation, Folder=FolderPath)

    with yaspin(text=f"[ Downloading Minecraft {Version} ]") as sp:
        urllib.request.urlretrieve(Versions[Version], FolderPath + "server.jar")

def Fabric(RamAllocation="", FolderPath=""):
    Versions = GetFabricVer()
    Fersion = inquirer.select(message="What version you want?",
                            choices=Versions).execute()

    Loader = GetFabricLoader(Fersion)
    Foader = inquirer.select(message="What loader version you'll use??",
                            choices=Loader).execute()

    SetupFolder(jar="fabric.jar", Ram=RamAllocation, Folder=FolderPath)

    with yaspin(text=f"[ Downloading Minecraft {Fersion} ]") as sp:
        urllib.request.urlretrieve(f"https://meta.fabricmc.net/v2/versions/loader/{Fersion}/{Foader}/1.0.0/server/jar", FolderPath + "fabric.jar")

def Paper(RamAllocation="", FolderPath=""):
    Versions = GetPaperVer()
    Persion = inquirer.select(message="What version you want?",
                                choices=Versions).execute()
    Builds = GetPaperBuild(Persion)
    Build = inquirer.select(message="What build version you'll use?",
                                choices=Builds).execute()

    SetupFolder(paper=True, jar="paper.jar", Ram=RamAllocation, Folder=FolderPath)

    with yaspin(text=f"[ Downloading Minecraft {Persion} ]") as sp:
        DownloadRaw = urllib.request.urlopen(f"https://api.papermc.io/v2/projects/paper/versions/{Persion}/builds/{Build}/").read()
        Download = loads(DownloadRaw)["downloads"]["application"]["name"]
        urllib.request.urlretrieve(f"https://api.papermc.io/v2/projects/paper/versions/{Persion}/builds/{Build}/downloads/{Download}", FolderPath + "paper.jar")


def Mohist(RamAllocation="", FolderPath=""):

    Versions = GetMohistVer()
    Mersion = inquirer.select(message="What version you want?",
                                choices=Versions).execute()

    Builds = GetMohistBuild(Mersion)
    Build = inquirer.select(message="What build version you'll use?",
                                choices=list(Builds.keys())).execute()

    SetupFolder(jar="mohist.jar", Ram=RamAllocation, Folder=FolderPath)

    with yaspin(text=f"[ Downloading Minecraft {Mersion} ]") as sp:
        UserAgent()
        urllib.request.urlretrieve(Builds[Build], FolderPath + "mohist.jar")
        urllib.request.urlcleanup()

def CreateMethod():
    FOLDER = Folder()
    RAM = Ram()

    Server = inquirer.select(
        message="What server type you'll use?",
        choices=["Fabric",
                 "Paper",
                 "Vanilla",
                 "Mohist",
                 "BTA (Better Than Adventure)"],
    ).execute()

    match Server:
        case "BTA (Better Than Adventure)": BTA(RamAllocation=RAM, FolderPath=FOLDER)
        case "Vanilla": Vanilla(RamAllocation=RAM, FolderPath=FOLDER)
        case "Fabric": Fabric(RamAllocation=RAM, FolderPath=FOLDER)
        case "Paper": Paper(RamAllocation=RAM, FolderPath=FOLDER)
        case "Mohist": Mohist(RamAllocation=RAM, FolderPath=FOLDER)

def SelectServer(title=""):
    HOME = os.environ["HOME"]
    serversNames = os.listdir(f"{HOME}/MinecraftServers")
    serversTypes = []
    for files in serversNames:
        serverFiles = os.listdir(f"{HOME}/MinecraftServers/{files}/")
        JarFileName = next((isTheFile for isTheFile in serverFiles if ".jar" in isTheFile), None)
        serversTypes.append(Choice(value=f"{HOME}/MinecraftServers/{files}/", name=f"{files} - {JarFileName[:-4]}"))
    serversTypes.append(Separator())
    serversTypes.append(Choice(value=None, name="Exit"))

    Server = inquirer.select(message=title,
                                choices=list(serversTypes)).execute()
    return Server

def StartMethod():
    Server = SelectServer("Select a server to run")
    if Server:
        os.chdir(Server)
        os.system("bash run.sh")

def RemoveMethod():
    while True:
        Server = SelectServer("Select a server to remove")

        if Server:
            if os.path.isdir(Server): # A very improbable edge case
                shutil.rmtree(Server) # But maybe can save someones computer
            else:
                print("WTF BRO? THIS IS ONLY 6e-1000000% POSSIBLE: No such file or directory")
        else:

            break

def EditMethod():
    EDITOR = shutil.which(os.environ["EDITOR"])
    ComparativeDict = {
        "ops.json": "ops.txt",
        "banned-players.json": "banned-players.txt",
        "banned-ips.json": "banned-ips.txt",
        "whitelist.json": "white-list.txt"
    }
    Server = SelectServer("Select a server to edit")

    def openWith(FilePath):
        if os.path.isfile(FilePath):
            os.system(f"{EDITOR} {FilePath}")
        else:
            print(f"openWith: {os.path.basename(os.path.normpath(FilePath))}: No such file or directory")

    if Server == None:
        return

    while True:
        Settings = inquirer.select(message=f"{os.path.basename(os.path.normpath(Server))} Settings...",
                                    choices=[
                                    Choice(value="server.properties", name="Server Properties"),
                                    Choice(value="run.sh", name="Run Script"),
                                    Choice(value="eula.txt", name="EULA File"),
                                    Choice(value="ops.json", name="Ops File"),
                                    "Banned Players/IP Files",
                                    Choice(value="whitelist.json", name="White List File"),
                                    Separator(),
                                    Choice(value=None, name="Exit")
                                    ]).execute()
        if Settings:
            if Settings == "Banned Players/IP Files":
                BannedFile = inquirer.select(message="Select which open",
                    choices=[Choice(value="banned-players.json", name="Banned Players"),
                            Choice(value="banned-ips.json", name="Banned IPs")
                    ]).execute()
                if os.path.isfile(Server + BannedFile):
                    openWith(Server + BannedFile)
                else:
                    openWith(Server + ComparativeDict[BannedFile])
            else:
                if os.path.isfile(Server + Settings):
                    openWith(Server + Settings)
                else:
                    openWith(Server + ComparativeDict[Settings])
        else: break

def Init():
    MethodSelection = inquirer.select(message="What do you want to do?",
                                    choices=["Create",
                                             "Edit",
                                             "Start",
                                             "Remove",
                                             Separator(),
                                             Choice(value=None, name="Exit")]
                                ).execute()
    if MethodSelection:
        match MethodSelection:
            case "Create":
                CreateMethod()
            case "Edit":
                EditMethod()
            case "Start":
                StartMethod()
            case "Remove":
                RemoveMethod()
        Init()

    quit()

if __name__ == "__main__":
    Init()
