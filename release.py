"""Script to automate build of BGForce releases.
Intended only for the framework releases, CAN be safely deleted on your game!"""

import os
from pathlib import Path
import shutil
import glob

PROJECT = "bgforce"
VERSION = [0, 1, 0]

curPath = Path(__file__).parent.resolve()
releaseTarget = curPath / ("release/" + PROJECT + "-v" + ".".join([str(i) for i in VERSION]))

def deletePath(_path):
    # type: (Path) -> None

    if _path.is_file():
        _path.unlink()

    elif _path.is_dir():
        shutil.rmtree(_path)


if releaseTarget.exists():
    shutil.rmtree(releaseTarget)

releaseTarget.mkdir(parents=True)

data = {
    "OverwriteString": "$COMMENT\n{\n    \n}\n",
    "CreatePaths": [
        "./sounds/sfx/DELETE-ME",
    ],
    "CopyPaths": [
        "./database",
        "./lang",
        "./fonts",
        "./scripts",
        "./sounds/bgm",
        "./textures",
        "./.gitignore",
        "./LibBgf.blend",
        "./Game.blend",
        "./ScnMenu.blend",
    ],
    "OverwritePaths": [],
    "Ignore": [
        "__pycache__",
        ".git",
    ]
} # type: dict[str, list[str]]

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
            shutil.copytree(curPath / source, releaseTarget / source)
            print("  > Copied:", source)
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

for pattern in data["Ignore"]:
    ignoredPath = releaseTarget / ("**/" + pattern)
    ignoredPaths = glob.glob(ignoredPath.as_posix(), recursive=True)

    for ignored in ignoredPaths:
        deletePath(Path(ignored))
        print("X Removed ignored:", ignored)
