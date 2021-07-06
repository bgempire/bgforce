import bge

from bge.logic import globalDict
from ast import literal_eval

from .. import DEBUG

__all__ = ["widget"]


COMMAND_SEPARATOR = " | "
EXEC_PREFIX = ">"
LOCALE_PREFIX = "#"
TRANSITION_ANIMS = {
    "SlideLeft": [0, 20],
    "SlideRight": [30, 50],
    "FallBack": [60, 80],
    "BendBack": [90, 110],
    "BendArc": [120, 140],
}


def widget(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    
    # Sensors
    always = cont.sensors["Always"]  # type: bge.types.SCA_AlwaysSensor
    message = cont.sensors["Message"] # type: bge.types.KX_NetworkMessageSensor
    mouseOver = cont.sensors["MouseOver"] # type: bge.types.KX_MouseFocusSensor
    lmb = cont.sensors["LMB"] # type: bge.types.SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: bge.types.SCA_MouseSensor

    # Ensure group instance
    if group is None:
        own.endObject()
        return

    if always.positive:
        
        own["Commands"] = getCommandsFromGroup(group)
        
        if mouseOver.positive:
            
            if lmb.positive:
                own.replaceMesh(own["WidgetType"] + "Click")
            else:
                own.replaceMesh(own["WidgetType"] + "Hover")
                
            if lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
                
                if own["WidgetType"] == "Button":
                    from .button import button
                    button(cont)
                    
                elif own["WidgetType"] == "List":
                    print("List decrease")
                
            elif rmb is not None and rmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
                if own["WidgetType"] == "List":
                    print("List decrease")
        else:
            own.replaceMesh(own["WidgetType"] + "Normal")


# Helper functions
def getLabelFromGroup(group):
    # type: (bge.types.KX_GameObject) -> str

    if "Label" in group:
        if str(group["Label"]).startswith(EXEC_PREFIX):
            try:
                return str(eval(group["Label"][1:]))
            except:
                return str(group["Label"])
                
        elif str(group["Label"]).startswith(LOCALE_PREFIX):
            try:
                curLang = globalDict["Config"]["Lang"]
                return globalDict["Locale"][curLang][group["Label"][1:]]
            except:
                return str(group["Label"])
                
        else:
            return str(group["Label"])

    else:
        return ""


def getCommandsFromGroup(group):
    # type: (bge.types.KX_GameObject) -> list[str]
    
    def processCommand(command):
        # type: (str) -> str
        
        if command.startswith(EXEC_PREFIX):
            return command[1:].strip()
        elif command[0] in ("(", "["):
            return "camera.worldPosition = list(" + command.strip() + ") + [camera.worldPosition.z]"
        else:
            return "bge.logic.sendMessage('" + command.strip() + "')"
            
    commands = []
    
    if "Commands" in group:
        commands = group["Commands"].split(COMMAND_SEPARATOR) # type: list[str]
        
        for i in range(len(commands)):
            commands[i] = processCommand(commands[i])
                
    else:
        props = group.getPropertyNames() # type: list[str]
        props.sort()
        
        for prop in props:
            if prop.startswith("Command"):
                commands.append(processCommand(group[prop]))
                
    return commands