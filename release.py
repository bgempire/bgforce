"""Script to automate build of BGForce releases.
Intended only for the framework releases, CAN be safely deleted on your game!"""

import os
from pathlib import Path
import shutil

PROJECT = "bgforce"
VERSION = [0, 0, 4]

curPath = Path(__file__).parent.resolve()
releaseTarget = curPath / ("release/" + PROJECT + "-v" + ".".join([str(i) for i in VERSION]))

if not releaseTarget.exists():
    releaseTarget.mkdir(parents=True)

data = {
    "OverwriteString": "$COMMENT\n{\n    \n}",
    "CreatePaths": [
        "./sounds/bgm/DELETE-ME",
        "./sounds/sfx/DELETE-ME",
    ],
    "CopyPaths": [
        "./database/Config.json",
        "./database/Global.json",
        "./database/Gui.json",
        "./database/Resolutions.json",
        "./fonts",
        "./textures/gui",
        "./LibBgf.blend",
    ],
    "OverwritePaths": [
        "./database/Contexts.json",
        "./database/State.json",
        "./database/Styles.json",
        "./lang/English.json",
    ],
}

for pathStr in data["CreatePaths"]:
    source = Path(pathStr)
    target = releaseTarget / source
    os.makedirs((releaseTarget / source).parent, exist_ok=True)
    if target.exists():
        target.unlink()
    target.touch()

for pathStr in data["CopyPaths"]:
    source = Path(pathStr)
    
    if source.exists():
        if source.is_file():
            os.makedirs((releaseTarget / source).parent, exist_ok=True)
            shutil.copy2(source, releaseTarget / source)
            print("> Copied:", source)
        elif source.is_dir():
            for f in source.rglob("*"):
                os.makedirs((releaseTarget / f).parent, exist_ok=True)
                shutil.copy2(curPath / f, releaseTarget / f)
                print("  > Copied from inside", source, ":", f)
    else:
        print("X Copy path do not exist:", source)

for path in data["OverwritePaths"]:
    source = Path(path)
    target = releaseTarget / source
    target.unlink(missing_ok=True)
    
    if source.exists() and source.is_file():
        os.makedirs((releaseTarget / source).parent, exist_ok=True)
        targetFileContent = data["OverwriteString"] # type: str
        
        with open(source.as_posix(), "r", encoding="utf-8") as openedFile:
            comment = ""
            sourceFileContent = openedFile.read().splitlines(keepends=True)
            
            for line in sourceFileContent:
                if line.strip().startswith("//"):
                    comment += line
                else:
                    break
                
            targetFileContent = targetFileContent.replace("$COMMENT", comment)
            
        
        with open(target.as_posix(), "w", encoding="utf-8") as openedFile:
            openedFile.write(targetFileContent)
            
