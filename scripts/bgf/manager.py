import bge

from bge.logic import globalDict
from bge.types import *
from ast import literal_eval

from . import DEBUG


__all__ = ["manager"]


config = globalDict["Config"]
db = globalDict["Database"]
state = globalDict["State"]


# Controller endpoint
def manager(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    
    # Sensors
    always = cont.sensors["Always"]  # type: SCA_AlwaysSensor
    message = cont.sensors["Message"] # type: KX_NetworkMessageSensor

    if always.positive:
        pass
    