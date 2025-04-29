#!/bin/python3

# THIS IS A HAS POSIX IN, SO DON'T RUN IT IN A WINDOWS/NT SYSTEM!!!
# ████████╗███████╗██████╗ ███╗   ███╗ ██████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██╔════╝
#    ██║   █████╗  ██████╔╝██╔████╔██║██║
#    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║
#    ██║   ███████╗██║  ██║██║ ╚═╝ ██║╚██████╗
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝
# “MANKIND IS DEAD. BLOOD IS FUEL. HELL IS FULL.” - UltraKill

import os
from subprocess import call as RunCommand
from prompt_toolkit.layout.containers import ColorColumn
from prompt_toolkit.styles.style import Style
import urllib.request
import shutil
import re
import argparse
import textwrap
from InquirerPy import inquirer
from InquirerPy import get_style
from functools import partial
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from psutil import virtual_memory as RamMemory
from yaspin import yaspin
from yaspin.core import Spinner
from yaspin.spinners import Spinners
from json import loads, load

global SHELL, VERSION, HOME
SHELL = shutil.which("bash")
VERSION = "v0.9.2"
if not os.path.isdir(f"{os.environ["HOME"]}/MinecraftServers/"):
    os.mkdir(f"{os.environ["HOME"]}/MinecraftServers/")
HOME = f"{os.environ["HOME"]}/MinecraftServers/"

# Translations -- maybe idk
AppParameters = ("A simple script to download and execute Minecraft servers", "Changes the default TerMC directory", "Changes the server command for running servers", "Ignores the config in .config/termc-config.json")
KeyInterruptMsg = "Operation interrupted"
SysErrorMsg = ("System Error", "End of System Error")
KeyInterruptMsgUndo = "Operation interrupted, undoing changes"
ExitOption = Choice(name="Exit", value=None)
DefaultExitMsg = "Going back"
MandatoryMessage = "You can't skip this!"
settingsDir = lambda path="": f"Using: {path}"
selectImpServerText = "Imported Server"
selectNoServerMsg = "Nothing is here"
selectErrServer = "Corrupted"
dwmanagerSpinners = ("[ Getting Available Versions ]", lambda version="": f"[ Downloading Minecraft {version} ]")
createChangesText = lambda mc=("", "", "", ""): f"""- CHANGES -
Folder Name: {mc[0]}
Minecraft Version: {mc[1]}
Minecraft Ram: {mc[2]}
Minecraft Jar Name: {mc[3]}"""
createBars = ("Starting the setup", lambda serverName="": f"Succesfully created {serverName}")
startTxts = ("Select a server to run", lambda serverName="": f"{serverName} has been shut down")
createRamTitle = "How many GB of ram you'll use?"
createFolderTitle = "Name:"
createInvalidFolderVal = "Invailid values: '/', '\\', '|', ' '"
createServerTypeTitle = "What server type you'll use?"
createEulaTitle = "Do you want to accept the Minecraft EULA?"
createPaperFlags = "-DPaper.IgnoreJavaVersion=true \
-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 \
-XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC \
-XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 \
-XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 \
-XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 \
-XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 \
-XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 \
-Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true"
editRemoveConfirm = (lambda name="": f"{name} removal has been halted", lambda name="": f"{name} has been deleted")
editExitBar = lambda name="": f"Closing settings of {name}"
editServerKey = (lambda name="": f"{name} Settings", "Risk Zone", lambda name="": f"Remove {name}", "Select a server to edit")
editFilesNames = ("Run Script", "Server Properties", "Operators", "EULA", "Banned Players", "Banned IPs", "White List")
editFileNotFound = lambda name="": f"Seems that {name} has been not yet created or has been deleted"
importMsgs = ("Server import incomming!", "Enter the server path of your run file", "Not a valid file!")
importNoName = "NoNameSupplied"
importChanges = lambda changes=("", ""): f"""- CHANGES -
Start File: {changes[0]}
Jar File: {changes[1]}"""
mainmenuModuleNames = ("Create Server", "Start Server", "Edit Server", "Import an Existing Server")
mainmenuTitle = "What do you want to do?"
mainmenuBars = (f"Welcome to TerMC {VERSION}", "See you later!")
TerMCStyle = get_style({
    "pointer": "#5fd700",
    "marker": "#5fd700",
    "fuzzy_prompt": "#5fd700",
    "answer": "#5fd700",
    "questionmark": "#84f82e",
    "answermark": "#84f82e",
    "fuzzy_match": "#9edf5e"
}, style_override=False)

creeperLogo = (
    ("\x1b[38;5;76m████    ████\x1b[0m"),
    ("\x1b[38;5;76m████    ████\x1b[0m"),
    ("\x1b[38;5;76m    ████    \x1b[0m"),
    ("\x1b[38;5;76m  ████████  \x1b[0m"),
    ("\x1b[38;5;76m  ████████  \x1b[0m"),
    ("\x1b[38;5;76m  ██    ██  \x1b[0m"),
    ("                                ")
)

creeperLogoSleep = (
    ("\x1b[38;5;76m                  Zz\x1b[0m"),
    ("\x1b[38;5;76m                zZ\x1b[0m"),
    ("\x1b[38;5;76m              Zz\x1b[0m"),
    ("\x1b[38;5;76m████    ████\x1b[0m"),
    ("\x1b[38;5;76m    ████    \x1b[0m"),
    ("\x1b[38;5;76m  ████████  \x1b[0m"),
    ("\x1b[38;5;76m  ████████  \x1b[0m"),
    ("\x1b[38;5;76m  ██    ██  \x1b[0m"),
    ("                                ")
)


class TextFormatting:
    def __init__(self, colorCode = None):
        self.RESET = "\x1b[0m"
        if colorCode is None:
            self.colorCode = 155
        else:
            self.colorCode = colorCode

    def PrintLogos(self, logo: tuple = ()):
        width, _ = os.get_terminal_size()
        LineLen = len(logo[0][-1]) + 10
        spaceNeeded = ( (width - (LineLen)) // 2 ) * " "
        print(spaceNeeded + (f"\n{spaceNeeded}".join(logo)), flush=True)

    def CustomBars(self, text: str = "", _colorCode=None): # Create a decorative bar with a title
        color = f"\x1b[38;5;{self.colorCode}m"
        colorSp = f"\x1b[38;5;240m"
        if _colorCode is not None:
            color = f"\x1b[38;5;{_colorCode}m"
            colorSp = f"\x1b[38;5;240m"
        width, _ = os.get_terminal_size()
        txt = f" {text} "
        centerTxt = txt.center(width, "/")
        left = centerTxt.rstrip("/").replace(txt, "")
        right = centerTxt.lstrip("/").replace(txt, "").replace("/", "\\")
        print(f"{colorSp}{left}{color}{txt}{colorSp}{right}{self.RESET}", flush=True)

    def CenteredColorText(self, text: str = "", _colorCode=None):
        contentColor = f"\x1b[38;5;{self.colorCode}m"
        if _colorCode is not None:
            contentColor = f"\x1b[38;5;{_colorCode}m"

        borderColor = "\x1b[38;5;240m"

        width, _ = os.get_terminal_size()
        innerWidth = width - 2  # 2 chars for borders

        newText = f"{borderColor}┌{'─' * innerWidth}┐{self.RESET}\n"
        for textRP in text.split("\n"):
            for line in textwrap.wrap(textRP, innerWidth):
                centered_line = line.center(innerWidth)
                newText += f"{borderColor}│{self.RESET}{contentColor}{centered_line}{self.RESET}{borderColor}│{self.RESET}\n"
        newText += f"{borderColor}└{'─' * innerWidth}┘{self.RESET}"
        print(newText, flush=True)

class DowloadManager: ## This manages all the request, just to make me this easier
    def __init__(self):
        self.downloadText = ""
        self.serversFunctions = {
            "fabric.jar": self.GetFabric,
            "bta.jar": self.GetBTA,
            "paper.jar": self.GetPaper,
            "server.jar": self.GetVanilla,
            # "mohist.jar": "Mohist", Not yet implemented
        }
        self.UserAgent = {'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion'}

    @yaspin(Spinners.growHorizontal, dwmanagerSpinners[0])
    def GetFabric(self):
        request = urllib.request.Request("https://meta.fabricmc.net/v2/versions",
                                            headers=self.UserAgent)

        with urllib.request.urlopen(request) as response:
            versions = loads(response.read())["game"]

        listVer = []

        for versionInfo in filter(lambda x: x["stable"], versions):
            listVer.append(versionInfo["version"])

        return listVer

    @yaspin(Spinners.growHorizontal, dwmanagerSpinners[0])
    def GetBTA(self):
        request = urllib.request.Request("https://downloads.betterthanadventure.net/bta-server/release/versions.json",
                                        headers=self.UserAgent)

        with urllib.request.urlopen(request) as response:
            versions = response.read()
        # Fix the comma in line -3
        importedVersion = versions.decode()
        newVersion = ""
        for n, release in enumerate(importedVersion.splitlines()):
            if n == len(importedVersion.splitlines()) - 4:
                newVersion += release[:-1] + "\n"
            else:
                newVersion += release + "\n"
        # End of the fix
        versionsJson = loads(newVersion)["versions"]
        versionsDictUrl = {}
        for release in reversed(versionsJson):
            versionsDictUrl[release] = f"https://downloads.betterthanadventure.net/bta-server/release/{release}/server.jar"
            if release == "v1.7.4_01_1":
                break

        return versionsDictUrl

    @yaspin(Spinners.growHorizontal, dwmanagerSpinners[0])
    def GetPaper(self):
            request = urllib.request.Request("https://api.papermc.io/v2/projects/paper/",
                                            headers=self.UserAgent)

            with urllib.request.urlopen(request) as response:
                versions = loads(response.read())["versions"]

            listVer = []

            for versionInfo in versions:
                if versionInfo != "1.13-pre7":
                    listVer.append(versionInfo)

            return list(reversed(listVer))

    @yaspin(Spinners.growHorizontal, dwmanagerSpinners[0])
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

    def DownloadJar(self, downloadUrl=None, path="", fileName="server.jar", version=""): # Download a server jar
        if fileName == "paper.jar":
            buildRoute = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/"
            request = urllib.request.Request(buildRoute,
                                             headers=self.UserAgent)
            with urllib.request.urlopen(request) as response:
                build = loads(response.read())["builds"][-1]
            buildName = build["build"]
            buildDownloadFile = build["downloads"]["application"]["name"]
            downloadUrl = f"{buildRoute}{buildName}/downloads/{buildDownloadFile}"

        if fileName == "mohist.jar":
            pass

        if fileName == "fabric.jar":
            loaderRoute = f"https://meta.fabricmc.net/v2/versions/loader/{version}/"
            request = urllib.request.Request(loaderRoute)
            with urllib.request.urlopen(request) as response:
                loaderName = loads((response.read()))[0]["loader"]["version"]

            downloadUrl = f"{loaderRoute}{loaderName}/1.0.0/server/jar"

        if downloadUrl is not None:
            with yaspin(text=dwmanagerSpinners[1](version)):
                request = urllib.request.Request(downloadUrl, headers=self.UserAgent)
                with urllib.request.urlopen(request) as response, open(path + fileName, "wb") as outFile:
                    outFile.write(response.read()) # I am a nester 😐

class ImportServer:
    def __init__(self):
        self.tl = Tools()
        self.tx = TextFormatting()
        self.barExit = TextFormatting(colorCode=76)
        self.txE = TextFormatting(colorCode=160)
        self.userHOME = f"{os.environ['HOME']}/"
        self._imFolderName = None
        self._newFolderName = None
        self._imServerPath = None
        self._newServerPath = None
        self._imJarName = None

    def DeterminateNewName(self): # Prevent ilegal names like "he\lo" or "he|lo"
        if self._imFolderName is None:
            return importNoName
                                                         # I dont want hidden folders
        newName = self._imFolderName.replace("/", "").replace("\\", "").replace("|", "").replace(".", "").replace(" ", "")
        # Copy and pasted CreateServer.Folder
        usedNames = [
            int(element.split('-')[-1])
            for element in os.listdir(HOME)
            if element.startswith(f"{newName}-") and element.split('-')[-1].isdigit()
        ]

        if usedNames:
            nextNumber = max(usedNames, default=0) + 1
            newName = f"{newName}-{nextNumber}"
        if newName in os.listdir(HOME):
            nextNumber = max(usedNames, default=0) + 1
            newName = f"{newName}-{nextNumber}"

        self._newFolderName = newName

    def myPathValidator(self, result):
        if os.path.isfile(result):
            with open(result, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if "java" in str(lines):
                    return True
                else:
                    return False
        else:
            return False

    def ChangeFiles(self):
        if os.path.isdir(str(self._imServerPath)) is False:
            return None

        scriptRoute = f"{self._newServerPath}run.sh"
        newJarName = "imported.jar"

        with open(scriptRoute, "r", encoding="utf-8") as f:
            lines = f.readlines()

        pattern = re.compile(r"(java\s+[^&|;\n]*?-jar\s+)([^\s&|;\n]+)", re.IGNORECASE)

        oldJarName = ""
        # Search for things like java -jar server.jar and stracts the server.jar
        for i, line in enumerate(lines):
            coincidence = pattern.search(line)
            if coincidence:
                oldJarName = coincidence.group(2)
                newLine = pattern.sub(rf"\1{newJarName}", line)
                lines[i] = newLine
        self._imJarName = oldJarName
        oldJarPath = f"{self._newServerPath}{self.tl.GetPathFileName(oldJarName)}"

        if os.path.isfile(oldJarPath):
            shutil.move(oldJarPath, f"{self._newServerPath}imported.jar")

        with open(scriptRoute, "w", encoding="utf-8") as f:
            f.writelines(lines)


    def ImportServer(self):
        self.barExit.CustomBars(importMsgs[0])
        self.tx.CenteredColorText(importMsgs[1])
        try: # It's a common error to get to this option
            startPath = self.tl.FilePathTERMC(
                message="run.sh/start.sh:",
                default=self.userHOME,
                validate=self.myPathValidator,
                invalid_message=importMsgs[2],
            ).execute()
        except KeyboardInterrupt:
            self.txE.CustomBars(KeyInterruptMsg)
            return
        self._imServerPath = startPath[:-len(self.tl.GetPathFileName(startPath))]
        self._imFolderName = self.tl.GetPathFileName(self._imServerPath)
        self.DeterminateNewName()
        self._newServerPath = f"{HOME}{self._newFolderName}/"

        try:
            with yaspin(spinner=Spinners.growHorizontal, text=f"[ {self._imFolderName} -> {HOME}{self._newFolderName} ]"):
                shutil.copytree(self._imServerPath, self._newServerPath)
                shutil.move(f"{self._newServerPath}{self.tl.GetPathFileName(startPath)}", f"{self._newServerPath}run.sh")
        except KeyboardInterrupt:
            self.txE.CustomBars(KeyInterruptMsgUndo)
            if os.path.isdir(self._newServerPath):
                shutil.rmtree(self._newServerPath)
            return

        self.ChangeFiles()
        self.tx.CenteredColorText(importChanges((f"{self.tl.GetPathFileName(startPath)} -> run.sh", f"{self._imJarName} -> imported.jar")), _colorCode="7")


class EditServer:
    def __init__(self):
        self.tl = Tools()
        self.tx = TextFormatting()
        self.barExit = TextFormatting(colorCode=76)
        self.txE = TextFormatting(colorCode=160)
        self._folderPath = ""
        self.serverFilenames = {
            "run.sh": "run.sh",
            "server.properties": "server.properties",
            "ops.json": "ops.txt",
            "eula.txt": "eula.txt",
            "banned-players.json": "banned-players.txt",
            "banned-ips.json": "banned-ips.txt",
            "whitelist.json": "white-list.txt",
        }

        self.optionNameFile = []
        for n, i in enumerate(editFilesNames):
            self.optionNameFile.append(Choice(value=n, name=f"{i}"))

        self._positionServer = 0

    def OpenWith(self, _positionServer):
        serverPath1 = self._folderPath + list(self.serverFilenames.keys())[self._positionServer]
        serverPath2 = self._folderPath + list(self.serverFilenames.values())[self._positionServer]

        if os.path.isfile(serverPath1):
            os.system(f"{self.tl.EDITOR} {serverPath1}")
        elif os.path.isfile(serverPath2):
            os.system(f"{self.tl.EDITOR} {serverPath2}")
        else:
            self.txE.CenteredColorText(editFileNotFound(self.tl.GetPathFileName(self._folderPath)))

    def GoUP(self, up=1):
        print(f"\x1b[{up}A", flush=True, end="")
        print("\x1b[2K", flush=True, end="")

    def RemoveServer(self):
            style = get_style(style={"answermark": "#9c061d",
                                        "questionmark": "#9c061d",
                                        "question": "#f7966d",
                                        "answered_question": "#f7966d",
                                        "answer": "#9c061d"}, style_override=False)
            ConfirmDelete = False
            ConfirmDelete = inquirer.confirm(
                message=f"Do you want to remove {self.tl.GetPathFileName(self._folderPath)}",
                style=style,
                qmark='!',
                amark='!',
                default=False,
                mandatory=False,
                raise_keyboard_interrupt=False
            ).execute()

            if ConfirmDelete:
                if os.path.isdir(self._folderPath): # A very improbable edge case
                    shutil.rmtree(self._folderPath) # But maybe can save someones computer
                else:
                    self.txE.CenteredColorText("WTF BRO? THIS IS ONLY 6e-1000000% POSSIBLE: No such file or directory", colorCode="51")
                self.GoUP(2)
                self.tx.CustomBars(editRemoveConfirm[1](self.tl.GetPathFileName(self._folderPath)))
                return True
            else:
                self.GoUP(2)
                self.txE.CustomBars(editRemoveConfirm[0](self.tl.GetPathFileName(self._folderPath)))
                print("\n", flush=True, end="")
                return False

    def EditServer(self):
        Server, serverName = self.tl.SelectServer(editServerKey[3])
        if serverName is None:
            return
        else:
            self._folderPath = Server
        serverTitle = editServerKey[0](serverName)
        self.optionNameFile.append(Separator(f" {editServerKey[1]} ".center(len(serverTitle), "─")))
        self.optionNameFile.append(Choice(value="remove", name=editServerKey[2](serverName)))
        self.optionNameFile.append(Separator("─" * len(serverTitle)))
        self.optionNameFile.append(ExitOption)
        while True:
            serverEditOptions = self.tl.SelectionTERMC(
                message=serverTitle,
                choices=self.optionNameFile,
                mandatory=False,
                default=None,
                raise_keyboard_interrupt=False
            ).execute()

            if serverEditOptions == "remove":
                ifExit = self.RemoveServer()
                if ifExit:
                    break

            elif serverEditOptions is None:
                self.tx.CustomBars(editExitBar(serverName))
                break
            else:
                self._positionServer = serverEditOptions
                self.OpenWith(serverEditOptions)

            self.GoUP()

class StartServer:
    def __init__(self):
        self.tl = Tools()
        self.tx = TextFormatting()
        self.txE = TextFormatting(colorCode=160)
        self.barExit = TextFormatting(colorCode=76)

    def StartServer(self):
        Server, serverName = self.tl.SelectServer(startTxts[0])
        if serverName is not None:
            os.chdir(Server)
            os.system(f"{SHELL} run.sh",)
            print("\n", end="")
            self.barExit.CustomBars(startTxts[1](serverName))

class CreateServer:
    def __init__(self, ):
        self.dw = DowloadManager()
        self.tl = Tools()
        self.tx = TextFormatting()
        self.barExit = TextFormatting(colorCode=76)
        self.txE = TextFormatting(colorCode=160)
        serverTypesJars = {
        "fabric.jar": "Fabric",
        "bta.jar": "Better Than Adventure (BTA)",
        "paper.jar": "Paper",
        "server.jar": "Vanilla",
        }
        self.optionsServerTypes = []
        for k, e in serverTypesJars.items():
            self.optionsServerTypes.append(Choice(value=k, name=e))

        self._flags = None
        self._folder = None
        self._ramGB = None
        self._serverBasis = None

    def CreateServer(self):
        self.tx.CustomBars(createBars[0])
        try:
            self.ServerTypeSelect()
        except KeyboardInterrupt:
            self.txE.CustomBars(KeyInterruptMsg)
            return

        self.Folder()
        self.Ram()
        self.Flags()

        try:
            self.SetupServer()
        except KeyboardInterrupt:
            self.txE.CustomBars(KeyInterruptMsgUndo)
            if os.path.isdir(f"{HOME}{self._folder}"): # A very improbable edge case
                shutil.rmtree(f"{HOME}{self._folder}") # But maybe can save someones computer
            return

        self.tx.CustomBars(createBars[1](str(self._folder)))


    def Ram(self): # Returns the ram allocation, selected by the user
        ramAllocation = []
        for ramSymbol in range(1, (RamMemory().total//1000000000)-1):
            ramAllocation.append(f"{ramSymbol}G")
        if ramAllocation == []:
            ramAllocation = ["1G"]

        RamSelection = self.tl.SelectionTERMC(
            message=createRamTitle,
            choices=ramAllocation,
            raise_keyboard_interrupt=False,
            mandatory=True
        ).execute()
        self._ramGB = RamSelection

    def Folder(self): # Creates a folder for the server with a designed name
        def GValidator(result):
            if len(result) == 0:
                return False
            if "/" in result or "\\" in result or " " in result or "|" in result:
                return False
            return True

        result = self.tl.TextTERMC(
                message=createFolderTitle,
                validate=GValidator,
                invalid_message=createInvalidFolderVal,
                raise_keyboard_interrupt=False,
                mandatory=True
        ).execute()

        usedNames = [
            int(element.split('-')[-1])
            for element in os.listdir(HOME)
            if element.startswith(f"{result}-") and element.split('-')[-1].isdigit()
        ]

        if usedNames:
            nextNumber = max(usedNames, default=0) + 1
            result = f"{result}-{nextNumber}"
        if result in os.listdir(HOME):
            nextNumber = max(usedNames, default=0) + 1
            result = f"{result}-{nextNumber}"

        self._folder = f"{result}"

    def ServerTypeSelect(self):
        jarName = self.tl.SelectionTERMC( # It's easy to get trapped in this option so exit now if you don't want this
            message=createServerTypeTitle,
            choices=self.optionsServerTypes
        ).execute()
        function = self.dw.serversFunctions[str(jarName)]
        serverGet = function()

        if isinstance(serverGet, dict):
            Versions = list(serverGet.keys())
        else:
            Versions = serverGet

        versionSelection = self.tl.FuzzyTERMC(mandatory=True,
            raise_keyboard_interrupt=False,
            message="What version you want?",
            choices=Versions).execute()

        url = None
        if isinstance(serverGet, dict):
            url = serverGet[versionSelection]

        self._serverBasis = (url, jarName, versionSelection)

    def Flags(self):
        jarName = self._serverBasis[1]
        eula = "eula=false"
        flags = f"java -Xms{self._ramGB} -Xmx{self._ramGB} -jar {jarName} nogui"

        acceptEula = self.tl.ConfirmTERMC(
            message=createEulaTitle,
            default=True,
            raise_keyboard_interrupt=False,
            mandatory=True,
        ).execute()

        if acceptEula:
            eula = "eula=true"

        if jarName == "paper.jar":
            flags = f"java -Xms{self._ramGB} -Xmx{self._ramGB} {createPaperFlags} -jar {jarName} nogui"

        self._flags = (eula, flags)

    def SetupServer(self):
        # Detect if there is a value that is not set
        # This means that someone skip a step

        #folder = self._folder
        url = self._serverBasis[0]
        jarName = self._serverBasis[1]
        version = self._serverBasis[2]
        eula = self._flags[0]
        flags = self._flags[1]

        self.tx.CenteredColorText(createChangesText((self._folder, version, self._ramGB, jarName)), _colorCode="7")

        serverPath = f"{HOME}{self._folder}/"

        os.mkdir(serverPath) # Creates the root dir of this server

        with open(f"{serverPath}eula.txt", "w") as file: # Write to the eula.txt file
            file.write(f"# Modified by TerMC\n{eula}")

        with open(f"{serverPath}run.sh", "w") as file:
            file.write(f"\n# -- TerMC Run File -- \n{flags}") # Write to the run.sh file

        self.dw.DownloadJar(url, serverPath, jarName, version)

class MainMenu:
    def __init__(self):
        self.tl = Tools()
        self.tx = TextFormatting()
        self.barExit = TextFormatting(colorCode=76)
        self.txE = TextFormatting(colorCode=160)
        cr = CreateServer()
        st = StartServer()
        ed = EditServer()
        ip = ImportServer()
        myModules = {
           cr.CreateServer: f"{mainmenuModuleNames[0]}",
           st.StartServer: f"{mainmenuModuleNames[1]}",
           ed.EditServer: f"{mainmenuModuleNames[2]}",
           ip.ImportServer: f"{mainmenuModuleNames[3]}"
        }
        self.menuOptions = []
        for k, e in myModules.items():
            self.menuOptions.append(Choice(value=k, name=e))
        self.menuOptions.extend((Separator(len(mainmenuTitle) * "─"), ExitOption))

    def MainMenu(self):
        menuOption = ""
        self.barExit.PrintLogos(creeperLogo)
        self.barExit.CustomBars(mainmenuBars[0])
        while menuOption is not None:
            menuOption = self.tl.SelectionTERMC(
                message=mainmenuTitle,
                choices=self.menuOptions,
                raise_keyboard_interrupt=False,
                mandatory=False,
                default=None
            ).execute()
            if menuOption is not None:
                menuOption()
        self.barExit.CustomBars(mainmenuBars[1])
        self.barExit.PrintLogos(creeperLogoSleep)

class Tools:
    def __init__(self):
        # .Jar names, if the server jar is not named like this, it's most likely that is corrupted
        self.serversJars = {
            "fabric.jar": "Fabric",
            "bta.jar": "BTA",
            "paper.jar": "Paper",
            "server.jar": "Vanilla",
            # "mohist.jar": "Mohist",
            "imported.jar": selectImpServerText
        }

        self.dw = DowloadManager() # Import dowload manager for ServerTypeSelect
        self.tx = TextFormatting()
        self.txE = TextFormatting(colorCode=160)
        self.SelectionTERMC = partial(inquirer.select, style=TerMCStyle, border=True, mandatory_message=MandatoryMessage)
        self.FuzzyTERMC = partial(inquirer.fuzzy, style=TerMCStyle, border=True, mandatory_message=MandatoryMessage)
        self.FilePathTERMC = partial(inquirer.filepath, style=TerMCStyle, mandatory_message=MandatoryMessage)
        self.TextTERMC = partial(inquirer.text, style=TerMCStyle, mandatory_message=MandatoryMessage)
        self.ConfirmTERMC = partial(inquirer.confirm, style=TerMCStyle, mandatory_message=MandatoryMessage)
        try:
            self.EDITOR = shutil.which(os.environ["EDITOR"])
        except KeyError:
            self.EDITOR = shutil.which("nano")

    def GetPathFileName(self, path=""): # Is basically the most used thing in my code
        return os.path.basename(os.path.normpath(path))

    def SelectServer(self, title="", _colorCode=None): # This code is a shit, yes it is
        width, _ = os.get_terminal_size()
        serversNames = os.listdir(HOME)
        serversTypes = []

        if serversNames != []: # Just don't waste compuer power
            for files in serversNames:
                fileNow = f"{HOME}{files}/"
                serverFiles = os.listdir(fileNow)
                JarFileNames = [Jar for Jar in serverFiles if Jar.endswith(".jar")]
                item = f"{files} -> "

                if len(JarFileNames) > 1:
                    item += f"{selectImpServerText} ({len(JarFileNames)} jars)"
                elif self.serversJars.get(str(JarFileNames[0])) is None:
                    item += f"{selectErrServer}"
                else:
                    item += f"{self.serversJars[JarFileNames[0]]}"

                serversTypes.append(Choice(value=fileNow, name=item))
        else:
            serversTypes.append(Separator(selectNoServerMsg))

        serversTypes.extend([Separator("─" * len(title)), ExitOption])

        serverName = self.SelectionTERMC(
            message=title,
            choices=serversTypes,
            mandatory=False,
            raise_keyboard_interrupt=False,
            default=None,
        ).execute()

        if serverName is None:
            if _colorCode is None:
                self.tx.CustomBars(DefaultExitMsg, _colorCode=76)
            else:
                self.tx.CustomBars(DefaultExitMsg, _colorCode=_colorCode)
            return (serverName, None)
        else:
            return (serverName, self.GetPathFileName(serverName))

class Settings:
    def __init__(self):
        self.tx = TextFormatting(colorCode="7")
        self.parser = argparse.ArgumentParser(description=AppParameters[0])
        self.parser.add_argument('-d', '--directory', type=str, help=AppParameters[1])
        self.parser.add_argument('-c', '--command', type=str, help=AppParameters[2])
        self.parser.add_argument('-i', '--ignore_config', type=bool, help=AppParameters[3])

    def IfDir(self, directory=None):
        if directory is None:
            return
        home = directory
        if home.startswith("~/"):
            home = home.replace("~/", f"{os.environ["HOME"]}/", 1)
        if home.endswith("/") is False:
            home = home + "/"
        if os.path.isdir(home):
            self.tx.CenteredColorText(settingsDir(home))
            return home

        return False

    def ImportSettings(self):
        global HOME, SHELL
        configFile = f"{os.environ["HOME"]}/.config/termc-config.json"
        if os.path.isfile(configFile):
            with open(configFile, "r") as f:
                file = load(f)
                directory = file["term-directory"]
                command = file["term-command"]
        else:
            return

        if directory != "":
            dir = self.IfDir(directory)
            if dir:
                HOME = dir
        if command != "":
            SHELL = command

    def CMDSettings(self):
        global HOME, SHELL
        args = self.parser.parse_args()

        if args.directory is not None:
            dir = self.IfDir(args.directory)
            if dir:
                HOME = dir

        if args.command is not None:
            global SHELL
            SHELL = args.command

        if args.ignore_config:
            return False
        return True

    def Settings(self):
        if self.CMDSettings():
            self.ImportSettings()
        mn = MainMenu()
        mn.MainMenu()

def main():
    se = Settings()
    se.Settings()
