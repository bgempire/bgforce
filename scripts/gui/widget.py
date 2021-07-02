import bge

from bge.logic import globalDict
from ast import literal_eval

__all__ = ["widget"]


def widget(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject

    # Sensors
    always = cont.sensors["Always"]  # type: bge.types.SCA_ISensor
    message = cont.sensors["Message"]

    # Ensure group instance
    if group is None:
        own.endObject()
        return

    if always.positive:
        pass
