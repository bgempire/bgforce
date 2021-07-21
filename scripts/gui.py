import bge

from bge.logic import globalDict
from ast import literal_eval
from textwrap import wrap

from . import DEBUG

__all__ = ["widget"]


COMMAND_SEPARATOR = " | "
INSTANT_PREFIX = "!"
EXEC_PREFIX = ">"
LOCALE_PREFIX = "#"
TRANSITION_ANIMS = {
    "SlideL": {"Shown" : 0, "Hidden" : 20},
    "SlideR": {"Shown" : 30, "Hidden" : 50},
    "ScaleV": {"Shown" : 60, "Hidden" : 80},
    "ScaleH": {"Shown" : 90, "Hidden" : 110},
    "Arc": {"Shown" : 120, "Hidden" : 140},
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
        
        # Update label if property Update is provided
        if "Update" in group and group["Update"] >= 0:
            always.skippedTicks = group["Update"]
            updateLabelObj(cont)
        
        # Start transition when GUI update is requested
        if message.positive and not own.isPlayingAction():
            own["TransitionState"] = "Hiding"
            
        processEnabled(cont)
        processTransition(cont)
        
        # Process clickable widget if applicable
        if own["ClickableObj"] is not None:
            processClickable(cont)
    

# Abstraction functions
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
    own["IconObj"] = ([obj for obj in group.groupMembers if "ICON" in obj] + [None])[0]
    
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
    
    # Set clickable widget properties
    if own["ClickableObj"] is not None:
        own["Commands"] = getCommandsFromGroup(cont)
        own["Clicked"] = False
        own["ClickableObj"].localScale = list(own["Size"]) + [1.0]
        own["ClickableObj"].localPosition = list(own["Offset"]) + [own["ClickableObj"].localPosition.z]
        
    # Set icon widget properties
    if own["IconObj"] is not None:
        own["IconObj"].localScale = list(own["IconSize"]) + [1.0]
        
        if own["ClickableObj"] is not None:
            clickablePos = list(own["ClickableObj"].localPosition)[0:2] + [own["IconObj"].localPosition.z]
            own["IconObj"].localPosition = clickablePos
            
        own["IconObj"].localPosition.x += own["IconOffset"][0]
        own["IconObj"].localPosition.y += own["IconOffset"][1]
        
        if "Icon" in group:
            meshName = "IconButtonIcon" + str(group["Icon"])
            try:
                own["IconObj"].replaceMesh(meshName)
            except:
                if DEBUG: print("X Icon mesh of", group, "not found:", meshName)
    
    # Show transition at start
    if own["Transition"] in TRANSITION_ANIMS.keys():
        own["TransitionState"] = "Showing"
        
    if own["WidgetType"] == "Checkbox":
        checkboxAction(cont, True)


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
    curAnim = TRANSITION_ANIMS.get(own["Transition"])
    config = globalDict["Config"]
    
    if not own.isPlayingAction() and curAnim:
        
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
                execCommands(cont, False)
            
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


def setClickableVisual(cont, state):
    # type: (bge.types.SCA_PythonController, str) -> None
    
    own = cont.owner
    clickableObj = own["ClickableObj"]
    other = ""
    
    if own["WidgetType"] == "Checkbox":
        other = str(own["Checked"])
        other = "Radio" + other if "Value" in own.groupObject else other
    
    clickableObj.replaceMesh(own["WidgetType"] + other + state)
    clickableObj.color = own["Color" + state]


def processClickable(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    mouseOver = cont.sensors.get("MouseOver", None) # type: bge.types.KX_MouseFocusSensor
    lmb = cont.sensors.get("LMB", None) # type: bge.types.SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: bge.types.SCA_MouseSensor
    
    if own["WidgetType"] == "Checkbox":
        checkboxAction(cont, True)
    
    if not own["Enabled"]:
        setClickableVisual(cont, "Disabled")
        
    elif mouseOver.positive and not own.isPlayingAction():
        
        if lmb is not None and lmb.positive:
            setClickableVisual(cont, "Click")
            
        else:
            setClickableVisual(cont, "Hover")
            
        if lmb is not None and lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            execCommands(cont, True)
            
            if not own["TransitionOnClick"]:
                execCommands(cont, False)
            else:
                own["Clicked"] = True
                bge.logic.sendMessage("UpdateGui")
                
            if own["WidgetType"] == "Checkbox":
                checkboxAction(cont)
                
            elif own["WidgetType"] == "List":
                listAction(cont, "Increase")
            
        elif rmb is not None and rmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            execCommands(cont, True)
            
            if not own["TransitionOnClick"]:
                execCommands(cont, False)
            else:
                own["Clicked"] = True
                bge.logic.sendMessage("UpdateGui")
            
            if own["WidgetType"] == "List":
                listAction(cont, "Decrease")
                
    else:
        setClickableVisual(cont, "Normal")
    

# Widget actions
def checkboxAction(cont, visualOnly=False):
    # type: (bge.types.SCA_PythonController, bool) -> None
    
    own = cont.owner
    group = own.groupObject
    config = globalDict["Config"]
    result = None
    
    if "Target" in group:
        
        if "Value" in group:
            value = group["Value"]
            
            if type(value) == str:
                try:
                    value = eval(value)
                except:
                    pass
            
            command = group["Target"] + " = " + repr(value)
            try:
                if not visualOnly: exec(command)
                own["Checked"] = result = eval(group["Target"]) == value
            except:
                if DEBUG: print("X Could not set value to target:", repr(command))
            
        else:
            command = group["Target"] + " = not bool(" + str(group["Target"]) + ")"
            try:
                if not visualOnly: exec(command)
                own["Checked"] = result = eval(group["Target"])
            except:
                if DEBUG: print("X Could not invert target:", repr(command))
        
    else:
        if not visualOnly: own["Checked"] = result = not own["Checked"]
        
    if DEBUG and not visualOnly: print(">", group, "set to:", result)
    setClickableVisual(cont, "Hover")
    

def listAction(cont, event):
    # type: (bge.types.SCA_PythonController, str) -> None
    
    own = cont.owner
    group = own.groupObject
    
    if DEBUG: print("> List", group, "event:", event)


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


def execCommands(cont, instant):
    # type: (bge.types.SCA_PythonController, bool) -> None
    
    own = cont.owner
    group = own.groupObject
    config = globalDict["Config"]
    index = 0 if instant else 1
    
    if DEBUG and len(own["Commands"][index]) > 0: print("> Exec commands of", group)
    
    for command in own["Commands"][index]:
        try:
            exec(command)
            if DEBUG: print("  > Command:", repr(command))
        except:
            if DEBUG: print("  X Command error:", repr(command))


def getCommandsFromGroup(cont):
    # type: (bge.types.SCA_PythonController) -> list[str]
    
    def processCommand(command):
        # type: (str) -> str
        
        command = command.strip()
        if command.startswith(EXEC_PREFIX):
            return command[1:].strip()
        elif command[0] in ("(", "["):
            return "own.scene.active_camera.worldPosition = list(" + command.strip() \
                + ") + [own.scene.active_camera.worldPosition.z]"
        else:
            return "bge.logic.sendMessage('" + command.strip() + "')"
            
    own = cont.owner
    group = own.groupObject
            
    commands = [[], []] # Instant commands, wait commands
    
    if "Commands" in group:
        commandsTemp = group["Commands"].split(COMMAND_SEPARATOR) # type: list[str]
        
        for i in range(len(commands)):
            commandsTemp[i] = processCommand(commandsTemp[i])
            commands = commandsTemp
            
        for command in commandsTemp:
            if str(command).strip().startswith(INSTANT_PREFIX):
                commands[0].append(processCommand(command[1:]))
            else:
                commands[1].append(processCommand(command))
            
    else:
        props = group.getPropertyNames() # type: list[str]
        props.sort()
        
        for prop in props:
            if prop.startswith("Command"):
                if str(group[prop]).strip().startswith(INSTANT_PREFIX):
                    commands[0].append(processCommand(group[prop][1:]))
                else:
                    commands[1].append(processCommand(group[prop]))
                    
    return commands

