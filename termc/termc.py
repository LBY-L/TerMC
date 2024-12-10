#!/bin/python3

# THIS IS A HAS POSIX IN, SO DON'T RUN IT IN A WINDOWS/NT SYSTEM!!!
# ████████╗███████╗██████╗ ███╗   ███╗ ██████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
#    ██║   █████╗  ██████╔╝██╔████╔██║██║
#    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║
#    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╗
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝
# “MANKIND IS DEAD. BLOOD IS FUEL. HELL IS FULL.” - UltraKill

import os, urllib.request, shutil
from InquirerPy import inquirer
from InquirerPy import get_style
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from psutil import virtual_memory as RamMemory
from yaspin import yaspin
from yaspin.spinners import Spinners
from json import loads, load

TerMCStyle = get_style({
    "pointer": "#5fd700",
    "marker": "#5fd700",
    "fuzzy_prompt": "#5fd700",
    "answer": "#5fd700",
    "questionmark": "#84f82e",
    "answermark": "#84f82e",
    "fuzzy_match": "#9edf5e"
}, style_override=False)

class Tools:
    # ######################
    # #░▀█▀░█▀█░█▀█░█░░░█▀▀#
    # #░░█░░█░█░█░█░█░░░▀▀█#
    # #░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀#
    # ######################
    def __init__(self):
        self.GREEN = "\x1b[38;5;76m"
        self.RESET = "\x1b[0m"
        self.HOME = os.environ["HOME"]
        try:
            self.EDITOR = shutil.which(os.environ["EDITOR"])
        except KeyError:
            self.EDITOR = shutil.which("nano")


    def SelectServer(self, title=""): # This code is a shit, yes it is
        serversNames = os.listdir(f"{self.HOME}/MinecraftServers")
        serversTypes = []

        serversJars = {
            "fabric.jar": "Fabric",
            "bta.jar": "BTA",
            "paper.jar": "Paper",
            "server.jar": "Vanilla",
            "mohist.jar": "Mohist"
        }

        for files in serversNames:
            serverFiles = os.listdir(f"{self.HOME}/MinecraftServers/{files}/")
            JarFileName = next((Jar for Jar in serverFiles if Jar.endswith(".jar")), None)
            try:
                serversTypes.append(Choice(value=f"{self.HOME}/MinecraftServers/{files}/",
                                    name=f"{files} -> {serversJars[JarFileName]}"))
            except KeyError:
                serversTypes.append(Choice(value=f"{self.HOME}/MinecraftServers/{files}/",
                                    name=f"{files} -> Corrupted, Please remove it!"))

        serversTypes.append(Separator("─" * len(title)))
        serversTypes.append(Choice(value=None, name="Exit"))

        Server = inquirer.select(message=title,
                                choices=serversTypes,
                                style=TerMCStyle
                                ).execute()
        if Server == None:
            return (Server, "")
        else:
            return (Server, self.GetNormPath(Server))


    def GetNormPath(self, path=""):
        return os.path.basename(os.path.normpath(path))


    def CustomBars(self, text="", colorCode="155"): # Create a decorative bar with a title
        color = f"\x1b[38;5;{colorCode}m"
        plusColorLen = len(colorCode)
        width, _ = os.get_terminal_size()
        midWidth = (len(text) // 2) + 1
        midBar = f"{'─' * (width//2 - midWidth)} {color}{text}\x1b[0m "
        print(f"{midBar}{'─' * (width - (len(midBar) - (12 + plusColorLen)))}", flush=True)


    def RemoveServer(self, serverFolderPath=""): # Gives a propt to remove a server and wait for user confirmation
            style = get_style(style={"answermark": "#9c061d", 
                                     "questionmark": "#9c061d", 
                                     "question": "#f7966d", 
                                     "answered_question": "#f7966d", 
                                     "answer": "#9c061d"}, style_override=False)
            if serverFolderPath:
                ConfirmDelete = inquirer.confirm(
                    message=f"Do you want to remove {self.GetNormPath(serverFolderPath)}",
                    style=style,
                    qmark='@',
                    amark='@',
                    default=False,
                ).execute()

            if serverFolderPath and ConfirmDelete == True:
                if os.path.isdir(serverFolderPath): # A very improbable edge case
                    shutil.rmtree(serverFolderPath) # But maybe can save someones computer
                else:
                    print("WTF BRO? THIS IS ONLY 6e-1000000% POSSIBLE: No such file or directory")
            
            return ConfirmDelete


    def Ram(self): # Returns the ram allocation, selected by the user
        ramAllocation = []
        for ramSymbol in range(1, (RamMemory().total//1000000000)-1):
            ramAllocation.append(f"{ramSymbol}G")
        RamSelection = inquirer.select(
            message="How many GB of ram you'll use?",
            choices=ramAllocation,
            style=TerMCStyle
        ).execute()

        return RamSelection


    def Folder(self): # Creates a folder for the server with a designed name
        def GValidator(result):
            if len(result) == 0:
                return False
            if "/" in result or "\\" in result or " " in result or "|" in result:
                return False
            return True

        result = inquirer.text(
                message="Name:",
                validate=GValidator,
                invalid_message="Invailid values: '/', '\\', '|', ' '",
                style=TerMCStyle
        ).execute()
        
        usedNames = [
            int(element.split('-')[-1])
            for element in os.listdir(f"{self.HOME}/MinecraftServers")
            if element.startswith(f"{result}-") and element.split('-')[-1].isdigit()
        ]
        
        if usedNames:
            nextNumber = max(usedNames, default=0) + 1

            result = f"{result}-{nextNumber}"

        elif result in os.listdir(f"{self.HOME}/MinecraftServers"):
            nextNumber = max(usedNames, default=0) + 1

            result = f"{result}-{nextNumber}"
        
        return f"{self.HOME}/MinecraftServers/{result}/"


    def SetupFolder(self, paper=False, jar="", Ram="", Folder=""):
        if not os.path.isdir(f"{self.HOME}/MinecraftServers"):
            os.mkdir(f"{self.HOME}/MinecraftServers")

        os.mkdir(Folder)

        AcceptEula = inquirer.confirm(
            message="Do you want to accept the Minecraft EULA?",
            default=True,
            style=TerMCStyle
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

    def OpenWith(self, filePath, serverFilenames):
        fileName = self.GetNormPath(filePath)
        newPath = filePath[:-len(fileName)] + serverFilenames[fileName]
        if os.path.isfile(filePath):
            os.system(f"{self.EDITOR} {filePath}")
        elif os.path.isfile(newPath):
            os.system(f"{self.EDITOR} {newPath}")
        else:
            print(f"  Seems that {self.GetNormPath(filePath)} has been not yet\n  created or has been deleted")


    def BannedIpsSettings(self, serverConf=[]) -> False:
            serverPath = serverConf[0]
            serverFilenames = serverConf[1]
            BannedFile = inquirer.select(
                message="Select which one to open",
                choices=[
                    Choice(value="banned-players.json", name="Banned Players"),
                    Choice(value="banned-ips.json", name="Banned IPs")
                    ],
                style=TerMCStyle
                ).execute()
            self.OpenWith(serverPath + BannedFile, serverFilenames)


    def printLogo(self):
        width, _ = os.get_terminal_size()
        logoSpaces = width//2-6
        creeperLogo = f"""
{" " * logoSpaces}{self.GREEN}████    ████{self.RESET}
{" " * logoSpaces}{self.GREEN}████    ████{self.RESET}
{" " * logoSpaces}{self.GREEN}    ████    {self.RESET}
{" " * logoSpaces}{self.GREEN}  ████████  {self.RESET}
{" " * logoSpaces}{self.GREEN}  ████████  {self.RESET}
{" " * logoSpaces}{self.GREEN}  ██    ██  {self.RESET}
"""
        print(creeperLogo, flush=True)


    def printGodByeLogo(self):
        width, _ = os.get_terminal_size()
        logoSpaces = width//2-6
        creeperLogo = f"""
{" " * logoSpaces}{self.GREEN}                  Zz{self.RESET}
{" " * logoSpaces}{self.GREEN}                zZ{self.RESET}
{" " * logoSpaces}{self.GREEN}              Zz{self.RESET}
{" " * logoSpaces}{self.GREEN}████    ████{self.RESET}
{" " * logoSpaces}{self.GREEN}    ████    {self.RESET}
{" " * logoSpaces}{self.GREEN}  ████████  {self.RESET}
{" " * logoSpaces}{self.GREEN}  ████████  {self.RESET}
{" " * logoSpaces}{self.GREEN}  ██    ██  {self.RESET}
"""
        print(creeperLogo, flush=True)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class ServersEntropy:
    # ############################################
    # #░█▀▀░█▀▀░█▀▄░█░█░█▀▀░█▀▄░░░█▀▀░█▀█░▀█▀░█░█#
    # #░▀▀█░█▀▀░█▀▄░▀▄▀░█▀▀░█▀▄░░░█▀▀░█░█░░█░░░█░#
    # #░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░░▀▀▀░▀░▀░░▀░░░▀░#
    # ############################################
    def __init__(self):
        Tl = Tools()
        self.SetupFolder = Tl.SetupFolder
        self.UserAgent = {'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'}

    def DowloadJar(self, dowloadUrl, path, fileName, version): # Download a server jar
        with yaspin(text=f"[ Downloading Minecraft {version} ]") as sp:
            request = urllib.request.Request(dowloadUrl, headers=self.UserAgent)
            with urllib.request.urlopen(request) as response, open(path + fileName, "wb") as outFile: 
                outFile.write(response.read()) # I am a nester 😐


    @yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
    def GetMohistVer(self):
        request = urllib.request.Request("https://mohistmc.com/api/v2/projects/mohist",
                                         headers=self.UserAgent)

        with urllib.request.urlopen(request) as response:
            versions = loads(response.read())["versions"]

        outputVersions = list(reversed(versions))
        outputVersions.remove("1.7.10"); outputVersions.remove("1.20") # <- These are unmainteined

        return outputVersions


    @yaspin(Spinners.growHorizontal, "[ Getting Available Builds ]")
    def GetMohistBuild(self, ver):
        request = urllib.request.Request(f"https://mohistmc.com/api/v2/projects/mohist/{ver}/builds",
                                         headers=self.UserAgent)
        with urllib.request.urlopen(request) as response:
            builds = loads(response.read())

        buildsDict = {}
        for buildsList in list(reversed(builds["builds"])):
            buildsDict[buildsList["number"]] = buildsList["url"]
        return buildsDict


    @yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
    def GetVanilla(self):
        request = urllib.request.Request("https://launchermeta.mojang.com/mc/game/version_manifest.json",
                                         headers=self.UserAgent)

        with urllib.request.urlopen(request) as response:
            versions = loads(response.read())["versions"]

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
    def GetFabricVer(self):
        request = urllib.request.Request("https://meta.fabricmc.net/v2/versions",
                                         headers=self.UserAgent)
        
        with urllib.request.urlopen(request) as response:
            versions = loads(response.read())["game"]

        listVer = []

        for versionInfo in filter(lambda x: x["stable"] == True, versions):
            listVer.append(versionInfo["version"])

        return listVer


    @yaspin(Spinners.growHorizontal, "[ Getting Available Loaders ]")
    def GetFabricLoader(self, ver):
        request = urllib.request.Request(f"https://meta.fabricmc.net/v2/versions/loader/{ver}",
                                         headers=self.UserAgent)
        
        with urllib.request.urlopen(request) as response:
            loaders = loads(response.read())
        
        loadersList = []
        for loaderVerRaw in loaders:
            loaderVer = loaderVerRaw["loader"]["version"]
            loadersList.append(loaderVer)
            if loaderVer == "0.12.0":
                break
        return loadersList


    @yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
    def GetPaperVer(self):
        request = urllib.request.Request("https://api.papermc.io/v2/projects/paper/",
                                         headers=self.UserAgent)
        
        with urllib.request.urlopen(request) as response:
            versions = loads(response.read())["versions"]
        
        listVer = []

        for versionInfo in versions:
            if versionInfo != "1.13-pre7":
                listVer.append(versionInfo)

        return list(reversed(listVer))


    @yaspin(Spinners.growHorizontal, "[ Getting Available Builds ]")
    def GetPaperBuild(self, ver):
        request = urllib.request.Request(f"https://api.papermc.io/v2/projects/paper/versions/{ver}/builds/",
                                         headers=self.UserAgent)
        
        with urllib.request.urlopen(request) as response:
            builds = loads(response.read())["builds"]

        buildsList = []

        for buildVerRaw in list(reversed(builds)):
            buildsList.append(buildVerRaw["build"])

        return buildsList


    @yaspin(Spinners.growHorizontal, "[ Getting Available Versions ]")
    def GetBTAVer(self):
        request = urllib.request.Request("https://api.github.com/repos/Better-than-Adventure/bta-download-repo/tags",
                                         headers=self.UserAgent)
        
        with urllib.request.urlopen(request) as response:
            versions = loads(response.read())

        verList = []

        for versionInfo in versions:
            verList.append(versionInfo['name'])
            if versionInfo['name'] == "v1.7.6-prerelease-2c":
                break

        verDict = {}

        for releases in verList:
            request = urllib.request.Request(f"https://api.github.com/repos/Better-than-Adventure/bta-download-repo/releases/tags/{releases}",
                                         headers=self.UserAgent)
        
            with urllib.request.urlopen(request) as response:
                releasesList = loads(response.read())

            for realeaseInfo in releasesList["assets"]:
                if "server" in realeaseInfo["name"]:
                    verDict[releases] = f"https://github.com/Better-than-Adventure/bta-download-repo/releases/download/{releases}/{realeaseInfo['name']}"

        return(verDict)


    def BTA(self, RamAllocation="", FolderPath=""): # Get bta.jar file for the server
        Versions = self.GetBTAVer()
        Bersion = inquirer.fuzzy(message="What version you want?",
                                choices=list(Versions.keys()),
                                style=TerMCStyle).execute()

        self.SetupFolder(jar="bta.jar", Ram=RamAllocation, Folder=FolderPath)
        self.DowloadJar(Versions[Bersion], FolderPath, "bta.jar", Bersion)


    def Vanilla(self, RamAllocation="", FolderPath=""): # Get server.jar file for the server
        Versions = self.GetVanilla()
        Version = inquirer.fuzzy(message="What version you want?",
                                choices=list(Versions.keys()),
                                style=TerMCStyle
                                ).execute()

        self.SetupFolder(jar="server.jar", Ram=RamAllocation, Folder=FolderPath)

        self.DowloadJar(Versions[Version], FolderPath, "server.jar", Version)


    def Fabric(self, RamAllocation="", FolderPath=""): # Get fabric.jar file for the server
        Versions = self.GetFabricVer()
        Fersion = inquirer.fuzzy(message="What version you want?",
                                choices=Versions,
                                style=TerMCStyle).execute()

        Loader = self.GetFabricLoader(Fersion)
        Foader = inquirer.fuzzy(message="What loader version you'll use??",
                                choices=Loader,
                                style=TerMCStyle).execute()

        self.SetupFolder(jar="fabric.jar", Ram=RamAllocation, Folder=FolderPath)

        self.DowloadJar(f"https://meta.fabricmc.net/v2/versions/loader/{Fersion}/{Foader}/1.0.0/server/jar",
                         FolderPath, "fabric.jar", Fersion)


    def Paper(self, RamAllocation="", FolderPath=""): # Get paper.jar file for the server
        Versions = self.GetPaperVer()
        Persion = inquirer.fuzzy(message="What version you want?",
                                    choices=Versions,
                                    style=TerMCStyle).execute()
        Builds = self.GetPaperBuild(Persion)
        Build = inquirer.fuzzy(message="What build version you'll use?",
                                    choices=Builds,
                                    style=TerMCStyle).execute()

        self.SetupFolder(paper=True, jar="paper.jar", Ram=RamAllocation, Folder=FolderPath)

        request = urllib.request.Request(f"https://api.papermc.io/v2/projects/paper/versions/{Persion}/builds/{Build}/",
                                         headers=self.UserAgent)
        
        with urllib.request.urlopen(request) as response:
            Download = loads(response.read())["downloads"]["application"]["name"]

        self.DowloadJar(f"https://api.papermc.io/v2/projects/paper/versions/{Persion}/builds/{Build}/downloads/{Download}", 
                        FolderPath, "paper.jar", Persion)


    def Mohist(self, RamAllocation="", FolderPath=""): # Get the mohist.jar for the server
        Versions = self.GetMohistVer()
        Mersion = inquirer.fuzzy(message="What version you want?",
                                choices=Versions,
                                style=TerMCStyle).execute()

        Builds = self.GetMohistBuild(Mersion)
        Build = inquirer.fuzzy(message="What build version you'll use?",
                                choices=list(Builds.keys()),
                                style=TerMCStyle).execute()

        self.SetupFolder(jar="mohist.jar", Ram=RamAllocation, Folder=FolderPath)

        with yaspin(text=f"[ Downloading Minecraft {Mersion} ]") as sp:
            self.DowloadJar(Builds[Build], FolderPath, "mohist.jar", Mersion)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class MethodSelections:
    # ####################################################
    # #░█▄█░█▀▀░▀█▀░█░█░█▀█░█▀▄░░░█▀▀░█▀▀░█░░░█▀▀░█▀▀░▀█▀#
    # #░█░█░█▀▀░░█░░█▀█░█░█░█░█░░░▀▀█░█▀▀░█░░░█▀▀░█░░░░█░#
    # #░▀░▀░▀▀▀░░▀░░▀░▀░▀▀▀░▀▀░░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░▀░#
    # ####################################################
    def __init__(self):
        self.ServerEnty = ServersEntropy()
        self.Tl = Tools()
        self.OpenWith = self.Tl.OpenWith
        self.GetNormPath = self.Tl.GetNormPath
        self.SelectServer = self.Tl.SelectServer
        self.CustomBars = self.Tl.CustomBars


    def CreateMethod(self): # Creates a new server
        Folder = self.Tl.Folder()
        self.CustomBars(f"Starting the setup of {self.GetNormPath(Folder)}")
        
        Ram = self.Tl.Ram()

        Server = inquirer.select(
            message="What server type you'll use?",
            choices=[Choice(value=self.ServerEnty.Fabric, name="Fabric"),
                    Choice(value=self.ServerEnty.Paper, name="Paper"),
                    Choice(value=self.ServerEnty.Vanilla, name="Vanilla"),
                    Choice(value=self.ServerEnty.Mohist, name="Mohist"),
                    Choice(value=self.ServerEnty.BTA, name="BTA (Better Than Adventure)")],
                    style=TerMCStyle
        ).execute()

        action = Server
        action(RamAllocation=Ram, FolderPath=Folder)

        self.CustomBars(f"{self.GetNormPath(Folder)} set up done!")


    def StartMethod(self): # Starts a selected server
        Server, serverName = self.SelectServer("Select a server to run")
        if Server:
            os.chdir(Server)
            os.system("bash run.sh")
            self.CustomBars(f"{serverName} has been shut down")
        else:
            self.CustomBars(f"Good bye!")


    def EditMethod(self): # Edit servers, the most large method
        Server, serverName = self.SelectServer("Select a server to edit")

        if Server == None:
            self.CustomBars("Good bye!")
            return

        serverFilenames = {
            "ops.json": "ops.txt",
            "banned-players.json": "banned-players.txt",
            "banned-ips.json": "banned-ips.txt",
            "whitelist.json": "white-list.txt",
            "server.properties": "server.properties"
        }

        while True:
            Settings = inquirer.select(
                        message=f"{serverName} Settings:",
                        choices=[
                                Choice(value="server.properties", name="Server Properties"),
                                Choice(value="run.sh", name="Run Script"),
                                Choice(value="eula.txt", name="EULA File"),
                                Choice(value="ops.json", name="Ops File"),
                                Choice(value=[self.Tl.BannedIpsSettings, [Server, serverFilenames]],
                                        name="Banned Players/IP Files"),
                                Choice(value="whitelist.json", name="White List File"),
                                Choice(value=[self.Tl.RemoveServer, Server], 
                                        name=f"Remove {serverName}"),
                                Separator("─" * (len(serverName) + 10)),
                                Choice(value=None, name="Exit")
                        ],
                        style=TerMCStyle
                        ).execute()

            if type(Settings) is list:
                action, serverConf = Settings
                breakIt = action(serverConf)
                if breakIt:
                    break
            elif Settings == None:
                self.CustomBars(f"Done editing {serverName}")
                break
            else:
                self.OpenWith(Server + Settings, serverFilenames)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def Init():
    Tl = Tools()
    MethodSel = MethodSelections()
    with open(f'{__file__[:-8]}MANIFIEST.json', 'r') as file:
        VERSION = load(file)["TerMCVersion"]

    Tl.printLogo()
    Tl.CustomBars(f"Welcome to TerMC {VERSION}!", colorCode="76")

    MethodSelection = True
    while MethodSelection:
        MethodSelection = inquirer.select(
            message="What do you want to do?",
            choices=[
                Choice(value=[MethodSel.CreateMethod, "Let's create your own server!"], 
                        name="Create New Server"),
                Choice(value=[MethodSel.EditMethod, "Let's edit your servers!"], 
                        name="Edit Server"),
                Choice(value=[MethodSel.StartMethod, "Let's start your server!"], 
                        name="Start Server"),
                Separator("─" * 23),
                Choice(value=None, name="Exit")
                ],
            style=TerMCStyle
            ).execute()

        if MethodSelection:
            action, name = MethodSelection
            Tl.CustomBars(name)
            action()
        else:
            Tl.CustomBars("Good Bye!", colorCode="76")
            Tl.printGodByeLogo()
            exit(0)

if __name__ == "__main__": # The most basic python trick
    Init()
