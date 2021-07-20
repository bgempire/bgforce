import bge

from bge.logic import globalDict
from ast import literal_eval
from textwrap import wrap

from . import DEBUG

__all__ = ["widget"]


COMMAND_SEPARATOR = " | "
EXEC_PREFIX = ">"
LOCALE_PREFIX = "#"
TRANSITION_ANIMS = {
    "SlideLeft": {"Shown" : 0, "Hidden" : 20},
    "SlideRight": {"Shown" : 30, "Hidden" : 50},
    "FallBack": {"Shown" : 60, "Hidden" : 80},
    "BendBack": {"Shown" : 90, "Hidden" : 110},
    "BendArc": {"Shown" : 120, "Hidden" : 140},
}

# Controller endpoint
def widget(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    config = globalDict["Config"]
    
    # Sensors
    always = cont.sensors["Always"]  # type: bge.types.SCA_AlwaysSensor
    message = cont.sensors["Message"] # type: bge.types.KX_NetworkMessageSensor

    if group is None:
        own.endObject()
        return

    if always.positive:
        
        # Initialize widget at start
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            initWidget(cont)
            
        # Start transition when GUI update is requested
        if message.positive and not own.isPlayingAction():
            own["TransitionState"] = "Hiding"
            
        processEnabled(cont)
        processTransition(cont)
        
        # Process clickable widget if applicable
        if own["ClickableObj"] is not None:
            processClickable(cont)
    

# Generic functions
def initWidget(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    debugProps = True if "Debug" in group and group["Debug"] else False
    
    # Set widget parent to group object
    own.setParent(group)
    
    # Store references to individual objects in widget's parent
    own["LabelObj"] = ([obj for obj in group.groupMembers if "LABEL" in obj] + [None])[0]
    own["LabelShadowObj"] = ([obj for obj in group.groupMembers if "LABEL_SHADOW" in obj] + [None])[0]
    own["ClickableObj"] = ([obj for obj in group.groupMembers if "CLICKABLE" in obj] + [None])[0]
    
    # Create widget properties based on its database config
    widgetDb = globalDict["Database"]["Gui"][own["WidgetType"]] # type: dict
    own["InlineProps"] = []
    
    for prop in widgetDb.keys():
        propValue = widgetDb[prop]
        
        if prop in group:
            propValue = group[prop]
            own["InlineProps"].append(prop)
        
        if type(propValue) == str:
            try:
                propValue = literal_eval(propValue)
            except:
                pass
                
        own[prop] = propValue
        if debugProps: own.addDebugProperty(prop)
        
    # Apply style to current widget
    if "Style" in group:
        styleName = own["WidgetType"] + ":" + str(group["Style"])
        styleDb = {}
        
        if styleName in globalDict["Database"]["Styles"].keys():
            styleDb = globalDict["Database"]["Styles"][styleName]
        
        elif styleName in globalDict["Database"]["Gui"].keys():
            styleDb = globalDict["Database"]["Gui"][styleName]
            
        for prop in styleDb.keys():
            if not prop in own["InlineProps"]:
                own[prop] = styleDb[prop]
    
    # Create additional props in widget
    additionalProps = {
        "TargetLabel" : "",
        "TransitionState" : "Shown",
    }
    
    for prop in additionalProps.keys():
        own[prop] = additionalProps[prop]
        if debugProps: own.addDebugProperty(prop)
    
    # Set label and shadow properties if they exist
    updateLabelObj(cont)
    
    # Get commands of clickable widget
    if own["ClickableObj"] is not None:
        own["Commands"] = getCommandsFromGroup(cont)
        own["Clicked"] = False
        own["ClickableObj"].localScale = list(own["Size"]) + [1.0]
        own["ClickableObj"].localPosition = list(own["Offset"]) + [own["ClickableObj"].localPosition.z]
    
    # Disable transition if prop Update is provided
    if "Update" in group:
        own["Transition"] = "None"
        cont.sensors["Always"].skippedTicks = group["Update"]
    
    # Show transition at start
    if own["Transition"] in TRANSITION_ANIMS.keys():
        own["TransitionState"] = "Showing"


def updateLabelObj(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    
    if own["LabelObj"] is not None and own["LabelShadowObj"] is not None:
        labelObj = own["LabelObj"]
        shadowObj = own["LabelShadowObj"]
        
        # Set text to label and shadow
        own["TargetLabel"] = labelObj.text = shadowObj.text = getLabelFromGroup(cont)
        
        # Set color and offset of label
        labelObj.color = own["LabelColor"]
        labelObj.localPosition = list(own["LabelOffset"]) + [labelObj.localPosition.z]
        labelObj.localScale = [own["LabelSize"], own["LabelSize"], 1.0]
        
        # Set visibility, color and offset of shadow
        shadowObj.visible = bool(own["ShadowEnable"])
        shadowObj.color = own["ShadowColor"]
        shadowObj.localPosition = list(labelObj.localPosition)[0:2] + [shadowObj.localPosition.z]
        shadowObj.localPosition.x += own["ShadowOffset"][0]
        shadowObj.localPosition.y += own["ShadowOffset"][1]
        shadowObj.localScale = [own["LabelSize"], own["LabelSize"], 1.0]


def processTransition(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    curAnim = TRANSITION_ANIMS[own["Transition"]]
    config = globalDict["Config"]
    
    if not own.isPlayingAction():
        
        # Play hide animation
        if own["TransitionState"] == "Hiding":
            own.playAction("GuiTransitions", curAnim["Shown"], curAnim["Hidden"], speed=own["TransitionSpeed"])
            own["TransitionState"] = "Showing"
        
        # Play show animation
        elif own["TransitionState"] == "Showing":
            own.playAction("GuiTransitions", curAnim["Hidden"], curAnim["Shown"], speed=own["TransitionSpeed"])
            own["TransitionState"] = "Shown"
            
            if own["ClickableObj"] is not None and own["TransitionOnClick"] and own["Clicked"]:
                own["Clicked"] = False
                execCommands(cont)
            
            # Update label while it's still hidden
            updateLabelObj(cont)


def processEnabled(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    config = globalDict["Config"]
    
    if "Enabled" in group:
        if type(group["Enabled"]) == str:
            try:
                own["Enabled"] = bool(eval(group["Enabled"]))
            except:
                own["Enabled"] = True
        else:
            own["Enabled"] = bool(group["Enabled"])
    else:
        own["Enabled"] = True


def processClickable(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    curAnim = TRANSITION_ANIMS[own["Transition"]]
    clickableObj = own["ClickableObj"]
    
    mouseOver = cont.sensors.get("MouseOver", None) # type: bge.types.KX_MouseFocusSensor
    lmb = cont.sensors.get("LMB", None) # type: bge.types.SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: bge.types.SCA_MouseSensor
    
    if not own["Enabled"]:
        clickableObj.replaceMesh(own["WidgetType"] + "Disabled")
        
    elif mouseOver.positive and not own.isPlayingAction():
        
        if lmb is not None and lmb.positive:
            clickableObj.replaceMesh(own["WidgetType"] + "Click")
            
        else:
            clickableObj.replaceMesh(own["WidgetType"] + "Hover")
            
        if lmb is not None and lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            
            if not own["TransitionOnClick"]:
                execCommands(cont)
            else:
                own["Clicked"] = True
                bge.logic.sendMessage("UpdateGui")
                
            if own["WidgetType"] == "List":
                print("List increased")
            
        elif rmb is not None and rmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            
            if not own["TransitionOnClick"]:
                execCommands(cont)
            else:
                own["Clicked"] = True
                bge.logic.sendMessage("UpdateGui")
            
            if own["WidgetType"] == "List":
                print("List decreased")
                
    else:
        clickableObj.replaceMesh(own["WidgetType"] + "Normal")
    

# Helper functions
def getLabelFromGroup(cont):
    # type: (bge.types.SCA_PythonController) -> str
    
    own = cont.owner
    group = own.groupObject
    
    label = ""

    if "Label" in group:
        
        try:
            # Get label from code execution
            if str(group["Label"]).startswith(EXEC_PREFIX):
                label = str(eval(group["Label"][1:]))
                
            # Get label from current locale strings
            elif str(group["Label"]).startswith(LOCALE_PREFIX):
                curLang = globalDict["Config"]["Lang"]
                label = globalDict["Locale"][curLang][group["Label"][1:]]
                
            # Assume label as literal text
            else:
                label = str(group["Label"])
                
        except:
            label = str(group["Label"])
            
        # Process label line breaks
        label = wrap(label, own["LineSize"])
        
        # Process label text align
        if own["Justify"].lower() == "center":
            label = [i.center(own["LineSize"]) for i in label]
        elif own["Justify"].lower() == "right":
            label = [i.rjust(own["LineSize"]) for i in label]
            
        label = "\n".join(label)

    return label


def execCommands(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    own = cont.owner
    group = own.groupObject
    config = globalDict["Config"]
    
    if DEBUG: print(">", own["WidgetType"], "clicked:", group)
    
    for command in own["Commands"]:
        try:
            exec(command)
            if DEBUG: print("  > Command:", repr(command))
        except:
            if DEBUG: print("  X Command error:", repr(command))


def getCommandsFromGroup(cont):
    # type: (bge.types.SCA_PythonController) -> list[str]
    
    def processCommand(command):
        # type: (str) -> str
        
        if command.startswith(EXEC_PREFIX):
            return command[1:].strip()
        elif command[0] in ("(", "["):
            return "camera.worldPosition = list(" + command.strip() + ") + [camera.worldPosition.z]"
        else:
            return "bge.logic.sendMessage('" + command.strip() + "')"
            
    own = cont.owner
    group = own.groupObject
            
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

