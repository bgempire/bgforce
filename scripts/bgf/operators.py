import bge
from bge.types import *


# Default operators
def applyConfig(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    from . import config
    
    # Resolution
    if config["Resolution"] in bge.logic.__resolutions.keys():
        resolution = bge.logic.__resolutions[config["Resolution"]]
        bge.render.setWindowSize(resolution[0], resolution[1])
        
    # Fullscreen
    bge.render.setFullScreen(bool(config["Fullscreen"]))
    
    # Anisotropic filtering
    if config["AnisotropicFiltering"] in (1, 2, 4, 8, 16):
        bge.render.setAnisotropicFiltering(config["AnisotropicFiltering"])
    
    # Mipmapping
    mipmapLevels = {
        "None" : 0,
        "Nearest" : 1,
        "Linear" : 2,
    }
    
    if config["Mipmaps"] in mipmapLevels.keys():
        bge.render.setMipmapping(mipmapLevels[config["Mipmaps"]])
        
    # Motion blur
    motionBlur = round(config["MotionBlur"], 1)
    
    if motionBlur == 0:
        bge.render.disableMotionBlur()
        
    elif 0 < motionBlur <= 1:
        bge.render.enableMotionBlur(motionBlur)
        
    # Vsync
    bge.render.setVsync(bool(config["Vsync"]))
    
    # GLSL material settings
    glslSettings = {
        "lights" : config["Lights"],
        "shaders" : config["Shaders"],
        "shadows" : config["Shadows"],
        "ramps" : config["Ramps"],
        "nodes" : config["Nodes"],
        "extra_textures" : config["ExtraTextures"],
    }
    
    for option in glslSettings.keys():
        bge.render.setGLSLMaterialSetting(option, bool(glslSettings[option]))


def exitGame(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    own = cont.owner
    own["ContextState"] = "ExitGame"
    own["ContextTransition"] = True


def hideMouseCursor(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    showMouseCursor(cont, "False")


def pauseContext(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    from . import database
    own = cont.owner
    
    if own["Context"] in database["Contexts"].keys():
        ctxScns = database["Contexts"][own["Context"]]["Scenes"] # type: list[dict]
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


def playBgm(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    if cont.owner["Bgm"] != arg:
        cont.owner["Bgm"] = arg
        cont.owner["BgmState"] = "FadeOut"
        cont.owner["BgmTransition"] = True


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


def setContext(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    from . import database
    own = cont.owner
    
    if arg in database["Contexts"].keys():
        own["Context"] = arg
        own["ContextTransition"] = True


def showMouseCursor(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    if (not arg or  str(arg).lower() == "true"):
        bge.logic.__showMouseCursor = True
    
    elif str(arg).lower() == "false":
        bge.logic.__showMouseCursor = False


def stopBgm(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    playBgm(cont)

