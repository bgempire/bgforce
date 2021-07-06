import bge

from bge.logic import globalDict
from .. import DEBUG

__all__ = ["button"]


def button(cont):
    # type: (bge.types.SCA_PythonController) -> None

    # Variables that can be used in commands
    own = cont.owner
    group = own.groupObject
    commands = own["Commands"]
    camera = own.scene.active_camera
    config = globalDict["Config"]
    
    if DEBUG and commands: print("> Executing list of commands")
    
    for command in commands:
        try:
            exec(command)
            if DEBUG: print("  > Executed:", repr(command))
        except:
            if DEBUG: print("  X Could not exec:", repr(command))