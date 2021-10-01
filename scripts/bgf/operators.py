import bge
from bge.types import *


# Default operators
def saveConfig(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    from . import curPath, config, saveFile
    saveFile(curPath / "Config.json", config)


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


def playSfx(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    import aud
    from . import config, sounds
    
    if config["SfxEnable"] and arg in sounds["Sfx"].keys():
        factory = aud.Factory.file(sounds["Sfx"][arg])
        handle = aud.device().play(factory) # type: aud.Handle
        handle.volume = config["SfxVol"]


# Operators declaration
OPERATORS = {
    "SaveConfig" : saveConfig,
    "ApplyConfig" : applyConfig,
    "PlaySfx" : playSfx,
} # type: dict[str, function]