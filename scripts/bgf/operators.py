import bge
from bge.types import *


# Default operators
def saveConfig(cont, arg=""):
    # type: (SCA_PythonController, str) -> None
    
    from . import curPath, config, saveFile
    saveFile(curPath / "Config.json", config)


# Operators declaration
OPERATORS = {
    "SaveConfig" : saveConfig,
} # type: dict[str, function]