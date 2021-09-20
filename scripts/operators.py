import bge

from bge.types import *


# Default operators
def saveConfig(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    from .bgf import curPath, config, saveFile
    saveFile(curPath / "Config.json", config)


# Custom operators


# Main declaration
OPERATORS = {
    "SaveConfig" : saveConfig,
}