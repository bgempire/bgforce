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
    
    if config["Resolution"] in bge.logic.__resolutions.keys():
        resolution = bge.logic.__resolutions[config["Resolution"]]
        bge.render.setWindowSize(resolution[0], resolution[1])
        
    bge.render.setFullScreen(config["Fullscreen"])


# Operators declaration
OPERATORS = {
    "SaveConfig" : saveConfig,
    "ApplyConfig" : applyConfig,
} # type: dict[str, function]