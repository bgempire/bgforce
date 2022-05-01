import bge
from bge.types import *
from . manager import Manager


# Default operators
def applyConfig(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    from . import config

    resolutions = bge.logic.__resolutions.keys() # type: dict[str, list[int, int]]

    # Resolution
    if config.get("Resolution") is not None and config["Resolution"] in resolutions:
        resolution = bge.logic.__resolutions[config["Resolution"]]
        bge.render.setWindowSize(resolution[0], resolution[1])

    # Fullscreen
    if config.get("Fullscreen") is not None:
        bge.render.setFullScreen(bool(config["Fullscreen"]))

    # Anisotropic filtering
    if config.get("AnisotropicFiltering") is not None and config["AnisotropicFiltering"] in (1, 2, 4, 8, 16):
        bge.render.setAnisotropicFiltering(config["AnisotropicFiltering"])

    # Mipmapping
    if config.get("Mipmapping") is not None:

        mipmapLevels = {
            "None" : 0,
            "Nearest" : 1,
            "Linear" : 2,
        }

        if config["Mipmaps"] in mipmapLevels.keys():
            bge.render.setMipmapping(mipmapLevels[config["Mipmaps"]])

    # Motion blur
    if config.get("MotionBlur") is not None:
        motionBlur = round(float(config["MotionBlur"]), 1) # type: float

        if motionBlur == 0:
            bge.render.disableMotionBlur()

        elif 0 < motionBlur <= 1:
            bge.render.enableMotionBlur(motionBlur)

    # Vsync
    if config.get("Vsync") is not None:
        bge.render.setVsync(bool(config["Vsync"]))

    # GLSL material settings
    glslSettings = {
        "lights" : config.get("Lights"),
        "shaders" : config.get("Shaders"),
        "shadows" : config.get("Shadows"),
        "ramps" : config.get("Ramps"),
        "nodes" : config.get("Nodes"),
        "extra_textures" : config.get("ExtraTextures"),
    }

    for option in glslSettings.keys():
        if glslSettings[option] is not None:
            bge.render.setGLSLMaterialSetting(option, bool(glslSettings[option]))


def exitGame(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    own = cont.owner # type: KX_GameObject

    if type(own) == Manager:
        own = own # type: Manager
        own.contextState = "ExitGame"
        own.contextTransition = True

    else:
        print("X Exit game must be called from manager")


def hideMouseCursor(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    showMouseCursor(cont, "False")


def loadState(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    from . import curPath, state, loadFile

    if arg:
        targetFile = curPath / ("save/" + arg + ".dat")

        if targetFile.exists():
            state.update(loadFile(targetFile))
            print("> Loaded state from save/" + arg + ".dat")
        else:
            print("X Could not load save/" + arg + ".dat")

    else:
        targetFile = curPath / "save.dat"

        if targetFile.exists():
            state.update(loadFile(targetFile))
            print("> Loaded state from save.dat")
        else:
            print("X Could not load save.dat")


def pauseContext(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    from . import database
    own = cont.owner

    if type(own) == Manager:
        own = own # type: Manager

        if own.context in database["Contexts"].keys():
            ctxScns = database["Contexts"][own.context]["Scenes"] # type: list[dict]
            sceneList = {} # type: dict[KX_Scene]

            for scn in bge.logic.getSceneList():
                if scn.name != "ScnManager":
                    sceneList[scn.name] = scn

            for scn in ctxScns:
                if scn.get("Name") in sceneList.keys() and scn.get("Pausable"):
                    curScene = sceneList[scn["Name"]] # type: KX_Scene

                    if (not arg or arg.lower() == "true") and not curScene.suspended:
                        curScene.suspend()

                    elif arg.lower() == "false" and curScene.suspended:
                        curScene.resume()
    else:
        print("X Pause context pause must be called from manager")


def playBgm(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    own = cont.owner

    if type(cont.owner) == Manager:
        own = own # type: Manager

        if own.bgm != arg:
            own.bgm = arg
            own.bgmState = "FadeOut"
            own.bgmTransition = True

    else:
        print("X Play bgm must be called from manager")


def playSfx(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    import aud
    from . import config, sounds

    if config["SfxEnable"] and arg in sounds["Sfx"].keys():
        factory = aud.Factory.file(sounds["Sfx"][arg])
        handle = aud.device().play(factory) # type: aud.Handle
        handle.volume = config["SfxVol"]


def resumeContext(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    pauseContext(cont, "False")


def saveConfig(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    from . import curPath, config, saveFile
    saveFile(curPath / "Config.json", config)


def saveState(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    from . import curPath, state, saveFile

    if arg:
        saveDir = curPath / "save"

        if not saveDir.exists():
            saveDir.mkdir()

        if saveDir.exists():
            targetFile = saveDir / arg
            saveFile(targetFile, state, ".dat")
            print("> Saved state to save/" + arg + ".dat")

    else:
        targetFile = curPath / "save.dat"
        saveFile(targetFile, state, ".dat")
        print("> Saved state to save.dat")


def setContext(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    from . import database
    own = cont.owner

    if type(own) == Manager:
        own = own # type: Manager

        if arg in database["Contexts"].keys():
            own.context = arg
            own.contextTransition = True

    else:
        print("X Set context must be called from manager")


def showMouseCursor(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    if (not arg or  str(arg).lower() == "true"):
        bge.logic.__showMouseCursor = True

    elif str(arg).lower() == "false":
        bge.logic.__showMouseCursor = False


def stopBgm(cont, arg=""):
    # type: (SCA_PythonController, str) -> None

    playBgm(cont)

