import bge

from bge.logic import globalDict
from bge.types import *


# Global variables
config = globalDict["Config"]
db = globalDict["Database"]
state = globalDict["State"]


# Custom operators
def testFunction(cont):
    # type: (SCA_PythonController) -> None
    
    print(cont.name)


# Main declaration
OPERATORS = {
    "TestFunction" : testFunction
}