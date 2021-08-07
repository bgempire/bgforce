import bge

from bge.logic import globalDict
from bge.types import *
from .bgf import config, database, state


# Custom operators
def testFunction(cont):
    # type: (SCA_PythonController) -> None
    
    print(cont.name)


# Main declaration
OPERATORS = {
    "TestFunction" : testFunction
}