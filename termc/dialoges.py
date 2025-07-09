from InquirerPy.base.control import Choice

# Translations -- maybe idk
AppParameters = (
    "A simple script to download and execute Minecraft servers",
    "Changes the default TerMC directory",
    "Changes the server command for running servers",
    "Ignores the config in .config/termc-config.json",
)
KeyInterruptMsg = "Operation interrupted"
SysErrorMsg = ("System Error", "End of System Error")
KeyInterruptMsgUndo = "Operation interrupted, undoing changes"
ExitOptionTx = "Exit"
ExitOption = Choice(name=ExitOptionTx, value=None)
DefaultExitMsg = "Going back"
MandatoryMessage = "You can't skip this!"


def settingsDir(path=""):
    settingsText = "Using: 1"
    return settingsText.replace("1", path)


selectImpServerText = "Imported Server"
selectNoServerMsg = "Nothing is here"
selectErrServer = "Corrupted"
dwmanagerSpinners = (
    "[ Getting Available Versions ]",
    lambda version="": "[ Downloading Minecraft 1 ]".replace("1", version),
)


def createChangesText(mc=("", "", "", "")):
    changes = """- CHANGES -
Folder Name: 1
Minecraft Version: 2
Minecraft Ram: 3
Minecraft Jar Name: 4"""
    return (
        changes.replace("1", mc[0])
        .replace("2", mc[1])
        .replace("3", mc[2])
        .replace("4", mc[3])
    )


createBars = (
    "Starting the setup",
    lambda serverName="": "Succesfully created 1".replace("1", serverName),
)
startTxts = (
    "Select a server to run",
    lambda serverName="": "1 has been shut down".replace("1", serverName),
)
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
editRemoveConfirm = (
    lambda name="": "1 removal has been halted".replace("1", name),
    lambda name="": "1 has been deleted".replace("1", name),
)


def editExitBar(name=""):
    bar = "Closing settings of 1"
    return bar.replace("1", name)


editServerKey = (
    lambda name="": "1 Settings".replace("1", name),
    "Risk Zone",
    lambda name="": "Remove 1".replace("1", name),
    "Select a server to edit",
)
editFilesNames = (
    "Run Script",
    "Server Properties",
    "Operators",
    "EULA",
    "Banned Players",
    "Banned IPs",
    "White List",
)


def editFileNotFound(name=""):
    msg = "Seems that 1 has been not yet created or has been deleted"
    return msg.replace("1", name)


importMsgs = (
    "Server import incomming!",
    "Enter the server path of your run file",
    "Not a valid file!",
)
importNoName = "NoNameSupplied"


def importChanges(changes=("", "")):
    imported = """- CHANGES -
Start File: 1
Jar File: 2"""
    return imported.replace("1", changes[0]).replace("2", changes[1])


mainmenuModuleNames = (
    "Create Server",
    "Start Server",
    "Edit Server",
    "Import an Existing Server",
)
mainmenuTitle = "What do you want to do?"


def mainmenuBars(version):
    return ("Welcome to TerMC 1".replace("1", version), "See you later!")
